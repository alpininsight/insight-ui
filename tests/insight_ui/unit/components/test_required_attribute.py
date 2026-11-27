# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the native required attribute on form field components."""

import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template


def render(template: str, context: dict | None = None) -> BeautifulSoup:
    """Render a template snippet with insight_tags loaded."""
    html = Template("{% load insight_tags %}" + template).render(Context(context or {}))
    return BeautifulSoup(html, "html.parser")


# Tag call without the required argument and the selector of the form control.
FIELDS = [
    pytest.param('{% input_field tag_id="f" name="f" label="F"', "input#f", id="input_field"),
    pytest.param('{% textarea tag_id="f" name="f" label="F"', "textarea#f", id="textarea"),
    pytest.param('{% select tag_id="f" name="f" label="F" options=options', "select#f", id="select"),
    pytest.param('{% checkbox tag_id="f" name="f" label="F"', "input#f", id="checkbox"),
    pytest.param('{% toggle tag_id="f" name="f" label="F"', "input#f", id="toggle"),
    pytest.param('{% toggle tag_id="f" name="f" label="F" switch=True', "input#f", id="toggle-switch"),
]


@pytest.mark.parametrize(("tag", "selector"), FIELDS)
def test_required_renders_the_native_attribute(tag: str, selector: str) -> None:
    """Browsers only validate required fields when the attribute is on the control."""
    soup = render(tag + " required=True %}", {"options": ["a", "b"]})

    assert soup.select_one(selector).has_attr("required")


@pytest.mark.parametrize(("tag", "selector"), FIELDS)
def test_optional_fields_omit_the_attribute(tag: str, selector: str) -> None:
    """Without required=True the control stays optional."""
    soup = render(tag + " %}", {"options": ["a", "b"]})

    assert not soup.select_one(selector).has_attr("required")


def test_required_select_keeps_disabled_handling() -> None:
    """Required and disabled are independent attributes."""
    soup = render(
        '{% select tag_id="f" name="f" options=options required=True disabled=True disabled_reason="Locked" %}',
        {"options": ["a"]},
    )

    control = soup.select_one("select#f")
    assert control.has_attr("required")
    assert control.has_attr("disabled")


def test_select_placeholder_submits_an_empty_value() -> None:
    """A required select only fails validation while an option with an empty value is chosen."""
    soup = render(
        '{% select tag_id="f" name="f" options=options required=True %}',
        {"options": {"placeholder": "-- Choose --", "a": "A"}},
    )

    options = soup.select("select#f option")
    assert options[0]["value"] == ""
    assert options[0].get_text(strip=True) == "-- Choose --"
    assert options[1]["value"] == "a"


# Fields that show a required marker next to their label.
LABELLED_FIELDS = [field for field in FIELDS if field.id != "toggle"]


@pytest.mark.parametrize(("tag", "selector"), LABELLED_FIELDS)
def test_required_label_marker_is_hidden_from_screen_readers(tag: str, selector: str) -> None:
    """The asterisk is visual only; screen readers announce the native required attribute instead."""
    soup = render(tag + " required=True %}", {"options": ["a"]})

    markers = [span for span in soup.find_all("span") if span.get_text(strip=True) == "*"]
    assert len(markers) == 1
    assert markers[0]["aria-hidden"] == "true"
    assert not markers[0].has_attr("aria-label")


@pytest.mark.parametrize(("tag", "selector"), FIELDS)
def test_optional_fields_show_no_marker(tag: str, selector: str) -> None:
    """Optional fields carry no asterisk."""
    soup = render(tag + " %}", {"options": ["a"]})

    assert not [span for span in soup.find_all("span") if span.get_text(strip=True) == "*"]


def test_toggle_button_shows_no_marker_inside_the_button() -> None:
    """An asterisk inside a button-styled toggle would read as part of its label."""
    soup = render('{% toggle tag_id="f" name="f" label="Bold" required=True %}')

    assert soup.select_one("input#f").has_attr("required")
    assert "*" not in soup.select_one("label").get_text()
