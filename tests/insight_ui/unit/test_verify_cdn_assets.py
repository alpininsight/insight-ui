# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the CDN verification gate.

The gate blocks deployments, so a false failure is as expensive as a missed
one. These tests run without network access.
"""

from __future__ import annotations

import urllib.error
from typing import Any

import pytest
from scripts import verify_cdn_assets as verify_module
from scripts.verify_cdn_assets import asset_url, check_asset, css_class_selector, stylesheet_contains, verify

IMMUTABLE = "public, max-age=31536000, immutable"
MANIFEST = {
    "cdn_prefix": "insight-ui",
    "url_template": "{cdn_base_url}/{cdn_prefix}/{version}/{path}",
    "required": [
        {"path": "css/tailwind.min.css", "condition": "always", "must_contain_selectors": ["lg:block"]},
        {"path": "js/insight-ui-init.min.js", "condition": "always"},
    ],
    "conditional": [{"path": "css/prism.min.css", "condition": "INSIGHT_UI.load_prism = True"}],
}


class _FakeResponse:
    """Minimal stand-in for the object urlopen returns."""

    def __init__(self, status: int = 200, headers: dict[str, str] | None = None, body: str = "") -> None:
        default = {"Cache-Control": IMMUTABLE, "Access-Control-Allow-Origin": "*"}
        self.status = status
        self.headers = default if headers is None else headers
        self._body = body

    def read(self) -> bytes:
        """Return the response body."""
        return self._body.encode()

    def __enter__(self) -> _FakeResponse:
        """Enter the context manager."""
        return self

    def __exit__(self, *_: object) -> None:
        """Leave the context manager."""


def _patch_response(
    monkeypatch: pytest.MonkeyPatch,
    response: Any,  # noqa: ANN401 - fake or exception
    sent: list[Any] | None = None,
) -> None:
    """Make urlopen return a fake response or raise a prepared error."""

    def _fake_urlopen(request: Any, timeout: int = 0) -> Any:  # noqa: ANN401
        if sent is not None:
            sent.append(request)
        if isinstance(response, Exception):
            raise response
        return response

    monkeypatch.setattr(verify_module.urllib.request, "urlopen", _fake_urlopen)


def test_utility_selectors_are_css_escaped() -> None:
    """Tailwind escapes the variant colon; the raw name never appears."""
    assert css_class_selector("lg:block") == r".lg\:block"


def test_stylesheet_matching_accepts_the_escaped_form() -> None:
    """A compiled stylesheet must not be reported as missing its own utilities."""
    compiled = r".lg\:block { display: block; }"

    assert stylesheet_contains(compiled, "lg:block")
    assert not stylesheet_contains(".other { display: block; }", "lg:block")


def test_asset_url_follows_the_manifest_template() -> None:
    """The deployer's base URL and the manifest prefix compose the final URL."""
    url = asset_url(MANIFEST, "https://cdn.example.com/", "v1.14.0", "css/tailwind.min.css")

    assert url == "https://cdn.example.com/insight-ui/v1.14.0/css/tailwind.min.css"


def test_non_https_urls_are_refused() -> None:
    """Verification must not be pointed at an unencrypted origin."""
    with pytest.raises(SystemExit, match="non-HTTPS"):
        check_asset("http://cdn.example.com/a.css", {})


def test_a_correctly_published_asset_verifies(monkeypatch: pytest.MonkeyPatch) -> None:
    """The happy path reports no problems."""
    _patch_response(monkeypatch, _FakeResponse(body=r".lg\:block{display:block}"))

    problems = check_asset("https://cdn.example.com/a.css", MANIFEST["required"][0])

    assert problems == []


@pytest.mark.parametrize(
    ("headers", "expected"),
    [
        ({"Cache-Control": "public, max-age=60", "Access-Control-Allow-Origin": "*"}, "immutable"),
        ({"Cache-Control": "immutable", "Access-Control-Allow-Origin": "*"}, "max-age"),
        ({"Cache-Control": IMMUTABLE, "Access-Control-Allow-Origin": ""}, "Access-Control-Allow-Origin"),
    ],
)
def test_cache_and_cors_problems_are_reported(
    monkeypatch: pytest.MonkeyPatch, headers: dict[str, str], expected: str
) -> None:
    """A mutable or non-shareable asset must not pass the gate."""
    _patch_response(monkeypatch, _FakeResponse(headers=headers))

    problems = check_asset("https://cdn.example.com/a.js", {})

    assert any(expected in problem for problem in problems), problems


def test_the_cors_probe_sends_an_origin(monkeypatch: pytest.MonkeyPatch) -> None:
    """Object stores answer CORS only for requests carrying an Origin.

    Probing without one sees no Access-Control-Allow-Origin and would report a
    correctly configured asset as broken, blocking a release for nothing.
    """
    sent: list[Any] = []
    _patch_response(monkeypatch, _FakeResponse(), sent)

    check_asset("https://cdn.example.com/a.js", {})

    assert sent[0].get_header("Origin") == verify_module.CORS_PROBE_ORIGIN


def test_a_stale_stylesheet_is_caught(monkeypatch: pytest.MonkeyPatch) -> None:
    """The skew that motivated the manifest: published CSS lacks current utilities."""
    _patch_response(monkeypatch, _FakeResponse(body=".unrelated{}"))

    problems = check_asset("https://cdn.example.com/a.css", MANIFEST["required"][0])

    assert any("missing required selectors" in problem for problem in problems), problems


def test_a_missing_asset_is_reported(monkeypatch: pytest.MonkeyPatch) -> None:
    """A version published without every asset must fail loudly."""
    _patch_response(monkeypatch, urllib.error.HTTPError("https://x/a.js", 404, "Not Found", {}, None))  # type: ignore[arg-type]

    assert check_asset("https://cdn.example.com/a.js", {}) == ["expected HTTP 200, got 404"]


def test_unknown_conditional_assets_are_rejected() -> None:
    """A typo in the deployer's invocation must not silently verify less."""
    with pytest.raises(SystemExit, match="Unknown conditional assets"):
        verify_module._selected_entries(MANIFEST, {"css/nope.min.css"})


def test_verify_checks_required_assets_and_aggregates_failures(monkeypatch: pytest.MonkeyPatch) -> None:
    """Every required asset is reported, not just the first failure."""
    _patch_response(monkeypatch, _FakeResponse(headers={"Cache-Control": "no-store"}, body=""))

    failures = verify("https://cdn.example.com", "v1.14.0", manifest=MANIFEST)

    checked = {failure.split(":", 2)[1] for failure in failures}
    assert len(checked) == len(MANIFEST["required"])


def test_verify_can_include_conditional_assets(monkeypatch: pytest.MonkeyPatch) -> None:
    """A deployment enabling Prism must be able to gate on its stylesheet too."""
    _patch_response(monkeypatch, _FakeResponse(body=r".lg\:block{}"))
    requested: list[str] = []
    monkeypatch.setattr(
        verify_module,
        "check_asset",
        lambda url, entry, timeout=0: requested.append(url) or [],  # noqa: ARG005
    )

    verify("https://cdn.example.com", "v1.14.0", conditional={"css/prism.min.css"}, manifest=MANIFEST)

    assert any("prism.min.css" in url for url in requested)
