# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Verify published CDN assets against the package verification manifest.

Run this before a deployment switches runtime asset delivery to a CDN version.
It answers one question per asset: would a browser loading this exact version
get the file the templates expect, cached immutably?

The package never pins a CDN host, so the deployer supplies the base URL:

    python scripts/verify_cdn_assets.py --base-url https://cdn.example.com --version v1.14.0
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

MANIFEST_PATH = Path(__file__).resolve().parents[1] / "insight_ui/cdn_manifest.json"
REQUIRED_SCHEME = "https://"
DEFAULT_TIMEOUT_SECONDS = 30
EXPECTED_CORS_ORIGIN = "*"
HTTP_OK = 200
# Object stores answer CORS only for requests that carry an Origin, so a probe
# without one sees no Access-Control-Allow-Origin even when CORS is configured.
CORS_PROBE_ORIGIN = "https://cdn-verification.invalid"


def css_class_selector(utility: str) -> str:
    r"""Return the CSS selector a compiled stylesheet uses for a utility class.

    Tailwind escapes the colon in variant utilities, so ``lg:block`` is emitted
    as ``.lg\:block``. Searching a stylesheet for the raw utility name never
    matches and would fail verification against a correctly published asset.

    Args:
        utility: A utility class name such as ``lg:block``.

    Returns:
        The escaped class selector such as ``.lg\:block``.

    """
    return "." + utility.replace(":", "\\:")


def stylesheet_contains(stylesheet: str, utility: str) -> bool:
    """Report whether a stylesheet defines a utility class.

    Args:
        stylesheet: The stylesheet body.
        utility: A utility class name such as ``lg:block``.

    Returns:
        True if the stylesheet carries the utility in escaped or raw form.

    """
    return css_class_selector(utility) in stylesheet or utility in stylesheet


def load_manifest(path: Path = MANIFEST_PATH) -> dict[str, Any]:
    """Read the package-owned verification manifest.

    Args:
        path: Location of the manifest document.

    Returns:
        The parsed manifest.

    """
    return json.loads(path.read_text())


def asset_url(manifest: dict[str, Any], base_url: str, version: str, path: str) -> str:
    """Build the full asset URL from the manifest's URL template.

    Args:
        manifest: The parsed manifest.
        base_url: Deployer-supplied CDN base URL.
        version: Immutable release version, for example ``v1.14.0``.
        path: CDN-relative asset path from the manifest.

    Returns:
        The absolute asset URL.

    """
    return manifest["url_template"].format(
        cdn_base_url=base_url.rstrip("/"),
        cdn_prefix=manifest["cdn_prefix"].strip("/"),
        version=version.strip("/"),
        path=path,
    )


def _check_headers(headers: Any, problems: list[str]) -> None:  # noqa: ANN401 - email.Message from urllib
    """Collect cache and CORS problems for one response.

    The caller must have sent an Origin header: without one an object store
    answers no CORS headers at all, and a correctly configured asset would be
    reported as broken.

    Args:
        headers: Response headers.
        problems: Accumulator the findings are appended to.

    """
    cache_control = headers.get("Cache-Control", "")
    if "immutable" not in cache_control:
        problems.append(f"Cache-Control must be immutable, got {cache_control!r}")
    if "max-age=" not in cache_control:
        problems.append(f"Cache-Control must set max-age, got {cache_control!r}")

    cors = headers.get("Access-Control-Allow-Origin", "")
    if cors != EXPECTED_CORS_ORIGIN:
        problems.append(f"Access-Control-Allow-Origin must be {EXPECTED_CORS_ORIGIN!r}, got {cors!r}")


