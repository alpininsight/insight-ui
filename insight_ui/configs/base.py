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
    swap_method: Literal[
        "innerHTML", "outerHTML", "beforebegin", "afterbegin", "beforeend", "afterend", "delete", "none"
    ] = field(default="innerHTML", metadata={"doc": _("The way in which the target is to be replaced (hx-swap).")})
    trigger: str = field(default="submit", metadata={"doc": _("Event trigger (hx-trigger).")})
    method: Literal["get", "post"] = field(default="get", metadata={"doc": _("HTTP method ('get' or 'post').")})
    loading_indicator_id: str = field(
        default="", metadata={"doc": _("CSS selector for loading indicator (hx-indicator).")}
    )
    push_url: bool = field(default=False, metadata={"doc": _("Whether to push URL to browser history (hx-push-url).")})
    confirm: str = field(default="", metadata={"doc": _("Confirmation message before request (hx-confirm).")})
    vals: dict[str, Any] = field(
        default_factory=dict, metadata={"doc": _("Additional values to include in request (hx-vals).")}
    )


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
