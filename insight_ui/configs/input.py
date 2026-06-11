"""Configuration classes for input and control components."""

from dataclasses import dataclass, field
from typing import Literal

from django.utils.translation import gettext_lazy as _

from insight_ui.configs.base import BaseFormFieldConfig, IconConfig


@dataclass
class InputFieldConfig(BaseFormFieldConfig):
    """
    Configuration for the input_field component.

    Renders any HTML <input> element with proper styling and accessibility.

    Attributes:
        tag_id: Optional, unique tag ID for identifying the element in JavaScript.
        name: Required for a `<form>`, as the name of the request parameter.
        label: A text label displayed above the field.
        disabled: **True** if the field should be disabled.
        required: **True** if the field must be filled in.
        input_type: The type of the input field, e.g.: 'text', 'password', 'date', etc.
        placeholder: Placeholder text, displayed in the field as long as it has not been selected.
        value: The value of the input field.
        minimum: Smallest numeric value (for `input_type='number'`).
        maximum: Largest numeric value (for `input_type='number'`).
        min_length: Minimum number of characters in a text field.
        max_length: Maximum number of characters in a text field.
        checked: **True** if `input_type='checkbox'` and the checkbox should be selected.

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

    input_type: Literal[
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
    ] = field(
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


@dataclass
class TextareaConfig(BaseFormFieldConfig):
    """
    Configuration for the textarea component.

    Renders a multi-line text input field.

    Attributes:
        tag_id: Optional, unique tag ID for identifying the element in JavaScript.
        name: Required for a `<form>`, as the name of the request parameter.
        label: A text label displayed above the field.
        disabled: **True** if the field should be disabled.
        required: **True** if the field must be filled in.
        placeholder: Placeholder text, displayed in the field as long as it has not been selected.
        value: The value of the input field.
        rows: Determines the number of lines.
        cols: Determines the number of characters in a line.

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
    """
    Configuration for the checkbox component.

    Renders a single checkbox with label.

    Attributes:
        tag_id: Optional, unique tag ID for identifying the element in JavaScript.
        name: Required for a `<form>`, as the name of the request parameter.
        label: A text label displayed above the field.
        disabled: **True** if the field should be disabled.
        required: **True** if the field must be filled in.
        value: The value of the checkbox (this is not the state, see 'checked' for that).
        checked: **True** if the checkbox should be selected.

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
    """
    Configuration for a single checkbox within a checkbox group.

    Attributes:
        tag_id: Unique ID for this checkbox.
        label: Label text.
        value: Value submitted when checked.
        disabled: **True** if the checkbox should be disabled.
        checked: **True** if the checkbox should be selected.

    """

    __example__ = """
        CheckboxItemConfig(tag_id="en", value="english", label="English")
        """

    tag_id: str = field(metadata={"doc": _("Unique ID for this checkbox.")})
    label: str = field(metadata={"doc": _("Label text.")})
    value: str = field(metadata={"doc": _("Value submitted when checked.")})
    disabled: bool = field(default=False, metadata={"doc": _("**True** if the checkbox should be disabled.")})
    checked: bool = field(default=False, metadata={"doc": _("**True** if the checkbox should be selected.")})


@dataclass
class CheckboxGroupConfig:
    """
    Configuration for the checkbox_group component.

    Renders a group of linked checkboxes with optional constraints.

    Attributes:
        name: Required for a `<form>`, as the name of the request parameter.
        label: Text label displayed above the checkbox elements.
        items: List of the checkbox elements.
        as_row: **True** if the checkbox elements should be displayed side by side.
        minimum_checked: Number of checkbox elements that must be selected at minimum.
        maximum_checked: Number of checkbox elements that may be selected at the same time.

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


@dataclass
class DropdownItemConfig:
    """
    Configuration for an item within a dropdown menu.

    Attributes:
        text: Label of the dropdown element.
        request_url: The URL to be called when clicking on the respective item.
        icon: An optional icon displayed before the label.

    """

    __example__ = """
        DropdownItemConfig(text="Profile", request_url="/profile/", icon=IconConfig(name="user"))
        """

    text: str = field(metadata={"doc": _("Label of the dropdown element.")})
    request_url: str = field(
        default="", metadata={"doc": _("The URL to be called when clicking on the respective item.")}
    )
    icon: IconConfig | None = field(default=None, metadata={"doc": _("An optional icon displayed before the label.")})


