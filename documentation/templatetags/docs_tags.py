"""Template-Tags for Insight UI-Components."""

from __future__ import annotations

import re
import uuid
from typing import TYPE_CHECKING, Any

from django import template
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from insight_ui.configs.base import IconConfig

from documentation.config_registry import get_config_class_names
from documentation.type_registry import get_type_info, is_known_type as _is_known_type

if TYPE_CHECKING:
    from documentation.component_details.component_context import ParameterDetails

register = template.Library()

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


@register.simple_tag
def config_type_link(type_name: str) -> str:
    """Render a type string as HTML, turning any known config dataclass name into a link.

    Appends an info-circle icon, matching the affordance used by the type
    popover and the parameter table's inline drill-down link.

    Args:
        type_name: The formatted type string (e.g. "list[NavbarLinkConfig]").

    Returns:
        Safe HTML with known config dataclass names replaced by links to
        their anchor on the config reference page; everything else (generic
        types, brackets, unions) is left as escaped plain text.

    """
    known = get_config_class_names()
    base_url = reverse("config_reference_view")
    icon_html = render_to_string(
        "insight_ui/components/icons.html", {"icon_config": IconConfig(name="information-circle", size="xs")}
    )

    def replace(match: re.Match) -> str:
        token = match.group(0)
        if token not in known:
            return escape(token)
        return (
            f'<a href="{base_url}#{token.lower()}" '
            f'class="inline-flex items-center gap-1 text-insight-text-link hover:underline">'
            f"{token}{icon_html}</a>"
        )

    return mark_safe(_TYPE_TOKEN_RE.sub(replace, type_name))  # nosec  # noqa: S308


@register.inclusion_tag("documentation/components/type_popover.html")
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


@register.inclusion_tag("documentation/components/parameter_table.html")
def parameter_table(rows: list[ParameterDetails], base_url: str = "", path: str = "") -> dict[str, Any]:
    """Render a parameter table, pairing each nested row with the path to drill into it.

    Rows with nested documentation get a drill-down link instead of expanding
    inline, so only a single table is ever shown at once - the caller swaps
    it via HTMX and navigates using the resulting path.

    Inclusion tags don't inherit the caller's template context (e.g. `request`),
    so the component's own URL must be passed in explicitly rather than relying
    on `{{ request.path }}` inside the template.

    Args:
        rows: The parameter rows to render as a table.
        base_url: The component detail page's own URL, used as the base for
            each row's drill-down link.
        path: The dot-separated path identifying the currently active table,
            used as the prefix for each row's drill-down path.

    Returns:
        Context dict with `base_url` and rows paired with the path to drill
        into them (or None, if a row has no nested documentation).

    """

    def child_path(row: ParameterDetails) -> str | None:
        if not row.nested:
            return None
        return f"{path}.{row.name}" if path else row.name

    return {"base_url": base_url, "rows": [(row, child_path(row)) for row in rows]}
