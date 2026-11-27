# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""A host changes theme tokens without a Tailwind build: INSIGHT_UI["theme_stylesheet"] sets them anew.

That only works while the compiled classes read the tokens at runtime through var(); Tailwind writes some
theme values into its classes as fixed values (shadows, for example).
"""

import re
from http import HTTPStatus
from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from django.test import override_settings

import insight_ui

BUILT_CSS = Path(insight_ui.__file__).parent / "static" / "insight_ui" / "css" / "tailwind.css"
CDN = {"assets": {"cdn_enabled": True, "cdn_base_url": "https://cdn.example.com", "cdn_version": "1.2.3"}}


def stylesheets(client) -> list[str]:  # noqa: ANN001
    """Render the base template and return the hrefs of its stylesheets in document order."""
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    return [link["href"] for link in BeautifulSoup(response.content, "html.parser").find_all("link", rel="stylesheet")]


@pytest.mark.django_db
@override_settings(INSIGHT_UI={"theme_stylesheet": "brand/theme.css"})
def test_theme_stylesheet_follows_the_main_stylesheet(client) -> None:  # noqa: ANN001
    """The theme stylesheet comes right after the package stylesheet, so its tokens win."""
    hrefs = stylesheets(client)

    assert hrefs[-2:] == ["/static/insight_ui/css/tailwind.css", "/static/brand/theme.css"]


@pytest.mark.django_db
def test_no_theme_stylesheet_by_default(client) -> None:  # noqa: ANN001
    """Without the setting only the package stylesheet is loaded."""
    assert stylesheets(client)[-1] == "/static/insight_ui/css/tailwind.css"


@pytest.mark.django_db
@override_settings(INSIGHT_UI={**CDN, "theme_stylesheet": "brand/theme.css"})
def test_theme_stylesheet_stays_local_with_the_cdn(client) -> None:  # noqa: ANN001
    """The CDN only hosts the package's files; the host's theme stylesheet is served locally."""
    assert "/static/brand/theme.css" in stylesheets(client)


@pytest.fixture(scope="module")
def built_css() -> str:
    """Read the compiled stylesheet shipped in the package."""
    return BUILT_CSS.read_text(encoding="utf-8")


@pytest.mark.django_db
@pytest.mark.parametrize("path", ["css/app.css", "insight_ui/css/app.css", "insight_ui/css/tailwind.css"])
@pytest.mark.parametrize("use_minified", [False, True])
def test_configured_main_stylesheet_stays_local(client, path: str, use_minified: bool) -> None:  # noqa: ANN001
    """An explicit host build never resolves to a package CDN file."""
    with override_settings(
        INSIGHT_UI={**CDN, "stylesheet": path, "assets": {**CDN["assets"], "use_minified": use_minified}}
    ):
        assert stylesheets(client)[-1] == f"/static/{path}"


@pytest.mark.parametrize(
    ("class_name", "token"),
    [
        ("bg-insight-surface", "--color-insight-bg-surface"),
        ("border-insight-raised", "--color-insight-border-raised"),
        ("text-insight-body", "--color-insight-text-body"),
        ("bg-insight-primary-action", "--color-insight-primary-action"),
        ("text-insight-danger-text", "--color-insight-danger-text"),
        ("rounded-insight-control", "--radius-insight-control"),
        ("p-insight-m", "--spacing-insight-m"),
        ("shadow-insight-raised", "--shadow-insight-raised"),
        ("text-sm", "--text-sm"),
    ],
)
def test_token_classes_read_the_token_at_runtime(built_css: str, class_name: str, token: str) -> None:
    """Each token group reaches its classes as var(), so a theme stylesheet can change it."""
    rule = re.search(rf"^\s*\.{re.escape(class_name)} {{([^}}]*)}}", built_css, re.MULTILINE)

    assert rule, f".{class_name} is missing from the stylesheet"
    assert f"var({token})" in rule.group(1)


def test_page_font_reads_the_font_token(built_css: str) -> None:
    """The page font comes from --font-sans, so a theme stylesheet can switch it."""
    assert "--default-font-family: var(--font-sans);" in built_css
    assert "font-family: var(--default-font-family" in built_css


PACKAGE = Path(insight_ui.__file__).parent
CLASS_ATTRIBUTE = re.compile(r"""\bclass\s*=\s*(?:"([^"]*)"|'([^']*)')""")
SHADOW_CLASS = re.compile(r"(?<![\w-])(?:[\w-]+:)*shadow-insight-")
RING_CLASS = re.compile(r"(?<![\w-])(?:[\w-]+:)*ring-[\w-]+")


def shadowed_class_lists() -> list[tuple[str, str]]:
    """Class lists of templates and @apply rules that use a shadow-insight-* class."""
    found = []
    for template in (PACKAGE / "templates").rglob("*.html"):
        for match in CLASS_ATTRIBUTE.finditer(template.read_text(encoding="utf-8")):
            value = match.group(1) or match.group(2) or ""
            if SHADOW_CLASS.search(value):
                found.append((template.name, value))
    css_lines = (PACKAGE / "utils" / "input.css").read_text(encoding="utf-8").splitlines()
    found.extend(("input.css", line) for line in css_lines if "@apply" in line and SHADOW_CLASS.search(line))
    return found


def test_shadowed_elements_show_focus_with_an_outline() -> None:
    """A theme may set a shadow token to none; a ring on the same element would share its box-shadow."""
    combined = [
        f"{source}: {RING_CLASS.findall(value)}" for source, value in shadowed_class_lists() if RING_CLASS.search(value)
    ]

    assert shadowed_class_lists(), "the scan found no shadow-insight-* classes"
    assert combined == []


@pytest.mark.parametrize("shadow", ["subtle", "surface", "raised", "overlay", "focus"])
def test_shadow_classes_set_box_shadow_alone(shadow: str, built_css: str) -> None:
    """The class reads only its token, so none is a valid value and removes just the shadow."""
    rule = re.search(rf"^\s*\.shadow-insight-{shadow} {{([^}}]*)}}", built_css, re.MULTILINE)

    assert rule is not None
    assert rule.group(1).split() == ["box-shadow:", f"var(--shadow-insight-{shadow});"]


@pytest.mark.parametrize("shadow", ["subtle", "surface", "raised", "overlay"])
def test_tailwind_shadow_form_combines_with_rings(shadow: str, built_css: str) -> None:
    """shadow-(--shadow-insight-*) is in the package stylesheet and shares the box-shadow list with ring-*."""
    selector = re.escape(rf".shadow-\(--shadow-insight-{shadow}\)")
    rule = re.search(rf"^\s*{selector} {{([^}}]*)}}", built_css, re.MULTILINE)

    assert rule is not None
    assert f"--tw-shadow: var(--shadow-insight-{shadow});" in rule.group(1)
    assert "var(--tw-ring-shadow)" in rule.group(1)
