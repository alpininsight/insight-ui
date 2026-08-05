"""Type registry for component parameter documentation.

This module provides a centralized registry of type definitions used in component
parameters. It serves as the single source of truth for type information displayed
in the parameter tables and the types documentation page.
"""

from django.utils.translation import gettext_lazy as _

from insight_ui.configs import types

# Type definitions registry - single source of truth for documentation
# Each entry contains:
#   - anchor: URL fragment for linking to types page
#   - values: Tuple of allowed values
#   - description: Human-readable description
TYPE_DEFINITIONS: dict[str, dict] = {
    "Size": {
        "anchor": "size",
        "values": types.SIZE_VALUES,
        "description": _("Standard size scale used for spacing, icons, and component dimensions."),
    },
    "ColorType": {
        "anchor": "colortype",
        "values": types.COLOR_TYPE_VALUES,
        "description": _("Base color palette for semantic coloring of components."),
    },
    "BadgeType": {
        "anchor": "badgetype",
        "values": types.BADGE_TYPE_VALUES,
        "description": _("Extended color palette for badges, includes 'disabled' state."),
    },
    "ButtonType": {
        "anchor": "buttontype",
        "values": types.BUTTON_TYPE_VALUES,
        "description": _("Extended color palette for buttons, includes 'disabled' and 'link' variants."),
    },
    "AlertType": {
        "anchor": "alerttype",
        "values": types.ALERT_TYPE_VALUES,
        "description": _("Semantic types for alerts and notifications."),
    },
    "StepStatus": {
        "anchor": "stepstatus",
        "values": types.STEP_STATUS_VALUES,
        "description": _("Status values for stepper components indicating step progress."),
    },
    "HtmlButtonType": {
        "anchor": "htmlbuttontype",
        "values": types.HTML_BUTTON_TYPE_VALUES,
        "description": _("Native HTML button type attribute values."),
    },
    "HtmlInputType": {
        "anchor": "htmlinputtype",
        "values": types.HTML_INPUT_TYPE_VALUES,
        "description": _("Native HTML input type attribute values."),
    },
    "FormFieldType": {
        "anchor": "formfieldtype",
        "values": types.FORM_FIELD_TYPE_VALUES,
        "description": _("High-level form field types for the form component."),
    },
    "CornerPosition": {
        "anchor": "cornerposition",
        "values": types.CORNER_POSITION_VALUES,
        "description": _("Corner positions for ribbons, badges, and overlays."),
    },
    "InlinePosition": {
        "anchor": "inlineposition",
        "values": types.INLINE_POSITION_VALUES,
        "description": _("Inline positions respecting text direction (RTL-aware)."),
    },
    "HtmxSwapMethod": {
        "anchor": "htmxswapmethod",
        "values": types.HTMX_SWAP_METHOD_VALUES,
        "description": _("HTMX swap methods for content replacement."),
    },
    "HtmxMethod": {
        "anchor": "htmxmethod",
        "values": types.HTMX_METHOD_VALUES,
        "description": _("HTTP methods for HTMX requests."),
    },
    "FilterFieldType": {
        "anchor": "filterfieldtype",
        "values": types.FILTER_FIELD_TYPE_VALUES,
        "description": _("Field types for query builder and filter components."),
    },
    "GeoMapMarkerType": {
        "anchor": "geomapmarkertype",
        "values": types.GEO_MAP_MARKER_TYPE_VALUES,
        "description": _("Marker types for the geo map component."),
    },
    "SliderLegendMode": {
        "anchor": "sliderlegendmode",
        "values": types.SLIDER_LEGEND_MODE_VALUES,
        "description": _("Legend display modes for the range slider component."),
    },
    "ToggleViewType": {
        "anchor": "toggleviewtype",
        "values": types.TOGGLE_VIEW_TYPE_VALUES,
        "description": _("View types for the toggle view component."),
    },
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
