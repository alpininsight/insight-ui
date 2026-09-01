"""Base configuration classes shared across multiple components."""

import warnings
from dataclasses import dataclass, field
from typing import Any

from django.utils.translation import gettext_lazy as _

from insight_ui.configs.types import (
    HtmxMethod,
    HtmxSwapMethod,
    IconColor,
    Size,
    validate_htmx_method,
    validate_htmx_swap_method,
    validate_icon_color,
    validate_size,
)


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
        color: Color token for the icon (e.g., 'primary', 'danger', 'text-secondary').

    """

    __example__ = """
        IconConfig(name="home", size="s", color="primary")
        """

    name: str = field(metadata={"doc": _("Name of the Insight UI icon.")})
    size: Size = field(default="m", metadata={"doc": _("Icon size: 'xl', 'l', 'm', 's', or 'xs'.")})
    color: IconColor = field(
        default="", metadata={"doc": _("Color token for the icon (e.g., 'primary', 'danger', 'text-secondary').")}
    )

    def __post_init__(self) -> None:
        """Validate size and color after initialization."""
        validate_size(self.size, "size")
        validate_icon_color(self.color, "color")


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
        swap_settle: Settle delay appended to hx-swap, e.g. '300ms', so CSS transitions have time to run.
        trigger: Event trigger (hx-trigger).
        method: HTTP method ('get' or 'post').
        loading_indicator_id: CSS selector for loading indicator (hx-indicator).
        push_url: Whether to push URL to browser history (hx-push-url).
        confirm: Confirmation message before request (hx-confirm).
        vals: Additional JSON values to include in the request (hx-vals).

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
    swap_settle: str = field(
        default="",
        metadata={"doc": _("Settle delay appended to hx-swap, e.g. '300ms', so CSS transitions have time to run.")},
    )
    trigger: str = field(default="submit", metadata={"doc": _("Event trigger (hx-trigger).")})
    method: HtmxMethod = field(default="get", metadata={"doc": _("HTTP method ('get' or 'post').")})
    loading_indicator_id: str = field(
        default="", metadata={"doc": _("CSS selector for loading indicator (hx-indicator).")}
    )
    push_url: bool = field(default=False, metadata={"doc": _("Whether to push URL to browser history (hx-push-url).")})
    confirm: str = field(default="", metadata={"doc": _("Confirmation message before request (hx-confirm).")})
    vals: dict[str, Any] = field(
        default_factory=dict, metadata={"doc": _("Additional JSON values to include in the request (hx-vals).")}
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
        disabled_reason: Explanation why the field is disabled, shown as tooltip when hovering. Set to empty string to explicitly skip.
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
    disabled_reason: str | None = field(
        default=None,
        metadata={
            "doc": _(
                "Explanation why the field is disabled, shown as tooltip when hovering. Set to empty string to explicitly skip."
            )
        },
    )
    required: bool = field(default=False, metadata={"doc": _("**True** if the field must be filled in.")})

    def __post_init__(self) -> None:
        """Warn if disabled without a reason."""
        if self.disabled and self.disabled_reason is None:
            identifier = self.name or self.label or self.tag_id or "(unnamed)"
            warnings.warn(
                f"{self.__class__.__name__} {identifier} is disabled without a disabled_reason. "
                "Consider providing a reason to improve accessibility, or set disabled_reason='' to suppress this warning.",
                stacklevel=3,
            )
