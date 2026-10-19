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
from django.template.loader import render_to_string
from django.test import RequestFactory, override_settings
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


def _template_asset_sources() -> dict[str, set[str]]:
    """Map referenced assets to the package templates that load them."""
    sources: dict[str, set[str]] = {}
    for template in sorted(TEMPLATE_ROOT.rglob("*.html")):
        for match in INSIGHT_ASSET_TAG.finditer(template.read_text()):
            argument = match.group("argument")
            if argument[0] in {"'", '"'}:
                asset_path = argument[1:-1]
            else:
                asset_path = CONTEXT_VARIABLES.get(argument)
                assert asset_path is not None, (
                    f"{template.relative_to(ROOT)}: '{argument}' is a new dynamic insight_asset source. "
                    f"Teach {Path(__file__).name} how to resolve it so manifest coverage stays checkable."
                )
            sources.setdefault(asset_path, set()).add(template.name)
    return sources


def _assert_manifest_covers_template_assets(manifest: dict[str, Any], asset_paths: set[str]) -> None:
    """Fail with actionable paths when a template asset is absent from the manifest."""
    manifest_paths = {entry["path"] for entry in _entries(manifest)}
    expected = {_to_manifest_path(path) for path in asset_paths}
    missing = sorted(expected - manifest_paths)
    assert not missing, (
        f"Templates request assets that CDN verification would not check: {missing}. "
        "Add them to insight_ui/cdn_manifest.json."
    )


def _rendered_base_asset_paths(*, load_prism: bool) -> set[str]:
    """Render the shipped base template and return package assets present in its output."""
    with override_settings(INSIGHT_UI={"load_prism": load_prism}):
        rendered = render_to_string("insight_ui/base.html", request=RequestFactory().get("/"))
    return {path for path in _template_asset_paths() if f"/{path}" in rendered}


def _assert_rendered_asset_classification(
    manifest: dict[str, Any],
    *,
    always_loaded: set[str],
    conditionally_loaded: set[str],
) -> None:
    """Match required and conditional manifest groups to observed template behavior."""
    expected_required = {_to_manifest_path(path) for path in always_loaded}
    expected_conditional = {_to_manifest_path(path) for path in conditionally_loaded}
    actual_required = {entry["path"] for entry in manifest["required"]}
    actual_conditional = {entry["path"] for entry in manifest["conditional"]}

    assert actual_required == expected_required, (
        "Required manifest entries disagree with unconditional template assets: "
        f"expected {sorted(expected_required)}, found {sorted(actual_required)}."
    )
    assert actual_conditional == expected_conditional, (
        "Conditional manifest entries disagree with conditional template assets: "
        f"expected {sorted(expected_conditional)}, found {sorted(actual_conditional)}."
    )

    for entry in manifest["required"]:
        assert entry["condition"] == "always", f"{entry['path']}: required assets must use condition 'always'."
    for entry in manifest["conditional"]:
        assert entry["condition"] == "INSIGHT_UI.load_prism = True", (
            f"{entry['path']}: no rendered-template check is defined for condition {entry['condition']!r}."
        )


def _assert_manifest_loaders_match_templates(manifest: dict[str, Any]) -> None:
    """Ensure each manifest loader names the template that contains its asset tag."""
    sources = _template_asset_sources()
    for entry in _entries(manifest):
        package_path = f"{PACKAGE_STATIC_PREFIX}{entry['path']}"
        package_path = re.sub(r"\.min(?=\.(?:css|js)$)", "", package_path)
        expected_sources = sorted(sources.get(package_path, set()))
        declared_source = entry["loaded_by"].split(" (", maxsplit=1)[0]
        assert declared_source == ", ".join(expected_sources), (
            f"{entry['path']}: loaded_by says {entry['loaded_by']!r}, but its template reference is in "
            f"{expected_sources or 'no shipped template'}."
        )


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


def test_rendered_templates_match_manifest_classification_and_loaders() -> None:
    """Classify assets by actual base-template output for both Prism settings."""
    manifest = _manifest()
    rendered_without_prism = _rendered_base_asset_paths(load_prism=False)
    rendered_with_prism = _rendered_base_asset_paths(load_prism=True)
    prism_asset = "insight_ui/css/prism.css"

    assert prism_asset not in rendered_without_prism
    assert prism_asset in rendered_with_prism
    always_loaded = rendered_without_prism
    conditionally_loaded = rendered_with_prism - rendered_without_prism
    assert rendered_without_prism <= rendered_with_prism
    _assert_rendered_asset_classification(
        manifest,
        always_loaded=always_loaded,
        conditionally_loaded=conditionally_loaded,
    )
    _assert_manifest_loaders_match_templates(manifest)


def test_manifest_fails_when_a_required_asset_is_misclassified_as_conditional() -> None:
    """A known always-loaded asset must not be moved into the conditional group."""
    manifest = _manifest()
    entry = manifest["required"].pop()
    entry["condition"] = "INSIGHT_UI.load_prism = True"
    manifest["conditional"].append(entry)

    with pytest.raises(AssertionError, match="Required manifest entries disagree"):
        _assert_rendered_asset_classification(
            manifest,
            always_loaded=_rendered_base_asset_paths(load_prism=False),
            conditionally_loaded=(
                _rendered_base_asset_paths(load_prism=True) - _rendered_base_asset_paths(load_prism=False)
            ),
        )


def test_manifest_fails_when_a_conditional_asset_is_misclassified_as_unconditional() -> None:
    """The conditional Prism stylesheet must not be moved into the required group."""
    manifest = _manifest()
    entry = manifest["conditional"].pop()
    entry["condition"] = "always"
    manifest["required"].append(entry)

    with pytest.raises(AssertionError, match="Required manifest entries disagree"):
        _assert_rendered_asset_classification(
            manifest,
            always_loaded=_rendered_base_asset_paths(load_prism=False),
            conditionally_loaded=(
                _rendered_base_asset_paths(load_prism=True) - _rendered_base_asset_paths(load_prism=False)
            ),
        )


def test_manifest_fails_when_a_conditional_entry_claims_to_be_always_loaded() -> None:
    """The condition text must describe the behavior observed in both renders."""
    manifest = _manifest()
    manifest["conditional"][0]["condition"] = "always"

    with pytest.raises(AssertionError, match="no rendered-template check is defined"):
        _assert_rendered_asset_classification(
            manifest,
            always_loaded=_rendered_base_asset_paths(load_prism=False),
            conditionally_loaded=(
                _rendered_base_asset_paths(load_prism=True) - _rendered_base_asset_paths(load_prism=False)
            ),
        )


def test_manifest_fails_when_loader_does_not_name_the_referencing_template() -> None:
    """Loader metadata is tied to the package template that contains the asset tag."""
    manifest = _manifest()
    manifest["required"][0]["loaded_by"] = "other.html (INSIGHT_UI.stylesheet)"

    with pytest.raises(AssertionError, match="loaded_by says"):
        _assert_manifest_loaders_match_templates(manifest)


def test_templates_do_not_request_assets_missing_from_the_manifest() -> None:
    """A new {% insight_asset %} reference must be added to the manifest."""
    _assert_manifest_covers_template_assets(_manifest(), _template_asset_paths())


def test_new_template_asset_reference_fails_with_actionable_manifest_diagnostic() -> None:
    """A newly referenced conditional asset cannot silently escape CDN verification."""
    with pytest.raises(AssertionError, match=r"Templates request assets.*css/new-feature\.min\.css"):
        _assert_manifest_covers_template_assets(
            _manifest(),
            _template_asset_paths() | {"insight_ui/css/new-feature.css"},
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
