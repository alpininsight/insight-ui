# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Type definitions and validation functions for Insight UI components.

This module provides centralized type aliases, value constants, and validation
functions used across all configuration classes. Each type follows a consistent
pattern:

1. A tuple constant for runtime validation (e.g., SIZE_VALUES)
2. A type alias using Python 3.12+ syntax (e.g., type Size = Literal[...])
3. A validation function with descriptive errors (e.g., validate_size())

Example usage:
    from insight_ui.configs.types import Size, validate_size

    def set_size(size: Size) -> None:
        validate_size(size)
        ...

"""

from difflib import get_close_matches
from functools import lru_cache
from typing import Literal

# =============================================================================
# Heading Level
# =============================================================================

# Heading levels a component title can use; h1 is reserved for the page title
HEADING_LEVEL_VALUES: tuple[int, ...] = (2, 3, 4, 5, 6)

# Type alias for the heading level of component titles
type HeadingLevel = Literal[2, 3, 4, 5, 6]

# =============================================================================
# Size
# =============================================================================

# Tuple of valid size values for runtime validation
SIZE_VALUES: tuple[str, ...] = ("xs", "s", "m", "l", "xl")

# Type alias for component sizes
type Size = Literal["xs", "s", "m", "l", "xl"]

# =============================================================================
# Color Types
# =============================================================================

# Tuple of valid color type values (base palette)
COLOR_TYPE_VALUES: tuple[str, ...] = (
    "primary",
    "secondary",
    "neutral",
    "info",
    "success",
    "warning",
    "danger",
)

# Type alias for base color types
type ColorType = Literal["primary", "secondary", "neutral", "info", "success", "warning", "danger"]

# Tuple of valid button colors: the color roles plus "light" for dark or colored surfaces (no grey button)
BUTTON_COLOR_VALUES: tuple[str, ...] = ("primary", "secondary", "light", "info", "success", "warning", "danger")

# Type alias for button colors
type ButtonColor = Literal["primary", "secondary", "light", "info", "success", "warning", "danger"]

# Tuple of valid button variants (visual style); "link" and "plain" ignore the color
BUTTON_VARIANT_VALUES: tuple[str, ...] = ("solid", "outline", "subtle", "link", "plain")

# Type alias for button variants
type ButtonVariant = Literal["solid", "outline", "subtle", "link", "plain"]

# Tuple of valid variants of toggle buttons and radio blocks; "neutral" ignores the color
CONTROL_VARIANT_VALUES: tuple[str, ...] = ("neutral", "subtle", "outline")

# Type alias for control variants
type ControlVariant = Literal["neutral", "subtle", "outline"]

# Icon color values: semantic colors + text colors
ICON_COLOR_VALUES: tuple[str, ...] = (
    "",
    "primary",
    "secondary",
    "success",
    "warning",
    "danger",
    "info",
    "text-headline",
    "text-body",
    "text-muted",
    "text-link",
)

# Type alias for icon colors
type IconColor = Literal[
    "",
    "primary",
    "secondary",
    "success",
    "warning",
    "danger",
    "info",
    "text-headline",
    "text-body",
    "text-muted",
    "text-link",
]


# =============================================================================
# Status Types
# =============================================================================

# Tuple of valid step status values (for stepper components)
STEP_STATUS_VALUES: tuple[str, ...] = ("pending", "current", "completed", "failed")

# Type alias for step status
type StepStatus = Literal["pending", "current", "completed", "failed"]

# Tuple of valid message severity values (alert, infobox, status screen)
SEVERITY_VALUES: tuple[str, ...] = ("info", "success", "warning", "error")

# Type alias for message severity: what happened, as opposed to the color role (ColorType)
type Severity = Literal["info", "success", "warning", "error"]

# =============================================================================
# HTML Element Types
# =============================================================================

# Tuple of valid HTML button type values (native <button> type attribute)
HTML_BUTTON_TYPE_VALUES: tuple[str, ...] = ("button", "submit", "reset")

# Type alias for HTML button types
type HtmlButtonType = Literal["button", "submit", "reset"]

# Tuple of valid HTML input type values (native <input> type attribute)
HTML_INPUT_TYPE_VALUES: tuple[str, ...] = (
    "text",
    "password",
    "email",
    "number",
    "tel",
    "url",
    "date",
    "time",
    "datetime-local",
    "month",
    "week",
    "color",
    "file",
    "hidden",
    "checkbox",
    "radio",
)

# Type alias for HTML input types
type HtmlInputType = Literal[
    "text",
    "password",
    "email",
    "number",
    "tel",
    "url",
    "date",
    "time",
    "datetime-local",
    "month",
    "week",
    "color",
    "file",
    "hidden",
    "checkbox",
    "radio",
]

# =============================================================================
# Position Types
# =============================================================================

# Tuple of valid corner position values (for corner ribbons, badges, etc.)
CORNER_POSITION_VALUES: tuple[str, ...] = ("top-right", "top-left", "bottom-right", "bottom-left")

# Type alias for corner positions
type CornerPosition = Literal["top-right", "top-left", "bottom-right", "bottom-left"]

# Tuple of valid inline position values (for logos, icons in text flow, etc.)
INLINE_POSITION_VALUES: tuple[str, ...] = ("start", "end")

# Type alias for inline positions
type InlinePosition = Literal["start", "end"]

# =============================================================================
# HTMX Types
# =============================================================================

# Tuple of valid HTMX swap method values
HTMX_SWAP_METHOD_VALUES: tuple[str, ...] = (
    "innerHTML",
    "outerHTML",
    "beforebegin",
    "afterbegin",
    "beforeend",
    "afterend",
    "delete",
    "none",
)

# Type alias for HTMX swap methods
type HtmxSwapMethod = Literal[
    "innerHTML",
    "outerHTML",
    "beforebegin",
    "afterbegin",
    "beforeend",
    "afterend",
    "delete",
    "none",
]

# Tuple of valid HTTP method values
HTTP_METHOD_VALUES: tuple[str, ...] = ("get", "post")

# Type alias for HTTP methods
type HttpMethod = Literal["get", "post"]

# =============================================================================
# Component-Specific Types
# =============================================================================

# Tuple of valid filter field type values (for query builders, model filters, etc.)
FILTER_FIELD_TYPE_VALUES: tuple[str, ...] = ("text", "number", "date", "datetime", "time", "boolean", "choice")

# Type alias for filter field types
type FilterFieldType = Literal["text", "number", "date", "datetime", "time", "boolean", "choice"]

# Tuple of valid values for combining query builder filters
QUERY_LOGIC_VALUES: tuple[str, ...] = ("AND", "OR")

# Type alias for combining query builder filters
type QueryLogic = Literal["AND", "OR"]

# Tuple of valid geo map marker type values
GEO_MAP_MARKER_TYPE_VALUES: tuple[str, ...] = ("marker", "circle")

# Type alias for geo map marker types
type GeoMapMarkerType = Literal["marker", "circle"]

# Tuple of valid slider legend mode values
SLIDER_LEGEND_MODE_VALUES: tuple[str, ...] = ("static", "skip", "rotate")

# Type alias for slider legend modes
type SliderLegendMode = Literal["static", "skip", "rotate"]

# Tuple of valid toggle view type values
TOGGLE_VIEW_TYPE_VALUES: tuple[str, ...] = ("card", "table", "carousel")

# Type alias for toggle view types
type ToggleViewType = Literal["card", "table", "carousel"]


# =============================================================================
# Validation Functions
# =============================================================================


def _validate_literal(value: str, allowed: tuple[str, ...], field_name: str) -> None:
    """Validate that a value is one of the allowed values.

    Args:
        value: The value to validate.
        allowed: Tuple of allowed values.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not in the allowed values.

    """
    if value not in allowed:
        raise ValueError(  # noqa: TRY003
            f"Invalid {field_name} '{value}'. Allowed values are: {', '.join(repr(s) for s in allowed)}"
        )


def validate_not_empty(config: object, *field_names: str) -> None:
    """Validate that fields which identify or locate a component are not empty.

    An empty ID, name or URL renders without error but breaks the component, e.g. duplicate
    element IDs, form values that are never submitted or HTMX requests to the current page.

    Args:
        config: The config instance to check.
        *field_names: Names of the fields that must not be empty or None.

    Raises:
        ValueError: If one of the fields is empty or None.

    """
    for field_name in field_names:
        if not getattr(config, field_name):
            raise ValueError(f"{config.__class__.__name__} requires a non-empty {field_name}.")  # noqa: TRY003


def validate_heading_level(value: int, field_name: str = "heading_level") -> None:
    """Validate that a heading level is between 2 and 6.

    Args:
        value: The heading level to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid heading level.

    """
    if value not in HEADING_LEVEL_VALUES:
        raise ValueError(  # noqa: TRY003
            f"Invalid {field_name} {value!r}. Allowed values are: {', '.join(map(str, HEADING_LEVEL_VALUES))}"
        )


def validate_size(value: str, field_name: str = "size") -> None:
    """Validate that a size value is one of the allowed sizes.

    Args:
        value: The size value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid size.

    """
    _validate_literal(value, SIZE_VALUES, field_name)


def validate_color_type(value: str, field_name: str = "color") -> None:
    """Validate that a color type value is one of the allowed types.

    Args:
        value: The color type value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid color type.

    """
    _validate_literal(value, COLOR_TYPE_VALUES, field_name)


def validate_button_color(value: str, field_name: str = "color") -> None:
    """Validate that a button color is one of the allowed colors.

    Args:
        value: The button color to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid button color.

    """
    if value == "neutral":
        raise ValueError(  # noqa: TRY003
            f"Invalid {field_name} 'neutral'. Use color='light' on dark or colored surfaces, "
            "or variant='plain' for an icon button in the text color."
        )
    _validate_literal(value, BUTTON_COLOR_VALUES, field_name)


def validate_button_variant(value: str, field_name: str = "variant") -> None:
    """Validate that a button variant is one of the allowed variants.

    Args:
        value: The button variant to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid button variant.

    """
    _validate_literal(value, BUTTON_VARIANT_VALUES, field_name)


def validate_control_variant(value: str, field_name: str = "variant") -> None:
    """Validate that a toggle button or radio block variant is one of the allowed variants.

    Args:
        value: The control variant to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid control variant.

    """
    _validate_literal(value, CONTROL_VARIANT_VALUES, field_name)


def validate_step_status(value: str, field_name: str = "status") -> None:
    """Validate that a step status value is one of the allowed values.

    Args:
        value: The step status value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid step status.

    """
    _validate_literal(value, STEP_STATUS_VALUES, field_name)


def validate_severity(value: str, field_name: str = "severity") -> None:
    """Validate that a severity value is one of the allowed values.

    Args:
        value: The severity value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid severity.

    """
    if value == "danger":
        raise ValueError(  # noqa: TRY003
            f"Invalid {field_name} 'danger'. Allowed values are: "
            f"{', '.join(repr(s) for s in SEVERITY_VALUES)}. Use 'error': the severity says what happened, "
            "'danger' is the color name."
        )
    _validate_literal(value, SEVERITY_VALUES, field_name)


def validate_html_button_type(value: str, field_name: str = "button_type") -> None:
    """Validate that an HTML button type value is one of the allowed values.

    Args:
        value: The HTML button type value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid HTML button type.

    """
    _validate_literal(value, HTML_BUTTON_TYPE_VALUES, field_name)


def validate_corner_position(value: str, field_name: str = "position") -> None:
    """Validate that a corner position value is one of the allowed values.

    Args:
        value: The corner position value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid corner position.

    """
    _validate_literal(value, CORNER_POSITION_VALUES, field_name)


def validate_inline_position(value: str, field_name: str = "position") -> None:
    """Validate that an inline position value is one of the allowed values.

    Args:
        value: The inline position value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid inline position.

    """
    _validate_literal(value, INLINE_POSITION_VALUES, field_name)


def validate_filter_field_type(value: str, field_name: str = "type") -> None:
    """Validate that a filter field type value is one of the allowed values.

    Args:
        value: The filter field type value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid filter field type.

    """
    _validate_literal(value, FILTER_FIELD_TYPE_VALUES, field_name)


def validate_query_logic(value: str, field_name: str = "logic") -> None:
    """Validate that a query builder logic value is one of the allowed values.

    Args:
        value: The logic value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid logic value.

    """
    _validate_literal(value, QUERY_LOGIC_VALUES, field_name)


def validate_html_input_type(value: str, field_name: str = "input_type") -> None:
    """Validate that an HTML input type value is one of the allowed values.

    Args:
        value: The HTML input type value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid HTML input type.

    """
    _validate_literal(value, HTML_INPUT_TYPE_VALUES, field_name)


def validate_htmx_swap_method(value: str, field_name: str = "swap_method") -> None:
    """Validate that an HTMX swap method value is one of the allowed values.

    Args:
        value: The HTMX swap method value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid HTMX swap method.

    """
    _validate_literal(value, HTMX_SWAP_METHOD_VALUES, field_name)


def validate_http_method(value: str, field_name: str = "method") -> None:
    """Validate that an HTTP method value is one of the allowed values.

    Args:
        value: The HTTP method value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid HTTP method.

    """
    _validate_literal(value, HTTP_METHOD_VALUES, field_name)


def validate_geo_map_marker_type(value: str, field_name: str = "type") -> None:
    """Validate that a geo map marker type value is one of the allowed values.

    Args:
        value: The geo map marker type value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid geo map marker type.

    """
    _validate_literal(value, GEO_MAP_MARKER_TYPE_VALUES, field_name)


def validate_slider_legend_mode(value: str, field_name: str = "legend_mode") -> None:
    """Validate that a slider legend mode value is one of the allowed values.

    Args:
        value: The slider legend mode value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid slider legend mode.

    """
    _validate_literal(value, SLIDER_LEGEND_MODE_VALUES, field_name)


def validate_toggle_view_type(value: str, field_name: str = "current_view") -> None:
    """Validate that a toggle view type value is one of the allowed values.

    Args:
        value: The toggle view type value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid toggle view type.

    """
    _validate_literal(value, TOGGLE_VIEW_TYPE_VALUES, field_name)


def validate_icon_color(value: str, field_name: str = "color") -> None:
    """Validate that an icon color value is one of the allowed values.

    Args:
        value: The icon color value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid icon color.

    """
    _validate_literal(value, ICON_COLOR_VALUES, field_name)


@lru_cache(maxsize=1)
def _get_available_icon_names() -> tuple[str, ...] | None:
    """Get all available icon names from the compiled icons.html template.

    Parses the icons.html template to extract all icon names that are
    actually available, including any custom icons added via compile_icons.

    Returns:
        Tuple of available icon names, or None if Django is not configured.

    """
    import re  # noqa: PLC0415
    from pathlib import Path  # noqa: PLC0415

    import django  # noqa: PLC0415

    if not django.apps.apps.ready:
        return None

    from django.template.loader import get_template  # noqa: PLC0415

    try:
        template = get_template("insight_ui/components/icons.html")
        template_path = Path(template.origin.name)
        template_content = template_path.read_text(encoding="utf-8")

        # Match icon names from: icon_config.name == "name"
        icon_names = re.findall(r'icon_config\.name == "([^"]+)"', template_content)
        return tuple(sorted(set(icon_names)))
    except (OSError, AttributeError, django.template.TemplateDoesNotExist):
        return None


def validate_icon_name(value: str) -> None:
    """Validate that an icon name exists in the available icons.

    Parses the compiled icons.html template to check if the icon exists.
    If Django is not configured yet, validation is skipped.

    Args:
        value: The icon name to validate.

    Raises:
        ValueError: If the icon name is not found, with suggestions for similar names.

    """
    available_icons = _get_available_icon_names()

    # Skip validation if Django is not configured (e.g., during import)
    if available_icons is None:
        return

    if value in available_icons:
        return

    # Find similar icon names for helpful error message
    suggestions = get_close_matches(value, available_icons, n=3, cutoff=0.5)

    if suggestions:
        suggestion_text = ", ".join(f"'{s}'" for s in suggestions)
        msg = f"Unknown icon '{value}'. Did you mean: {suggestion_text}?"
    else:
        msg = f"Unknown icon '{value}'. Use `python manage.py compile_icons --list-bundled` to see available icons."

    raise ValueError(msg)


# =============================================================================
# Type Registry for Documentation
# =============================================================================
# Single source of truth for type documentation. The documentation app imports
# this directly instead of maintaining a separate registry.
#
# Each entry contains:
#   - values: Tuple of allowed values (references the *_VALUES constant)
#   - description: Human-readable description for documentation

TYPE_REGISTRY: dict[str, dict] = {
    "Severity": {
        "values": SEVERITY_VALUES,
        "description": "Message severity of alerts, infoboxes and status screens.",
    },
    "ButtonColor": {
        "values": BUTTON_COLOR_VALUES,
        "description": "Button colors; 'light' is for dark or colored surfaces.",
    },
    "ControlVariant": {
        "values": CONTROL_VARIANT_VALUES,
        "description": "Visual style of toggle buttons and radio blocks; 'neutral' ignores the color.",
    },
    "ButtonVariant": {
        "values": BUTTON_VARIANT_VALUES,
        "description": "Visual style of buttons; 'link' and 'plain' ignore the color.",
    },
    "ColorType": {
        "values": COLOR_TYPE_VALUES,
        "description": "Base color palette for semantic coloring of components.",
    },
    "CornerPosition": {
        "values": CORNER_POSITION_VALUES,
        "description": "Corner positions for ribbons, badges, and overlays.",
    },
    "FilterFieldType": {
        "values": FILTER_FIELD_TYPE_VALUES,
        "description": "Field types for query builder and filter components.",
    },
    "GeoMapMarkerType": {
        "values": GEO_MAP_MARKER_TYPE_VALUES,
        "description": "Marker types for the geo map component.",
    },
    "HtmlButtonType": {
        "values": HTML_BUTTON_TYPE_VALUES,
        "description": "Native HTML button type attribute values.",
    },
    "HtmlInputType": {
        "values": HTML_INPUT_TYPE_VALUES,
        "description": "Native HTML input type attribute values.",
    },
    "HttpMethod": {
        "values": HTTP_METHOD_VALUES,
        "description": "HTTP methods for requests.",
    },
    "HtmxSwapMethod": {
        "values": HTMX_SWAP_METHOD_VALUES,
        "description": "HTMX swap methods for content replacement.",
    },
    "IconColor": {
        "values": ICON_COLOR_VALUES,
        "description": "Color tokens for icons (semantic colors and text colors).",
    },
    "InlinePosition": {
        "values": INLINE_POSITION_VALUES,
        "description": "Inline positions respecting text direction (RTL-aware).",
    },
    "HeadingLevel": {
        "values": HEADING_LEVEL_VALUES,
        "description": "Heading level of component titles; h1 is reserved for the page title.",
    },
    "QueryLogic": {
        "values": QUERY_LOGIC_VALUES,
        "description": "Combination of a query builder filter with the previous one.",
    },
    "Size": {
        "values": SIZE_VALUES,
        "description": "Standard size scale used for spacing, icons, and component dimensions.",
    },
    "SliderLegendMode": {
        "values": SLIDER_LEGEND_MODE_VALUES,
        "description": "Legend display modes for the range slider component.",
    },
    "StepStatus": {
        "values": STEP_STATUS_VALUES,
        "description": "Status values for stepper components indicating step progress.",
    },
    "ToggleViewType": {
        "values": TOGGLE_VIEW_TYPE_VALUES,
        "description": "View types for the toggle view component.",
    },
}
