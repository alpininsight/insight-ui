# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for help and error texts linked to form fields."""

import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template
from insight_ui.configs import (
    CheckboxGroupConfig,
    CheckboxItemConfig,
    FormConfig,
    HtmxConfig,
    InputFieldConfig,
    RadioItemConfig,
)


def render(template: str, context: dict | None = None) -> BeautifulSoup:
    """Render a template snippet with insight_tags loaded."""
    html = Template("{% load insight_tags %}" + template).render(Context(context or {}))
    return BeautifulSoup(html, "html.parser")


ITEMS = {"items": [RadioItemConfig(value="a", label="A")], "options": ["a", "b"]}

# Tag call (without help_text/error_text) and the selector of the element that carries the state.
FIELDS = [
    pytest.param('{% input_field tag_id="f" name="f" label="F"', "input#f", id="input_field"),
    pytest.param('{% textarea tag_id="f" name="f" label="F"', "textarea#f", id="textarea"),
    pytest.param('{% select tag_id="f" name="f" label="F" options=options', "select#f", id="select"),
    pytest.param('{% checkbox tag_id="f" name="f" label="F"', "input#f", id="checkbox"),
    pytest.param('{% toggle tag_id="f" name="f" label="F"', "input#f", id="toggle"),
    pytest.param('{% toggle tag_id="f" name="f" label="F" switch=True', "input#f", id="toggle-switch"),
    pytest.param('{% slider tag_id="f" name="f" label="F"', "input#f", id="slider"),
    pytest.param('{% multiselect name="f" label="F" options=options', "input#f-search", id="multiselect"),
    pytest.param('{% radio_group name="f" label="F" items=items', "fieldset", id="radio_group"),
    pytest.param('{% radio_block name="f" label="F" items=items', "fieldset", id="radio_block"),
]


@pytest.mark.parametrize(("tag", "selector"), FIELDS)
def test_help_and_error_are_linked_to_the_control(tag: str, selector: str) -> None:
    """The control is described by help then error; the error also marks it as invalid."""
    soup = render(tag + ' help_text="Hint" error_text="Wrong" %}', ITEMS)
    control = soup.select_one(selector)

    assert control["aria-describedby"] == "f-help f-error"
    assert control["aria-invalid"] == "true"
    assert control["aria-errormessage"] == "f-error"
    assert soup.find(id="f-help").get_text(strip=True) == "Hint"
    assert soup.find(id="f-error").get_text(strip=True) == "Wrong"


@pytest.mark.parametrize(("tag", "selector"), FIELDS)
def test_help_text_alone_does_not_mark_the_field_invalid(tag: str, selector: str) -> None:
    """A hint is a description, not an error."""
    control = render(tag + ' help_text="Hint" %}', ITEMS).select_one(selector)

    assert control["aria-describedby"] == "f-help"
    assert not control.has_attr("aria-invalid")
    assert not control.has_attr("aria-errormessage")


@pytest.mark.parametrize(("tag", "selector"), FIELDS)
def test_fields_without_texts_stay_unchanged(tag: str, selector: str) -> None:
    """Without help or error no attribute points to a missing element."""
    soup = render(tag + " %}", ITEMS)
    control = soup.select_one(selector)

    for attribute in ("aria-describedby", "aria-invalid", "aria-errormessage"):
        assert not control.has_attr(attribute)
    assert soup.find(id="f-help") is None
    assert soup.find(id="f-error") is None


@pytest.mark.parametrize(("tag", "selector"), FIELDS)
def test_error_text_is_plain_text_not_a_live_region(tag: str, selector: str) -> None:
    """Field errors are read with the field; only the form-level container announces itself."""
    error = render(tag + ' error_text="Wrong" %}', ITEMS).find(id="f-error")

    assert not error.has_attr("role")
    assert not error.has_attr("aria-live")


def test_ids_fall_back_to_the_name_without_tag_id() -> None:
    """Fields without tag_id still get linked texts."""
    soup = render('{% input_field name="email" label="E-Mail" error_text="Wrong" %}')

    assert soup.find("input")["aria-describedby"] == "email-error"
    assert soup.find(id="email-error") is not None


def test_required_fields_rely_on_the_native_attribute() -> None:
    """Required already announces the state; no duplicate aria-required."""
    control = render('{% input_field tag_id="f" name="f" label="F" required=True error_text="Wrong" %}').find("input")

    assert control.has_attr("required")
    assert not control.has_attr("aria-required")


