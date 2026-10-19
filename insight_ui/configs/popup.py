# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Configuration classes for popup components."""

from dataclasses import dataclass, field

from django.utils.translation import gettext_lazy as _

from insight_ui.configs.input import ButtonConfig
from insight_ui.configs.layout import ModalConfig
from insight_ui.configs.types import Severity, validate_not_empty, validate_severity


@dataclass
class AlertConfig:
    """Configuration for the alert component.

    Renders a notification/alert box.

    Attributes:
        tag_id: Optional, unique tag ID for identifying the element in JavaScript.
        message: Message displayed in the alert.
        severity: Severity of the alert.
        dismissible: Shows a button to close the alert at the end of the alert container.

    """

    __example__ = """
        AlertConfig(
            message="Your changes have been saved successfully!",
            severity="success",
            dismissible=True,
        )
        """

    tag_id: str = field(
        default="", metadata={"doc": _("Optional, unique tag ID for identifying the element in JavaScript.")}
    )
    message: str = field(default="", metadata={"doc": _("Message displayed in the alert.")})
    severity: Severity = field(default="info", metadata={"doc": _("Severity of the alert.")})
    dismissible: bool = field(
        default=True, metadata={"doc": _("Shows a button to close the alert at the end of the alert container.")}
    )

    def __post_init__(self) -> None:
        """Validate severity after initialization."""
        validate_severity(self.severity)


@dataclass
class MessageDialogConfig(ModalConfig):
    """Configuration for the message_dialog component.

    A modal dialog with a predefined message and action buttons, e.g. an about box or a confirmation.
    Without actions, a close button is shown. For arbitrary content use the modal block tag instead.

    Attributes:
        id: Unique ID for JavaScript targeting (data-insight-modal).
        title: Optional heading displayed in the modal header.
        width: Maximum width in rem units.
        show_close: Show the close button in the header.
        message: Text of the dialog, or a list of paragraphs.
        actions: Buttons at the bottom of the dialog.
        alert: Whether the dialog asks for a decision, e.g. a confirmation (role "alertdialog").

    """

    __example__ = """
        MessageDialogConfig(
            id="confirm-delete",
            title="Delete project?",
            message="The project and all its data will be deleted. This cannot be undone.",
            alert=True,
            actions=[
                ButtonConfig(label="Cancel", type="secondary", data_attrs=[DataAttrConfig("insight-dismiss", "modal")]),
                ButtonConfig(label="Delete", type="danger", htmx_config=HtmxConfig("/projects/7/delete/", method="post")),
            ],
        )
        """

    message: str | list[str] = field(default="", metadata={"doc": _("Text of the dialog, or a list of paragraphs.")})
    actions: list[ButtonConfig] = field(
        default_factory=list,
        metadata={"doc": _("Buttons at the bottom of the dialog.")},
    )
    alert: bool = field(
        default=False,
        metadata={"doc": _('Whether the dialog asks for a decision, e.g. a confirmation (role "alertdialog").')},
    )

    def __post_init__(self) -> None:
        """Require an ID and a message."""
        super().__post_init__()
        validate_not_empty(self, "message")
