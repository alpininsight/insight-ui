"""Base configuration classes shared across multiple components."""

from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass
class IconConfig:
    """
    Configuration for an icon.

    Attributes:
        name: The icon name from the Insight UI icon set.
        size: Icon size. One of 'xs', 's', 'm', 'l', 'xl'.

    Example:
        >>> icon = IconConfig(name="home", size="s")

    """

    name: str
    size: Literal["xs", "s", "m", "l", "xl"] = "m"


@dataclass
class ImageConfig:
    """
    Configuration for an image element.

    Attributes:
        url: Static path, absolute URL, or data URL for the image.
        alt: Accessible alt text. Empty string marks as decorative.
        url_dark: Optional dark-theme variant URL.
        height: CSS height value (e.g., '2rem', '100px').
        width: Optional CSS width value.

    Example:
        >>> image = ImageConfig(
        ...     url="img/logo.png",
        ...     alt="Company Logo",
        ...     height="3rem",
        ... )

    """

    url: str
    alt: str = ""
    url_dark: str | None = None
    height: str | None = None
    width: str | None = None


@dataclass
class ActionConfig:
    """
    Configuration for an action button.

    Used in cards, modals, and other components that have action buttons.

    Attributes:
        text: Button label text.
        url: Target URL for link-style actions.
        type: Button style variant.
        onclick: JavaScript onclick handler.
        dismiss: If True, clicking dismisses the parent (e.g., modal).
        icon: Optional icon configuration.

    Example:
        >>> action = ActionConfig(
        ...     text="Learn more",
        ...     url="/details/",
        ...     type="primary",
        ... )

    """

    text: str
    url: str = ""
    type: Literal["primary", "secondary", "cancel", "danger"] = "primary"
    onclick: str | None = None
    dismiss: bool = False
    icon: IconConfig | None = None


@dataclass
class HtmxConfig:
    """
    Configuration for HTMX attributes.

    Attributes:
        url: The URL for the HTMX request (hx-get/hx-post).
        target: CSS selector for the target element (hx-target).
        swap: Swap strategy (hx-swap).
        trigger: Event trigger (hx-trigger).
        method: HTTP method ('get' or 'post').
        indicator: CSS selector for loading indicator.
        push_url: Whether to push URL to browser history.
        confirm: Confirmation message before request.
        vals: Additional values to include in request.

    Example:
        >>> htmx = HtmxConfig(
        ...     url="/api/search/",
        ...     target="#results",
        ...     swap="innerHTML",
        ...     trigger="keyup changed delay:300ms",
        ... )

    """

    url: str = ""
    target: str = ""
    swap: Literal["innerHTML", "outerHTML", "beforebegin", "afterbegin", "beforeend", "afterend", "delete", "none"] = (
        "innerHTML"
    )
    trigger: str = "submit"
    method: Literal["get", "post"] = "get"
    indicator: str = ""
    push_url: bool = False
    confirm: str = ""
    vals: dict[str, Any] = field(default_factory=dict)


@dataclass
class BaseFormFieldConfig:
    """
    Base configuration for form field components.

    This is the base class for all form input components (input, textarea,
    checkbox, select, etc.). It contains common attributes shared by all
    form fields.

    Attributes:
        tag_id: Unique ID for JavaScript/CSS targeting.
        name: Form field name (used in request parameters).
        label: Label text displayed above the field.
        disabled: Whether the field is disabled.
        required: Whether the field is required.

    """

    tag_id: str | None = None
    name: str | None = None
    label: str | None = None
    disabled: bool = False
    required: bool = False


@dataclass
class BaseCardConfig:
    """
    Base configuration for card components.

    Shared attributes for card, app_card, and flip_card.

    Attributes:
        title: Card title.
        content: Main card content.
        image: Optional card image configuration.
        actions: List of action buttons.

    """

    title: str
    content: str
    image: ImageConfig | None = None
    actions: list[ActionConfig] = field(default_factory=list)
