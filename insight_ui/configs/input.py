# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Configuration classes for input and control components."""

import warnings
from dataclasses import dataclass, field
from unicodedata import category

from django.utils.translation import gettext_lazy as _

from insight_ui.configs.base import BaseFormFieldConfig, DataAttrConfig, HtmxConfig, IconConfig
from insight_ui.configs.types import (
    ButtonColor,
    ButtonVariant,
    ControlVariant,
    HtmlButtonType,
    HtmlInputType,
    Size,
    SliderLegendMode,
    validate_button_color,
    validate_button_variant,
    validate_control_variant,
    validate_html_button_type,
    validate_html_input_type,
    validate_not_empty,
    validate_size,
    validate_slider_legend_mode,
)


@dataclass
class ButtonConfig:
    """Configuration for the button component.

    Renders a <button>, or an <a> if request_url is set. An htmx without its own request_url
    requests the link URL, so the link also works without JavaScript.

    Attributes:
        label: The text on the button or for Screenreader if the button shows only an icon.
        tag_id: Unique ID for JavaScript/CSS targeting.
        request_url: URL of the link (renders as <a>).
        external: **True** to open the link in a new tab.
        on_click: The name of the JavaScript method to be called when clicking on the button.
        icon: Icon config for an optional icon.
        icon_end: **True** if the icon should be shown after the label, otherwise the icon is shown in front of the label.
        icon_only: **True** if only the icon should be shown. In this case the `label` will be used for Screenreader.
        color: Color of the button.
        variant: Visual style of the button.
        size: Defines the size of the button.
        round: **True** for full rounded corners.
        tooltip: Optional text for a tooltip shown on hover.
        htmx: Configuration for asynchronous requests.
        hidden: **True** to render the button with CSS 'hidden' class for JS-controlled visibility.
        disabled: **True** to disable the button.
        disabled_reason: Explanation why the button is disabled, shown as tooltip when hovering. Set to empty string to explicitly skip.
        button_type: HTML type attribute: 'button', 'submit', or 'reset'.
        extra_classes: Additional CSS classes to append to the button element.
        data_attrs: List of custom data attributes to add to the button element.
        aria_attrs: List of ARIA attributes to add to the button element.
        hx_attrs: List of HTMX attributes to add to the button element.
        download: Lets the browser download the link target; a string suggests the file name.

    """

    __example__ = """
        ButtonConfig(
            tag_id="my-button",
            label="Click Me!",
            request_url="",
            on_click="calculateSomething()",
            icon=IconConfig("rocket-launch", "m"),
            icon_end=True,
            icon_only=False,
            color="primary",
            variant="solid",
            size="xl",
            round=False,
            tooltip="Click to calculate something",
            htmx=HtmxConfig(...),
            hidden=False,
            button_type="submit",
            extra_classes="w-full",
            data_attrs=[DataAttrConfig(name="testid", value="submit-btn")],
        )
        """

    label: str = field(metadata={"doc": "The text on the button or for Screenreader if the button shows only an icon."})
    tag_id: str = field(default="", metadata={"doc": _("Unique ID for JavaScript/CSS targeting.")})
    request_url: str = field(default="", metadata={"doc": "URL of the link (renders as <a>)."})
    external: bool = field(default=False, metadata={"doc": _("**True** to open the link in a new tab.")})
    on_click: str = field(
        default="", metadata={"doc": "The name of the JavaScript method to be called when clicking on the button."}
    )
    icon: IconConfig | None = field(default=None, metadata={"doc": "Icon config for an optional icon."})
    icon_end: bool = field(
        default=False,
        metadata={
            "doc": "**True** if the icon should be shown after the label, otherwise the icon is shown in front of the label."
        },
    )
    icon_only: bool = field(
        default=False,
        metadata={
            "doc": "**True** if only the icon should be shown. In this case the `label` will be used for Screenreader."
        },
    )
    color: ButtonColor = field(default="primary", metadata={"doc": _("Color of the button.")})
    variant: ButtonVariant = field(default="solid", metadata={"doc": _("Visual style of the button.")})
    size: Size = field(default="m", metadata={"doc": "Defines the size of the button."})
    round: bool = field(default=False, metadata={"doc": "**True** for full rounded corners."})
    tooltip: str = field(default="", metadata={"doc": "Optional text for a tooltip shown on hover."})
    htmx: HtmxConfig | None = field(default=None, metadata={"doc": "Configuration for asynchronous requests."})
    hidden: bool = field(
        default=False,
        metadata={"doc": "**True** to render the button with CSS 'hidden' class for JS-controlled visibility."},
    )
    disabled: bool = field(default=False, metadata={"doc": "**True** to disable the button."})
    disabled_reason: str | None = field(
        default=None,
        metadata={
            "doc": "Explanation why the button is disabled, shown as tooltip when hovering. Set to empty string to explicitly skip."
        },
    )
    button_type: HtmlButtonType = field(
        default="button", metadata={"doc": _("HTML type attribute: 'button', 'submit', or 'reset'.")}
    )
    extra_classes: str = field(
        default="", metadata={"doc": _("Additional CSS classes to append to the button element.")}
    )
    data_attrs: list[DataAttrConfig] = field(
        default_factory=list, metadata={"doc": "List of custom data attributes to add to the button element."}
    )
    aria_attrs: list[DataAttrConfig] = field(
        default_factory=list, metadata={"doc": "List of ARIA attributes to add to the button element."}
    )
    hx_attrs: list[DataAttrConfig] = field(
        default_factory=list, metadata={"doc": "List of HTMX attributes to add to the button element."}
    )
    # Append to preserve positional construction of all existing fields.
    download: bool | str = field(
        default=False,
        metadata={"doc": "Lets the browser download the link target; a string suggests the file name."},
    )

    def __post_init__(self) -> None:
        """Require a label, validate the values and reject options that would be silently ignored.

        Raises:
            ValueError: If a value is invalid or an option does not apply to the rendered element.

        """
        # The label is the accessible name, also for icon-only buttons (aria-label).
        validate_not_empty(self, "label")
        if not isinstance(self.download, (bool, str)):
            raise TypeError("ButtonConfig.download must be a bool or a filename string.")  # noqa: TRY003
        if self.download == "":
            self.download = True
        if self.download:
            validate_not_empty(self, "request_url")
            if self.htmx is not None or self.hx_attrs:
                raise ValueError("Native downloads cannot be combined with HTMX request attributes.")  # noqa: TRY003
            if isinstance(self.download, str) and any(category(char) == "Cc" for char in self.download):
                raise ValueError("Download filenames must not contain control characters.")  # noqa: TRY003
        validate_button_color(self.color)
        validate_button_variant(self.variant)
        validate_size(self.size, "size")
        validate_html_button_type(self.button_type, "button_type")
        # A request_url renders an <a>: it has no type or onclick of a button, and without it there is no link.
        if self.external and not self.request_url:
            raise ValueError(f"ButtonConfig {self.label}: external only applies together with request_url.")  # noqa: TRY003
        if self.request_url and (self.on_click or self.button_type != "button"):
            raise ValueError(  # noqa: TRY003
                f"ButtonConfig {self.label}: on_click and button_type only apply to buttons without request_url."
            )
        if self.disabled and self.disabled_reason is None:
            warnings.warn(
                f"ButtonConfig {self.label} is disabled without a disabled_reason. "
                "Consider providing a reason to improve accessibility, or set disabled_reason='' to suppress this warning.",
                stacklevel=2,
            )


