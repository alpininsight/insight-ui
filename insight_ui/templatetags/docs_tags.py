"""Template-Tags for Insight UI-Components."""

from __future__ import annotations

import re
import uuid
from typing import TYPE_CHECKING, Any

from django import template
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe

from insight_ui.utils.config_registry import get_config_class_names
from insight_ui.utils.type_registry import get_type_info, is_known_type as _is_known_type

if TYPE_CHECKING:
    from insight_ui.component_details.component_context import ParameterDetails

register = template.Library()

# Beyond this many levels, inline expansion gets hard to follow, so deeper rows
# are shown flat with a hint instead of another nested, expandable table.
MAX_PARAMETER_NESTING_DEPTH = 2

_TYPE_TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


@register.filter
def is_known_type(type_name: str) -> bool:
    """Check if a type name is a documented type in the registry."""
    return _is_known_type(type_name)


@register.filter
def is_config_type(type_name: str) -> bool:
    """Check whether a type string references at least one known config dataclass."""
    known = get_config_class_names()
    return any(token in known for token in _TYPE_TOKEN_RE.findall(type_name))


@register.filter
def config_type_anchor(type_name: str) -> str:
    """Get the anchor of the first known config dataclass referenced in a type string.

    Args:
        type_name: The formatted type string (e.g. "list[NavbarLinkConfig]").

    Returns:
        The lowercase anchor of the first matching dataclass, or an empty
        string if the type string references no known dataclass.

    """
    known = get_config_class_names()
    for token in _TYPE_TOKEN_RE.findall(type_name):
        if token in known:
            return token.lower()
    return ""


@register.simple_tag
def config_type_link(type_name: str) -> str:
    """Render a type string as HTML, turning any known config dataclass name into a link.

    Args:
        type_name: The formatted type string (e.g. "list[NavbarLinkConfig]").

    Returns:
        Safe HTML with known config dataclass names replaced by links to
        their anchor on the config reference page; everything else (generic
        types, brackets, unions) is left as escaped plain text.

    """
    known = get_config_class_names()
    base_url = reverse("config_reference_view")

    def replace(match: re.Match) -> str:
        token = match.group(0)
        if token not in known:
            return escape(token)
        return f'<a href="{base_url}#{token.lower()}" class="text-insight-text-link hover:underline">{token}</a>'

    return mark_safe(_TYPE_TOKEN_RE.sub(replace, type_name))  # nosec  # noqa: S308


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


@register.inclusion_tag("insight_ui/components/parameter_table.html")
def parameter_table(rows: list[ParameterDetails], depth: int = 0) -> dict[str, Any]:
    """Render a parameter table, generating a unique toggle id for rows with nested documentation.

    Rows are only made expandable up to MAX_PARAMETER_NESTING_DEPTH; beyond that,
    a row with nested documentation is shown flat with a hint instead of yet
    another indented, expandable table.

    Args:
        rows: The parameter rows to render as a table.
        depth: The current nesting depth, starting at 0 for the top-level table.

    Returns:
        Context dict pairing each row with a unique toggle id (or None, if it
        has no nested documentation, or the nesting limit was reached), plus
        the depth to pass to a recursive call.

    """
    can_expand = depth < MAX_PARAMETER_NESTING_DEPTH
    return {
        "rows": [(row, f"param-row-{uuid.uuid4().hex[:8]}" if row.nested and can_expand else None) for row in rows],
        "next_depth": depth + 1,
        "nesting_limit_reached": not can_expand,
    }
