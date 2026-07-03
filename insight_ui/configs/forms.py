"""Configuration classes for form components."""

from dataclasses import dataclass, field
from typing import Literal

from django.utils.translation import gettext_lazy as _

from insight_ui.configs.base import HtmxConfig


@dataclass
class FormFieldConfig:
    """Configuration for a single field within the form component.

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

    """

    __example__ = """
        FormFieldConfig(
            input_type="email",
            name="email",
            label="E-Mail",
            required=True,
        )
        """

    input_type: Literal["text", "password", "email", "number", "tel", "url", "date", "textarea", "select"] = field(
        default="text", metadata={"doc": _("Type of form field (text, email, password, textarea, select).")}
    )
    tag_id: str = field(default="", metadata={"doc": _("Unique ID for the field.")})
    name: str = field(default="", metadata={"doc": _("Form field name.")})
    label: str = field(default="", metadata={"doc": _("Label text.")})
    placeholder: str = field(default="", metadata={"doc": _("Placeholder text.")})
    value: str = field(default="", metadata={"doc": _("Default value.")})
    explanation: str = field(default="", metadata={"doc": _("Tooltip explanation text.")})
    required: bool = field(default=False, metadata={"doc": _("Whether field is required.")})
    disabled: bool = field(default=False, metadata={"doc": _("Whether field is disabled.")})
    options: list[str] = field(default_factory=list, metadata={"doc": _("List of options for select fields.")})
    selected_option: str = field(default="", metadata={"doc": _("Currently selected value.")})
    rows: int = field(default=3, metadata={"doc": _("Number of rows for textarea fields.")})


@dataclass
class FormConfig:
    """Configuration for the form component.

    Renders a complete form with multiple fields and HTMX support.

    Attributes:
        tag_id: Unique ID for the form element.
        title: Form title displayed at the top.
        description: Optional description below the title.
        fields: List of form field configurations.
        show_reset_button: Whether to show a reset button.
        request_url: Target URL for form submission.
        htmx_config: HTMX configuration for AJAX submission.

    """

    __example__ = """
        FormConfig(
            tag_id="contact-form",
            title="Contact Us",
            description="We'll get back to you within 24 hours.",
            fields=[
                FormFieldConfig(input_type="text", name="name", label="Name", required=True),
                FormFieldConfig(input_type="email", name="email", label="E-Mail", required=True),
                FormFieldConfig(input_type="textarea", name="message", label="Message", rows=5),
            ],
            show_reset_button=True,
            htmx_config=HtmxConfig(request_url="/contact_submission", target="#form-response", swap_method="innerHTML"),
        )
        """

    tag_id: str = field(default="", metadata={"doc": _("Unique ID for the form element.")})
    title: str = field(default="", metadata={"doc": _("Form title displayed at the top.")})
    description: str = field(default="", metadata={"doc": _("Optional description below the title.")})
    fields: list[FormFieldConfig] = field(
        default_factory=list, metadata={"doc": _("List of form field configurations.")}
    )
    show_reset_button: bool = field(default=False, metadata={"doc": _("Whether to show a reset button.")})
    request_url: str = field(default="", metadata={"doc": _("Target URL for form submission.")})
    htmx_config: HtmxConfig | None = field(default=None, metadata={"doc": _("HTMX configuration for AJAX submission.")})