@dataclass
class InputFieldConfig(BaseFormFieldConfig):
    """Configuration for the input_field component.

    Renders any HTML <input> element with proper styling and accessibility.

    Attributes:
        tag_id: Optional, unique tag ID for identifying the element in JavaScript.
        name: Required for a `<form>`, as the name of the request parameter.
        label: A text label displayed above the field.
        disabled: **True** if the field should be disabled.
        disabled_reason: Explanation why the field is disabled, shown as visible linked text below the field. Set to empty string to explicitly skip.
        required: **True** if the field must be filled in.
        input_type: The type of the input field, e.g.: 'text', 'password', 'date', etc.
        placeholder: Placeholder text, displayed in the field as long as it has not been selected.
        value: The value of the input field.
        minimum: Smallest numeric value (for `input_type='number'`).
        maximum: Largest numeric value (for `input_type='number'`).
        min_length: Minimum number of characters in a text field.
        max_length: Maximum number of characters in a text field.
        checked: **True** if `input_type='checkbox'` and the checkbox should be selected.
        data_attrs: Custom data attributes for JavaScript hooks or tests.
        help_text: Hint shown below the field.
        error_text: Error message shown below the field; marks the field as invalid.

    """

    __example__ = """
        InputFieldConfig(
            name="email",
            input_type="email",
            label="E-Mail Address",
            placeholder="you@example.com",
            required=True,
        )
        """

    input_type: HtmlInputType = field(
        default="text", metadata={"doc": _("The type of the input field, e.g.: 'text', 'password', 'date', etc.")}
    )
    placeholder: str = field(
        default="", metadata={"doc": _("Placeholder text, displayed in the field as long as it has not been selected.")}
    )
    value: str | int | float | None = field(default=None, metadata={"doc": _("The value of the input field.")})
    minimum: int | None = field(
        default=None, metadata={"doc": _("Smallest numeric value (for `input_type='number'`).")}
    )
    maximum: int | None = field(default=None, metadata={"doc": _("Largest numeric value (for `input_type='number'`).")})
    min_length: int | None = field(default=None, metadata={"doc": _("Minimum number of characters in a text field.")})
    max_length: int | None = field(default=None, metadata={"doc": _("Maximum number of characters in a text field.")})
    checked: bool = field(
        default=False, metadata={"doc": _("**True** if `input_type='checkbox'` and the checkbox should be selected.")}
    )

    def __post_init__(self) -> None:
        """Validate input_type, minimum/maximum, and min_length/max_length after initialization."""
        super().__post_init__()
        validate_html_input_type(self.input_type, "input_type")
        if self.minimum is not None and self.maximum is not None and self.minimum > self.maximum:
            raise ValueError(f"minimum ({self.minimum}) cannot be greater than maximum ({self.maximum})")  # noqa: TRY003
        if self.min_length is not None and self.max_length is not None and self.min_length > self.max_length:
            raise ValueError(  # noqa: TRY003
                f"min_length ({self.min_length}) cannot be greater than max_length ({self.max_length})"
            )


