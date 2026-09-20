# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Keep the CDN verification manifest aligned with the templates and the package.

The manifest is a verification subset, not the publication list: release
automation decides what is uploaded. That split only stays honest while the
manifest still describes assets the templates actually request and the package
actually ships, so these tests fail on drift in either direction.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest
from insight_ui.asset_urls import to_minified_asset_path
from insight_ui.config import CONFIG_DEFAULTS
from scripts.verify_cdn_assets import stylesheet_contains

ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = ROOT / "insight_ui/cdn_manifest.json"
TEMPLATE_ROOT = ROOT / "insight_ui/templates"
STATIC_ROOT = ROOT / "insight_ui/static/insight_ui"
PACKAGE_STATIC_PREFIX = "insight_ui/"
# Matches a quoted literal or a dotted context variable: {% insight_asset 'a/b.js' %}
INSIGHT_ASSET_TAG = re.compile(
    r"{%\s*insight_asset\s+(?P<argument>'[^']*'|\"[^\"]*\"|[A-Za-z_][\w.]*)",
)
# Context variables the base template resolves from the package defaults.
CONTEXT_VARIABLES = {"INSIGHT_UI.stylesheet": CONFIG_DEFAULTS["stylesheet"]}


def _manifest() -> dict[str, Any]:
    """Read the package-owned verification manifest.

    Returns:
        The parsed manifest document.

    """
    return json.loads(MANIFEST_PATH.read_text())


def _entries(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    """Return every manifest entry, required and conditional alike.

    Args:
        manifest: The parsed manifest document.

    Returns:
        The concatenated required and conditional entries.

    """
    return [*manifest["required"], *manifest["conditional"]]


def _template_asset_paths() -> set[str]:
    """Collect the package assets the shipped templates request through the tag.

    Returns:
        Package-relative asset paths, for example ``insight_ui/css/tailwind.css``.

    Raises:
        AssertionError: If a template resolves the tag through an unknown variable.

    """
    paths: set[str] = set()
    for template in sorted(TEMPLATE_ROOT.rglob("*.html")):
        for match in INSIGHT_ASSET_TAG.finditer(template.read_text()):
            argument = match.group("argument")
            if argument[0] in {"'", '"'}:
                paths.add(argument[1:-1])
                continue
            resolved = CONTEXT_VARIABLES.get(argument)
            assert resolved is not None, (
                f"{template.relative_to(ROOT)}: '{argument}' is a new dynamic insight_asset source. "
                f"Teach {Path(__file__).name} how to resolve it so manifest coverage stays checkable."
            )
            paths.add(resolved)
    return paths


def _to_manifest_path(package_asset_path: str) -> str:
    """Convert a package asset path into the manifest's CDN-relative form.

    Args:
        package_asset_path: A path such as ``insight_ui/css/tailwind.css``.

    Returns:
        The minified, prefix-stripped path such as ``css/tailwind.min.css``.

    """
    return to_minified_asset_path(package_asset_path).removeprefix(PACKAGE_STATIC_PREFIX)


def _to_source_asset(manifest_path: str) -> Path:
    """Resolve a manifest path back to the readable package source file.

    Generated minified variants are build artifacts and are not committed, so the
    readable sibling is what must exist in the package.

    Args:
        manifest_path: A CDN-relative path such as ``css/tailwind.min.css``.

    Returns:
        The absolute path of the readable package asset.

    """
    suffix = Path(manifest_path).suffix
    readable = re.sub(rf"\.min{re.escape(suffix)}$", suffix, manifest_path)
    return STATIC_ROOT / readable


def test_manifest_is_valid_and_deployment_neutral() -> None:
    """The manifest must stay parseable and must not pin a deployer's CDN host."""
    manifest = _manifest()

    assert manifest["cdn_prefix"] == CONFIG_DEFAULTS["assets"]["cdn_prefix"]
    assert manifest["url_template"] == "{cdn_base_url}/{cdn_prefix}/{version}/{path}"
    assert "cdn_base_url" not in manifest, "The deployer supplies the base URL; do not pin one in the package."


def test_manifest_entries_are_well_formed() -> None:
    """Every entry needs a path, its loader and the condition it is loaded under."""
    entries = _entries(_manifest())
    paths = [entry["path"] for entry in entries]

    assert len(paths) == len(set(paths)), "Manifest paths must be unique across required and conditional."
    for entry in entries:
        assert entry["path"], "Each entry needs a CDN-relative path."
        assert entry["loaded_by"], f"{entry['path']}: record which template loads the asset."
        assert entry["condition"], f"{entry['path']}: record the condition the asset is loaded under."


def test_required_entries_are_loaded_unconditionally() -> None:
    """The required subset is what every rendered page needs, so it is not optional."""
    for entry in _manifest()["required"]:
        assert entry["condition"] == "always", (
            f"{entry['path']}: a conditionally loaded asset belongs in 'conditional', not 'required'."
        )


def test_templates_do_not_request_assets_missing_from_the_manifest() -> None:
    """A new {% insight_asset %} reference must be added to the manifest."""
    manifest_paths = {entry["path"] for entry in _entries(_manifest())}
    expected = {_to_manifest_path(path) for path in _template_asset_paths()}

    missing = sorted(expected - manifest_paths)
    assert not missing, (
        f"Templates request assets that CDN verification would not check: {missing}. "
        "Add them to insight_ui/cdn_manifest.json."
    )


def test_manifest_does_not_require_assets_no_template_requests() -> None:
    """A removed template reference must not leave a stale entry behind."""
    manifest_paths = {entry["path"] for entry in _entries(_manifest())}
    expected = {_to_manifest_path(path) for path in _template_asset_paths()}

    stale = sorted(manifest_paths - expected)
    assert not stale, (
        f"The manifest still requires assets no shipped template loads: {stale}. "
        "Remove them, or the verification gate blocks releases over unused files."
    )


@pytest.mark.parametrize("entry", _entries(_manifest()), ids=lambda entry: entry["path"])
def test_every_manifest_entry_maps_to_a_packaged_asset(entry: dict[str, Any]) -> None:
    """The manifest must not require a URL the package cannot produce."""
    source = _to_source_asset(entry["path"])

    assert source.is_file(), (
        f"{entry['path']}: no readable package asset at {source.relative_to(ROOT)}. "
        "The minified variant is generated from it, so verification would ask for a file that is never built."
    )


def test_stylesheet_entry_guards_against_template_and_asset_skew() -> None:
    """The stylesheet carries the selector guard that motivated the manifest."""
    stylesheet_path = _to_manifest_path(CONFIG_DEFAULTS["stylesheet"])
    entry = next(item for item in _manifest()["required"] if item["path"] == stylesheet_path)

    selectors = entry["must_contain_selectors"]
    assert selectors, "Keep the responsive selector guard: it is what catches a stale stylesheet on the CDN."
    # Uses the verification script's own matcher, so the gate and this guard cannot drift apart.
    stylesheet = (STATIC_ROOT / "css/tailwind.css").read_text()
    absent = sorted(selector for selector in selectors if not stylesheet_contains(stylesheet, selector))
    assert not absent, (
        f"The packaged stylesheet no longer contains guarded selectors: {absent}. "
        "Verification would fail against a correctly published asset."
    )
