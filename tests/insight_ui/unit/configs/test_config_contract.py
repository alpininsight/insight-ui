# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""The public Configs follow the Config contract that extension packages check as well."""

import pytest
from insight_ui.testing import config_problems

from insight_ui import configs


def test_public_configs_follow_the_config_contract() -> None:
    """Every exported Config has keyword-only fields with the same docstring and metadata["doc"] text."""
    assert config_problems(configs) == []


def test_positional_arguments_are_rejected() -> None:
    """A positional call fails loudly instead of filling the wrong field."""
    with pytest.raises(TypeError, match="positional"):
        configs.SearchBarConfig("/search/", True)
