"""Configuration classes for form components."""

from dataclasses import dataclass, field
from typing import Literal

from insight_ui.configs.base import HtmxConfig


@dataclass
class FormFieldConfig:
    """
    Configuration for a single field within the form component.

    This is used within FormConfig.fields to define form structure.
    It supports multiple field types including input, textarea, and select.

    Attributes:
        input_type: Type of form field (text, email, password, textarea, select).
        tag_id: Unique ID for the field.
        name: Form field name.
        label: Label text.
        placeholder: Placeholder text.
        value: Default value.
        explanation: Tooltip explanation text.
        required: Whether field is required.
        disabled: Whether field is disabled.
        options: List of options for select fields.
        selected_option: Currently selected value.
        rows: Number of rows for textarea fields.

    Example:
        >>> fields = [
        ...     FormFieldConfig(
        ...         input_type="email",
        ...         name="email",
        ...         label="E-Mail",
        ...         required=True,
        ...     ),
        ...     FormFieldConfig(
        ...         input_type="textarea",
        ...         name="bio",
        ...         label="Biography",
        ...         rows=4,
        ...     ),
        ... ]

    """

    input_type: Literal["text", "password", "email", "number", "tel", "url", "date", "textarea", "select"] = "text"
    tag_id: str = ""
    name: str = ""
    label: str = ""
    placeholder: str = ""
    value: str = ""
    explanation: str = ""
    required: bool = False
    disabled: bool = False
    options: list[str] = field(default_factory=list)
    selected_option: str = ""
    rows: int = 3


@dataclass
class FormConfig:
    """
    Configuration for the form component.

    Renders a complete form with multiple fields and HTMX support.

    Attributes:
        tag_id: Unique ID for the form element.
        title: Form title displayed at the top.
        description: Optional description below the title.
        fields: List of form field configurations.
        show_reset_button: Whether to show a reset button.
        request_url: Target URL for form submission.
        htmx_config: HTMX configuration for AJAX submission.

    Example:
        >>> contact_form = FormConfig(
        ...     tag_id="contact-form",
        ...     title="Contact Us",
        ...     description="We'll get back to you within 24 hours.",
        ...     fields=[
        ...         FormFieldConfig(input_type="text", name="name", label="Name", required=True),
        ...         FormFieldConfig(input_type="email", name="email", label="E-Mail", required=True),
        ...         FormFieldConfig(input_type="textarea", name="message", label="Message", rows=5),
        ...     ],
        ...     show_reset_button=True,
        ...     htmx_config=HtmxConfig(url="/contact_submission", target="#form-response", swap="innerHTML"),
        ... )

    """

    tag_id: str = ""
    title: str = ""
    description: str = ""
    fields: list[FormFieldConfig] = field(default_factory=list)
    show_reset_button: bool = False
    request_url: str = ""
    htmx_config: HtmxConfig | None = None
