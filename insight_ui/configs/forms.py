# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Configuration classes for form components."""

import warnings
from dataclasses import dataclass, field

from django.utils.translation import gettext_lazy as _

from insight_ui.configs.base import HtmxConfig
from insight_ui.configs.types import FormFieldType, validate_form_field_type


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
        help_text: Persistent hint shown below the control and linked via `aria-describedby`.
        error: Validation error shown as text below the control and linked via `aria-describedby`; sets `aria-invalid` and `aria-errormessage`.

    Note:
        If `options` is a list, the value is also used as the name.

    """

    __example__ = """
        FormFieldConfig(
            input_type="email",
            name="email",
            label="E-Mail",
            required=True,
        )
        """

    input_type: FormFieldType = field(
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
    options: list[str] | dict[str, str] = field(
        default_factory=list, metadata={"doc": _("List of options for select fields.")}
    )
    selected_option: str = field(default="", metadata={"doc": _("Currently selected value.")})
    rows: int = field(default=3, metadata={"doc": _("Number of rows for textarea fields.")})
    help_text: str = field(
        default="",
        metadata={"doc": _("Persistent hint shown below the control and linked via `aria-describedby`.")},
    )
    error: str = field(
        default="",
        metadata={
            "doc": _(
                "Validation error shown as text below the control and linked via `aria-describedby`; sets `aria-invalid` and `aria-errormessage`."
            )
        },
    )

    def __post_init__(self) -> None:
        """Validate input_type and normalize options to dict format."""
        validate_form_field_type(self.input_type, "input_type")
        if isinstance(self.options, list):
            self.options = dict(zip(self.options, self.options, strict=True))


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
        submit_label: Label for the submit button.
        reset_label: Label for the reset button.
        request_url: Target URL for form submission.
        method: HTTP method for form submission (get or post).
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
    submit_label: str = field(default="", metadata={"doc": _("Label for the submit button.")})
    reset_label: str = field(default="", metadata={"doc": _("Label for the reset button.")})
    request_url: str = field(default="", metadata={"doc": _("Target URL for form submission.")})
    method: str = field(default="post", metadata={"doc": _("HTTP method for form submission (get or post).")})
    htmx_config: HtmxConfig | None = field(default=None, metadata={"doc": _("HTMX configuration for AJAX submission.")})

    def __post_init__(self) -> None:
        """Validate that request_url and htmx_config.request_url are not both set."""
        if self.request_url and self.htmx_config and self.htmx_config.request_url:
            identifier = self.tag_id or self.title or "(unnamed)"
            warnings.warn(
                f"FormConfig {identifier} has both 'request_url' and 'htmx_config.request_url' set. "
                "This may cause conflicting behavior. Use 'request_url' for a plain form submission, or "
                "'htmx_config.request_url' for HTMX requests, but not both.",
                UserWarning,
                stacklevel=2,
            )
