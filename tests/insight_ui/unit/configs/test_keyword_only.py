# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Config dataclasses accept keyword arguments only."""

import inspect
from dataclasses import is_dataclass

import pytest

from insight_ui import configs

CONFIG_CLASSES = [getattr(configs, name) for name in configs.__all__ if is_dataclass(getattr(configs, name))]


@pytest.mark.parametrize("config_cls", CONFIG_CLASSES, ids=lambda cls: cls.__name__)
def test_config_fields_are_keyword_only(config_cls: type) -> None:
    """New or reordered fields never change the meaning of an existing call."""
    positional = [
        name
        for name, parameter in inspect.signature(config_cls).parameters.items()
        if parameter.kind is not inspect.Parameter.KEYWORD_ONLY
    ]

    assert positional == []


def test_positional_arguments_are_rejected() -> None:
    """A positional call fails loudly instead of filling the wrong field."""
    with pytest.raises(TypeError, match="positional"):
        configs.SearchBarConfig("/search/", True)