@dataclass
class TextareaConfig(BaseFormFieldConfig):
    """Configuration for the textarea component.

    Renders a multi-line text input field.

    Attributes:
        tag_id: Optional, unique tag ID for identifying the element in JavaScript.
        name: Required for a `<form>`, as the name of the request parameter.
        label: A text label displayed above the field.
        disabled: **True** if the field should be disabled.
        disabled_reason: Explanation why the field is disabled, shown as visible linked text below the field. Set to empty string to explicitly skip.
        required: **True** if the field must be filled in.
        placeholder: Placeholder text, displayed in the field as long as it has not been selected.
        value: The value of the input field.
        rows: Determines the number of lines.
        cols: Determines the number of characters in a line.
        data_attrs: Custom data attributes for JavaScript hooks or tests.
        help_text: Hint shown below the field.
        error_text: Error message shown below the field; marks the field as invalid.

    """

    __example__ = """
        TextareaConfig(
            name="message",
            label="Your Message",
            placeholder="Enter your message here...",
            rows=5,
            required=True,
        )
        """

    placeholder: str = field(
        default="", metadata={"doc": _("Placeholder text, displayed in the field as long as it has not been selected.")}
    )
    value: str = field(default="", metadata={"doc": _("The value of the input field.")})
    rows: int = field(default=3, metadata={"doc": _("Determines the number of lines.")})
    cols: int | None = field(default=None, metadata={"doc": _("Determines the number of characters in a line.")})


@dataclass
class CheckboxConfig(BaseFormFieldConfig):
    """Configuration for the checkbox component.

    Renders a single checkbox with label.

    Attributes:
        tag_id: Optional, unique tag ID for identifying the element in JavaScript.
        name: Required for a `<form>`, as the name of the request parameter.
        label: A text label displayed above the field.
        disabled: **True** if the field should be disabled.
        disabled_reason: Explanation why the field is disabled, shown as visible linked text below the field. Set to empty string to explicitly skip.
        required: **True** if the field must be filled in.
        value: The value of the checkbox (this is not the state, see 'checked' for that).
        checked: **True** if the checkbox should be selected.
        data_attrs: Custom data attributes for JavaScript hooks or tests.
        help_text: Hint shown below the field.
        error_text: Error message shown below the field; marks the field as invalid.

    """

    __example__ = """
        CheckboxConfig(
            tag_id="accept-terms",
            name="accept_terms",
            value="accepted",
            label="I accept the terms and conditions",
        )
        """

    value: str = field(
        default="", metadata={"doc": _("The value of the checkbox (this is not the state, see 'checked' for that).")}
    )
    checked: bool = field(default=False, metadata={"doc": _("**True** if the checkbox should be selected.")})


@dataclass
class CheckboxItemConfig:
    """Configuration for a single checkbox within a checkbox group.

    Attributes:
        tag_id: Unique ID for this checkbox.
        label: Label text.
        value: Value submitted when checked.
        disabled: **True** if the checkbox should be disabled.
        disabled_reason: Explanation why the checkbox is disabled, shown as visible linked text below the option. Set to empty string to explicitly skip.
        checked: **True** if the checkbox should be selected.
        data_attrs: Custom data attributes for JavaScript hooks or tests.

    """

    __example__ = """
        CheckboxItemConfig(tag_id="en", value="english", label="English")
        """

    tag_id: str = field(metadata={"doc": _("Unique ID for this checkbox.")})
    label: str = field(metadata={"doc": _("Label text.")})
    value: str = field(metadata={"doc": _("Value submitted when checked.")})
    disabled: bool = field(default=False, metadata={"doc": _("**True** if the checkbox should be disabled.")})
    disabled_reason: str | None = field(
        default=None,
        metadata={
            "doc": _(
                "Explanation why the checkbox is disabled, shown as visible linked text below the option. Set to empty string to explicitly skip."
            )
        },
    )
    checked: bool = field(default=False, metadata={"doc": _("**True** if the checkbox should be selected.")})
    data_attrs: list[DataAttrConfig] = field(
        default_factory=list, metadata={"doc": _("Custom data attributes for JavaScript hooks or tests.")}
    )

    def __post_init__(self) -> None:
        """Require a tag_id and warn if disabled without a reason."""
        validate_not_empty(self, "tag_id")
        if self.disabled and self.disabled_reason is None:
            identifier = self.label or self.value
            warnings.warn(
                f"CheckboxItemConfig {identifier} is disabled without a disabled_reason. "
                "Consider providing a reason to improve accessibility, or set disabled_reason='' to suppress this warning.",
                stacklevel=2,
            )


