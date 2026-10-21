# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Configuration classes for form components."""

import warnings
from dataclasses import dataclass, field
from re import fullmatch
from typing import Literal, get_args

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
class TurnstileConfig:
    """Public widget settings for an optional Cloudflare Turnstile challenge.

    The host application must validate the submitted token before processing the
    form. Never put the secret key in this config or in a template context.

    Attributes:
        site_key: Public Turnstile site key. Never use the secret key here.
        theme: Widget theme: auto, light, or dark.
        size: Widget size: normal, flexible, or compact.
        action: Optional action identifier verified by the host view.
    """

    site_key: str = field(metadata={"doc": _("Public Turnstile site key. Never use the secret key here.")})
    theme: Literal["auto", "light", "dark"] = field(
        default="auto", metadata={"doc": _("Widget theme: auto, light, or dark.")}
    )
    size: Literal["normal", "flexible", "compact"] = field(
        default="normal", metadata={"doc": _("Widget size: normal, flexible, or compact.")}
    )
    action: str = field(default="", metadata={"doc": _("Optional action identifier verified by the host view.")})

    def __post_init__(self) -> None:
        """Reject invalid widget values before they reach the browser."""
        if not self.site_key.strip():
            raise ValueError("TurnstileConfig requires a public site_key.")  # noqa: TRY003
        if self.theme not in {"auto", "light", "dark"}:
            raise ValueError("TurnstileConfig theme must be auto, light, or dark.")  # noqa: TRY003
        if self.size not in {"normal", "flexible", "compact"}:
            raise ValueError("TurnstileConfig size must be normal, flexible, or compact.")  # noqa: TRY003
        if self.action and not fullmatch(r"[A-Za-z0-9_-]{1,32}", self.action):
            raise ValueError("TurnstileConfig action must be up to 32 letters, digits, _ or -.")  # noqa: TRY003


@dataclass
class FormConfig:
    """Configuration for the form component.

    Renders a complete form with multiple fields and HTMX support.

    Attributes:
        tag_id: Unique ID for the form element.
        title: Form title displayed at the top.
        description: Optional description below the title.
        fields: Field configs rendered in order.
        show_reset_button: Whether to show a reset button.
        submit_label: Label for the submit button.
        reset_label: Label for the reset button.
        request_url: Target URL for form submission.
        method: HTTP method for form submission (get or post).
        htmx_config: HTMX configuration for AJAX submission.
        turnstile: Optional Turnstile widget; the host must verify its token.
        show_loading_indicator: Whether to show the loading indicator of the form during HTMX requests.

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
    fields: list[FormField] = field(default_factory=list, metadata={"doc": _("Field configs rendered in order.")})
    show_reset_button: bool = field(default=False, metadata={"doc": _("Whether to show a reset button.")})
    submit_label: str = field(default="", metadata={"doc": _("Label for the submit button.")})
    reset_label: str = field(default="", metadata={"doc": _("Label for the reset button.")})
    request_url: str = field(default="", metadata={"doc": _("Target URL for form submission.")})
    method: str = field(default="post", metadata={"doc": _("HTTP method for form submission (get or post).")})
    htmx_config: HtmxConfig | None = field(default=None, metadata={"doc": _("HTMX configuration for AJAX submission.")})
    turnstile: TurnstileConfig | None = field(
        default=None, metadata={"doc": _("Optional Turnstile widget; the host must verify its token.")}
    )
    show_loading_indicator: bool = field(
        default=True,
        metadata={"doc": _("Whether to show the loading indicator of the form during HTMX requests.")},
    )

    def __post_init__(self) -> None:
        """Validate the field configs and warn if request_url and htmx_config.request_url are both set."""
        for form_field in self.fields:
            if not isinstance(form_field, FORM_FIELD_CONFIGS):
                supported = ", ".join(config.__name__ for config in FORM_FIELD_CONFIGS)
                raise TypeError(  # noqa: TRY003
                    f"FormConfig fields must be one of {supported}; got {type(form_field).__name__}."
                )
        if self.turnstile is not None:
            if not isinstance(self.turnstile, TurnstileConfig):
                raise TypeError("FormConfig turnstile must be a TurnstileConfig instance.")  # noqa: TRY003
            method = self.htmx_config.method if self.htmx_config else self.method
            if method.lower() != "post":
                raise ValueError("Turnstile-protected forms must submit via POST.")  # noqa: TRY003
        if self.request_url and self.htmx_config and self.htmx_config.request_url:
            identifier = self.tag_id or self.title or "(unnamed)"
            warnings.warn(
                f"FormConfig {identifier} has both 'request_url' and 'htmx_config.request_url' set. "
                "This may cause conflicting behavior. Use 'request_url' for a plain form submission, or "
                "'htmx_config.request_url' for HTMX requests, but not both.",
                UserWarning,
                stacklevel=2,
            )
