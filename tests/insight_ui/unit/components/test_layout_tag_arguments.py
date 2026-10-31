# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for how layout block tags resolve and render their arguments."""

from unittest import mock

import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template
from django.utils.functional import lazy


def render(body: str, context: dict | None = None) -> BeautifulSoup:
    """Render a template snippet with layout_tags loaded."""
    html = Template("{% load layout_tags %}" + body).render(Context(context or {}))
    return BeautifulSoup(html, "html.parser")


def test_filters_on_literals_are_applied() -> None:
    """A filter on a quoted value is applied instead of being dropped."""
    section = render('{% section id="tab-"|add:name %}x{% endsection %}', {"name": "intro"}).find("section")

    assert section["id"] == "tab-intro"


def test_translated_arguments_follow_the_language_of_each_render() -> None:
    """_("…") stays lazy: a cached template renders every request in that request's language."""
    language = {"code": "en"}
    fake_gettext_lazy = lazy(lambda message: f"{language['code']}:{message}", str)

    with mock.patch("django.template.base.gettext_lazy", fake_gettext_lazy):
        template = Template('{% load layout_tags %}{% section id="s" aria_label=_("Close") %}x{% endsection %}')

    labels = []
    for code in ("de", "fr"):
        language["code"] = code
        labels.append(BeautifulSoup(template.render(Context()), "html.parser").find("section")["aria-label"])

    assert labels == ["de:Close", "fr:Close"]


EVIL = 'x" onmouseover="alert(1)'


@pytest.mark.parametrize(
    "body",
    [
        pytest.param("{% section id=value aria_label=value class=value %}x{% endsection %}", id="section"),
        pytest.param("{% surface href=value id=value class=value %}x{% endsurface %}", id="surface-link"),
        pytest.param("{% surface id=value class=value %}x{% endsurface %}", id="surface"),
        pytest.param("{% grid id=value min=value class=value %}x{% endgrid %}", id="grid"),
        pytest.param(
            "{% list id=value aria_label=value class=value %}{% listitem %}a{% endlistitem %}{% endlist %}", id="list"
        ),
        pytest.param("{% list %}{% listitem id=value class=value %}a{% endlistitem %}{% endlist %}", id="listitem"),
        pytest.param("{% hbox id=value class=value %}x{% endhbox %}", id="hbox"),
    ],
)
def test_attribute_values_from_variables_are_escaped(body: str) -> None:
    """A value from user data cannot break out of its attribute and add an event handler."""
    soup = render(body, {"value": EVIL})

    assert not soup.find(attrs={"onmouseover": True})


@pytest.mark.parametrize(
    "href",
    [
        "/docs/",
        "docs/",
        "#section",
        "?page=2",
        "//cdn.example.com/x",
        "https://example.com",
        "HTTP://example.com",
        "mailto:a@b.c",
    ],
)
def test_surface_accepts_relative_and_allowed_urls(href: str) -> None:
    """Relative URLs and http, https and mailto render as links."""
    link = render("{% surface href=href %}x{% endsurface %}", {"href": href}).find("a")

    assert link["href"] == href


@pytest.mark.parametrize(
    "href",
    [
        pytest.param("javascript:alert(1)", id="javascript"),
        pytest.param("JavaScript:alert(1)", id="uppercase"),
        pytest.param("  javascript:alert(1)", id="leading-space"),
        pytest.param("java\tscript:alert(1)", id="tab-inside-scheme"),
        pytest.param("java\nscript:alert(1)", id="newline-inside-scheme"),
        pytest.param("data:text/html,<script>alert(1)</script>", id="data"),
        pytest.param("vbscript:msgbox(1)", id="vbscript"),
    ],
)
def test_surface_rejects_schemes_that_can_run_code(href: str) -> None:
    """Escaping does not neutralise javascript: and friends, so the scheme is checked against an allowlist."""
    with pytest.raises(ValueError, match="is not allowed"):
        render("{% surface href=href %}x{% endsurface %}", {"href": href})


def test_filtered_surface_href_is_resolved_before_the_scheme_check() -> None:
    """Filters on href run at render time, then the resolved URL must use an allowed scheme."""
    link = render('{% surface href="https://example.com"|add:path %}x{% endsurface %}', {"path": "/docs"}).find("a")

    assert link is not None
    assert link["href"] == "https://example.com/docs"

    with pytest.raises(ValueError, match="is not allowed"):
        render('{% surface href="java"|add:rest %}x{% endsurface %}', {"rest": "script:alert(1)"})


@pytest.mark.parametrize("radius", ["xs", "s", "m", "l", "xl"])
def test_surface_radius_uses_the_radius_token(radius: str) -> None:
    """Radius picks the theme's radius token of the same name, so a theme stylesheet can change it."""
    surface = render(f'{{% surface radius="{radius}" %}}x{{% endsurface %}}').find("div")

    assert f"rounded-insight-{radius}" in surface["class"]


def test_surface_radius_none_removes_the_rounding() -> None:
    """radius="none" squares the corners instead of keeping the variant's rounding."""
    surface = render('{% surface radius="none" %}x{% endsurface %}').find("div")

    assert "rounded-none" in surface["class"]


def test_external_surface_link_tells_screen_readers_about_the_new_tab() -> None:
    """A linked surface that opens a new tab says so after its content; an internal one does not."""
    external = render('{% surface href="https://example.com/" external=True %}Report{% endsurface %}').find("a")
    internal = render('{% surface href="/report/" %}Report{% endsurface %}').find("a")

    assert external.get_text(" ", strip=True) == "Report (opens in a new tab)"
    assert internal.get_text(" ", strip=True) == "Report"