@dataclass
class CheckboxGroupConfig:
    """Configuration for the checkbox_group component.

    Renders a group of linked checkboxes with optional constraints.

    Attributes:
        name: Required for a `<form>`, as the name of the request parameter.
        label: Text label displayed above the checkbox elements.
        items: List of the checkbox elements.
        as_row: **True** if the checkbox elements should be displayed side by side.
        minimum_checked: Number of checkbox elements that must be selected at minimum.
        maximum_checked: Number of checkbox elements that may be selected at the same time.
        data_attrs: Custom data attributes for JavaScript hooks or tests.
        help_text: Hint shown below the field.
        error_text: Error message shown below the field; marks the field as invalid.

    """

    __example__ = """
        CheckboxGroupConfig(
            name="languages",
            label="Select languages (max 3):",
            as_row=True,
            maximum_checked=3,
            items=[
                CheckboxItemConfig(tag_id="en", value="english", label="English"),
                CheckboxItemConfig(tag_id="de", value="german", label="German"),
                CheckboxItemConfig(tag_id="fr", value="french", label="French"),
            ],
        )
        """

    name: str = field(metadata={"doc": _("Required for a `<form>`, as the name of the request parameter.")})
    label: str = field(default="", metadata={"doc": _("Text label displayed above the checkbox elements.")})
    items: list[CheckboxItemConfig] = field(default_factory=list, metadata={"doc": _("List of the checkbox elements.")})
    as_row: bool = field(
        default=True, metadata={"doc": _("**True** if the checkbox elements should be displayed side by side.")}
    )
    minimum_checked: int = field(
        default=0, metadata={"doc": _("Number of checkbox elements that must be selected at minimum.")}
    )
    maximum_checked: int | None = field(
        default=None, metadata={"doc": _("Number of checkbox elements that may be selected at the same time.")}
    )
    data_attrs: list[DataAttrConfig] = field(
        default_factory=list, metadata={"doc": _("Custom data attributes for JavaScript hooks or tests.")}
    )
    help_text: str = field(default="", metadata={"doc": _("Hint shown below the field.")})
    error_text: str = field(
        default="", metadata={"doc": _("Error message shown below the field; marks the field as invalid.")}
    )

    def __post_init__(self) -> None:
        """Require a non-empty name and validate that minimum_checked does not exceed maximum_checked."""
        validate_not_empty(self, "name")
        if self.maximum_checked is not None and self.minimum_checked > self.maximum_checked:
            raise ValueError(  # noqa: TRY003
                f"minimum_checked ({self.minimum_checked}) cannot be greater than maximum_checked ({self.maximum_checked})"
            )


@dataclass
class DropdownItemConfig:
    """Configuration for an item within a dropdown menu.

    Attributes:
        text: Label of the dropdown element.
        request_url: The URL to be called when clicking on the respective item.
        icon: An optional icon displayed before the label.
        htmx: Optional HTMX configuration for dynamic content loading.

    """

    __example__ = """
        DropdownItemConfig(text="Profile", request_url="/profile/", icon=IconConfig(name="user"))
        DropdownItemConfig(
            text="Dashboard",
            request_url="/dashboard/",
            htmx=HtmxConfig(target="#content", push_url=True),
        )
        """

    text: str = field(metadata={"doc": _("Label of the dropdown element.")})
    request_url: str = field(metadata={"doc": _("The URL to be called when clicking on the respective item.")})
    icon: IconConfig | None = field(default=None, metadata={"doc": _("An optional icon displayed before the label.")})
    htmx: HtmxConfig | None = field(
        default=None, metadata={"doc": _("Optional HTMX configuration for dynamic content loading.")}
    )

    def __post_init__(self) -> None:
        """Reject empty values for fields that identify or locate the component."""
        validate_not_empty(self, "request_url")


@dataclass
class DropdownConfig:
    """Configuration for the dropdown component.

    Renders a dropdown menu with a trigger button.

    Attributes:
        tag_id: Unique tag ID for identifying the element in JavaScript. Required to open/close the dropdown.
        title: Label of the dropdown button.
        show_arrow: **True** displays an arrow behind the title.
        items: A list of the menu elements.
        color: Color of the dropdown button.
        variant: Visual style of the dropdown button.

    """

    __example__ = """
        DropdownConfig(
            tag_id="user-dropdown",
            title="Account",
            show_arrow=True,
            items=[
                DropdownItemConfig(text="Profile", request_url="/profile/", icon=IconConfig(name="user")),
                DropdownItemConfig(text="Settings", request_url="/settings/", icon=IconConfig(name="cog-8-tooth")),
                DropdownItemConfig(text="Logout", request_url="/logout/", icon=IconConfig(name="arrow-left-on-rectangle")),
            ],
        )
        """

    tag_id: str = field(
        metadata={
            "doc": _("Unique tag ID for identifying the element in JavaScript. Required to open/close the dropdown.")
        }
    )
    title: str = field(metadata={"doc": _("Label of the dropdown button.")})
    show_arrow: bool = field(default=True, metadata={"doc": _("**True** displays an arrow behind the title.")})
    items: list[DropdownItemConfig] = field(default_factory=list, metadata={"doc": _("A list of the menu elements.")})
    color: ButtonColor = field(default="primary", metadata={"doc": _("Color of the dropdown button.")})
    variant: ButtonVariant = field(default="solid", metadata={"doc": _("Visual style of the dropdown button.")})

    def __post_init__(self) -> None:
        """Reject empty values for fields that identify or locate the component and validate the button look."""
        validate_not_empty(self, "tag_id")
        validate_button_color(self.color)
        validate_button_variant(self.variant)


