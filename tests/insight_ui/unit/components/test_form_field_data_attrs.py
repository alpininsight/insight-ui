# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for custom data attributes on form field components."""

import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template
from insight_ui.configs import (
    CheckboxGroupConfig,
    CheckboxItemConfig,
    DataAttrConfig,
    InputFieldConfig,
    RadioBlockConfig,
    RadioGroupConfig,
    RadioItemConfig,
)


def render(template: str, context: dict | None = None) -> BeautifulSoup:
    """Render a template snippet with insight_tags loaded."""
    html = Template("{% load insight_tags %}" + template).render(Context(context or {}))
    return BeautifulSoup(html, "html.parser")


# Tag call and CSS selector of the element that must carry the data attributes.
FIELD_TAGS = [
    pytest.param('{% input_field tag_id="f" name="f" label="F" data_flow_hook="1" %}', "input#f", id="input_field"),
    pytest.param('{% textarea tag_id="f" name="f" label="F" data_flow_hook="1" %}', "textarea#f", id="textarea"),
    pytest.param('{% select tag_id="f" name="f" label="F" data_flow_hook="1" %}', "select#f", id="select"),
    pytest.param('{% checkbox tag_id="f" name="f" label="F" data_flow_hook="1" %}', "input#f", id="checkbox"),
    pytest.param('{% toggle tag_id="f" name="f" label="F" data_flow_hook="1" %}', "input#f", id="toggle"),
    pytest.param(
        '{% toggle tag_id="f" name="f" label="F" switch=True data_flow_hook="1" %}', "input#f", id="toggle-switch"
    ),
    pytest.param('{% slider tag_id="f" name="f" label="F" data_flow_hook="1" %}', "input#f", id="slider"),
    pytest.param(
        '{% slider tag_id="f" name="f" label="F" dual=True data_flow_hook="1" %}', "[role=group]", id="slider-dual"
    ),
    pytest.param(
        '{% multiselect name="f" label="F" data_flow_hook="1" %}', "[data-insight-multiselect]", id="multiselect"
    ),
    pytest.param('{% radio_group name="f" items=items data_flow_hook="1" %}', "fieldset", id="radio_group"),
    pytest.param('{% radio_block name="f" items=items data_flow_hook="1" %}', "fieldset", id="radio_block"),
]


@pytest.mark.parametrize(("template", "selector"), FIELD_TAGS)
def test_data_kwargs_render_on_the_field_element(template: str, selector: str) -> None:
    """data_* arguments land on the element JavaScript works with, not on a wrapper."""
    soup = render(template, {"items": [RadioItemConfig(value="a")]})

    assert soup.select_one(selector)["data-flow-hook"] == "1"
    assert len(soup.select("[data-flow-hook]")) == 1


def test_config_data_attrs_render() -> None:
    """data_attrs from a config are rendered, marker attributes included."""
    config = InputFieldConfig(
        name="title",
        tag_id="title",
        data_attrs=[DataAttrConfig(name="inspector-label"), DataAttrConfig(name="testid", value="title-input")],
    )

    field = render("{% input_field config %}", {"config": config}).select_one("input#title")

    assert field["data-inspector-label"] == ""
    assert field["data-testid"] == "title-input"


def test_data_kwargs_extend_config_data_attrs() -> None:
    """Tag arguments add to the config's data attributes instead of replacing them."""
    config = InputFieldConfig(name="title", tag_id="title", data_attrs=[DataAttrConfig(name="testid", value="t")])

    field = render('{% input_field config data_inspector_label="" %}', {"config": config}).select_one("input#title")

    assert field["data-testid"] == "t"
    assert field["data-inspector-label"] == ""


def test_data_attribute_values_are_escaped() -> None:
    """Attribute values cannot break out of the attribute."""
    html = Template('{% load insight_tags %}{% input_field name="f" data_hook=value %}').render(
        Context({"value": '"><script>alert(1)</script>'})
    )

    assert "<script>" not in html


def test_unknown_extra_argument_is_rejected() -> None:
    """Only data_* arguments are accepted beyond the declared parameters."""
    with pytest.raises(ValueError, match=r"Unknown parameter 'aria_label' in \{% input_field %\}"):
        render('{% input_field name="f" aria_label="x" %}')


@pytest.mark.parametrize(
    ("tag", "config"),
    [
        pytest.param(
            "radio_group",
            RadioGroupConfig(
                name="mode",
                data_attrs=[DataAttrConfig(name="group")],
                items=[RadioItemConfig(value="a", tag_id="a", data_attrs=[DataAttrConfig(name="option", value="a")])],
            ),
            id="radio_group",
        ),
        pytest.param(
            "radio_block",
            RadioBlockConfig(
                name="mode",
                data_attrs=[DataAttrConfig(name="group")],
                items=[RadioItemConfig(value="a", tag_id="a", data_attrs=[DataAttrConfig(name="option", value="a")])],
            ),
            id="radio_block",
        ),
        pytest.param(
            "checkbox_group",
            CheckboxGroupConfig(
                name="mode",
                data_attrs=[DataAttrConfig(name="group")],
                items=[
                    CheckboxItemConfig(
                        tag_id="a", label="A", value="a", data_attrs=[DataAttrConfig(name="option", value="a")]
                    )
                ],
            ),
            id="checkbox_group",
        ),
    ],
)
def test_groups_render_group_and_option_data_attrs(tag: str, config: object) -> None:
    """Group attributes sit on the fieldset, option attributes on each option's input."""
    soup = render(f"{{% {tag} config %}}", {"config": config})

    assert soup.select_one("fieldset").has_attr("data-group")
    option = soup.select_one("input[data-option]")
    assert option["data-option"] == "a"
    assert option["type"] in {"radio", "checkbox"}
