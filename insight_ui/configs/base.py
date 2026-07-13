"""Base configuration classes shared across multiple components."""

from dataclasses import dataclass, field
from typing import Any, Literal

from django.utils.translation import gettext_lazy as _

# Tuple of valid size values for runtime validation
SIZE_VALUES: tuple[str, ...] = ("xs", "s", "m", "l", "xl")

# Type alias for component sizes
type Size = Literal["xs", "s", "m", "l", "xl"]

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

# Tuple of valid step status values (for stepper components)
STEP_STATUS_VALUES: tuple[str, ...] = ("active", "success", "failed", "")

# Type alias for step status
type StepStatus = Literal["active", "success", "failed", ""]

# Tuple of valid alert/notification type values
ALERT_TYPE_VALUES: tuple[str, ...] = ("info", "success", "warning", "error")

# Type alias for alert/notification types
type AlertType = Literal["info", "success", "warning", "error"]

# Tuple of valid HTML button type values (native <button> type attribute)
HTML_BUTTON_TYPE_VALUES: tuple[str, ...] = ("button", "submit", "reset")

# Type alias for HTML button types
type HtmlButtonType = Literal["button", "submit", "reset"]

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

# Tuple of valid filter field type values (for query builders, model filters, etc.)
FILTER_FIELD_TYPE_VALUES: tuple[str, ...] = ("text", "number", "date", "datetime", "time", "boolean", "choice")

# Type alias for filter field types
type FilterFieldType = Literal["text", "number", "date", "datetime", "time", "boolean", "choice"]

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


@dataclass
class DataAttrConfig:
    """Configuration for a custom data attribute.

    Attributes:
        name: Attribute name without 'data-' prefix.
        value: Attribute value. Empty string for marker attributes.

    """

    __example__ = """
        DataAttrConfig(name="testid", value="submit-btn")
        DataAttrConfig(name="progress-retry", value="")
        """

    name: str = field(default="", metadata={"doc": _("Attribute name without 'data-' prefix.")})
    value: str = field(default="", metadata={"doc": _("Attribute value. Empty string for marker attributes.")})


@dataclass
class IconConfig:
    """Configuration for an icon.

    Attributes:
        name: Name of the Insight UI icon.
        size: Icon size: 'xl', 'l', 'm', 's', or 'xs'.
        color: Color Hex-Code of the icon.

    """

    __example__ = """
        IconConfig(name="home", size="s", color="#123456")
        """

    name: str = field(metadata={"doc": _("Name of the Insight UI icon.")})
    size: Size = field(default="m", metadata={"doc": _("Icon size: 'xl', 'l', 'm', 's', or 'xs'.")})
    color: str = field(default="", metadata={"doc": _("Color Hex-Code of the icon.")})

    def __post_init__(self) -> None:
        """Validate size after initialization."""
        validate_size(self.size, "size")


@dataclass
class ImageConfig:
    """Configuration for an image element.

    Attributes:
        url: Static, absolute, root-relative, or data URL for the image.
        alt: Accessible text. Empty values make the image decorative.
        url_dark: Optional dark-theme URL.
        height: CSS height value (e.g., '2rem', '100px').
        width: Optional CSS width value.

    """

    __example__ = """
        ImageConfig(
            url="img/logo.png",
            alt="Company Logo",
            height="3rem",
        )
        """

    url: str = field(metadata={"doc": _("Static, absolute, root-relative, or data URL for the image.")})
    alt: str = field(default="", metadata={"doc": _("Accessible text. Empty values make the image decorative.")})
    url_dark: str | None = field(default=None, metadata={"doc": _("Optional dark-theme URL.")})
    height: str | None = field(default=None, metadata={"doc": _("CSS height value (e.g., '2rem', '100px').")})
    width: str | None = field(default=None, metadata={"doc": _("Optional CSS width value.")})


@dataclass
class HtmxConfig:
    """Configuration for HTMX attributes.

    Attributes:
        request_url: The URL for the HTMX request (hx-get/hx-post).
        target: CSS selector for the target element (hx-target).
        swap_method: The way in which the target is to be replaced (hx-swap).
        trigger: Event trigger (hx-trigger).
        method: HTTP method ('get' or 'post').
        loading_indicator_id: CSS selector for loading indicator (hx-indicator).
        push_url: Whether to push URL to browser history (hx-push-url).
        confirm: Confirmation message before request (hx-confirm).
        vals: Additional values to include in request (hx-vals).

    """

    __example__ = """
        HtmxConfig(
            request_url="/api/search/",
            target="#results",
            swap_method="innerHTML",
            trigger="keyup changed delay:300ms",
        )
        """

    request_url: str = field(default="", metadata={"doc": _("The URL for the HTMX request (hx-get/hx-post).")})
    target: str = field(default="", metadata={"doc": _("CSS selector for the target element (hx-target).")})
    swap_method: HtmxSwapMethod = field(
        default="innerHTML", metadata={"doc": _("The way in which the target is to be replaced (hx-swap).")}
    )
    trigger: str = field(default="submit", metadata={"doc": _("Event trigger (hx-trigger).")})
    method: HtmxMethod = field(default="get", metadata={"doc": _("HTTP method ('get' or 'post').")})
    loading_indicator_id: str = field(
        default="", metadata={"doc": _("CSS selector for loading indicator (hx-indicator).")}
    )
    push_url: bool = field(default=False, metadata={"doc": _("Whether to push URL to browser history (hx-push-url).")})
    confirm: str = field(default="", metadata={"doc": _("Confirmation message before request (hx-confirm).")})
    vals: dict[str, Any] = field(
        default_factory=dict, metadata={"doc": _("Additional values to include in request (hx-vals).")}
    )

    def __post_init__(self) -> None:
        """Validate swap_method and method after initialization."""
        validate_htmx_swap_method(self.swap_method, "swap_method")
        validate_htmx_method(self.method, "method")


@dataclass
class BaseFormFieldConfig:
    """Base configuration for form field components.

    This is the base class for all form input components (input, textarea,
    checkbox, select, etc.). It contains common attributes shared by all
    form fields.

    Attributes:
        tag_id: Optional, unique tag ID for identifying the element in JavaScript.
        name: Required for a `<form>`, as the name of the request parameter.
        label: A text label displayed above the field.
        disabled: **True** if the field should be disabled.
        required: **True** if the field must be filled in.

    """

    tag_id: str | None = field(
        default=None, metadata={"doc": _("Optional, unique tag ID for identifying the element in JavaScript.")}
    )
    name: str | None = field(
        default=None, metadata={"doc": _("Required for a `<form>`, as the name of the request parameter.")}
    )
    label: str | None = field(default=None, metadata={"doc": _("A text label displayed above the field.")})
    disabled: bool = field(default=False, metadata={"doc": _("**True** if the field should be disabled.")})
    required: bool = field(default=False, metadata={"doc": _("**True** if the field must be filled in.")})