@dataclass
class RadioItemConfig:
    """Configuration for a single radio button within a group.

    Attributes:
        value: Value of the respective radio button.
        tag_id: Optional, unique tag ID for identifying the element in JavaScript.
        label: Label of the respective radio button.
        icon: Optional icon displayed before the label.
        disabled: **True** if the radio button should be disabled.
        disabled_reason: Explanation why the radio button is disabled, shown as visible linked text below the option. Set to empty string to explicitly skip.
        data_attrs: Custom data attributes for JavaScript hooks or tests.

    """

    __example__ = """
        RadioItemConfig(value="gpt-4", tag_id="gpt4", label="GPT-4")
        """

    value: str = field(metadata={"doc": _("Value of the respective radio button.")})
    tag_id: str = field(
        default="", metadata={"doc": _("Optional, unique tag ID for identifying the element in JavaScript.")}
    )
    label: str = field(default="", metadata={"doc": _("Label of the respective radio button.")})
    icon: IconConfig | None = field(default=None, metadata={"doc": _("Optional icon displayed before the label.")})
    disabled: bool = field(default=False, metadata={"doc": _("**True** if the radio button should be disabled.")})
    disabled_reason: str | None = field(
        default=None,
        metadata={
            "doc": _(
                "Explanation why the radio button is disabled, shown as visible linked text below the option. Set to empty string to explicitly skip."
            )
        },
    )
    data_attrs: list[DataAttrConfig] = field(
        default_factory=list, metadata={"doc": _("Custom data attributes for JavaScript hooks or tests.")}
    )

    def __post_init__(self) -> None:
        """Warn if disabled without a reason."""
        if self.disabled and self.disabled_reason is None:
            identifier = self.label or self.value
            warnings.warn(
                f"RadioItemConfig {identifier} is disabled without a disabled_reason. "
                "Consider providing a reason to improve accessibility, or set disabled_reason='' to suppress this warning.",
                stacklevel=2,
            )


@dataclass
class RadioGroupConfig:
    """Configuration for the radio_group component.

    Renders a group of standard radio buttons.

    Attributes:
        name: The shared HTML `name` attribute for all radio buttons in this group.
        label: A text label displayed above the radio elements.
        items: A list of the radio elements.
        as_row: **True** if the radio elements should be displayed side by side.
        current_value: The value of the currently selected radio button.
        data_attrs: Custom data attributes for JavaScript hooks or tests.
        help_text: Hint shown below the field.
        error_text: Error message shown below the field; marks the field as invalid.

    """

    __example__ = """
        RadioGroupConfig(
            name="model",
            label="Select AI Model:",
            items=[
                RadioItemConfig(tag_id="gpt4", value="gpt-4", label="GPT-4"),
                RadioItemConfig(tag_id="claude", value="claude", label="Claude"),
                RadioItemConfig(tag_id="llama", value="llama", label="LLaMA", disabled=True),
            ],
            current_value="claude",
        )
        """

    name: str = field(metadata={"doc": _("The shared HTML `name` attribute for all radio buttons in this group.")})
    label: str = field(default="", metadata={"doc": _("A text label displayed above the radio elements.")})
    items: list[RadioItemConfig] = field(default_factory=list, metadata={"doc": _("A list of the radio elements.")})
    as_row: bool = field(
        default=True, metadata={"doc": _("**True** if the radio elements should be displayed side by side.")}
    )
    current_value: str = field(default="", metadata={"doc": _("The value of the currently selected radio button.")})
    data_attrs: list[DataAttrConfig] = field(
        default_factory=list, metadata={"doc": _("Custom data attributes for JavaScript hooks or tests.")}
    )
    help_text: str = field(default="", metadata={"doc": _("Hint shown below the field.")})
    error_text: str = field(
        default="", metadata={"doc": _("Error message shown below the field; marks the field as invalid.")}
    )

    def __post_init__(self) -> None:
        """Require a non-empty name, set first option for current_value if empty, and validate it against items."""
        validate_not_empty(self, "name")
        if not self.current_value and self.items:
            self.current_value = self.items[0].value
        elif self.items and self.current_value not in (item.value for item in self.items):
            raise ValueError(f"current_value '{self.current_value}' must match one of the items' values.")  # noqa: TRY003


