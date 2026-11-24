# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Contract checks for Configs and template tags, for Insight UI and the packages that extend it.

Each check returns one message per problem and an empty list when the contract holds, so any test runner can use it:

    from insight_ui.testing import config_problems, tag_problems
    from profiles import configs
    from profiles.templatetags.profile_tags import register

    def test_configs_follow_the_contract() -> None:
        assert config_problems(configs) == []

    def test_tags_follow_the_contract() -> None:
        assert tag_problems(register) == []

The checks use reflection: they find drift between Configs, docstrings and tags, but do not replace rendering tests.
"""

from __future__ import annotations

import inspect
import re
from dataclasses import fields, is_dataclass
from typing import TYPE_CHECKING, Any, get_args

from django.template import Context
from django.utils.translation import override

if TYPE_CHECKING:
    from collections.abc import Callable, Collection, Mapping
    from types import ModuleType

    from django.template import Library

# The Attributes section of a Google docstring: its title, then indented or blank lines up to the next unindented one.
_ATTRIBUTES_SECTION = re.compile(r"^Attributes:[ \t]*\n((?:[ \t]*\n|[ \t]+\S.*\n?)*)", re.MULTILINE)
_TYPED_NAME = re.compile(r"(.+?)\s*\(.*\)")
_IDENTIFIER = re.compile(r"[A-Za-z_]\w*")
# build_config's message for a config that is not a dataclass instance.
_DICT_CONFIG_MESSAGE = "must be a dataclass instance"


def config_problems(module: ModuleType) -> list[str]:
    """Check the Config dataclasses that a module exports in ``__all__``.

    Every field is keyword-only and has the same description in the ``Attributes`` section of the class docstring
    and in ``metadata["doc"]``. Descriptions are compared in their source language, whatever language is active.

    Args:
        module: The package's public Config module, e.g. ``insight_ui.configs``.

    Returns:
        One message per problem; empty when all exported Configs follow the contract.

    """
    exported = getattr(module, "__all__", None)
    if exported is None:
        return [f"{module.__name__}: no __all__, so its public Configs are unknown"]

    problems = []
    for name in exported:
        config_cls = getattr(module, name)
        if isinstance(config_cls, type) and is_dataclass(config_cls):
            problems.extend(_positional_field_problems(config_cls))
            problems.extend(_field_doc_problems(config_cls))
    return problems


def tag_problems(
    library: Library,
    *,
    convenience_arguments: Mapping[str, Collection[str]] | None = None,
    config_only_tags: Collection[str] = (),
    fields_without_tag_argument: Mapping[str, Collection[str]] | None = None,
) -> list[str]:
    """Check the template tags of a library that take a ``config`` argument.

    The Config class comes from the annotation of ``config``. Every keyword-only argument is a field of that Config,
    every field is an argument, and a dict as ``config`` raises the ``TypeError`` of ``build_config()``.

    Args:
        library: The package's template library, the ``register`` of its tag module.
        convenience_arguments: Per tag, arguments that the tag turns into a field instead of passing them on.
        config_only_tags: Tags that take a complete Config and no field arguments.
        fields_without_tag_argument: Per tag, fields that can only be set through the Config.

    Returns:
        One message per problem, including exceptions that name unknown tags or no longer apply; empty when all
        tags follow the contract.

    """
    convenience_arguments = convenience_arguments or {}
    fields_without_tag_argument = fields_without_tag_argument or {}
    tags = {name: inspect.unwrap(compile_func) for name, compile_func in library.tags.items()}
    config_tags = {name: func for name, func in tags.items() if "config" in inspect.signature(func).parameters}

    problems = []
    listed = set(convenience_arguments) | set(config_only_tags) | set(fields_without_tag_argument)
    if unknown := sorted(listed - config_tags.keys()):
        problems.append(f"Exceptions name tags without a config argument: {', '.join(unknown)}")

    for name, func in sorted(config_tags.items()):
        problems.extend(
            _single_tag_problems(
                name,
                func,
                convenience=set(convenience_arguments.get(name, ())),
                config_only=name in config_only_tags,
                without_argument=set(fields_without_tag_argument.get(name, ())),
            )
        )
    return problems


def _positional_field_problems(config_cls: type) -> list[str]:
    """Report fields that can be passed by position."""
    positional = [
        name
        for name, parameter in inspect.signature(config_cls).parameters.items()
        if parameter.kind is not inspect.Parameter.KEYWORD_ONLY
    ]
    if positional:
        return [f"{config_cls.__name__}: fields that are not keyword-only: {', '.join(positional)}"]
    return []


def _field_doc_problems(config_cls: type) -> list[str]:
    """Report fields whose docstring entry and ``metadata["doc"]`` are missing or differ."""
    name = config_cls.__name__
    documented = _attribute_docs(config_cls.__doc__ or "")
    config_fields = fields(config_cls)
    field_names = [config_field.name for config_field in config_fields]

    problems = []
    if missing := [field_name for field_name in field_names if field_name not in documented]:
        problems.append(f"{name}: fields missing in the Attributes docstring: {', '.join(missing)}")
    if extra := sorted(documented.keys() - set(field_names)):
        problems.append(f"{name}: Attributes docstring entries without a field: {', '.join(extra)}")

    # Without an active language, lazy translations return their source text, the language of the docstring.
    with override(None):
        for config_field in config_fields:
            doc = config_field.metadata.get("doc")
            if doc is None:
                problems.append(f"{name}.{config_field.name}: metadata['doc'] is missing")
            elif config_field.name in documented and str(doc).strip() != documented[config_field.name]:
                problems.append(
                    f"{name}.{config_field.name}: docstring and metadata['doc'] differ: "
                    f"{documented[config_field.name]!r} != {str(doc).strip()!r}"
                )
    return problems


def _attribute_docs(docstring: str) -> dict[str, str]:
    """Return the field descriptions of a Google docstring's ``Attributes`` section.

    Continuation lines are dedented and kept on their own lines, as in docstring_parser.
    """
    match = _ATTRIBUTES_SECTION.search(inspect.cleandoc(docstring) + "\n")
    block = match.group(1).strip("\n") if match else ""
    if not block:
        return {}

    indent = block[: len(block) - len(block.lstrip(" \t"))]
    docs = {}
    for entry in re.split(rf"^{re.escape(indent)}(?=\S)", block, flags=re.MULTILINE)[1:]:
        name, _, description = entry.strip("\n").partition(":")
        typed = _TYPED_NAME.fullmatch(name.strip())
        first_line, newline, rest = description.removeprefix(" ").partition("\n")
        if newline:
            description = f"{first_line}\n{inspect.cleandoc(rest)}"
        docs[(typed.group(1) if typed else name).strip()] = description.strip()
    return docs


def _single_tag_problems(
    name: str,
    func: Callable[..., Any],
    *,
    convenience: set[str],
    config_only: bool,
    without_argument: set[str],
) -> list[str]:
    """Report the contract problems of one tag."""
    config_cls = _config_class(func)
    if config_cls is None:
        return [f"{name}: the annotation of config names no single Config dataclass"]

    field_names = {config_field.name for config_field in fields(config_cls)}
    arguments = {
        parameter.name
        for parameter in inspect.signature(func).parameters.values()
        if parameter.kind is inspect.Parameter.KEYWORD_ONLY
    }
    config_name = config_cls.__name__

    problems = []
    if unknown := sorted(arguments - field_names - convenience):
        problems.append(f"{name}: arguments without a {config_name} field: {', '.join(unknown)}")
    if stale := sorted(convenience - arguments):
        problems.append(f"{name}: listed as convenience arguments, but no arguments: {', '.join(stale)}")
    if not config_only:
        missing = field_names - arguments
        if undeclared := sorted(missing - without_argument):
            problems.append(f"{name}: {config_name} fields without a tag argument: {', '.join(undeclared)}")
        if stale := sorted(without_argument - missing):
            problems.append(f"{name}: listed as fields without a tag argument, but are arguments: {', '.join(stale)}")
    problems.extend(_dict_config_problems(name, func))
    return problems


def _config_class(func: Callable[..., Any]) -> type | None:
    """Return the single dataclass named in the annotation of the ``config`` parameter."""
    annotation = inspect.signature(func).parameters["config"].annotation
    if isinstance(annotation, str):
        namespace = getattr(func, "__globals__", {})
        candidates = [namespace.get(word) for word in _IDENTIFIER.findall(annotation)]
    else:
        candidates = [annotation, *get_args(annotation)]
    classes = {candidate for candidate in candidates if isinstance(candidate, type) and is_dataclass(candidate)}
    return classes.pop() if len(classes) == 1 else None


def _dict_config_problems(name: str, func: Callable[..., Any]) -> list[str]:
    """Report a tag that does not reject a dict as ``config`` through ``build_config()``."""
    context_args = (Context(),) if next(iter(inspect.signature(func).parameters)) == "context" else ()
    try:
        func(*context_args, config={"name": "field", "label": "Label"})
    except TypeError as error:
        if _DICT_CONFIG_MESSAGE in str(error):
            return []
        return [f"{name}: a dict as config raised {error!r} instead of the TypeError of build_config()"]
    except Exception as error:  # noqa: BLE001 - report every other failure as a problem of this tag
        return [f"{name}: a dict as config raised {error!r} instead of the TypeError of build_config()"]
    return [f"{name}: accepts a dict as config instead of rejecting it with build_config()"]
