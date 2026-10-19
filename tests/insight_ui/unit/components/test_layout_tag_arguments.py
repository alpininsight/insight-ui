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