@dataclass
class RadioBlockConfig:
    """Configuration for the radio_block component.

    Renders radio buttons as a compact block that can trigger requests.

    Attributes:
        name: The shared HTML `name` attribute for all radio buttons in this group.
        label: A text label displayed above the radio elements.
        items: A list of the radio elements.
        integrated: **True** if the group is inside a `<form>`. If **False** the group gets its own `<form>`.
        as_row: **True** if the radio elements should be displayed side by side.
        request_url: The URL to which the request should be sent when clicking one of the radio buttons.
        htmx: HTMX configuration; the radio buttons send their value to request_url and swap htmx.target.
        method: Name of the JavaScript method to be executed when clicking one of the radio buttons.
        current_value: The value of the currently selected radio button.
        variant: Visual style of the options.
        color: Color of the options; ignored by the neutral variant.
        data_attrs: Custom data attributes for JavaScript hooks or tests.
        help_text: Hint shown below the field.
        error_text: Error message shown below the field; marks the field as invalid.

    """

    __example__ = """
        RadioBlockConfig(
            name="view",
            items=[
                RadioItemConfig(tag_id="card", value="card", icon=IconConfig(name="squares-2x2")),
                RadioItemConfig(tag_id="table", value="table", icon=IconConfig(name="list-bullet")),
            ],
            current_value="card",
            request_url="/products/",
            htmx=HtmxConfig(target="#content-area", swap_method="outerHTML"),
        )
        """

    name: str = field(metadata={"doc": _("The shared HTML `name` attribute for all radio buttons in this group.")})
    label: str = field(default="", metadata={"doc": _("A text label displayed above the radio elements.")})
    items: list[RadioItemConfig] = field(default_factory=list, metadata={"doc": _("A list of the radio elements.")})
    integrated: bool = field(
        default=False,
        metadata={
            "doc": _("**True** if the group is inside a `<form>`. If **False** the group gets its own `<form>`.")
        },
    )
    as_row: bool = field(
        default=True, metadata={"doc": _("**True** if the radio elements should be displayed side by side.")}
    )
    request_url: str = field(
        default="",
        metadata={"doc": _("The URL to which the request should be sent when clicking one of the radio buttons.")},
    )
    htmx: HtmxConfig | None = field(
        default=None,
        metadata={
            "doc": _("HTMX configuration; the radio buttons send their value to request_url and swap htmx.target.")
        },
    )
    method: str = field(
        default="",
        metadata={"doc": _("Name of the JavaScript method to be executed when clicking one of the radio buttons.")},
    )
    current_value: str = field(default="", metadata={"doc": _("The value of the currently selected radio button.")})
    variant: ControlVariant = field(default="neutral", metadata={"doc": _("Visual style of the options.")})
    color: ButtonColor = field(
        default="primary", metadata={"doc": _("Color of the options; ignored by the neutral variant.")}
    )
    data_attrs: list[DataAttrConfig] = field(
        default_factory=list, metadata={"doc": _("Custom data attributes for JavaScript hooks or tests.")}
    )
    help_text: str = field(default="", metadata={"doc": _("Hint shown below the field.")})
    error_text: str = field(
        default="", metadata={"doc": _("Error message shown below the field; marks the field as invalid.")}
    )

    def __post_init__(self) -> None:
        """Require a non-empty name, reject HTMX options that would be ignored and validate the values."""
        validate_not_empty(self, "name")
        validate_control_variant(self.variant)
        validate_button_color(self.color)
        if self.htmx is not None:
            if self.integrated:
                msg = (
                    f"RadioBlockConfig {self.name!r}: integrated radio blocks are sent with their form, not with htmx."
                )
                raise ValueError(msg)
            if not (self.request_url or self.htmx.request_url):
                msg = f"RadioBlockConfig {self.name!r} with htmx needs a request_url."
                raise ValueError(msg)
            if not self.htmx.target:
                msg = f"RadioBlockConfig {self.name!r} with htmx needs htmx.target, otherwise the radio button is swapped."
                raise ValueError(msg)
        if not self.current_value and self.items:
            self.current_value = self.items[0].value
        elif self.items and self.current_value not in (item.value for item in self.items):
            raise ValueError(f"current_value '{self.current_value}' must match one of the items' values.")  # noqa: TRY003


