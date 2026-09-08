# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Exercise public guide examples without restoring the documentation app."""

import ast
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import pytest
from bs4 import BeautifulSoup
from django.contrib.staticfiles import finders
from django.template import engines
from django.test import RequestFactory, override_settings
from insight_ui.config import get_config
from insight_ui.configs import ButtonConfig
from markdown import markdown

ROOT = Path(__file__).resolve().parents[3]
GUIDES = (
    "getting-started.md",
    "components.md",
    "conventions.md",
    "design-system.md",
    "static-assets.md",
    "i18n.md",
    "accessibility.md",
    "testing.md",
    "new-component-checklist.md",
)
DOCUMENTS = (ROOT / "README.md", ROOT / "CONTRIBUTING.md", *sorted((ROOT / "docs").glob("*.md")))
pytestmark = pytest.mark.skipif(
    not (ROOT / ".git").exists(),
    reason="Contributor guides belong to the Git checkout, not the source distribution.",
)


def _code_blocks(path: Path, language: str) -> list[str]:
    """Extract the actual fenced examples rather than duplicating their source."""
    pattern = rf"^```{re.escape(language)}\n(.*?)^```"
    return re.findall(pattern, path.read_text(encoding="utf-8"), re.MULTILINE | re.DOTALL)


def _documented_host_settings() -> dict[str, object]:
    """Use the guide's literal settings so tests cannot hide stale setup examples."""
    code = _code_blocks(ROOT / "docs/getting-started.md", "python")[0]
    tree = ast.parse(code)
    return {
        node.targets[0].id: ast.literal_eval(node.value)
        for node in tree.body
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)
    }


def test_public_guide_index_covers_contributor_tasks() -> None:
    """Every required public guide is present and discoverable from the index."""
    index = (ROOT / "docs/README.md").read_text(encoding="utf-8")
    for name in GUIDES:
        assert (ROOT / "docs" / name).is_file(), name
        assert f"]({name})" in index, name
    assert "](CONTRIBUTING.md)" in (ROOT / "README.md").read_text(encoding="utf-8")


@pytest.mark.parametrize("path", DOCUMENTS, ids=lambda path: str(path.relative_to(ROOT)))
def test_public_document_links_resolve(path: Path) -> None:
    """Keep repository-relative guide, source and image links usable on GitHub."""
    html = markdown(path.read_text(encoding="utf-8"), extensions=["fenced_code", "tables"])
    soup = BeautifulSoup(html, "html.parser")
    for element in soup.select("[href], [src]"):
        target = urlsplit(str(element.get("href") or element.get("src")))
        if target.scheme or target.netloc:
            continue
        linked_path = (path.parent / unquote(target.path)).resolve() if target.path else path
        assert linked_path.is_relative_to(ROOT), (path, target.path)
        assert linked_path.exists(), (path, target.path)
        if target.fragment and linked_path.suffix == ".md":
            linked_html = markdown(linked_path.read_text(encoding="utf-8"), extensions=["fenced_code", "tables", "toc"])
            linked_soup = BeautifulSoup(linked_html, "html.parser")
            assert linked_soup.find(id=unquote(target.fragment)) is not None, (path, target.fragment)


@pytest.mark.parametrize("path", DOCUMENTS, ids=lambda path: str(path.relative_to(ROOT)))
def test_public_python_examples_parse(path: Path) -> None:
    """Partial settings examples must still be valid Python snippets."""
    for code in _code_blocks(path, "python"):
        ast.parse(code, filename=str(path))


@pytest.mark.parametrize("path", DOCUMENTS, ids=lambda path: str(path.relative_to(ROOT)))
def test_public_template_examples_render(path: Path) -> None:
    """Compile real tag signatures and render the documented template examples."""
    host_settings = _documented_host_settings()
    with override_settings(INSIGHT_UI=host_settings["INSIGHT_UI"], STATIC_URL=host_settings["STATIC_URL"]):
        for code in _code_blocks(path, "django"):
            template = engines["django"].from_string(code)
            rendered = template.render(
                {
                    **get_config(),
                    "save_button": ButtonConfig(label="Save", button_type="submit"),
                    "display_name": "Contributor",
                    "items": ["one", "two"],
                },
                request=RequestFactory().get("/"),
            )
            assert rendered.strip(), path
            assert "{%" not in rendered, path


def test_readme_example_renders_content_and_packaged_assets() -> None:
    """The quick start renders actual content, with CSS/JS and valid icon paths."""
    examples = _code_blocks(ROOT / "README.md", "django")
    assert examples, "README must contain a runnable component example"
    host_settings = _documented_host_settings()
    assert "insight_ui" in host_settings["INSTALLED_APPS"]
    assert "django.contrib.staticfiles" in host_settings["INSTALLED_APPS"]
    assert "documentation" not in host_settings["INSTALLED_APPS"]
    with override_settings(INSIGHT_UI=host_settings["INSIGHT_UI"], STATIC_URL=host_settings["STATIC_URL"]):
        html = engines["django"].from_string(examples[0]).render({}, request=RequestFactory().get("/"))
    soup = BeautifulSoup(html, "html.parser")
    assert soup.title.get_text() == "My application"
    assert soup.select_one("button.btn-primary").get_text(strip=True) == "Get started"
    assert "Welcome" in soup.get_text()
    assert "Card content goes here." in soup.get_text()
    assert "Component rendered successfully." in soup.get_text()
    assert soup.select_one('link[href="/static/insight_ui/css/tailwind.css"]') is not None
    assert soup.select_one('script[src="/static/insight_ui/js/insight-ui-init.js"]') is not None
    for element in soup.select("[href], [src]"):
        url = str(element.get("href") or element.get("src"))
        if url.startswith("/static/"):
            assert finders.find(url.removeprefix("/static/")), url


@pytest.mark.parametrize("version", ["1.2.3", "v1.2.3"])
def test_documented_cdn_example_resolves_versioned_minified_assets(version: str) -> None:
    """The same documented include supports a host-owned, versioned CDN."""
    examples = _code_blocks(ROOT / "docs/static-assets.md", "django")
    assert examples
    with override_settings(
        INSIGHT_UI={
            "assets": {
                "cdn_enabled": True,
                "use_minified": True,
                "cdn_base_url": "https://cdn.example.com",
                "cdn_prefix": "insight-ui",
                "cdn_version": version,
            }
        }
    ):
        html = engines["django"].from_string(examples[0]).render({})
    soup = BeautifulSoup(html, "html.parser")
    prefix = "https://cdn.example.com/insight-ui/v1.2.3"
    assert soup.link["href"] == f"{prefix}/css/tailwind.min.css"
    assert soup.script["src"] == f"{prefix}/js/insight-ui-init.min.js"


def test_documented_design_tokens_exist_in_source() -> None:
    """The public role table must not advertise invented or removed variables."""
    guide = (ROOT / "docs/design-system.md").read_text(encoding="utf-8")
    css = (ROOT / "insight_ui/utils/input.css").read_text(encoding="utf-8")
    tokens = re.findall(r"`(--[a-z][a-z0-9-]*)`", guide)
    assert tokens
    for token in tokens:
        assert re.search(rf"{re.escape(token)}\s*:", css), token


def test_public_guides_are_markdown_not_an_application() -> None:
    """Allow contributor text without weakening the application source boundary."""
    files = [path for path in (ROOT / "docs").rglob("*") if path.is_file()]
    assert files
    assert not any(path.suffix in {".py", ".html", ".js", ".css"} for path in files)
    assert not (ROOT / "docs/enterprise").exists()
    assert not (ROOT / "docs/audit-preparation").exists()
