# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Base configuration classes shared across multiple components."""

import re
import warnings
from dataclasses import dataclass, field
from typing import Any

from django.utils.translation import gettext_lazy as _

from insight_ui.configs.types import (
    HtmxSwapMethod,
    HttpMethod,
    IconColor,
    Size,
    validate_htmx_swap_method,
    validate_http_method,
    validate_icon_color,
    validate_icon_name,
    validate_not_empty,
    validate_size,
    validate_urls,
)

# Lowercase words joined by single hyphens; anything else could break out of the attribute name.
_ATTRIBUTE_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


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

    name: str = field(metadata={"doc": _("Attribute name without 'data-' prefix.")})
    value: str = field(default="", metadata={"doc": _("Attribute value. Empty string for marker attributes.")})

    def __post_init__(self) -> None:
        """Reject names that are not a plain attribute name.

        Templates render the name unescaped after ``data-``, ``aria-`` or ``hx-``; a space or ``=`` would
        start a second attribute (e.g. an event handler).

        Raises:
            ValueError: If the name is not lowercase letters and digits joined by single hyphens.

        """
        if not _ATTRIBUTE_NAME.fullmatch(self.name):
            raise ValueError(  # noqa: TRY003
                f"Invalid attribute name {self.name!r}: use lowercase letters and digits joined by single hyphens, "
                "e.g. 'testid' or 'progress-retry'."
            )


# Built-in icons that point along the reading direction; they are mirrored in right-to-left layouts by default.
DIRECTIONAL_ICON_NAMES: frozenset[str] = frozenset(
    {
        "arrow-left",
        "arrow-right",
        "arrow-left-circle",
        "arrow-right-circle",
        "arrow-long-left",
        "arrow-long-right",
        "arrow-small-left",
        "arrow-small-right",
        "arrow-uturn-left",
        "arrow-uturn-right",
        "chevron-left",
        "chevron-right",
        "chevron-double-left",
        "chevron-double-right",
    }
)


@dataclass
class IconConfig:
    """Configuration for an icon.

    Attributes:
        name: Name of the Insight UI icon.
        size: Icon size: 'xl', 'l', 'm', 's', or 'xs'.
        color: Color token for the icon (e.g., 'primary', 'danger', 'text-body').
        mirror_rtl: **True** to mirror the icon in right-to-left layouts, **False** never; unset mirrors built-in arrows.

    """

    __example__ = """
        IconConfig(name="home", size="s", color="primary")
        IconConfig(name="my-custom-arrow", mirror_rtl=True)
        """

    name: str = field(metadata={"doc": _("Name of the Insight UI icon.")})
    size: Size = field(default="m", metadata={"doc": _("Icon size: 'xl', 'l', 'm', 's', or 'xs'.")})
    color: IconColor = field(
        default="", metadata={"doc": _("Color token for the icon (e.g., 'primary', 'danger', 'text-body').")}
    )
    mirror_rtl: bool | None = field(
        default=None,
        metadata={
            "doc": _(
                "**True** to mirror the icon in right-to-left layouts, **False** never; unset mirrors built-in arrows."
            )
        },
    )

    @property
    def mirrors_in_rtl(self) -> bool:
        """Whether the icon is mirrored in right-to-left layouts."""
        return self.name in DIRECTIONAL_ICON_NAMES if self.mirror_rtl is None else self.mirror_rtl

    @property
    def color_class(self) -> str:
        """The text color class of the icon; color families use their -text token, readable in both themes."""
        if not self.color:
            return ""
        if self.color.startswith("text-"):
            return f"text-insight-{self.color}"
        return f"text-insight-{self.color}-text"

    def __post_init__(self) -> None:
        """Validate name, size and color after initialization."""
        validate_icon_name(self.name)
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

    def __post_init__(self) -> None:
        """Reject empty values for fields that identify or locate the component."""
        validate_urls(self)
        validate_not_empty(self, "url")