@dataclass
class SliderConfig(BaseFormFieldConfig):
    """Configuration for the slider (range slider) component.

    Renders a range slider for selecting numeric values.

    Attributes:
        tag_id: Optional, unique tag ID for identifying the element in JavaScript.
        name: Required for a `<form>`, as the name of the request parameter.
        label: A text label displayed above the field.
        disabled: **True** if the field should be disabled.
        disabled_reason: Explanation why the field is disabled, shown as visible linked text below the field. Set to empty string to explicitly skip.
        required: **True** if the field must be filled in.
        value: The value of the range slider (single-thumb mode only).
        minimum: Smallest configurable value of the range slider.
        maximum: Largest configurable value of the range slider.
        step_size: The size of the steps by which the value changes when moving the range slider.
        items: A list of texts displayed as a legend below the slider.
        legend_mode: Controls responsive legend behavior. Options: **'static'** (default) - no adjustment; **'skip'** - progressively hides legend items when space is limited; **'rotate'** - rotates legend text vertically when space is limited.
        dual: **True** to enable dual-thumb mode for selecting a range with min and max values.
        value_min: The minimum value in dual-thumb mode. Defaults to `minimum`.
        value_max: The maximum value in dual-thumb mode. Defaults to `maximum`.
        color: Color of the filled track and the thumb border.
        data_attrs: Custom data attributes for JavaScript hooks or tests.
        help_text: Hint shown below the field.
        error_text: Error message shown below the field; marks the field as invalid.

    Note:
        In dual-thumb mode, two form fields are submitted:
        `{name}_min` and `{name}_max`.

    """

    __example__ = """
        SliderConfig(
            name="price",
            label="Price Range",
            minimum=0,
            maximum=1000,
            dual=True,
            value_min=200,
            value_max=800,
            items=["0€", "250€", "500€", "750€", "1000€"],
        )
        """

    value: int | None = field(
        default=None, metadata={"doc": _("The value of the range slider (single-thumb mode only).")}
    )
    minimum: int = field(default=0, metadata={"doc": _("Smallest configurable value of the range slider.")})
    maximum: int = field(default=100, metadata={"doc": _("Largest configurable value of the range slider.")})
    step_size: int = field(
        default=1, metadata={"doc": _("The size of the steps by which the value changes when moving the range slider.")}
    )
    items: list[str] = field(
        default_factory=list, metadata={"doc": _("A list of texts displayed as a legend below the slider.")}
    )
    legend_mode: SliderLegendMode = field(
        default="static",
        metadata={
            "doc": _(
                "Controls responsive legend behavior. Options: **'static'** (default) - no adjustment; **'skip'** - progressively hides legend items when space is limited; **'rotate'** - rotates legend text vertically when space is limited."
            )
        },
    )
    dual: bool = field(
        default=False,
        metadata={"doc": _("**True** to enable dual-thumb mode for selecting a range with min and max values.")},
    )
    value_min: int | None = field(
        default=None, metadata={"doc": _("The minimum value in dual-thumb mode. Defaults to `minimum`.")}
    )
    value_max: int | None = field(
        default=None, metadata={"doc": _("The maximum value in dual-thumb mode. Defaults to `maximum`.")}
    )
    color: ButtonColor = field(
        default="primary", metadata={"doc": _("Color of the filled track and the thumb border.")}
    )

    def __post_init__(self) -> None:
        """Validate slider configuration."""
        super().__post_init__()
        validate_slider_legend_mode(self.legend_mode, "legend_mode")
        validate_button_color(self.color)
        if self.minimum >= self.maximum:
            raise ValueError(f"minimum ({self.minimum}) must be less than maximum ({self.maximum})")  # noqa: TRY003
        if self.value is not None and not (self.minimum <= self.value <= self.maximum):
            raise ValueError(  # noqa: TRY003
                f"value ({self.value}) must be between minimum ({self.minimum}) and maximum ({self.maximum})"
            )
        if self.dual:
            if self.value_min is not None and self.value_min < self.minimum:
                raise ValueError(f"value_min ({self.value_min}) cannot be less than minimum ({self.minimum})")  # noqa: TRY003
            if self.value_max is not None and self.value_max > self.maximum:
                raise ValueError(f"value_max ({self.value_max}) cannot be greater than maximum ({self.maximum})")  # noqa: TRY003
            if self.value_min is not None and self.value_max is not None and self.value_min > self.value_max:
                raise ValueError(  # noqa: TRY003
                    f"value_min ({self.value_min}) cannot be greater than value_max ({self.value_max})"
                )


@dataclass
class ToggleConfig(BaseFormFieldConfig):
    """Configuration for the toggle component.

    Renders a toggle button or switch.

    Attributes:
        tag_id: Optional, unique tag ID for identifying the element in JavaScript.
        name: Required for a `<form>`, as the name of the request parameter.
        label: A text label displayed above the field.
        disabled: **True** if the field should be disabled.
        disabled_reason: Explanation why the field is disabled, shown as visible linked text below the field. Set to empty string to explicitly skip.
        required: **True** if the field must be filled in.
        value: The value of the toggle button.
        icon: Optional icon configuration.
        icon_only: **True** shows only the icon; the label becomes the accessible name and tooltip.
        checked: **True** if the toggle button should be selected.
        switch: **True** if the toggle button should look like a typical switch select.
        variant: Visual style of the toggle button; switches ignore it.
        color: Color of the toggle button or the switched-on track; ignored by the neutral variant.
        method: Name of the JavaScript method to be executed when the toggle button is clicked.
        data_attrs: Custom data attributes for JavaScript hooks or tests.
        help_text: Hint shown below the field.
        error_text: Error message shown below the field; marks the field as invalid.

    """

    __example__ = """
        ToggleConfig(
            tag_id="dark-mode",
            name="dark_mode",
            label="Dark Mode",
            switch=True,
        )
        """

    value: str = field(default="", metadata={"doc": _("The value of the toggle button.")})
    icon: IconConfig | None = field(default=None, metadata={"doc": _("Optional icon configuration.")})
    icon_only: bool = field(
        default=False,
        metadata={"doc": _("**True** shows only the icon; the label becomes the accessible name and tooltip.")},
    )
    checked: bool = field(default=False, metadata={"doc": _("**True** if the toggle button should be selected.")})
    switch: bool = field(
        default=False, metadata={"doc": _("**True** if the toggle button should look like a typical switch select.")}
    )
    variant: ControlVariant = field(
        default="neutral", metadata={"doc": _("Visual style of the toggle button; switches ignore it.")}
    )
    color: ButtonColor = field(
        default="primary",
        metadata={"doc": _("Color of the toggle button or the switched-on track; ignored by the neutral variant.")},
    )
    method: str = field(
        default="",
        metadata={"doc": _("Name of the JavaScript method to be executed when the toggle button is clicked.")},
    )

    def __post_init__(self) -> None:
        """Validate the look and require an icon and a label for an icon-only toggle button."""
        super().__post_init__()
        validate_control_variant(self.variant)
        validate_button_color(self.color)
        if self.icon_only:
            if self.switch:
                msg = f"ToggleConfig {self.name!r}: icon_only applies to toggle buttons, not to switches."
                raise ValueError(msg)
            if self.icon is None or not self.label:
                msg = f"ToggleConfig {self.name!r}: icon_only needs an icon and a label as its accessible name."
                raise ValueError(msg)