def check_asset(url: str, entry: dict[str, Any], timeout: int = DEFAULT_TIMEOUT_SECONDS) -> list[str]:
    """Verify one published asset.

    Args:
        url: Absolute asset URL.
        entry: The manifest entry describing the asset.
        timeout: Per-request timeout in seconds.

    Returns:
        Human-readable problems; empty when the asset verifies.

    Raises:
        SystemExit: If the URL is not HTTPS.

    """
    if not url.startswith(REQUIRED_SCHEME):
        message = f"Refusing to verify a non-HTTPS URL: {url}"
        raise SystemExit(message)

    problems: list[str] = []
    request = urllib.request.Request(url, headers={"Origin": CORS_PROBE_ORIGIN})  # noqa: S310 # nosec B310 - scheme checked above
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310 # nosec B310 - scheme checked above
            if response.status != HTTP_OK:
                problems.append(f"expected HTTP {HTTP_OK}, got {response.status}")
            _check_headers(response.headers, problems)
            body = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as error:
        return [f"expected HTTP {HTTP_OK}, got {error.code}"]
    except (urllib.error.URLError, TimeoutError) as error:
        return [f"unreachable: {error}"]

    absent = sorted(
        selector for selector in entry.get("must_contain_selectors", []) if not stylesheet_contains(body, selector)
    )
    if absent:
        problems.append(f"missing required selectors: {absent}")
    return problems


def _selected_entries(manifest: dict[str, Any], conditional: set[str]) -> list[dict[str, Any]]:
    """Return the required entries plus any explicitly enabled conditional ones.

    Args:
        manifest: The parsed manifest.
        conditional: CDN-relative paths of conditional assets to include.

    Returns:
        The entries to verify.

    Raises:
        SystemExit: If a requested conditional path is not in the manifest.

    """
    available = {entry["path"]: entry for entry in manifest["conditional"]}
    unknown = sorted(conditional - available.keys())
    if unknown:
        message = f"Unknown conditional assets {unknown}; available: {sorted(available)}"
        raise SystemExit(message)
    return [*manifest["required"], *(available[path] for path in sorted(conditional))]


def verify(
    base_url: str,
    version: str,
    *,
    conditional: set[str] | None = None,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
    manifest: dict[str, Any] | None = None,
) -> list[str]:
    """Verify every selected asset of one published version.

    Args:
        base_url: Deployer-supplied CDN base URL.
        version: Immutable release version.
        conditional: CDN-relative paths of conditional assets to include.
        timeout: Per-request timeout in seconds.
        manifest: Parsed manifest; read from the package when omitted.

    Returns:
        Failure lines; empty when every asset verifies.

    """
    document = manifest if manifest is not None else load_manifest()
    failures: list[str] = []
    for entry in _selected_entries(document, conditional or set()):
        url = asset_url(document, base_url, version, entry["path"])
        problems = check_asset(url, entry, timeout)
        status = "FAIL" if problems else "ok"
        sys.stdout.write(f"[{status}] {url}\n")
        failures.extend(f"{url}: {problem}" for problem in problems)
    return failures


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse the command line.

    Args:
        argv: Argument list; defaults to ``sys.argv``.

    Returns:
        The parsed arguments.

    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True, help="CDN base URL supplied by the deployer.")
    parser.add_argument("--version", required=True, help="Immutable version to verify, for example v1.14.0.")
    parser.add_argument(
        "--include-conditional",
        action="append",
        default=[],
        metavar="PATH",
        help="Conditional asset to verify as well; repeatable.",
    )
    parser.add_argument("--all-conditional", action="store_true", help="Verify every conditional asset too.")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS, help="Per-request timeout in seconds.")
    return parser.parse_args(argv)


if __name__ == "__main__":
    arguments = _parse_args()
    document = load_manifest()
    selected = (
        {entry["path"] for entry in document["conditional"]}
        if arguments.all_conditional
        else set(arguments.include_conditional)
    )
    problems = verify(
        arguments.base_url,
        arguments.version,
        conditional=selected,
        timeout=arguments.timeout,
        manifest=document,
    )
    if problems:
        report = "\n".join(["CDN verification failed:", *(f"- {problem}" for problem in problems)])
        raise SystemExit(report)
    sys.stdout.write(f"All required CDN assets verified for {arguments.version}.\n")
