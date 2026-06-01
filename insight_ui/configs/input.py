"""Configuration classes for input and control components."""

from dataclasses import dataclass, field
from typing import Literal

from insight_ui.configs.base import BaseFormFieldConfig, IconConfig


@dataclass
class InputFieldConfig(BaseFormFieldConfig):
    """
    Configuration for the input_field component.

    Renders any HTML <input> element with proper styling and accessibility.

    Attributes:
        tag_id: Unique ID for JavaScript/CSS targeting.
        name: Form field name (used in request parameters).
        input_type: HTML input type (text, password, email, number, date, etc.).
        placeholder: Placeholder text shown when empty.
        value: Current value of the input.
        minimum: Minimum value (for number/date inputs).
        maximum: Maximum value (for number/date inputs).
        min_length: Minimum character length.
        max_length: Maximum character length.
        checked: Whether checkbox/radio is checked.
        label: Label text displayed above the field.
        disabled: Whether the field is disabled.
        required: Whether the field is required.

    Example:
        >>> email_input = InputFieldConfig(
        ...     name="email",
        ...     input_type="email",
        ...     label="E-Mail Address",
        ...     placeholder="you@example.com",
        ...     required=True,
        ... )

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
    ] = "text"
    placeholder: str = ""
    value: str | int | float | None = None
    minimum: int | None = None
    maximum: int | None = None
    min_length: int | None = None
    max_length: int | None = None
    checked: bool = False


@dataclass
class TextareaConfig(BaseFormFieldConfig):
    """
    Configuration for the textarea component.

    Renders a multi-line text input field.

    Attributes:
        tag_id: Unique ID for JavaScript/CSS targeting.
        name: Form field name.
        placeholder: Placeholder text.
        value: Current text content.
        rows: Number of visible text lines.
        cols: Visible width in characters.
        label: Label text displayed above the field.
        disabled: Whether the field is disabled.
        required: Whether the field is required.

    Example:
        >>> message_field = TextareaConfig(
        ...     name="message",
        ...     label="Your Message",
        ...     placeholder="Enter your message here...",
        ...     rows=5,
        ...     required=True,
        ... )

    """

    placeholder: str = ""
    value: str = ""
    rows: int = 3
    cols: int | None = None


@dataclass
class CheckboxConfig(BaseFormFieldConfig):
    """
    Configuration for the checkbox component.

    Renders a single checkbox with label.

    Attributes:
        tag_id: Unique ID for JavaScript/CSS targeting.
        name: Form field name.
        label: Label text displayed next to the checkbox.
        value: The value submitted when checked.
        checked: Whether the checkbox is initially checked.
        disabled: Whether the checkbox is disabled.

    Example:
        >>> accept_terms = CheckboxConfig(
        ...     tag_id="accept-terms",
        ...     name="accept_terms",
        ...     value="accepted",
        ...     label="I accept the terms and conditions",
        ... )

    """

    value: str = ""
    checked: bool = False


@dataclass
class CheckboxItemConfig:
    """
    Configuration for a single checkbox within a checkbox group.

    Attributes:
        tag_id: Unique ID for this checkbox.
        label: Label text.
        value: Value submitted when checked.
        disabled: Whether this checkbox is disabled.
        checked: Whether initially checked.

    """

    tag_id: str
    label: str
    value: str
    disabled: bool = False
    checked: bool = False


@dataclass
class CheckboxGroupConfig:
    """
    Configuration for the checkbox_group component.

    Renders a group of linked checkboxes with optional constraints.

    Attributes:
        name: Form field name for the group.
        label: Label for the entire group.
        items: List of checkbox configurations.
        as_row: If True, arrange checkboxes horizontally.
        minimum_checked: Minimum number that must be checked.
        maximum_checked: Maximum number that can be checked.

    Example:
        >>> languages = CheckboxGroupConfig(
        ...     name="languages",
        ...     label="Select languages (max 3):",
        ...     as_row=True,
        ...     maximum_checked=3,
        ...     items=[
        ...         CheckboxItemConfig(tag_id="en", value="english", label="English"),
        ...         CheckboxItemConfig(tag_id="de", value="german", label="German"),
        ...         CheckboxItemConfig(tag_id="fr", value="french", label="French"),
        ...     ],
        ... )

    """

    name: str
    label: str = ""
    items: list[CheckboxItemConfig] = field(default_factory=list)
    as_row: bool = True
    minimum_checked: int = 0
    maximum_checked: int | None = None


@dataclass
class DropdownItemConfig:
    """
    Configuration for an item within a dropdown menu.

    Attributes:
        text: Item text label.
        request_url: Target URL when clicked.
        icon: Optional icon configuration.

    """

    text: str
    request_url: str = ""
    icon: IconConfig | None = None


@dataclass
class DropdownConfig:
    """
    Configuration for the dropdown component.

    Renders a dropdown menu with a trigger button.

    Attributes:
        tag_id: Unique ID for JavaScript/CSS targeting.
        title: Dropdown trigger button text.
        show_arrow: Show dropdown arrow indicator.
        items: List of dropdown items.

    Example:
        >>> user_menu = DropdownConfig(
        ...     tag_id="user-dropdown",
        ...     title="Account",
        ...     show_arrow=True,
        ...     items=[
        ...         DropdownItemConfig(text="Profile", request_url="/profile/", icon=IconConfig(name="user")),
        ...         DropdownItemConfig(text="Settings", request_url="/settings/", icon=IconConfig(name="gear")),
        ...         DropdownItemConfig(text="Logout", request_url="/logout/", icon=IconConfig(name="leave")),
        ...     ],
        ... )

    """

    tag_id: str
    title: str
    show_arrow: bool = True
    items: list[DropdownItemConfig] = field(default_factory=list)


@dataclass
class RadioItemConfig:
    """
    Configuration for a single radio button within a group.

    Attributes:
        tag_id: Unique ID for this radio button.
        value: Value submitted when selected.
        label: Text label (for text-based radio buttons).
        icon: Icon configuration (for icon-based radio buttons).
        disabled: Whether this option is disabled.

    """

    tag_id: str
    value: str
    label: str = ""
    icon: IconConfig | None = None
    disabled: bool = False


@dataclass
class RadioGroupConfig:
    """
    Configuration for the radio_group component.

    Renders a group of standard radio buttons.

    Attributes:
        name: Form field name for the group.
        label: Label for the entire group.
        items: List of radio button configurations.
        as_row: If True, arrange radio buttons horizontally.
        current_value: Currently selected value.

    Example:
        >>> model_select = RadioGroupConfig(
        ...     name="model",
        ...     label="Select AI Model:",
        ...     items=[
        ...         RadioItemConfig(tag_id="gpt4", value="gpt-4", label="GPT-4"),
        ...         RadioItemConfig(tag_id="claude", value="claude", label="Claude"),
        ...         RadioItemConfig(tag_id="llama", value="llama", label="LLaMA", disabled=True),
        ...     ],
        ...     current_value="claude",
        ... )

    """

    name: str
    label: str = ""
    items: list[RadioItemConfig] = field(default_factory=list)
    as_row: bool = True
    current_value: str = ""

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
        name: Form field name.
        label: Label for the group.
        items: List of radio button configurations.
        integrated: If False, component has its own <form> element.
        as_row: If True, arrange buttons horizontally.
        request_url: Url for request on change.
        hx_target_id: HTMX target element ID.
        hx_swap_method: HTMX swap method.
        method: JavaScript method to execute on change.
        current_value: Currently selected value.

    Example:
        >>> view_toggle = RadioBlockConfig(
        ...     name="view",
        ...     items=[
        ...         RadioItemConfig(tag_id="card", value="card", icon=IconConfig(name="cards")),
        ...         RadioItemConfig(tag_id="table", value="table", icon=IconConfig(name="list")),
        ...     ],
        ...     current_value="card",
        ...     hx_target_id="content-area",
        ... )

    """

    name: str
    label: str = ""
    items: list[RadioItemConfig] = field(default_factory=list)
    integrated: bool = False
    as_row: bool = True
    request_url: str = ""
    hx_target_id: str = ""
    hx_swap_method: Literal["innerHTML", "outerHTML", "beforebegin", "afterbegin", "beforeend", "afterend"] = (
        "outerHTML"
    )
    method: str = ""
    current_value: str = ""

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
        tag_id: Unique ID for JavaScript/CSS targeting.
        name: Form field name.
        value: Current value (single-thumb mode).
        minimum: Minimum allowed value.
        maximum: Maximum allowed value.
        step_size: Step increment.
        label: Label text displayed above slider.
        disabled: Whether slider is disabled.
        items: Legend labels displayed below the slider.
        legend_mode: Responsive legend behavior ('static', 'skip', 'rotate').
        dual: Enable dual-thumb mode for range selection.
        value_min: Minimum value in dual-thumb mode.
        value_max: Maximum value in dual-thumb mode.

    Example:
        >>> price_range = SliderConfig(
        ...     name="price",
        ...     label="Price Range",
        ...     minimum=0,
        ...     maximum=1000,
        ...     dual=True,
        ...     value_min=200,
        ...     value_max=800,
        ...     items=["0€", "250€", "500€", "750€", "1000€"],
        ... )

    Note:
        In dual-thumb mode, two form fields are submitted:
        `{name}_min` and `{name}_max`.

    """

    value: int | None = None
    minimum: int = 0
    maximum: int = 100
    step_size: int = 1
    items: list[str] = field(default_factory=list)
    legend_mode: Literal["static", "skip", "rotate"] = "static"
    dual: bool = False
    value_min: int | None = None
    value_max: int | None = None

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
        tag_id: Unique ID for JavaScript/CSS targeting.
        name: Form field name.
        value: Value submitted when toggled on.
        label: Label text.
        icon: Optional icon configuration.
        checked: Whether initially toggled on.
        disabled: Whether toggle is disabled.
        switch: If True, render as iOS-style switch.
        method: JavaScript method to execute on change.

    Example:
        >>> dark_mode = ToggleConfig(
        ...     tag_id="dark-mode",
        ...     name="dark_mode",
        ...     label="Dark Mode",
        ...     switch=True,
        ... )

    """

    value: str = ""
    icon: IconConfig | None = None
    checked: bool = False
    switch: bool = False
    method: str = ""


