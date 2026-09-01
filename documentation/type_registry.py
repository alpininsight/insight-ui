"""Type registry for component parameter documentation.

This module provides a centralized registry of type definitions used in component
parameters. It imports the TYPE_REGISTRY from insight_ui.configs.types as the
single source of truth.
"""

from django.utils.translation import gettext_lazy as _
from insight_ui.configs.types import TYPE_REGISTRY as _TYPE_REGISTRY

# Build the documentation registry with translated descriptions and anchors
TYPE_DEFINITIONS: dict[str, dict] = {
    name: {
        "anchor": name.lower(),
        "values": info["values"],
        "description": _(info["description"]),
    }
    for name, info in _TYPE_REGISTRY.items()
}


def get_type_info(type_name: str) -> dict | None:
    """Look up type information by name.

    Args:
        type_name: The type name to look up (case-insensitive).

    Returns:
        Dictionary with type info including name, anchor, values and description.
        Returns None if type is not found.

    """
    # Try exact match first
    if type_name in TYPE_DEFINITIONS:
        return {"name": type_name, **TYPE_DEFINITIONS[type_name]}

    # Try case-insensitive match
    for name, info in TYPE_DEFINITIONS.items():
        if name.lower() == type_name.lower():
            return {"name": name, **info}

    return None


def is_known_type(type_name: str) -> bool:
    """Check if a type name is a documented type.

    Args:
        type_name: The type name to check.

    Returns:
        True if the type is documented in the registry.

    """
    return get_type_info(type_name) is not None


def get_all_type_definitions() -> list[dict]:
    """Get all type definitions as a list for template rendering.

    Returns:
        List of dictionaries containing type information,
        each with name, anchor, values and description.

    """
    return [{"name": name, **info} for name, info in TYPE_DEFINITIONS.items()]