@dataclass
class DropdownConfig:
    """
    Configuration for the dropdown component.

    Renders a dropdown menu with a trigger button.

    Attributes:
        tag_id: Optional, unique tag ID for identifying the element in JavaScript.
        title: Label of the dropdown button.
        show_arrow: **True** displays an arrow behind the title.
        items: A list of the menu elements.

    """

    __example__ = """
        DropdownConfig(
            tag_id="user-dropdown",
            title="Account",
            show_arrow=True,
            items=[
                DropdownItemConfig(text="Profile", request_url="/profile/", icon=IconConfig(name="user")),
                DropdownItemConfig(text="Settings", request_url="/settings/", icon=IconConfig(name="gear")),
                DropdownItemConfig(text="Logout", request_url="/logout/", icon=IconConfig(name="leave")),
            ],
        )
        """

    tag_id: str = field(metadata={"doc": _("Optional, unique tag ID for identifying the element in JavaScript.")})
    title: str = field(metadata={"doc": _("Label of the dropdown button.")})
    show_arrow: bool = field(default=True, metadata={"doc": _("**True** displays an arrow behind the title.")})
    items: list[DropdownItemConfig] = field(default_factory=list, metadata={"doc": _("A list of the menu elements.")})


@dataclass
class RadioItemConfig:
    """
    Configuration for a single radio button within a group.

    Attributes:
        tag_id: Optional, unique tag ID for identifying the element in JavaScript.
        value: Value of the respective radio button.
        label: Label of the respective radio button.
        icon: Optional icon displayed before the label.
        disabled: **True** if the radio button should be disabled.

    """

    __example__ = """
        RadioItemConfig(tag_id="gpt4", value="gpt-4", label="GPT-4")
        """

    tag_id: str = field(metadata={"doc": _("Optional, unique tag ID for identifying the element in JavaScript.")})
    value: str = field(metadata={"doc": _("Value of the respective radio button.")})
    label: str = field(default="", metadata={"doc": _("Label of the respective radio button.")})
    icon: IconConfig | None = field(default=None, metadata={"doc": _("Optional icon displayed before the label.")})
    disabled: bool = field(default=False, metadata={"doc": _("**True** if the radio button should be disabled.")})


