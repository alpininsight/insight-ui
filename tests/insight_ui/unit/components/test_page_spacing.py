# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the shared page spacing: gutter, content box, content grid and page bands."""

import pytest
from bs4 import BeautifulSoup, Tag
from django.conf import settings
from django.template import Context, Template
from django.template.loader import render_to_string
from django.test import override_settings
from insight_ui.config import get_config
from insight_ui.configs import FooterConfig, LegalNoticeConfig

STATIC_STORAGE = {"staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}}


def render(body: str, context: dict | None = None) -> BeautifulSoup:
    """Render a template snippet with insight_tags and layout_tags loaded."""
    html = Template("{% load insight_tags layout_tags %}" + body).render(Context(context or {}))
    return BeautifulSoup(html, "html.parser")


def render_base(**context: object) -> BeautifulSoup:
    """Render the base template with the merged INSIGHT_UI config and extra context."""
    with override_settings(STORAGES=STATIC_STORAGE):
        html = render_to_string("insight_ui/base.html", {**get_config(), **context})
    return BeautifulSoup(html, "html.parser")


def classes(element: Tag) -> set[str]:
    """Return the class names of an element."""
    return set(element.get("class", []))


# --- {% page %} ---------------------------------------------------------------


def test_page_is_a_full_bleed_band_with_its_content_in_the_box() -> None:
    """The band spans the content area; its children sit in the shared content box."""
    band = render('{% page id="intro" %}<p>Text</p>{% endpage %}').find(id="intro")
    inner = band.find("div")

    assert "insight-full-bleed" in classes(band)
    assert "insight-content-box" in classes(inner)
    assert inner.p.get_text() == "Text"


@pytest.mark.parametrize(
    ("padding", "expected"),
    [
        ("none", {"py-0"}),
        ("s", {"py-insight-s"}),
        ("m", {"py-insight-m"}),
        ("xl", {"py-insight-l", "md:py-insight-xl"}),
    ],
)
def test_page_padding_is_vertical_only(padding: str, expected: set[str]) -> None:
    """The content box provides the horizontal gutter, so padding only sets the band's height."""
    band = render(f'{{% page id="p" padding="{padding}" %}}x{{% endpage %}}').find(id="p")

    assert expected <= classes(band)
    assert not any(name.startswith(("p-", "px-")) for name in classes(band))


def test_page_with_height_lets_its_content_grow() -> None:
    """A page with a height keeps the flex column through the inner box, so children can fill it."""
    inner = render('{% page id="p" height="full" %}x{% endpage %}').find(id="p").find("div")

    assert {"flex", "flex-col", "grow"} <= classes(inner)


# --- base.html ----------------------------------------------------------------


def test_content_is_a_content_grid_by_default() -> None:
    """Direct children of #content sit in the content column; bands break out of it."""
    content = render_base().find(id="content")

    assert "insight-content-grid" in classes(content)


def test_content_full_width_removes_the_grid() -> None:
    """A page can opt out of the content box entirely."""
    content = render_base(content_full_width=True).find(id="content")

    assert not {"insight-content-grid", "insight-content-box"} & classes(content)


def test_content_fill_keeps_the_flex_column_in_the_box() -> None:
    """Filling pages such as a login stay a flex column, boxed but without the grid."""
    content = render_base(content_fill=True).find(id="content")

    assert {"flex", "flex-col", "grow", "insight-content-box"} <= classes(content)
    assert "insight-content-grid" not in classes(content)


def test_content_max_width_from_settings_and_template() -> None:
    """The content width comes from INSIGHT_UI and can be overridden per page."""
    assert not render_base().body.has_attr("style")

    with override_settings(INSIGHT_UI={**settings.INSIGHT_UI, "content_max_width": "64rem"}):
        assert render_base().body["style"] == "--insight-content-max-width: 64rem"
        assert render_base(content_max_width="48rem").body["style"] == "--insight-content-max-width: 48rem"


def test_content_max_width_is_escaped() -> None:
    """A template value cannot break out of the style attribute."""
    body = render_base(content_max_width='1rem" onload="alert(1)').body

    assert not body.has_attr("onload")


# --- Navbar and footer ------------------------------------------------------------


FOOTER = FooterConfig(legal=LegalNoticeConfig(year="2026", holder="Example"))


def test_navbar_and_footer_use_the_window_gutter_by_default() -> None:
    """By default the bars span the window with the shared gutter."""
    soup = render("{% navbar %}{% footer config=footer %}", {"footer": FOOTER})

    assert "insight-gutter" in classes(soup.nav)
    assert "insight-gutter" in classes(soup.footer)
    assert not soup.select(".insight-content-box")


def test_navbar_and_footer_can_align_with_the_content() -> None:
    """With the setting, the bars put their content into the content box instead."""
    with override_settings(INSIGHT_UI={**settings.INSIGHT_UI, "align_navbar_footer_to_content": True}):
        soup = render("{% navbar %}{% footer config=footer %}", {"footer": FOOTER})

    assert "insight-gutter" not in classes(soup.nav)
    assert "insight-gutter" not in classes(soup.footer)
    assert soup.nav.select_one(".insight-content-box") is not None
    assert soup.footer.select_one(".insight-content-box") is not None


def test_page_header_content_sits_in_the_content_box() -> None:
    """The page header lines up with the content."""
    soup = render('{% page_header title="Title" %}')

    assert soup.select_one(".insight-content-box h1") is not None


# --- Sticky navbar -------------------------------------------------------------------


def test_fixed_navbar_is_a_sticky_header_in_the_flow() -> None:
    """navbar_fixed makes the header sticky; the main area no longer reserves the navbar's height."""
    with override_settings(INSIGHT_UI={**settings.INSIGHT_UI, "navbar_fixed": True}):
        soup = render_base()

    assert {"sticky", "top-0"} <= classes(soup.find(id="header"))
    assert "pt-16" not in classes(soup.find(id="main"))


def test_header_is_not_sticky_by_default() -> None:
    """Without navbar_fixed the header scrolls away with the page."""
    assert "sticky" not in classes(render_base().find(id="header"))


@pytest.mark.parametrize("navbar_fixed", [True, False])
def test_header_stacks_above_the_page(navbar_fixed: bool) -> None:
    """The open mobile menu reaches below the navbar; it must cover the page header, sticky or not."""
    with override_settings(INSIGHT_UI={**settings.INSIGHT_UI, "navbar_fixed": navbar_fixed}):
        header = render_base().find(id="header")

    assert "z-50" in classes(header)
    assert {"relative", "sticky"} & classes(header)


def test_static_sidebar_sticks_below_a_fixed_navbar() -> None:
    """The sidebar starts below the navbar and is exactly as tall as the rest of the window."""
    with override_settings(INSIGHT_UI={**settings.INSIGHT_UI, "navbar_fixed": True}):
        aside = render('{% sidebar side="left" %}x{% endsidebar %}', {"INSIGHT_UI": get_config()["INSIGHT_UI"]}).aside

    assert {"top-(--insight-navbar-height)", "h-[calc(100dvh-var(--insight-navbar-height))]"} <= classes(aside)
