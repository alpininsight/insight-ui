# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the shared config contract of all component template tags."""

from dataclasses import dataclass, field

import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template
from django.template.backends.django import DjangoTemplates
from insight_ui.configs import UNSET, ButtonConfig, build_config
from insight_ui.templatetags import insight_tags
from insight_ui.testing import tag_problems


@dataclass
class SampleConfig:
    """Minimal config used to exercise build_config."""

    name: str
    label: str = ""
    items: list[str] = field(default_factory=list)


# --- build_config ------------------------------------------------------


def test_build_config_creates_instance_from_kwargs() -> None:
    """Without a config, a new instance is built from the keyword arguments."""
    config = build_config(SampleConfig, name="email", label="E-Mail")

    assert config == SampleConfig(name="email", label="E-Mail")


def test_build_config_ignores_unset_kwargs() -> None:
    """UNSET keyword arguments fall back to the dataclass defaults."""
    config = build_config(SampleConfig, name="email", label=UNSET)

    assert config.label == ""


def test_build_config_applies_overrides_to_copy() -> None:
    """Keyword arguments override fields of a given config without mutating it."""
    original = SampleConfig(name="email", label="E-Mail")

    config = build_config(SampleConfig, original, label="Override")

    assert config.label == "Override"
    assert config.name == "email"
    assert original.label == "E-Mail"


def test_build_config_rejects_missing_required_fields() -> None:
    """Required fields must be provided when no config is given."""
    with pytest.raises(ValueError, match="Missing required fields for SampleConfig: name"):
        build_config(SampleConfig, label="E-Mail")


@pytest.mark.parametrize(
    "config",
    [
        pytest.param({"name": "email"}, id="dict"),
        pytest.param("email", id="str"),
        pytest.param(SampleConfig, id="dataclass-type"),
    ],
)
def test_build_config_rejects_non_dataclass_config(config: object) -> None:
    """Only dataclass instances are accepted as config."""
    with pytest.raises(TypeError, match="config for SampleConfig must be a dataclass instance"):
        build_config(SampleConfig, config)


# --- Template tags -----------------------------------------------------


# Tag arguments that are not config fields but are converted into one (icon_name/icon_size -> icon).
CONVENIENCE_ARGUMENTS: dict[str, set[str]] = {
    "badge": {"icon_name", "icon_size", "icon_mirror_rtl"},
    "button": {"icon_name", "icon_size", "icon_mirror_rtl"},
}

# Tags that only accept a complete config and offer no field arguments.
CONFIG_ONLY_TAGS = {"accordion", "checkbox_group", "dropdown", "footer", "infinite_scroll_items", "navbar", "table"}

# Known config fields without a matching tag argument. Settable only via config.
FIELDS_WITHOUT_TAG_ARGUMENT: dict[str, set[str]] = {
    "badge": {"icon"},
    "button": {"icon", "aria_attrs", "data_attrs", "hx_attrs"},
    "logo": {"icon"},
    # required has no effect yet: the hidden inputs cannot carry it, it would need JS validation.
    "multiselect": {"required"},
    # required has no effect: a range always has a value.
    "slider": {"required"},
}


def test_core_tags_follow_the_tag_contract() -> None:
    """Tag arguments and Config fields match, apart from the listed exceptions, and a dict config is rejected."""
    problems = tag_problems(
        insight_tags.register,
        convenience_arguments=CONVENIENCE_ARGUMENTS,
        config_only_tags=CONFIG_ONLY_TAGS,
        fields_without_tag_argument=FIELDS_WITHOUT_TAG_ARGUMENT,
    )

    assert problems == []


def test_template_tag_rejects_dict_config() -> None:
    """A dict passed as config in a template fails instead of rendering silently."""
    template = Template("{% load insight_tags %}{% button config=cfg %}")

    with pytest.raises(TypeError, match="must be a dataclass instance"):
        template.render(Context({"cfg": {"label": "Label"}}))


# --- Extension packages ------------------------------------------------


@pytest.mark.parametrize(
    ("arguments", "label", "tooltip"),
    [
        pytest.param("", "Save", "Saves the draft", id="omitted"),
        pytest.param('label="Save now"', "Save now", "Saves the draft", id="override"),
        pytest.param('tooltip=""', "Save", None, id="empty-override"),
    ],
)
def test_extension_tag_forwards_omitted_arguments_to_core_tag(arguments: str, label: str, tooltip: str | None) -> None:
    """An extension tag passes its UNSET defaults on to a Core tag, which keeps the Config values for them."""
    engine = DjangoTemplates(
        {
            "NAME": "extension",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {"libraries": {"extension_tags": "tests.insight_ui.unit.utils.extension_tags"}},
        }
    )
    template = engine.from_string(f"{{% load extension_tags %}}{{% extension_button config=save {arguments} %}}")

    html = template.render({"save": ButtonConfig(label="Save", tooltip="Saves the draft")})

    button = BeautifulSoup(html, "html.parser").button
    assert button is not None
    assert button.get_text(strip=True) == label
    assert button.get("data-insight-tooltip") == tooltip
