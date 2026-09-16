# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Test contributor tooling without a documentation app or a private checkout."""

from __future__ import annotations

import importlib
import io
import os
import shutil
import subprocess  # nosec B404
import sys
from http import HTTPStatus
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import Client, override_settings

if TYPE_CHECKING:
    from devtools.management.commands.create_component import Command

ROOT = Path(__file__).resolve().parents[3]
pytestmark = pytest.mark.skipif(
    not (ROOT / ".git").exists(), reason="Contributor tools are Git-checkout-only, not distribution payload."
)
CATEGORIES = ("layout", "navigation", "input", "popup", "util", "list", "filter", "card", "form")


@pytest.fixture
def scaffold(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Command, Path, io.StringIO]:
    """Run the real command against a disposable copy, never the worktree."""
    module = importlib.import_module("devtools.management.commands.create_component")
    public = tmp_path / "public"
    shutil.copytree(ROOT / "insight_ui", public / "insight_ui", ignore=shutil.ignore_patterns("__pycache__"))
    monkeypatch.setattr(module, "__file__", str(public / "devtools/management/commands/create_component.py"))
    output = io.StringIO()
    return module.Command(stdout=output), public, output


def source_snapshot(root: Path) -> dict[str, bytes]:
    """Detect even partial or accidental writes by the generator."""
    return {str(path.relative_to(root)): path.read_bytes() for path in root.rglob("*") if path.is_file()}


@pytest.mark.parametrize("category", CATEGORIES)
def test_each_category_generates_importable_renderable_component(
    scaffold: tuple[Command, Path, io.StringIO], category: str
) -> None:
    """Include filter.py's dc_field alias and render the actual generated tag."""
    command, public, _ = scaffold
    call_command(command, name="Example Panel", category=category, js=False)
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            """
import django
django.setup()
from django.template import Context, Template
from insight_ui.configs import ExamplePanelConfig
config = ExamplePanelConfig(tag_id='example-"quoted')
html = Template('{% load insight_tags %}{% example_panel config=config %}').render(Context({'config': config}))
assert 'id="example-&quot;quoted"' in html, html
assert 'bg-insight-surface' in html
assert 'rounded-insight-surface' in html
assert 'data-insight-example-panel' not in html
assert 'Example Panel component placeholder' in html
""",
        ],
        cwd=public,
        env={
            **os.environ,
            "PYTHONPATH": os.pathsep.join((str(public), str(ROOT))),
            "DJANGO_SETTINGS_MODULE": "tests.settings",
            "PYTHONDONTWRITEBYTECODE": "1",
        },
        capture_output=True,
        check=False,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert not (public / "insight_ui/component_manifests").exists()


def test_dry_run_does_not_write(scaffold: tuple[Command, Path, io.StringIO]) -> None:
    """The guide's preview command validates all files but changes none."""
    command, public, output = scaffold
    before = source_snapshot(public)
    call_command(command, "--name", "Example Panel", "--category", "form", "--no-js", "--dry-run")
    assert source_snapshot(public) == before
    assert "no files written" in output.getvalue()
    assert "insight_ui/configs/forms.py" in output.getvalue()


@pytest.mark.parametrize("name", ["Button", "class", "../Outside"])
def test_invalid_or_existing_name_never_writes(scaffold: tuple[Command, Path, io.StringIO], name: str) -> None:
    """Existing components and Python-invalid slugs cannot leave partial output."""
    command, public, _ = scaffold
    before = source_snapshot(public)
    with pytest.raises(CommandError):
        call_command(command, name=name, category="util", js=False)
    assert source_snapshot(public) == before


def test_repeated_generation_preserves_first_result(scaffold: tuple[Command, Path, io.StringIO]) -> None:
    """A retry must not silently overwrite a contributor's existing work."""
    command, public, _ = scaffold
    call_command(command, name="Example Panel", category="filter", js=False)
    before = source_snapshot(public)
    with pytest.raises(CommandError, match="already exists"):
        call_command(command, name="Example Panel", category="filter", js=False)
    assert source_snapshot(public) == before


