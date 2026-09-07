# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Exercise generated sources in fresh Python processes, not only string mocks."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from insight_ui.component_manifest import CATEGORIES, build_example_config, parse_manifest, validate_slug
from insight_ui.scaffolding import ComponentScaffold, FileChange, apply_component

ROOT = Path(__file__).resolve().parents[3]


def run_python(root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    """Use the test interpreter but import the isolated source checkout."""
    return subprocess.run(  # noqa: S603 - test-only subprocess, no shell
        [sys.executable, *arguments],
        cwd=root,
        env={**os.environ, "PYTHONPATH": str(root), "DJANGO_SETTINGS_MODULE": "tests.settings"},
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )


@pytest.fixture
def source_checkout(tmp_path: Path) -> Path:
    """Copy only the public package and a minimal Django host into a Git target."""
    root = tmp_path / "package"
    root.mkdir()
    shutil.copytree(ROOT / "insight_ui", root / "insight_ui", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    shutil.copy2(ROOT / "pyproject.toml", root / "pyproject.toml")
    (root / "tests").mkdir()
    for name in ("__init__.py", "settings.py", "context.py", "urls.py"):
        shutil.copy2(ROOT / "tests" / name, root / "tests" / name)
    subprocess.run(["git", "init", "--quiet", str(root)], check=True, capture_output=True, timeout=15)  # noqa: S603, S607
    return root


def generate(root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    """Invoke the real public Django command."""
    return run_python(root, "-m", "django", "create_component", *arguments)


def source_snapshot(root: Path) -> dict[str, bytes]:
    """Ignore import caches while proving that validation caused no source edits."""
    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts
    }


@pytest.mark.parametrize("category", CATEGORIES)
def test_every_category_generates_importable_renderable_source(source_checkout: Path, category: str) -> None:
    """Filter's field alias and every other category survive real import and render."""
    result = generate(source_checkout, "--name", "Sample Unit", "--category", category)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "documentation" not in result.stdout
    check = run_python(source_checkout, "-m", "django", "check")
    assert check.returncode == 0, check.stdout + check.stderr
    rendered = run_python(
        source_checkout,
        "-c",
        """
import django
django.setup()
from django.template import Template, Context
from insight_ui.component_manifest import load_manifest, manifest_path, build_example_config
from dataclasses import is_dataclass
manifest = load_manifest(manifest_path("sample_unit"))
config = build_example_config(manifest)
assert is_dataclass(config)
html = Template("{% load insight_tags %}{% sample_unit config=config %}").render(Context({"config": config}))
assert 'id="sample_unit-example"' in html
assert 'Sample Unit' in html
""",
    )
    assert rendered.returncode == 0, rendered.stdout + rendered.stderr


@pytest.mark.parametrize("level", ["molecule", "organism"])
def test_composition_uses_real_nested_configs_and_existing_tags(source_checkout: Path, level: str) -> None:
    """Composition handles ButtonConfig's required label and optional field configs."""
    result = generate(
        source_checkout,
        "--name",
        "Sample Panel",
        "--category",
        "form",
        "--level",
        level,
        "--compose",
        "input_field,button",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    rendered = run_python(
        source_checkout,
        "-c",
        """
import django
django.setup()
from django.template import Context, Template
from insight_ui.component_manifest import build_example_config, load_manifest, manifest_path
from insight_ui.configs import ButtonConfig, InputFieldConfig
config = build_example_config(load_manifest(manifest_path("sample_panel")))
assert isinstance(config.button, ButtonConfig)
assert isinstance(config.input_field, InputFieldConfig)
html = Template("{% load insight_tags %}{% sample_panel config=config %}").render(Context({"config":config}))
assert '<button' in html and '<input' in html
assert 'Input Field' in html and 'Button' in html
assert 'Sample Panel' in html
""",
    )
    assert rendered.returncode == 0, rendered.stdout + rendered.stderr
    template = (source_checkout / "insight_ui/templates/insight_ui/components/sample_panel.html").read_text()
    assert "{% button config=sample_panel_config.button %}" in template
    assert "<button" not in template


def test_generated_component_tests_execute(source_checkout: Path) -> None:
    """The scaffold contains runnable assertions rather than placeholder tests."""
    result = generate(source_checkout, "--name", "Sample Unit", "--category", "util")
    assert result.returncode == 0, result.stderr
    tests = run_python(source_checkout, "-m", "pytest", "tests/insight_ui/unit/components/test_sample_unit.py", "-q")
    assert tests.returncode == 0, tests.stdout + tests.stderr
    assert "2 passed" in tests.stdout


def test_dry_run_and_duplicate_do_not_modify_sources(source_checkout: Path) -> None:
    """Contributors can inspect changes; a second run never overwrites their work."""
    arguments = ("--name", "Sample Unit", "--category", "filter")
    before = source_snapshot(source_checkout)
    result = generate(source_checkout, *arguments, "--dry-run")
    assert result.returncode == 0, result.stderr
    assert "Would write" in result.stdout
    assert source_snapshot(source_checkout) == before
    result = generate(source_checkout, *arguments)
    assert result.returncode == 0, result.stderr
    generated = source_snapshot(source_checkout)
    result = generate(source_checkout, *arguments)
    assert result.returncode != 0
    assert "already exists" in result.stderr
    assert source_snapshot(source_checkout) == generated


@pytest.mark.parametrize(
    ("name", "level", "compose"),
    [
        ("../Bad", "atom", ""),
        ("class", "atom", ""),
        ("Build Config", "atom", ""),
        ("Sample Unit", "atom", "button"),
        ("Sample Unit", "molecule", ""),
        ("Sample Unit", "organism", "button,does_not_exist"),
        ("Sample Unit", "molecule", "button,button"),
    ],
)
def test_invalid_request_never_partially_registers(
    source_checkout: Path,
    name: str,
    level: str,
    compose: str,
) -> None:
    """Validate every target and composition before the first mutation."""
    before = source_snapshot(source_checkout)
    result = generate(source_checkout, "--name", name, "--category", "util", "--level", level, "--compose", compose)
    assert result.returncode != 0
    assert source_snapshot(source_checkout) == before


def test_cross_checkout_import_mismatch_is_rejected(source_checkout: Path) -> None:
    """--package-root must never write sources different from the imported package."""
    before = source_snapshot(source_checkout)
    result = generate(ROOT, "--name", "Sample Unit", "--category", "util", "--package-root", str(source_checkout))
    assert result.returncode != 0
    assert "imported insight_ui" in result.stderr
    assert source_snapshot(source_checkout) == before


def test_symlink_target_is_rejected(source_checkout: Path, tmp_path: Path) -> None:
    """A new template must not overwrite a file outside the repository."""
    outside = tmp_path / "outside.html"
    outside.write_text("preserve me")
    target = source_checkout / "insight_ui/templates/insight_ui/components/sample_unit.html"
    target.symlink_to(outside)
    before = source_snapshot(source_checkout)
    result = generate(source_checkout, "--name", "Sample Unit", "--category", "util")
    assert result.returncode != 0
    assert outside.read_text() == "preserve me"
    assert source_snapshot(source_checkout) == before


def test_optional_js_is_registered_in_all_lifecycle_entry_points(source_checkout: Path) -> None:
    """Generated JS is imported, initialized and has a lifecycle regression test."""
    result = generate(source_checkout, "--name", "Sample Unit", "--category", "util", "--js")
    assert result.returncode == 0, result.stderr
    initializer = (source_checkout / "insight_ui/static/insight_ui/js/insight-ui-init.js").read_text()
    assert 'import { SampleUnit } from "./insight-ui-sample-unit.js";' in initializer
    assert "\tSampleUnit," in initializer
    assert "\tSampleUnit.initAll();" in initializer
    module = (source_checkout / "insight_ui/static/insight_ui/js/insight-ui-sample-unit.js").read_text()
    assert "this.controller.abort()" in module
    assert (source_checkout / "tests/js/sample-unit.test.js").exists()


def test_atomic_level_does_not_change_category() -> None:
    """Purpose and composition depth are separate metadata axes."""
    atom = ComponentScaffold("Sample Unit", "input")
    organism = ComponentScaffold("Sample Panel", "input", "organism", ("button", "input_field"))
    atom.validate()
    organism.validate()
    assert atom.category == organism.category


@pytest.mark.parametrize(
    "name", ["ThemeToggle", "Object", "WeakMap", "AbortController", "TableOfContents", "InsightUI"]
)
def test_js_name_collision_never_modifies_sources(source_checkout: Path, name: str) -> None:
    """A new tag must not shadow initializer bindings or its own lifecycle globals."""
    before = source_snapshot(source_checkout)
    result = generate(source_checkout, "--name", name, "--category", "util", "--js")
    assert result.returncode != 0
    assert "JavaScript name" in result.stderr
    assert source_snapshot(source_checkout) == before


@pytest.mark.parametrize("compose", ["modal,button", "navbar,button"])
def test_config_import_cycle_never_modifies_sources(source_checkout: Path, compose: str) -> None:
    """Both direct and transitive Config cycles are rejected before registration."""
    before = source_snapshot(source_checkout)
    result = generate(
        source_checkout,
        "--name",
        "Sample Panel",
        "--category",
        "input",
        "--level",
        "molecule",
        "--compose",
        compose,
    )
    assert result.returncode != 0
    assert "Config import cycle" in result.stderr
    assert source_snapshot(source_checkout) == before


def test_apply_refuses_concurrent_edits(tmp_path: Path) -> None:
    """Never overwrite changes made between planning and applying."""
    path = tmp_path / "config.py"
    path.write_text("user content")
    with pytest.raises(ValueError, match="changed after planning"):
        apply_component([FileChange(path, "old", "new")])
    assert path.read_text() == "user content"


@pytest.fixture
def contract() -> dict:
    """A manifest referencing an existing Config for pure contract tests."""
    return {
        "schema_version": 1,
        "slug": "sample_button",
        "name": "Sample Button",
        "category": "input",
        "level": "atom",
        "config_class": "insight_ui.configs.input.ButtonConfig",
        "template": "insight_ui/components/button.html",
        "uses": [],
        "examples": [{"name": "default", "config": {"label": "Sample"}}],
        "js_module": None,
    }


def test_manifest_builds_example_with_existing_config_api(contract: dict) -> None:
    """The contract is JSON data rather than an executable example docstring."""
    from insight_ui.configs.input import ButtonConfig  # noqa: PLC0415

    manifest = parse_manifest(json.loads(json.dumps(contract)))
    assert build_example_config(manifest) == ButtonConfig(label="Sample")
    with pytest.raises(ValueError, match="Unknown example"):
        build_example_config(manifest, "not_present")


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("schema_version", 2),
        ("schema_version", True),
        ("slug", "../outside"),
        ("config_class", "os.system"),
        ("template", "insight_ui/components/../other.html"),
        ("js_module", "https://example.com/app.js"),
        ("level", "page"),
        ("category", "website"),
        ("uses", ["button"]),
        ("examples", []),
    ],
)
def test_manifest_rejects_invalid_contract_fields(contract: dict, key: str, value: object) -> None:
    """Downstream imports cannot use arbitrary modules, paths or schema versions."""
    contract[key] = value
    with pytest.raises(ValueError, match=r".+"):
        parse_manifest(contract)


@pytest.mark.parametrize("slug", ["../button", "button.html", "button %}", "", "Button"])
def test_invalid_preview_slug(slug: str) -> None:
    """Only known identifier-shaped paths reach the preview loader."""
    with pytest.raises(ValueError, match="lowercase snake_case"):
        validate_slug(slug)
