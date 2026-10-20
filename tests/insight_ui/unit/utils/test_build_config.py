# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the shared config contract of all component template tags."""

import inspect
import re
from dataclasses import dataclass, field, fields

import pytest
from django.template import Context, Template
from insight_ui.templatetags import insight_tags
from insight_ui.templatetags.insight_tags import UNSET, build_config


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
    "badge": {"icon_name", "icon_size"},
    "button": {"icon_name", "icon_size"},
}

# Tags that only accept a complete config and offer no field arguments.
CONFIG_ONLY_TAGS = {"accordion", "checkbox_group", "dropdown", "footer", "navbar", "table"}

# Known config fields without a matching tag argument. Settable only via config.
FIELDS_WITHOUT_TAG_ARGUMENT: dict[str, set[str]] = {
    "badge": {"icon"},
    "brand_mark": {"primary_text_color", "secondary_text_color"},
    "button": {"icon", "aria_attrs", "data_attrs", "hx_attrs"},
    "logo": {"icon"},
    "multiselect": {"required", "tag_id"},
    "search_bar": {"button_label", "placeholder"},
    "slider": {"required"},
    "toggle_view": {"current_view"},
}


def _tags_accepting_config() -> list[str]:
    """Return the names of all insight_tags template tags with a config parameter."""
    return sorted(
        name
        for name, compile_func in insight_tags.register.tags.items()
        if "config" in inspect.signature(inspect.unwrap(compile_func)).parameters
    )


def _config_class(tag_name: str) -> type:
    """Return the config dataclass named in the tag's ``config`` annotation."""
    func = inspect.unwrap(insight_tags.register.tags[tag_name])
    annotation = str(inspect.signature(func).parameters["config"].annotation)
    class_names = re.findall(r"\b\w+Config\b", annotation)
    assert len(class_names) == 1, f"{tag_name}: cannot derive config class from {annotation!r}"
    return getattr(insight_tags, class_names[0])


def _tag_arguments(tag_name: str) -> set[str]:
    """Return the keyword-only arguments of a tag."""
    func = inspect.unwrap(insight_tags.register.tags[tag_name])
    return {name for name, param in inspect.signature(func).parameters.items() if param.kind is param.KEYWORD_ONLY}


@pytest.mark.parametrize("tag_name", _tags_accepting_config())
def test_tag_arguments_are_config_fields(tag_name: str) -> None:
    """Every tag argument maps to a field of the tag's config, so build_config can apply it."""
    config_fields = {f.name for f in fields(_config_class(tag_name))}
    unknown = _tag_arguments(tag_name) - config_fields - CONVENIENCE_ARGUMENTS.get(tag_name, set())

    assert not unknown, f"{tag_name}: arguments without a config field: {sorted(unknown)}"


@pytest.mark.parametrize("tag_name", sorted(set(_tags_accepting_config()) - CONFIG_ONLY_TAGS))
def test_config_fields_are_tag_arguments(tag_name: str) -> None:
    """Every config field is a tag argument, apart from the documented exceptions."""
    config_fields = {f.name for f in fields(_config_class(tag_name))}
    missing = config_fields - _tag_arguments(tag_name)

    assert missing == FIELDS_WITHOUT_TAG_ARGUMENT.get(tag_name, set()), (
        f"{tag_name}: config fields without a tag argument: {sorted(missing)}. "
        "Add the argument or update FIELDS_WITHOUT_TAG_ARGUMENT."
    )


def test_exception_lists_name_existing_tags() -> None:
    """The exception lists do not refer to removed or renamed tags."""
    tags = set(_tags_accepting_config())
    listed = set(CONVENIENCE_ARGUMENTS) | CONFIG_ONLY_TAGS | set(FIELDS_WITHOUT_TAG_ARGUMENT)

    assert listed <= tags, f"Unknown tags: {sorted(listed - tags)}"


@pytest.mark.parametrize("tag_name", _tags_accepting_config())
def test_template_tag_rejects_dict_config(tag_name: str) -> None:
    """Every component tag rejects dicts as config instead of rendering them silently."""
    template = Template(f"{{% load insight_tags %}}{{% {tag_name} config=cfg %}}")

    with pytest.raises(TypeError, match="must be a dataclass instance"):
        template.render(Context({"cfg": {"name": "field", "label": "Label"}}))
