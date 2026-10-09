# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Configuration classes for form components."""

import warnings
from dataclasses import dataclass, field
from typing import get_args

from django.utils.translation import gettext_lazy as _

from insight_ui.configs.base import HtmxConfig
from insight_ui.configs.input import (
    CheckboxConfig,
    CheckboxGroupConfig,
    InputFieldConfig,
    MultiselectConfig,
    RadioBlockConfig,
    RadioGroupConfig,
    SelectConfig,
    SliderConfig,
    TextareaConfig,
    ToggleConfig,
)

# Field configs the form component can render, in the order they appear in error messages.
type FormField = (
    InputFieldConfig
    | TextareaConfig
    | SelectConfig
    | MultiselectConfig
    | CheckboxConfig
    | CheckboxGroupConfig
    | RadioGroupConfig
    | RadioBlockConfig
    | SliderConfig
    | ToggleConfig
)

FORM_FIELD_CONFIGS: tuple[type, ...] = get_args(FormField.__value__)


@dataclass
class FormConfig:
    """Configuration for the form component.

    Renders a complete form with multiple fields and HTMX support.

    Attributes:
        tag_id: Unique ID for the form element.
        title: Form title displayed at the top.
        description: Optional description below the title.
        fields: Field configs rendered in order. Supported: InputFieldConfig, TextareaConfig, SelectConfig, MultiselectConfig, CheckboxConfig, CheckboxGroupConfig, RadioGroupConfig, RadioBlockConfig (always rendered integrated), SliderConfig and ToggleConfig.
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
                InputFieldConfig(name="name", label="Name", required=True),
                InputFieldConfig(name="email", input_type="email", label="E-Mail", required=True),
                SelectConfig(name="topic", label="Topic", options=["Support", "Sales", "Other"]),
                SliderConfig(name="budget", label="Budget", minimum=0, maximum=10000, step_size=500, value=2000),
                CheckboxGroupConfig(
                    name="contact_via",
                    label="Contact me via",
                    items=[
                        CheckboxItemConfig(tag_id="via-email", value="email", label="E-Mail", checked=True),
                        CheckboxItemConfig(tag_id="via-phone", value="phone", label="Phone"),
                    ],
                    minimum_checked=1,
                ),
                TextareaConfig(name="message", label="Message", rows=5),
            ],
            show_reset_button=True,
            htmx_config=HtmxConfig(request_url="/contact_submission", target="#form-response", swap_method="innerHTML"),
        )
        """

    tag_id: str = field(default="", metadata={"doc": _("Unique ID for the form element.")})
    title: str = field(default="", metadata={"doc": _("Form title displayed at the top.")})
    description: str = field(default="", metadata={"doc": _("Optional description below the title.")})
    fields: list[FormField] = field(
        default_factory=list,
        metadata={
            "doc": _(
                "Field configs rendered in order. Supported: InputFieldConfig, TextareaConfig, SelectConfig, MultiselectConfig, CheckboxConfig, CheckboxGroupConfig, RadioGroupConfig, RadioBlockConfig (always rendered integrated), SliderConfig and ToggleConfig."
            )
        },
    )
    show_reset_button: bool = field(default=False, metadata={"doc": _("Whether to show a reset button.")})
    submit_label: str = field(default="", metadata={"doc": _("Label for the submit button.")})
    reset_label: str = field(default="", metadata={"doc": _("Label for the reset button.")})
    request_url: str = field(default="", metadata={"doc": _("Target URL for form submission.")})
    method: str = field(default="post", metadata={"doc": _("HTTP method for form submission (get or post).")})
    htmx_config: HtmxConfig | None = field(default=None, metadata={"doc": _("HTMX configuration for AJAX submission.")})

    def __post_init__(self) -> None:
        """Validate the field configs and warn if request_url and htmx_config.request_url are both set."""
        for form_field in self.fields:
            if not isinstance(form_field, FORM_FIELD_CONFIGS):
                supported = ", ".join(config.__name__ for config in FORM_FIELD_CONFIGS)
                raise TypeError(  # noqa: TRY003
                    f"FormConfig fields must be one of {supported}; got {type(form_field).__name__}."
                )
        if self.request_url and self.htmx_config and self.htmx_config.request_url:
            identifier = self.tag_id or self.title or "(unnamed)"
            warnings.warn(
                f"FormConfig {identifier} has both 'request_url' and 'htmx_config.request_url' set. "
                "This may cause conflicting behavior. Use 'request_url' for a plain form submission, or "
                "'htmx_config.request_url' for HTMX requests, but not both.",
                UserWarning,
                stacklevel=2,
            )
