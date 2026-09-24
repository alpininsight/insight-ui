# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Exercise public guide examples without restoring the documentation app."""

import ast
import re
import tomllib
from pathlib import Path
from urllib.parse import unquote, urlsplit

import pytest
from bs4 import BeautifulSoup
from defusedxml import ElementTree
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
    assert "](https://github.com/alpininsight/insight-ui/blob/main/CONTRIBUTING.md)" in (ROOT / "README.md").read_text(
        encoding="utf-8"
    )


def test_readme_links_work_outside_github() -> None:
    """PyPI cannot resolve repository-relative README links or image sources."""
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    # Include Markdown inside the raw HTML hero, which Python-Markdown skips.
    links = re.findall(r"\]\(([^\s)]+)\)", readme)
    links.extend(re.findall(r"^\[[^\]]+\]:\s*<?([^\s>]+)>?", readme, re.MULTILINE))
    soup = BeautifulSoup(readme, "html.parser")
    links.extend(str(element.get("href") or element.get("src")) for element in soup.select("[href], [src]"))
    assert links
    for link in links:
        target = urlsplit(link)
        assert target.scheme == "https", link
        assert target.netloc, link


def test_public_site_links_use_the_documented_routes() -> None:
    """The package entry points use the public host and exact no-slash docs routes."""
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    assert project["urls"]["Homepage"] == "https://django-insight-ui.com/"
    assert project["urls"]["Documentation"] == "https://django-insight-ui.com/docs/installation"
    assert "](https://django-insight-ui.com/)" in readme
    assert "](https://django-insight-ui.com/docs/installation)" in readme
    assert "](https://django-insight-ui.com/docs/configs)" in readme
    assert "https://insight-ui.com" not in readme


def test_readme_hero_uses_the_public_display_name() -> None:
    """The README bubble and its accessible label must name the same product."""
    label = "Django-Insight-UI"
    soup = BeautifulSoup((ROOT / "README.md").read_text(encoding="utf-8"), "html.parser")
    image = soup.find(
        "img",
        src=lambda value: value and urlsplit(value).path.endswith("/.github/assets/hero-title.svg"),
    )
    assert image is not None
    assert urlsplit(image["src"]).query == "v=django-insight-ui"
    assert image["alt"] == label
    assert image["width"] == "600"

    svg = ElementTree.parse(ROOT / ".github/assets/hero-title.svg").getroot()
    namespace = {"svg": "http://www.w3.org/2000/svg"}
    title = svg.find("svg:title", namespace)
    assert title is not None
    assert title.text == label
    assert svg.attrib["role"] == "img"
    assert svg.attrib["aria-labelledby"] == title.attrib["id"]
    assert len(svg.findall(".//svg:clipPath/svg:path", namespace)) == len(label)
    assert svg.findall(".//svg:text", namespace) == []


@pytest.mark.parametrize("path", DOCUMENTS, ids=lambda path: str(path.relative_to(ROOT)))
def test_public_document_links_resolve(path: Path) -> None:
    """Keep repository-relative guide, source and image links usable on GitHub."""
    html = markdown(path.read_text(encoding="utf-8"), extensions=["fenced_code", "tables"])
    soup = BeautifulSoup(html, "html.parser")
    for element in soup.select("[href], [src]"):
        target = urlsplit(str(element.get("href") or element.get("src")))
        repository_prefix = "/alpininsight/insight-ui/blob/main/"
        if target.netloc == "github.com" and target.path.startswith(repository_prefix):
            linked_path = (ROOT / unquote(target.path.removeprefix(repository_prefix))).resolve()
        elif target.scheme or target.netloc:
            continue
        else:
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
