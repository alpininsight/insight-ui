"""Base configuration classes shared across multiple components."""

from dataclasses import dataclass, field
from typing import Any, Literal

from django.utils.translation import gettext_lazy as _


@dataclass
class DataAttrConfig:
    """
    Configuration for a custom data attribute.

    Attributes
    ----------
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
    """
    Configuration for an icon.

    Attributes
    ----------
        name: Name of the Insight UI icon.
        size: Icon size: 'xl', 'l', 'm', 's', or 'xs'.
        color: Color Hex-Code of the icon.

    """

    __example__ = """
        IconConfig(name="home", size="s", color="#123456")
        """

    name: str = field(metadata={"doc": _("Name of the Insight UI icon.")})
    size: Literal["xs", "s", "m", "l", "xl"] = field(
        default="m", metadata={"doc": _("Icon size: 'xl', 'l', 'm', 's', or 'xs'.")}
    )
    color: str = field(default="", metadata={"doc": _("Color Hex-Code of the icon.")})


@dataclass
class ImageConfig:
    """
    Configuration for an image element.

    Attributes
    ----------
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
    """
    Configuration for HTMX attributes.

    Attributes
    ----------
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
    """
    Base configuration for form field components.

    This is the base class for all form input components (input, textarea,
    checkbox, select, etc.). It contains common attributes shared by all
    form fields.

    Attributes
    ----------
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
