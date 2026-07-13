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

from typing import Literal

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

# Tuple of valid badge type values (colors + disabled)
BADGE_TYPE_VALUES: tuple[str, ...] = (*COLOR_TYPE_VALUES, "disabled")

# Type alias for badge types
type BadgeType = Literal["primary", "secondary", "neutral", "info", "success", "warning", "danger", "disabled"]

# Tuple of valid button type values (colors + disabled + link)
BUTTON_TYPE_VALUES: tuple[str, ...] = (*COLOR_TYPE_VALUES, "disabled", "link")

# Type alias for button types
type ButtonType = Literal["primary", "secondary", "neutral", "info", "success", "warning", "danger", "disabled", "link"]

# =============================================================================
# Status Types
# =============================================================================

# Tuple of valid step status values (for stepper components)
STEP_STATUS_VALUES: tuple[str, ...] = ("active", "success", "failed", "")

# Type alias for step status
type StepStatus = Literal["active", "success", "failed", ""]

# Tuple of valid alert/notification type values
ALERT_TYPE_VALUES: tuple[str, ...] = ("info", "success", "warning", "error")

# Type alias for alert/notification types
type AlertType = Literal["info", "success", "warning", "error"]

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

# Tuple of valid form field type values (high-level form abstraction)
FORM_FIELD_TYPE_VALUES: tuple[str, ...] = (
    "text",
    "password",
    "email",
    "number",
    "tel",
    "url",
    "date",
    "textarea",
    "select",
)

# Type alias for form field types
type FormFieldType = Literal[
    "text",
    "password",
    "email",
    "number",
    "tel",
    "url",
    "date",
    "textarea",
    "select",
]

# =============================================================================
# Position Types
# =============================================================================

# Tuple of valid corner position values (for corner ribbons, badges, etc.)
CORNER_POSITION_VALUES: tuple[str, ...] = ("top-right", "top-left", "bottom-right", "bottom-left")

# Type alias for corner positions
type CornerPosition = Literal["top-right", "top-left", "bottom-right", "bottom-left"]

# Tuple of valid horizontal side values (for sidebars, panels, etc.)
HORIZONTAL_SIDE_VALUES: tuple[str, ...] = ("left", "right")

# Type alias for horizontal sides
type HorizontalSide = Literal["left", "right"]

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

# Tuple of valid HTMX HTTP method values
HTMX_METHOD_VALUES: tuple[str, ...] = ("get", "post")

# Type alias for HTMX HTTP methods
type HtmxMethod = Literal["get", "post"]

# =============================================================================
# Component-Specific Types
# =============================================================================

# Tuple of valid filter field type values (for query builders, model filters, etc.)
FILTER_FIELD_TYPE_VALUES: tuple[str, ...] = ("text", "number", "date", "datetime", "time", "boolean", "choice")

# Type alias for filter field types
type FilterFieldType = Literal["text", "number", "date", "datetime", "time", "boolean", "choice"]

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


def validate_size(value: str, field_name: str = "size") -> None:
    """Validate that a size value is one of the allowed sizes.

    Args:
        value: The size value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid size.

    """
    _validate_literal(value, SIZE_VALUES, field_name)


def validate_color_type(value: str, field_name: str = "type") -> None:
    """Validate that a color type value is one of the allowed types.

    Args:
        value: The color type value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid color type.

    """
    _validate_literal(value, COLOR_TYPE_VALUES, field_name)


def validate_badge_type(value: str, field_name: str = "type") -> None:
    """Validate that a badge type value is one of the allowed types.

    Args:
        value: The badge type value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid badge type.

    """
    _validate_literal(value, BADGE_TYPE_VALUES, field_name)


def validate_button_type(value: str, field_name: str = "type") -> None:
    """Validate that a button type value is one of the allowed types.

    Args:
        value: The button type value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid button type.

    """
    _validate_literal(value, BUTTON_TYPE_VALUES, field_name)


def validate_step_status(value: str, field_name: str = "status") -> None:
    """Validate that a step status value is one of the allowed values.

    Args:
        value: The step status value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid step status.

    """
    _validate_literal(value, STEP_STATUS_VALUES, field_name)


def validate_alert_type(value: str, field_name: str = "type") -> None:
    """Validate that an alert type value is one of the allowed values.

    Args:
        value: The alert type value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid alert type.

    """
    _validate_literal(value, ALERT_TYPE_VALUES, field_name)


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


def validate_horizontal_side(value: str, field_name: str = "side") -> None:
    """Validate that a horizontal side value is one of the allowed values.

    Args:
        value: The horizontal side value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid horizontal side.

    """
    _validate_literal(value, HORIZONTAL_SIDE_VALUES, field_name)


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


def validate_html_input_type(value: str, field_name: str = "input_type") -> None:
    """Validate that an HTML input type value is one of the allowed values.

    Args:
        value: The HTML input type value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid HTML input type.

    """
    _validate_literal(value, HTML_INPUT_TYPE_VALUES, field_name)


def validate_form_field_type(value: str, field_name: str = "input_type") -> None:
    """Validate that a form field type value is one of the allowed values.

    Args:
        value: The form field type value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid form field type.

    """
    _validate_literal(value, FORM_FIELD_TYPE_VALUES, field_name)


def validate_htmx_swap_method(value: str, field_name: str = "swap_method") -> None:
    """Validate that an HTMX swap method value is one of the allowed values.

    Args:
        value: The HTMX swap method value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid HTMX swap method.

    """
    _validate_literal(value, HTMX_SWAP_METHOD_VALUES, field_name)


def validate_htmx_method(value: str, field_name: str = "method") -> None:
    """Validate that an HTMX HTTP method value is one of the allowed values.

    Args:
        value: The HTMX HTTP method value to validate.
        field_name: Name of the field for error messages.

    Raises:
        ValueError: If the value is not a valid HTMX HTTP method.

    """
    _validate_literal(value, HTMX_METHOD_VALUES, field_name)


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
