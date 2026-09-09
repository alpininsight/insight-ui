# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Query builder utilities for dynamic filtering."""

from collections.abc import Iterable, Mapping
from typing import Any

from django.db.models import Q

from insight_ui.configs.filter import QueryBuilderFieldConfig


def _coerce_operations(operations: object) -> list[str]:
    """Check whether the specified operations are a list of strings."""
    if isinstance(operations, Iterable) and not isinstance(operations, str | bytes):
        return [op for op in operations if isinstance(op, str)]
    return []


def _coerce_values(values: object) -> dict[str, str]:
    """Check whether the specified values are a list of strings."""
    if isinstance(values, Mapping):
        return {
            str(key): str(value) for key, value in values.items() if isinstance(key, str) and isinstance(value, str)
        }
    return {}


def get_filter_settings_for_field(
    fields: list[QueryBuilderFieldConfig], field: QueryBuilderFieldConfig
) -> tuple[str, list[str], dict[str, str]]:
    """Retrieve the allowed operators based on the type of field.

    Args:
        fields: A list of all available fields.
        field: The field to get the desired information from.

    Returns:
        A tuple of input type, allowed operators, and possible values.

    """
    for config in fields:
        if config.field == field:
            return config.type, _coerce_operations(config.operations), _coerce_values(config.values)

    return "text", [], {}


def build_dynamic_query(filters: list[Mapping[str, Any]]) -> tuple[Q, dict[str, Any], dict[str, Any]]:
    """Build django query by the given filters.

    Args:
        filters: A list of filter dictionaries used to generate the query.

    Returns:
        A tuple of the generated Q object, annotations dict, and annotation filters dict.

    """
    if not filters:
        return Q(), {}, {}

    base_query = Q()
    annotations: dict[str, Any] = {}
    annotation_filters: dict[str, Any] = {}

    # Group filters by model field
    grouped_filters: dict[str, list[Mapping[str, Any]]] = {}
    for filter_config in filters:
        field = filter_config.get("field")
        # Ignore empty filters
        if field == "":
            continue
        if not isinstance(field, str):
            continue
        grouped_filters.setdefault(field, []).append(filter_config)

    for field, group in grouped_filters.items():
        # Normal fields
        for filter_config in group:
            operator = filter_config.get("operator", "exact")
            if not isinstance(operator, str):
                operator = "exact"

            value = filter_config.get("value")

            logic = filter_config.get("logic", "AND")
            if not isinstance(logic, str):
                logic = "AND"

            q = Q(**{f"{field}__{operator}": value})
            base_query = base_query & q if logic == "AND" else base_query | q

    return base_query, annotations, annotation_filters
