# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""The public contract checks report drift in Configs and tags of any package."""

from collections.abc import Callable
from dataclasses import dataclass, field, fields
from types import ModuleType
from typing import Any

import pytest
from django import template
from django.utils.translation import override
from insight_ui.configs import UNSET, Unset, build_config
from insight_ui.testing import config_problems, tag_problems

from insight_ui import configs


def _module(*members: object) -> ModuleType:
    """Return a Config module that exports the given members."""
    module = ModuleType("extension.configs")
    for member in members:
        setattr(module, member.__name__, member)  # type: ignore[attr-defined]
    module.__all__ = [member.__name__ for member in members]  # type: ignore[attr-defined]
    return module


def _library(*funcs: Callable[..., Any], takes_context: bool = False) -> template.Library:
    """Return a template library with the given functions as simple tags."""
    library = template.Library()
    for func in funcs:
        library.simple_tag(func, takes_context=takes_context)
    return library


# --- Configs -----------------------------------------------------------


@dataclass(kw_only=True)
class TagConfig:
    """Config of the tags under test.

    Attributes:
        label: Text of the tag.
        tone: Look of the tag.
    """

    label: str = field(default="", metadata={"doc": "Text of the tag."})
    tone: str = field(default="plain", metadata={"doc": "Look of the tag."})


@dataclass
class PositionalConfig:
    """Config whose fields can be passed by position.

    Attributes:
        label: Text of the tag.
    """

    label: str = field(default="", metadata={"doc": "Text of the tag."})


@dataclass(kw_only=True)
class UndocumentedConfig:
    """Config without an Attributes entry for its field."""

    label: str = field(default="", metadata={"doc": "Text of the tag."})


@dataclass(kw_only=True)
class ExtraEntryConfig:
    """Config whose docstring documents a field it does not have.

    Attributes:
        label: Text of the tag.
        colour: Removed field.
    """

    label: str = field(default="", metadata={"doc": "Text of the tag."})


@dataclass(kw_only=True)
class NoMetadataConfig:
    """Config without metadata["doc"].

    Attributes:
        label: Text of the tag.
    """

    label: str = ""


@dataclass(kw_only=True)
class DivergingConfig:
    """Config whose two descriptions differ.

    Attributes:
        label: Text of the tag.
    """

    label: str = field(default="", metadata={"doc": "Label of the tag."})


def test_config_problems_accept_documented_keyword_only_configs() -> None:
    """A matching Config passes; exports that are no dataclasses are not Configs."""
    assert config_problems(_module(TagConfig, _module)) == []


@pytest.mark.parametrize(
    ("config_cls", "names"),
    [
        pytest.param(PositionalConfig, ["PositionalConfig", "keyword-only", "label"], id="positional"),
        pytest.param(UndocumentedConfig, ["UndocumentedConfig", "missing", "label"], id="missing-entry"),
        pytest.param(ExtraEntryConfig, ["ExtraEntryConfig", "without a field", "colour"], id="extra-entry"),
        pytest.param(NoMetadataConfig, ["NoMetadataConfig.label", "metadata['doc'] is missing"], id="no-metadata"),
        pytest.param(DivergingConfig, ["DivergingConfig.label", "Text of the tag.", "Label of the tag."], id="differ"),
    ],
)
def test_config_problems_report_drift(config_cls: type, names: list[str]) -> None:
    """Each kind of drift is reported once, with the Config and the field."""
    problems = config_problems(_module(config_cls))

    assert len(problems) == 1, problems
    assert all(name in problems[0] for name in names), problems


def test_config_problems_require_all() -> None:
    """Without __all__ the public Configs are unknown, which is a problem, not an empty pass."""
    assert len(config_problems(ModuleType("extension.configs"))) == 1


def test_config_problems_compare_the_source_text_in_any_language() -> None:
    """Translated descriptions do not count as different from the English docstring."""
    tag_id = next(config_field for config_field in fields(configs.AccordionConfig) if config_field.name == "tag_id")
    with override("de"):
        assert str(tag_id.metadata["doc"]) != configs.AccordionConfig.__doc__  # precondition: really translated
        assert "Tag-ID" in str(tag_id.metadata["doc"])

        assert config_problems(configs) == []


# --- Tags --------------------------------------------------------------


def matching(config: TagConfig | None = None, *, label: str | Unset = UNSET, tone: str | Unset = UNSET) -> str:
    """Tag whose arguments are the fields of its Config."""
    return build_config(TagConfig, config, label=label, tone=tone).label


def extra_argument(
    config: TagConfig | None = None, *, label: str | Unset = UNSET, tone: str | Unset = UNSET, size: str = "m"
) -> str:
    """Tag with an argument that is no field."""
    return build_config(TagConfig, config, label=label, tone=tone).label + size


def missing_argument(config: TagConfig | None = None, *, label: str | Unset = UNSET) -> str:
    """Tag without an argument for the tone field."""
    return build_config(TagConfig, config, label=label).label


def lenient(config: TagConfig | None = None, *, label: str | Unset = UNSET, tone: str | Unset = UNSET) -> str:
    """Tag that renders whatever it gets instead of building its Config."""
    return f"{config} {label} {tone}"


def untyped(config: object = None) -> str:
    """Tag whose config annotation names no Config."""
    return str(config)


def with_context(
    context: template.Context, config: TagConfig | None = None, *, label: str | Unset = UNSET, tone: str | Unset = UNSET
) -> str:
    """Tag that takes the template context first."""
    return build_config(TagConfig, config, label=label, tone=tone).label + str(len(context.dicts))


def test_tag_problems_accept_matching_tags() -> None:
    """Tags whose arguments match their Config and that build it with build_config pass, with or without context."""
    assert tag_problems(_library(matching)) == []
    assert tag_problems(_library(with_context, takes_context=True)) == []


def test_tag_problems_accept_listed_exceptions() -> None:
    """Documented exceptions silence exactly the drift they describe."""
    library = _library(extra_argument, missing_argument)
    convenience = {"extra_argument": {"size"}}
    without_argument = {"missing_argument": {"tone"}}

    assert tag_problems(library, convenience_arguments=convenience, fields_without_tag_argument=without_argument) == []
    assert tag_problems(library, convenience_arguments=convenience, config_only_tags={"missing_argument"}) == []


@pytest.mark.parametrize(
    ("tag", "options", "names"),
    [
        pytest.param(extra_argument, {}, ["extra_argument", "without a TagConfig field", "size"], id="extra-argument"),
        pytest.param(
            missing_argument, {}, ["missing_argument", "without a tag argument", "tone"], id="missing-argument"
        ),
        pytest.param(lenient, {}, ["lenient", "accepts a dict"], id="accepts-dict"),
        pytest.param(untyped, {}, ["untyped", "no single Config dataclass"], id="no-config-class"),
        pytest.param(
            matching, {"fields_without_tag_argument": {"matching": {"tone"}}}, ["matching", "tone"], id="stale-field"
        ),
        pytest.param(
            matching, {"convenience_arguments": {"matching": {"size"}}}, ["matching", "size"], id="stale-convenience"
        ),
        pytest.param(matching, {"config_only_tags": {"removed"}}, ["removed"], id="unknown-tag"),
    ],
)
def test_tag_problems_report_drift(tag: Callable[..., Any], options: dict[str, Any], names: list[str]) -> None:
    """Each kind of drift, including outdated exceptions, is reported once with the tag and the names involved."""
    problems = tag_problems(_library(tag), **options)

    assert len(problems) == 1, problems
    assert all(name in problems[0] for name in names), problems
