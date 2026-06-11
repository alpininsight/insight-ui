"""Base configuration classes shared across multiple components."""

from dataclasses import dataclass, field
from typing import Any, Literal

from django.utils.translation import gettext_lazy as _


@dataclass
class IconConfig:
    """
    Configuration for an icon.

    Attributes:
        name: Name of the Insight UI icon.
        size: Icon size: 'xl', 'l', 'm', 's', or 'xs'.

    """

    __example__ = """
        IconConfig(name="home", size="s")
        """

    name: str = field(metadata={"doc": _("Name of the Insight UI icon.")})
    size: Literal["xs", "s", "m", "l", "xl"] = field(
        default="m", metadata={"doc": _("Icon size: 'xl', 'l', 'm', 's', or 'xs'.")}
    )


@dataclass
class ImageConfig:
    """
    Configuration for an image element.

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
class ActionConfig:
    """
    Configuration for an action button.

    Used in cards, modals, and other components that have action buttons.

    Attributes:
        text: Button label.
        url: Target URL for link-style actions.
        type: Describes the importance of the button (purely visual): 'primary', 'secondary', 'cancel', or 'danger'.
        onclick: Call a JavaScript function, e.g.: alert('Confirmed!').
        dismiss: Closes the dialog on click.
        icon: Optional icon configuration.

    """

    __example__ = """
        ActionConfig(
            text="Learn more",
            url="/details/",
            type="primary",
        )
        """

    text: str = field(metadata={"doc": _("Button label.")})
    url: str = field(default="", metadata={"doc": _("Target URL for link-style actions.")})
    type: Literal["primary", "secondary", "cancel", "danger"] = field(
        default="primary",
        metadata={
            "doc": _(
                "Describes the importance of the button (purely visual): 'primary', 'secondary', 'cancel', or 'danger'."
            )
        },
    )
    onclick: str | None = field(
        default=None, metadata={"doc": _("Call a JavaScript function, e.g.: alert('Confirmed!').")}
    )
    dismiss: bool = field(default=False, metadata={"doc": _("Closes the dialog on click.")})
    icon: IconConfig | None = field(default=None, metadata={"doc": _("Optional icon configuration.")})


@dataclass
class HtmxConfig:
    """
    Configuration for HTMX attributes.

    Attributes:
        url: The URL for the HTMX request (hx-get/hx-post).
        target: CSS selector for the target element (hx-target).
        swap: The way in which the target is to be replaced (hx-swap).
        trigger: Event trigger (hx-trigger).
        method: HTTP method ('get' or 'post').
        indicator: CSS selector for loading indicator.
        push_url: Whether to push URL to browser history.
        confirm: Confirmation message before request.
        vals: Additional values to include in request.

    """

    __example__ = """
        HtmxConfig(
            url="/api/search/",
            target="#results",
            swap="innerHTML",
            trigger="keyup changed delay:300ms",
        )
        """

    url: str = field(default="", metadata={"doc": _("The URL for the HTMX request (hx-get/hx-post).")})
    target: str = field(default="", metadata={"doc": _("CSS selector for the target element (hx-target).")})
    swap: Literal["innerHTML", "outerHTML", "beforebegin", "afterbegin", "beforeend", "afterend", "delete", "none"] = (
        field(default="innerHTML", metadata={"doc": _("The way in which the target is to be replaced (hx-swap).")})
    )
    trigger: str = field(default="submit", metadata={"doc": _("Event trigger (hx-trigger).")})
    method: Literal["get", "post"] = field(default="get", metadata={"doc": _("HTTP method ('get' or 'post').")})
    indicator: str = field(default="", metadata={"doc": _("CSS selector for loading indicator.")})
    push_url: bool = field(default=False, metadata={"doc": _("Whether to push URL to browser history.")})
    confirm: str = field(default="", metadata={"doc": _("Confirmation message before request.")})
    vals: dict[str, Any] = field(default_factory=dict, metadata={"doc": _("Additional values to include in request.")})


@dataclass
class BaseFormFieldConfig:
    """
    Base configuration for form field components.

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

    title: str = field(metadata={"doc": _("Card title.")})
    content: str = field(metadata={"doc": _("Main card content.")})
    image: ImageConfig | None = field(default=None, metadata={"doc": _("Optional card image configuration.")})
    actions: list[ActionConfig] = field(default_factory=list, metadata={"doc": _("List of action buttons.")})
