# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Markdown fields render formatting but no raw HTML or unsafe URLs from plain strings."""

import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template
from django.utils.safestring import mark_safe
from insight_ui.configs import InfoboxConfig, PageHeaderConfig

RAW_HTML = '<img src="x" onerror="alert(1)"> **Ada**'
UNSAFE_LINKS = {
    "inline": "[Open](javascript:alert(1))",
    "reference": "[Open][ref]\n\n[ref]: JaVaScRiPt:alert(1)",
    "character reference": "[Open](&#106;avascript:alert(1))",
    "leading space": "[Open]( javascript:alert(1))",
}


def render(template: str, **context: object) -> BeautifulSoup:
    """Render a template with the insight tags loaded."""
    html = Template("{% load insight_tags %}" + template).render(Context(context))
    return BeautifulSoup(html, "html.parser")


def render_infobox(message: str) -> BeautifulSoup:
    """Render an infobox whose message is the given Markdown."""
    return render("{% infobox config=config %}", config=InfoboxConfig(message=message))


def render_page_header(description: str) -> BeautifulSoup:
    """Render a page header whose description is the given Markdown."""
    return render("{% page_header config=config %}", config=PageHeaderConfig(title="Title", description=description))


RENDERERS = {"infobox.message": render_infobox, "page_header.description": render_page_header}


@pytest.mark.parametrize("render_markdown", RENDERERS.values(), ids=RENDERERS.keys())
def test_raw_html_in_plain_markdown_is_shown_as_text(render_markdown) -> None:  # noqa: ANN001
    """Markdown formatting works, HTML tags from the text never become elements."""
    soup = render_markdown(RAW_HTML)

    assert soup.select_one("img[onerror]") is None
    assert soup.find("strong", string="Ada") is not None
    assert '<img src="x" onerror="alert(1)">' in soup.get_text()


@pytest.mark.parametrize("render_markdown", RENDERERS.values(), ids=RENDERERS.keys())
@pytest.mark.parametrize("source", UNSAFE_LINKS.values(), ids=UNSAFE_LINKS.keys())
def test_links_with_disallowed_schemes_lose_their_url(render_markdown, source: str) -> None:  # noqa: ANN001
    """A link to javascript: keeps its text but cannot be followed."""
    link = render_markdown(source).find("a", string="Open")

    assert link is not None
    assert not link.has_attr("href")


@pytest.mark.parametrize(
    ("source", "href"),
    [
        ("[Docs](https://example.com/docs)", "https://example.com/docs"),
        ("[Page](/path/?a=1&b=2)", "/path/?a=1&b=2"),
        ("[Mail](mailto:team@example.com)", "mailto:team@example.com"),
        ("<https://example.com>", "https://example.com"),
    ],
)
def test_allowed_links_keep_their_url(source: str, href: str) -> None:
    """Relative URLs and the link schemes allowed in configs stay links."""
    link = render_infobox(source).find("a")

    assert link is not None
    assert link["href"] == href


def test_image_with_disallowed_scheme_loses_its_source() -> None:
    """Images follow the image URL schemes of the configs."""
    soup = render_infobox("![Logo](javascript:alert(1)) ![Chart](/static/chart.png)")

    assert not soup.find("img", alt="Logo").has_attr("src")
    assert soup.find("img", alt="Chart")["src"] == "/static/chart.png"


def test_safe_string_markdown_may_contain_html() -> None:
    """HTML the host marked as safe is trusted."""
    soup = render_infobox(mark_safe('<span class="note">Ada</span> **bold**'))

    assert soup.find("span", class_="note", string="Ada") is not None
    assert soup.find("strong", string="bold") is not None


def test_markdownify_filter_treats_template_variables_as_plain_text() -> None:
    """The public filter applies the same rules to host templates."""
    soup = render("{{ text|markdownify }}", text=RAW_HTML)

    assert soup.select_one("img[onerror]") is None
    assert soup.find("strong", string="Ada") is not None
