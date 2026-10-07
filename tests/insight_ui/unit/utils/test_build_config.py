# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the shared config contract of all component template tags."""

import inspect
from dataclasses import dataclass, field

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


def _tags_accepting_config() -> list[str]:
    """Return the names of all insight_tags template tags with a config parameter."""
    return sorted(
        name
        for name, compile_func in insight_tags.register.tags.items()
        if "config" in inspect.signature(inspect.unwrap(compile_func)).parameters
    )


@pytest.mark.parametrize("tag_name", _tags_accepting_config())
def test_template_tag_rejects_dict_config(tag_name: str) -> None:
    """Every component tag rejects dicts as config instead of rendering them silently."""
    template = Template(f"{{% load insight_tags %}}{{% {tag_name} config=cfg %}}")

    with pytest.raises(TypeError, match="must be a dataclass instance"):
        template.render(Context({"cfg": {"name": "field", "label": "Label"}}))