def test_missing_config_import_fails_without_partial_writes(scaffold: tuple[Command, Path, io.StringIO]) -> None:
    """Do not print success when a changed source layout cannot be handled."""
    command, public, _ = scaffold
    config = public / "insight_ui/configs/filter.py"
    config.write_text(config.read_text().replace("field as dc_field", "fields as dc_field"))
    before = source_snapshot(public)
    with pytest.raises(CommandError, match=r"Missing dataclasses\.field"):
        call_command(command, name="Example Panel", category="filter", js=False)
    assert source_snapshot(public) == before


def test_optional_js_selector_matches_template(scaffold: tuple[Command, Path, io.StringIO]) -> None:
    """JS remains an explicit skeleton, with a usable template hook and handoff."""
    command, public, output = scaffold
    call_command(command, name="Example Panel", category="util", js=True)
    package = public / "insight_ui"
    template = (package / "templates/insight_ui/components/example_panel.html").read_text()
    script = (package / "static/insight_ui/js/insight-ui-example-panel.js").read_text()
    assert "data-insight-example-panel" in template
    assert 'querySelectorAll("[data-insight-example-panel]")' in script
    assert "Register the class in insight-ui-init.js" in output.getvalue()
    assert "Add component render/behavior tests" in output.getvalue()


def test_write_failure_restores_all_files(
    scaffold: tuple[Command, Path, io.StringIO], monkeypatch: pytest.MonkeyPatch
) -> None:
    """A mid-write failure must not leave a new template or truncated Config."""
    command, public, _ = scaffold
    before = source_snapshot(public)
    target = public / "insight_ui/configs/utils.py"
    original_write = Path.write_text

    def fail_after_truncation(path: Path, content: str, *args, **kwargs) -> int:
        if path == target:
            path.write_bytes(b"")
            message = "Simulated disk error"
            raise OSError(message)
        return original_write(path, content, *args, **kwargs)

    monkeypatch.setattr(Path, "write_text", fail_after_truncation)
    with pytest.raises(CommandError, match="Changes rolled back"):
        call_command(command, name="Example Panel", category="util", js=False)
    assert source_snapshot(public) == before


def test_documented_generator_commands_match_parser(scaffold: tuple[Command, Path, io.StringIO]) -> None:
    """Read the guide's real commands so removed CLI options cannot survive unnoticed."""
    import re  # noqa: PLC0415 - local to source-only documentation validation
    import shlex  # noqa: PLC0415

    command, _, _ = scaffold
    guide = (ROOT / "CONTRIBUTING.md").read_text().replace("\\\n", " ")
    calls = re.findall(r"^uv run python manage.py create_component (.+)$", guide, re.MULTILINE)
    assert calls
    parser = command.create_parser("manage.py", "create_component")
    for call in calls:
        options = parser.parse_args(shlex.split(call))
        assert options.name == "Example Panel"
        assert options.category == "form"
        assert options.js is False


def test_preview_renders_real_base_in_same_origin_frame() -> None:
    """The preview has real package assets and is frameable only on its own origin."""
    settings = importlib.import_module("devtools.settings")
    with override_settings(
        INSTALLED_APPS=settings.INSTALLED_APPS,
        ROOT_URLCONF="devtools.urls",
        TEMPLATES=settings.TEMPLATES,
        MIDDLEWARE=settings.MIDDLEWARE,
        INSIGHT_UI=settings.INSIGHT_UI,
        ALLOWED_HOSTS=["testserver"],
    ):
        client = Client()
        controls = client.get("/")
        preview = client.get("/preview/")
    assert controls.status_code == HTTPStatus.OK
    assert b'<iframe id="component-preview"' in controls.content
    assert b'src="/preview/"' in controls.content
    assert preview.status_code == HTTPStatus.OK
    assert preview.headers["X-Frame-Options"] == "SAMEORIGIN"
    assert controls.headers["X-Frame-Options"] == "DENY"
    assert b"Example Button" in preview.content
    assert b"insight_ui/css/tailwind.css" in preview.content
    assert b"insight-ui-init.js" in preview.content


def test_readme_does_not_claim_component_conformance() -> None:
    """Keep the public promise aligned with the accessibility guide."""
    readme = (ROOT / "README.md").read_text()
    assert "design target, not a verified package-wide conformance claim" in readme
    assert "WCAG 2.2 AA-compliant UI components" not in readme
