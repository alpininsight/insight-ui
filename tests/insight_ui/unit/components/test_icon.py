# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the icon component and its generated template."""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template
from insight_ui.management.commands.compile_icons import Command

import insight_ui

ICONS_TEMPLATE = Path(insight_ui.__file__).parent / "templates/insight_ui/components/icons.html"


def render(template: str) -> BeautifulSoup:
    """Render a template string that uses insight_tags and parse the result."""
    return BeautifulSoup(Template("{% load insight_tags %}" + template).render(Context()), "html.parser")


def test_icon_wrapper_is_phrasing_content() -> None:
    """The wrapper is a <span>, so icons are valid HTML inside buttons, labels and paragraphs."""
    wrapper = render("{% icon name='check' size='s' %}").find(["span", "div"])

    assert wrapper.name == "span"
    assert wrapper.find("svg") is not None


@pytest.mark.parametrize(
    "template",
    [
        pytest.param("{% button label='Save' icon_name='check' %}", id="button"),
        pytest.param("{% button label='Close' icon_name='x-mark' icon_only=True %}", id="icon-only-button"),
        pytest.param("<p>Done {% icon name='check' %} today</p>", id="paragraph"),
        pytest.param("{% input_field name='email' label='E-Mail' help_text='Info' %}", id="input-label"),
        pytest.param("{% textarea name='message' label='Message' help_text='Info' %}", id="textarea-label"),
        pytest.param("{% select name='topic' label='Topic' options='' help_text='Info' %}", id="select-label"),
        pytest.param("{% toggle name='news' label='News' switch=True %}", id="toggle-switch-label"),
    ],
)
def test_no_block_elements_inside_phrasing_containers(template: str) -> None:
    """Block elements inside <button>, <label> or <p> are invalid; in <p> the parser even splits the paragraph."""
    soup = render(template)
    container = soup.find(["button", "p", "label"])

    assert container.find(["div", "p", "ul"]) is None


def test_generated_wrapper_matches_icons_template() -> None:
    """compile_icons must produce the same wrapper as the checked-in icons.html, or a rerun reverts it."""
    generated = Command()._generate_template({}).splitlines()
    checked_in = ICONS_TEMPLATE.read_text(encoding="utf-8").splitlines()

    assert generated[0] == checked_in[0]
    assert generated[-1] == checked_in[-1]
