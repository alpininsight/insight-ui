# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests that every form field config requires a name, however the field is built."""

from collections.abc import Callable
from dataclasses import replace

import pytest
from django.template import Context, Template
from insight_ui.configs import (
    CheckboxConfig,
    CheckboxGroupConfig,
    CheckboxItemConfig,
    InputFieldConfig,
    MultiselectConfig,
    RadioBlockConfig,
    RadioGroupConfig,
    RadioItemConfig,
    SelectConfig,
    SliderConfig,
    TextareaConfig,
    ToggleConfig,
)
from insight_ui.configs.base import BaseFormFieldConfig

FIELD_CONFIGS = [
    pytest.param(InputFieldConfig, "input_field", id="input_field"),
    pytest.param(TextareaConfig, "textarea", id="textarea"),
    pytest.param(CheckboxConfig, "checkbox", id="checkbox"),
    pytest.param(SliderConfig, "slider", id="slider"),
    pytest.param(ToggleConfig, "toggle", id="toggle"),
    pytest.param(SelectConfig, "select", id="select"),
    pytest.param(MultiselectConfig, "multiselect", id="multiselect"),
]

# Group fields do not inherit BaseFormFieldConfig and need items to render their inputs.
GROUP_CONFIGS = [
    pytest.param(
        lambda name: CheckboxGroupConfig(name=name, items=[CheckboxItemConfig(tag_id="a", value="a", label="A")]),
        id="checkbox_group",
    ),
    pytest.param(
        lambda name: RadioGroupConfig(name=name, items=[RadioItemConfig(tag_id="a", value="a", label="A")]),
        id="radio_group",
    ),
    pytest.param(
        lambda name: RadioBlockConfig(name=name, items=[RadioItemConfig(tag_id="a", value="a", label="A")]),
        id="radio_block",
    ),
]


def render(template: str, context: dict | None = None) -> str:
    """Render a template string that uses insight_tags."""
    return Template("{% load insight_tags %}" + template).render(Context(context or {}))


@pytest.mark.parametrize(("config_class", "tag"), FIELD_CONFIGS)
def test_field_renders_with_name_from_config_or_keyword(config_class: type[BaseFormFieldConfig], tag: str) -> None:
    """The name can come from a config or from the name keyword."""
    from_config = render(f"{{% {tag} config=config %}}", {"config": config_class(name="field")})
    from_keyword = render(f"{{% {tag} name='field' %}}")

    assert "field" in from_config
    assert "field" in from_keyword


@pytest.mark.parametrize(("config_class", "tag"), FIELD_CONFIGS)
def test_field_without_name_is_rejected(config_class: type[BaseFormFieldConfig], tag: str) -> None:
    """Omitting the name entirely fails before anything is rendered."""
    with pytest.raises(ValueError, match="Missing required fields"):
        render(f"{{% {tag} label='Label' %}}")


@pytest.mark.parametrize(("config_class", "tag"), FIELD_CONFIGS)
@pytest.mark.parametrize(
    "template",
    [
        pytest.param("{{% {tag} name='' %}}", id="empty-string"),
        pytest.param("{{% {tag} name=undefined_variable %}}", id="undefined-template-variable"),
        pytest.param("{{% {tag} config=config name=None %}}", id="config-overridden-with-none"),
    ],
)
def test_field_with_empty_name_is_rejected(config_class: type[BaseFormFieldConfig], tag: str, template: str) -> None:
    """An empty name would render a field that is never submitted, so it is rejected."""
    context = {"config": config_class(name="field")}

    with pytest.raises(ValueError, match="requires a non-empty name"):
        render(template.format(tag=tag), context)


@pytest.mark.parametrize(("config_class", "tag"), FIELD_CONFIGS)
def test_config_with_empty_name_is_rejected(config_class: type[BaseFormFieldConfig], tag: str) -> None:
    """The check also applies to configs built or copied in Python."""
    with pytest.raises(ValueError, match="requires a non-empty name"):
        config_class(name="")
    with pytest.raises(ValueError, match="requires a non-empty name"):
        replace(config_class(name="field"), name="")


@pytest.mark.parametrize("build", GROUP_CONFIGS)
def test_group_config_with_empty_name_is_rejected(build: Callable[[str | None], object]) -> None:
    """Checkbox and radio groups are form fields too and need a name to be submitted."""
    assert build("field") is not None
    for empty_name in ("", None):
        with pytest.raises(ValueError, match="requires a non-empty name"):
            build(empty_name)
    with pytest.raises(ValueError, match="requires a non-empty name"):
        replace(build("field"), name="")


@pytest.mark.parametrize("tag", ["radio_group", "radio_block"])
@pytest.mark.parametrize("name", ["''", "undefined_variable"], ids=["empty-string", "undefined-template-variable"])
def test_group_tag_with_empty_name_is_rejected(tag: str, name: str) -> None:
    """Radio tags that take the name as a keyword reject an empty one."""
    with pytest.raises(ValueError, match="requires a non-empty name"):
        render(f"{{% {tag} name={name} %}}")
