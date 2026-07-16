"""Template-Tags for Insight UI-Components."""

from __future__ import annotations

import uuid
from typing import Any

from django import template

from insight_ui.utils.type_registry import get_type_info, is_known_type as _is_known_type

register = template.Library()


@register.filter
def is_known_type(type_name: str) -> bool:
    """Check if a type name is a documented type in the registry."""
    return _is_known_type(type_name)


@register.inclusion_tag("insight_ui/components/type_popover.html")
def type_popover(type_name: str) -> dict[str, Any]:
    """Render a type popover trigger with popup content.

    Args:
        type_name: The type name to look up in the registry.

    Returns:
        Context dict with type_info, popover_id, and type_name.

    """
    type_info = get_type_info(type_name)
    unique_id = uuid.uuid4().hex[:8]
    return {
        "type_info": type_info,
        "type_name": type_name,
        "popover_id": f"type-popover-{unique_id}",
    }