@dataclass
class RadioGroupConfig:
    """
    Configuration for the radio_group component.

    Renders a group of standard radio buttons.

    Attributes:
        name: Optional, unique tag ID for identifying the element in JavaScript.
        label: A text label displayed above the radio elements.
        items: A list of the radio elements.
        as_row: **True** if the radio elements should be displayed side by side.
        current_value: The value of the currently selected radio button.

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

    name: str = field(metadata={"doc": _("Optional, unique tag ID for identifying the element in JavaScript.")})
    label: str = field(default="", metadata={"doc": _("A text label displayed above the radio elements.")})
    items: list[RadioItemConfig] = field(default_factory=list, metadata={"doc": _("A list of the radio elements.")})
    as_row: bool = field(
        default=True, metadata={"doc": _("**True** if the radio elements should be displayed side by side.")}
    )
    current_value: str = field(default="", metadata={"doc": _("The value of the currently selected radio button.")})

    def __post_init__(self) -> None:
        """Set first option for current_value if empty."""
        if not self.current_value and self.items:
            self.current_value = self.items[0].value


@dataclass
class RadioBlockConfig:
    """
    Configuration for the radio_block component.

    Renders radio buttons as a compact block that can trigger requests.

    Attributes:
        name: Optional, unique tag ID for identifying the element in JavaScript.
        label: A text label displayed above the radio elements.
        items: A list of the radio elements.
        integrated: **True** if the group is inside a `<form>`. If **False** the group gets its own `<form>`.
        as_row: **True** if the radio elements should be displayed side by side.
        request_url: Name of the URL to which the request should be sent when clicking one of the radio buttons.
        hx_target_id: The ID of the HTML tag to be replaced when switching the radio button.
        hx_swap_method: The way in which the target is to be replaced.
        method: Name of the JavaScript method to be executed when clicking one of the radio buttons.
        current_value: The value of the currently selected radio button.

    """

    __example__ = """
        RadioBlockConfig(
            name="view",
            items=[
                RadioItemConfig(tag_id="card", value="card", icon=IconConfig(name="cards")),
                RadioItemConfig(tag_id="table", value="table", icon=IconConfig(name="list")),
            ],
            current_value="card",
            hx_target_id="content-area",
        )
        """

    name: str = field(metadata={"doc": _("Optional, unique tag ID for identifying the element in JavaScript.")})
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
        metadata={
            "doc": _("Name of the URL to which the request should be sent when clicking one of the radio buttons.")
        },
    )
    hx_target_id: str = field(
        default="", metadata={"doc": _("The ID of the HTML tag to be replaced when switching the radio button.")}
    )
    hx_swap_method: Literal["innerHTML", "outerHTML", "beforebegin", "afterbegin", "beforeend", "afterend"] = field(
        default="outerHTML", metadata={"doc": _("The way in which the target is to be replaced.")}
    )
    method: str = field(
        default="",
        metadata={"doc": _("Name of the JavaScript method to be executed when clicking one of the radio buttons.")},
    )
    current_value: str = field(default="", metadata={"doc": _("The value of the currently selected radio button.")})

    def __post_init__(self) -> None:
        """Set first option for current_value if empty."""
        if not self.current_value and self.items:
            self.current_value = self.items[0].value


@dataclass
class SliderConfig(BaseFormFieldConfig):
    """
    Configuration for the slider (range slider) component.

    Renders a range slider for selecting numeric values.

    Attributes:
        tag_id: Optional, unique tag ID for identifying the element in JavaScript.
        name: Required for a `<form>`, as the name of the request parameter.
        label: A text label displayed above the field.
        disabled: **True** if the field should be disabled.
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
    legend_mode: Literal["static", "skip", "rotate"] = field(
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

    def __post_init__(self) -> None:
        """Validate slider configuration."""
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


@dataclass
class ToggleConfig(BaseFormFieldConfig):
    """
    Configuration for the toggle component.

    Renders a toggle button or switch.

    Attributes:
        tag_id: Optional, unique tag ID for identifying the element in JavaScript.
        name: Required for a `<form>`, as the name of the request parameter.
        label: A text label displayed above the field.
        disabled: **True** if the field should be disabled.
        required: **True** if the field must be filled in.
        value: The value of the toggle button.
        icon: Optional icon configuration.
        checked: **True** if the toggle button should be selected.
        switch: **True** if the toggle button should look like a typical switch select.
        method: Name of the JavaScript method to be executed when the toggle button is clicked.

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
    checked: bool = field(default=False, metadata={"doc": _("**True** if the toggle button should be selected.")})
    switch: bool = field(
        default=False, metadata={"doc": _("**True** if the toggle button should look like a typical switch select.")}
    )
    method: str = field(
        default="",
        metadata={"doc": _("Name of the JavaScript method to be executed when the toggle button is clicked.")},
    )


@dataclass
class SelectConfig(BaseFormFieldConfig):
    """
    Configuration for the select component.

    Renders a dropdown selection box.

    Attributes:
        tag_id: Optional, unique tag ID for identifying the element in JavaScript.
        name: Required for a `<form>`, as the name of the request parameter.
        label: A text label displayed above the field.
        disabled: **True** if the field should be disabled.
        required: **True** if the field must be filled in.
        explanation: A brief description of the filter that appears in a tooltip.
        options: List of values that can be selected.
        selected_option: Value (the key value, if the options were passed as a dict) of the currently selected option.

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

    explanation: str = field(
        default="", metadata={"doc": _("A brief description of the filter that appears in a tooltip.")}
    )
    options: list[str] | dict[str, str] = field(
        default_factory=list, metadata={"doc": _("List of values that can be selected.")}
    )
    selected_option: str = field(
        default="",
        metadata={
            "doc": _("Value (the key value, if the options were passed as a dict) of the currently selected option.")
        },
    )


@dataclass
class MultiselectConfig(BaseFormFieldConfig):
    """
    Configuration for the multiselect component.

    Renders a selection box allowing multiple selections with search.

    Attributes:
        tag_id: Optional, unique tag ID for identifying the element in JavaScript.
        name: Required for a `<form>`, as the name of the request parameter.
        label: A text label displayed above the field.
        disabled: **True** if the field should be disabled.
        required: **True** if the field must be filled in.
        maximum: Maximum number of selectable options.
        show_buttons: Show additional buttons for 'Select All' and 'Deselect All'.
        options: List of values that can be selected.
        selected_options: List of currently selected options.

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


@dataclass
class ChatConfig:
    """
    Configuration for the chat component.

    Renders a chat interface with an input line and a response container.

    Attributes:
        request_url: URL for sending chat messages via HTMX POST.

    """

    __example__ = """
        ChatConfig(request_url=reverse("chat_api"))
        """

    request_url: str = field(metadata={"doc": _("URL for sending chat messages via HTMX POST.")})