@dataclass
class HtmxConfig:
    """Request options shared by all components that send HTMX requests.

    How a request is triggered depends on the component, so the trigger is set by the component itself.

    Attributes:
        request_url: The URL for the HTMX request (hx-get/hx-post).
        target: CSS selector for the target element (hx-target).
        swap_method: The way in which the target is to be replaced (hx-swap).
        swap_settle: Settle delay appended to hx-swap, e.g. '300ms', so CSS transitions have time to run.
        method: HTTP method ('get' or 'post').
        loading_indicator_id: CSS selector for loading indicator (hx-indicator).
        push_url: Whether to push URL to browser history (hx-push-url).
        confirm: Confirmation message before request (hx-confirm).
        vals: Additional JSON values to include in the request (hx-vals).
        show_global_loading_indicator: Whether the request shows the global loading bar; None keeps the component default.

    """

    __example__ = """
        HtmxConfig(
            request_url="/api/search/",
            target="#results",
            swap_method="innerHTML",
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
    method: HttpMethod = field(default="get", metadata={"doc": _("HTTP method ('get' or 'post').")})
    loading_indicator_id: str = field(
        default="", metadata={"doc": _("CSS selector for loading indicator (hx-indicator).")}
    )
    push_url: bool = field(default=False, metadata={"doc": _("Whether to push URL to browser history (hx-push-url).")})
    confirm: str = field(default="", metadata={"doc": _("Confirmation message before request (hx-confirm).")})
    vals: dict[str, Any] = field(
        default_factory=dict, metadata={"doc": _("Additional JSON values to include in the request (hx-vals).")}
    )
    show_global_loading_indicator: bool | None = field(
        default=None,
        metadata={"doc": _("Whether the request shows the global loading bar; None keeps the component default.")},
    )

    def __post_init__(self) -> None:
        """Validate swap_method and method after initialization."""
        validate_urls(self)
        validate_htmx_swap_method(self.swap_method, "swap_method")
        validate_http_method(self.method, "method")


@dataclass
class BaseFormFieldConfig:
    """Base configuration for form field components.

    This is the base class for all form input components (input, textarea,
    checkbox, select, etc.). It contains common attributes shared by all
    form fields.

    Attributes:
        name: Required for a `<form>`, as the name of the request parameter.
        tag_id: Optional, unique tag ID for identifying the element in JavaScript.
        label: A text label displayed above the field.
        disabled: **True** if the field should be disabled.
        disabled_reason: Explanation why the field is disabled, shown as visible linked text below the field. Set to empty string to explicitly skip.
        required: **True** if the field must be filled in.
        data_attrs: Custom data attributes for JavaScript hooks or tests.
        help_text: Hint shown below the field.
        error_text: Error message shown below the field; marks the field as invalid.

    """

    name: str = field(metadata={"doc": _("Required for a `<form>`, as the name of the request parameter.")})
    tag_id: str | None = field(
        default=None, metadata={"doc": _("Optional, unique tag ID for identifying the element in JavaScript.")}
    )
    label: str | None = field(default=None, metadata={"doc": _("A text label displayed above the field.")})
    disabled: bool = field(default=False, metadata={"doc": _("**True** if the field should be disabled.")})
    disabled_reason: str | None = field(
        default=None,
        metadata={
            "doc": _(
                "Explanation why the field is disabled, shown as visible linked text below the field. Set to empty string to explicitly skip."
            )
        },
    )
    required: bool = field(default=False, metadata={"doc": _("**True** if the field must be filled in.")})
    data_attrs: list[DataAttrConfig] = field(
        default_factory=list, metadata={"doc": _("Custom data attributes for JavaScript hooks or tests.")}
    )
    help_text: str = field(default="", metadata={"doc": _("Hint shown below the field.")})
    error_text: str = field(
        default="", metadata={"doc": _("Error message shown below the field; marks the field as invalid.")}
    )

    @property
    def field_id(self) -> str:
        """Id of the field: the tag_id, otherwise the name. Label, help and error texts build their ids on it."""
        return self.tag_id or self.name

    def __post_init__(self) -> None:
        """Require a non-empty name and warn if disabled without a reason.

        Raises:
            ValueError: If name is empty or None.

        """
        # Browsers never submit fields without a name.
        validate_not_empty(self, "name")
        if self.disabled and self.disabled_reason is None:
            warnings.warn(
                f"{self.__class__.__name__} {self.name} is disabled without a disabled_reason. "
                "Consider providing a reason to improve accessibility, or set disabled_reason='' to suppress this warning.",
                stacklevel=3,
            )
