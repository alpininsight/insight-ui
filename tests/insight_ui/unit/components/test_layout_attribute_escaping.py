# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Regression tests for layout-tag attribute escaping and href schemes."""

import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template

HOST_VALUE = 'x" onmouseover="alert(1)'


def render(body: str, context: dict | None = None) -> str:
    """Render a layout-tag snippet and return the HTML string."""
    return Template("{% load layout_tags %}" + body).render(Context(context or {}))


def parse(body: str, context: dict | None = None) -> BeautifulSoup:
    """Render a layout-tag snippet and parse it."""
    return BeautifulSoup(render(body, context), "html.parser")


@pytest.mark.parametrize(
    "body",
    [
        pytest.param("{% section id=value aria_label=value class=value %}x{% endsection %}", id="section"),
        pytest.param("{% surface href=value id=value class=value %}x{% endsurface %}", id="surface-link"),
        pytest.param("{% surface id=value class=value %}x{% endsurface %}", id="surface"),
        pytest.param("{% grid id=value min=value class=value %}x{% endgrid %}", id="grid"),
        pytest.param(
            "{% list id=value aria_label=value class=value %}{% listitem %}a{% endlistitem %}{% endlist %}",
            id="list",
        ),
        pytest.param("{% list %}{% listitem id=value class=value %}a{% endlistitem %}{% endlist %}", id="listitem"),
        pytest.param("{% hbox id=value class=value %}x{% endhbox %}", id="hbox"),
        pytest.param("{% page id=value class=value %}x{% endpage %}", id="page"),
    ],
)
def test_attribute_values_from_variables_are_escaped(body: str) -> None:
    """Host-supplied layout-tag values stay inside their attributes."""
    html = render(body, {"value": HOST_VALUE})
    soup = BeautifulSoup(html, "html.parser")

    assert "&quot;" in html
    assert soup.find(attrs={"onmouseover": True}) is None


@pytest.mark.parametrize(
    "href",
    [
        "/docs/",
        "docs/",
        "#section",
        "?page=2",
        "//cdn.example.com/x",
        "https://example.com",
        "https://example.com/?a=1&b=2",
        "HTTP://example.com",
        "mailto:a@b.c",
    ],
)
def test_surface_accepts_relative_and_allowed_urls(href: str) -> None:
    """Relative URLs and http, https and mailto render unchanged after parsing."""
    link = parse("{% surface href=href %}x{% endsurface %}", {"href": href}).find("a")

    assert link is not None
    assert link["href"] == href


def test_surface_escapes_reserved_characters_in_an_allowed_href() -> None:
    """An allowed URL keeps its query string and does not break the attribute."""
    href = "https://example.com/?a=1&b=2"
    html = render("{% surface href=href %}x{% endsurface %}", {"href": href})

    assert "a=1&amp;b=2" in html
    assert parse("{% surface href=href %}x{% endsurface %}", {"href": href}).find("a")["href"] == href


@pytest.mark.parametrize(
    "href",
    [
        pytest.param("javascript:alert(1)", id="javascript"),
        pytest.param("JavaScript:alert(1)", id="mixed-case"),
        pytest.param("  javascript:alert(1)", id="leading-space"),
        pytest.param("\tjavascript:alert(1)", id="leading-tab"),
        pytest.param("java\tscript:alert(1)", id="tab-inside-scheme"),
        pytest.param("java\nscript:alert(1)", id="newline-inside-scheme"),
        pytest.param("data:text/html,example", id="data"),
        pytest.param("vbscript:msgbox(1)", id="vbscript"),
    ],
)
def test_surface_rejects_disallowed_href_schemes(href: str) -> None:
    """Disallowed schemes raise ValueError, the same way invalid layout config does."""
    with pytest.raises(ValueError, match="is not allowed"):
        render("{% surface href=href %}x{% endsurface %}", {"href": href})