@dataclass
class SelectConfig(BaseFormFieldConfig):
    """
    Configuration for the select component.

    Renders a dropdown selection box.

    Attributes:
        name: Form field name.
        label: Label text displayed above the select.
        explanation: Tooltip explanation text.
        options: Available options (list of strings or dict mapping value→label).
        selected_option: Currently selected value.

    Example:
        >>> country_select = SelectConfig(
        ...     name="country",
        ...     label="Country",
        ...     options={"de": "Germany", "fr": "France", "uk": "United Kingdom"},
        ...     selected_option="de",
        ... )

    """

    explanation: str = ""
    options: list[str] | dict[str, str] = field(default_factory=list)
    selected_option: str = ""


@dataclass
class MultiselectConfig(BaseFormFieldConfig):
    """
    Configuration for the multiselect component.

    Renders a selection box allowing multiple selections with search.

    Attributes:
        name: Form field name.
        label: Label text.
        maximum: Maximum number of selections allowed.
        show_buttons: Show "Select All" / "Deselect All" buttons.
        options: Available options.
        selected_options: Currently selected values.

    Example:
        >>> tags_select = MultiselectConfig(
        ...     name="tags",
        ...     label="Select Tags (max 5):",
        ...     maximum=5,
        ...     show_buttons=True,
        ...     options=["Python", "Django", "JavaScript", "React", "Docker"],
        ...     selected_options=["Python", "Django"],
        ... )

    """

    maximum: int | None = None
    show_buttons: bool = False
    options: list[str] | dict[str, str] = field(default_factory=list)
    selected_options: list[str] = field(default_factory=list)
