# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Build component configs from a Config instance and template tag arguments.

Core tags and tags of packages that extend Insight UI share these helpers:

    from insight_ui.configs import UNSET, Unset, build_config

    def profile_card(config: ProfileCardConfig | None = None, *, title: str | Unset = UNSET) -> dict[str, Any]:
        config = build_config(ProfileCardConfig, config, title=title)
        return {"profile_card_config": config}
"""

from __future__ import annotations

from dataclasses import MISSING, fields, is_dataclass, replace
from typing import TYPE_CHECKING, Any, Final, Literal

if TYPE_CHECKING:
    from _typeshed import DataclassInstance


class Unset:
    """Type of UNSET, the default of template tag arguments that were not passed."""

    def __repr__(self) -> Literal["UNSET"]:
        """Show the sentinel by its name in tracebacks and signatures."""
        return "UNSET"


UNSET: Final = Unset()


def build_config[T: DataclassInstance](cls: type[T], config: T | None = None, **kwargs: Any) -> T:  # noqa: ANN401
    """Create or update a dataclass instance.

    Parameters with value UNSET are ignored. If config is None, creates a new
    instance and validates required fields. If config is given, returns a copy
    with provided overrides applied.

    Args:
        cls: The dataclass type to create or update.
        config: An existing config instance to update, or None to create new.
        **kwargs: Field values to set or override.

    Returns:
        A new or updated dataclass instance.

    Raises:
        TypeError: If config is neither None nor a dataclass instance.
        ValueError: If required fields are missing when creating a new instance.

    """
    overrides = {key: value for key, value in kwargs.items() if value is not UNSET}

    if config is not None:
        if not is_dataclass(config) or isinstance(config, type):
            raise TypeError(  # noqa: TRY003
                f"config for {cls.__name__} must be a dataclass instance, got {type(config).__name__}."
            )
        return replace(config, **overrides)

    required_fields = [
        field.name for field in fields(cls) if field.default is MISSING and field.default_factory is MISSING
    ]

    missing = [field_name for field_name in required_fields if field_name not in overrides]

    if missing:
        raise ValueError(f"Missing required fields for {cls.__name__}: {', '.join(missing)}")  # noqa: TRY003

    return cls(**overrides)