@dataclass
class SelectConfig(BaseFormFieldConfig):
    """Configuration for the select component.

    Renders a dropdown selection box.

    Attributes:
        tag_id: Optional, unique tag ID for identifying the element in JavaScript.
        name: Required for a `<form>`, as the name of the request parameter.
        label: A text label displayed above the field.
        disabled: **True** if the field should be disabled.
        disabled_reason: Explanation why the field is disabled, shown as visible linked text below the field. Set to empty string to explicitly skip.
        required: **True** if the field must be filled in.
        options: List of values that can be selected.
        selected_option: Value (the key value, if the options were passed as a dict) of the currently selected option.
        data_attrs: Custom data attributes for JavaScript hooks or tests.
        help_text: Hint shown below the field.
        error_text: Error message shown below the field; marks the field as invalid.

    Note:
        If `options` is a list, the value is also used as the name.

    """

    __example__ = """
        SelectConfig(
            name="country",
            label="Country",
            options={"de": "Germany", "fr": "France", "uk": "United Kingdom"},
            selected_option="de",
        )
        """

    options: list[str] | dict[str, str] = field(
        default_factory=list, metadata={"doc": _("List of values that can be selected.")}
    )
    selected_option: str = field(
        default="",
        metadata={
            "doc": _("Value (the key value, if the options were passed as a dict) of the currently selected option.")
        },
    )

    def __post_init__(self) -> None:
        """Validate disabled/disabled_reason, normalize options, and validate selected_option."""
        super().__post_init__()
        if isinstance(self.options, list):
            self.options = dict(zip(self.options, self.options, strict=True))
        if self.selected_option and self.selected_option not in self.options:
            raise ValueError(f"selected_option '{self.selected_option}' must be included in 'options'.")  # noqa: TRY003


@dataclass
class MultiselectConfig(BaseFormFieldConfig):
    """Configuration for the multiselect component.

    Renders a selection box allowing multiple selections with search.

    Attributes:
        tag_id: Optional, unique tag ID for identifying the element in JavaScript.
        name: Required for a `<form>`, as the name of the request parameter.
        label: A text label displayed above the field.
        disabled: **True** if the field should be disabled.
        disabled_reason: Explanation why the field is disabled, shown as visible linked text below the field. Set to empty string to explicitly skip.
        required: **True** if the field must be filled in.
        maximum: Maximum number of selectable options.
        show_buttons: Show additional buttons for 'Select All' and 'Deselect All'.
        options: List of values that can be selected.
        selected_options: List of currently selected options.
        data_attrs: Custom data attributes for JavaScript hooks or tests.
        help_text: Hint shown below the field.
        error_text: Error message shown below the field; marks the field as invalid.

    Note:
        If `options` is a list, the value is also used as the name.

    """

    __example__ = """
        MultiselectConfig(
            name="tags",
            label="Select Tags (max 5):",
            maximum=5,
            show_buttons=True,
            options=["Python", "Django", "JavaScript", "React", "Docker"],
            selected_options=["Python", "Django"],
        )
        """

    maximum: int | None = field(default=None, metadata={"doc": _("Maximum number of selectable options.")})
    show_buttons: bool = field(
        default=False, metadata={"doc": _("Show additional buttons for 'Select All' and 'Deselect All'.")}
    )
    options: list[str] | dict[str, str] = field(
        default_factory=list, metadata={"doc": _("List of values that can be selected.")}
    )
    selected_options: list[str] = field(
        default_factory=list, metadata={"doc": _("List of currently selected options.")}
    )

    def __post_init__(self) -> None:
        """Validate disabled/disabled_reason, normalize options, and validate selected_options against maximum."""
        super().__post_init__()
        if isinstance(self.options, list):
            self.options = dict(zip(self.options, self.options, strict=True))
        if self.maximum is not None and len(self.selected_options) > self.maximum:
            raise ValueError(  # noqa: TRY003
                f"selected_options has {len(self.selected_options)} entries, which exceeds maximum ({self.maximum})"
            )
        invalid = [option for option in self.selected_options if option not in self.options]
        if invalid:
            raise ValueError(f"selected_options {invalid} must be included in 'options'.")  # noqa: TRY003


@dataclass
class ChatConfig:
    """Configuration for the chat component.

    Renders a chat interface with an input line and a response container.

    The message is posted as ``msg``; the response is appended to the response container.

    Attributes:
        request_url: URL for sending chat messages via HTMX POST.
        tag_id: Prefix of the element IDs, unique on the page.
        htmx: Shared request options such as vals or a loading indicator.

    """

    __example__ = """
        ChatConfig(request_url=reverse("chat_api"))
        """

    request_url: str = field(metadata={"doc": _("URL for sending chat messages via HTMX POST.")})
    tag_id: str = field(default="chat", metadata={"doc": _("Prefix of the element IDs, unique on the page.")})
    htmx: HtmxConfig | None = field(
        default=None, metadata={"doc": _("Shared request options such as vals or a loading indicator.")}
    )

    def __post_init__(self) -> None:
        """Reject empty values for fields that identify or locate the component."""
        validate_not_empty(self, "request_url", "tag_id")