@pytest.mark.parametrize("tag", ["radio_group", "radio_block"])
def test_radio_groups_are_radiogroups_named_by_their_legend(tag: str) -> None:
    """Role radiogroup allows aria-invalid on the fieldset; the legend keeps naming it."""
    soup = render(f'{{% {tag} name="plan" label="Plan" items=items %}}', ITEMS)
    fieldset = soup.find("fieldset")

    assert fieldset["role"] == "radiogroup"
    assert soup.find(id=fieldset["aria-labelledby"]).get_text(strip=True) == "Plan"


def test_checkbox_group_links_texts_without_aria_invalid() -> None:
    """A plain fieldset does not support aria-invalid, so the linked error text carries the state."""
    config = CheckboxGroupConfig(
        name="langs", items=[CheckboxItemConfig(tag_id="en", label="English", value="en")], error_text="Pick one."
    )
    soup = render("{% checkbox_group config %}", {"config": config})
    fieldset = soup.find("fieldset")

    assert fieldset["aria-describedby"] == "langs-error"
    assert not fieldset.has_attr("aria-invalid")
    assert soup.find(id="langs-error").get_text(strip=True) == "Pick one."


def test_form_error_container_announces_itself() -> None:
    """Errors swapped into the form-level container of an HTMX form are read out immediately."""
    config = FormConfig(
        request_url="/save/",
        tag_id="signup",
        htmx=HtmxConfig(target="#signup"),
        fields=[InputFieldConfig(name="email")],
    )
    container = render("{% form config %}", {"config": config}).find(id="signup-error")

    assert container["role"] == "alert"


# Fields that can be disabled with a reason (the groups disable single options instead).
DISABLEABLE = [field for field in FIELDS if field.id not in {"radio_group", "radio_block"}]


@pytest.mark.parametrize(("tag", "selector"), DISABLEABLE)
def test_disabled_reason_is_visible_and_linked(tag: str, selector: str) -> None:
    """A disabled control cannot be focused, so its reason is visible text instead of a tooltip."""
    soup = render(tag + ' disabled=True disabled_reason="Locked by an admin" help_text="Hint" %}', ITEMS)
    control = soup.select_one(selector)

    assert control["aria-describedby"] == "f-help f-disabled"
    assert soup.find(id="f-disabled").get_text(strip=True) == "Locked by an admin"
    assert soup.find(attrs={"data-insight-tooltip": "Locked by an admin"}) is None


@pytest.mark.parametrize(("tag", "selector"), DISABLEABLE)
def test_disabled_reason_is_hidden_while_enabled(tag: str, selector: str) -> None:
    """The reason only matters while the field is disabled."""
    soup = render(tag + ' disabled_reason="Locked" %}', ITEMS)

    assert soup.find(id="f-disabled") is None
    assert not soup.select_one(selector).has_attr("aria-describedby")


def test_reason_does_not_become_part_of_the_label() -> None:
    """The label names the field; the reason describes it."""
    soup = render('{% checkbox tag_id="f" name="f" label="Newsletter" disabled=True disabled_reason="Not available" %}')

    assert soup.find("label").get_text(strip=True) == "Newsletter"


@pytest.mark.parametrize("tag", ["radio_group", "radio_block"])
def test_disabled_option_reason_is_linked_to_the_option(tag: str) -> None:
    """Each disabled option points to its own reason; enabled options stay undescribed."""
    items = [
        RadioItemConfig(value="a", label="A"),
        RadioItemConfig(value="b", label="B", disabled=True, disabled_reason="Sold out"),
    ]
    soup = render(f'{{% {tag} name="plan" label="Plan" items=items %}}', {"items": items})
    enabled, disabled = soup.find_all("input", type="radio")

    assert not enabled.has_attr("aria-describedby")
    assert "Sold out" in soup.find(id=disabled["aria-describedby"]).get_text()
    assert "Sold out" not in " ".join(label.get_text() for label in soup.find_all("label"))


def test_explanation_tooltip_is_gone() -> None:
    """help_text replaces the former explanation tooltip."""
    with pytest.raises(ValueError, match="Unknown parameter 'explanation'"):
        render('{% input_field name="f" explanation="Info" %}')
