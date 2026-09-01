"""Configuration classes for popup components."""

from dataclasses import dataclass, field

from django.utils.translation import gettext_lazy as _

from insight_ui.configs.input import ButtonConfig
from insight_ui.configs.types import AlertType, validate_alert_type


@dataclass
class AnnouncementConfig:
    """Configuration for a site-wide announcement bar.

    Renders a concise, non-dismissible message above the application
    navigation. An optional link lets each consumer provide its own call to
    action while preserving a consistent semantic structure.

    Attributes:
        tag_id: Optional unique HTML ID for the announcement landmark.
        message: The announcement message.
        link_label: Visible label for the optional link.
        link_url: Destination for the optional link.
        aria_label: Accessible name for the announcement landmark.

    """

    __example__ = """
        AnnouncementConfig(
            message="This service is in beta.",
            link_label="Contact us",
            link_url="mailto:contact@example.com",
        )
    """

    tag_id: str = field(default="", metadata={"doc": _("Optional unique HTML ID for the announcement landmark.")})
    message: str = field(default="", metadata={"doc": _("The announcement message.")})
    link_label: str = field(default="", metadata={"doc": _("Visible label for the optional link.")})
    link_url: str = field(default="", metadata={"doc": _("Destination for the optional link.")})
    aria_label: str = field(default="", metadata={"doc": _("Accessible name for the announcement landmark.")})


@dataclass
class AlertConfig:
    """Configuration for the alert component.

    Renders a notification/alert box.

    Attributes:
        tag_id: Optional, unique tag ID for identifying the element in JavaScript.
        message: Message displayed in the alert.
        type: Type of the alert.
        dismissible: Shows a button to close the alert at the end of the alert container.

    """

    __example__ = """
        AlertConfig(
            message="Your changes have been saved successfully!",
            type="success",
            dismissible=True,
        )
        """

    tag_id: str = field(
        default="", metadata={"doc": _("Optional, unique tag ID for identifying the element in JavaScript.")}
    )
    message: str = field(default="", metadata={"doc": _("Message displayed in the alert.")})
    type: AlertType = field(default="info", metadata={"doc": _("Type of the alert.")})
    dismissible: bool = field(
        default=True, metadata={"doc": _("Shows a button to close the alert at the end of the alert container.")}
    )

    def __post_init__(self) -> None:
        """Validate type after initialization."""
        validate_alert_type(self.type, "type")


@dataclass
class ModalConfig:
    """Configuration for the modal component.

    Renders an accessible modal dialog.

    Attributes:
        tag_id: Optional, unique tag ID for identifying the element in JavaScript.
        title: Heading of the modal dialog.
        description: A text in the center of the modal dialog. This can be exchanged by extending the template.
        actions: List of buttons displayed at the bottom of the dialog.
        width: The maximum width of the dialog box relative to the screen in 'rem'.

    """

    __example__ = """
        ModalConfig(
            tag_id="delete-confirm",
            title="Confirm Deletion",
            description="Are you sure you want to delete this item? This action cannot be undone.",
            actions=[
                ButtonConfig(label="Delete", type="danger", on_click="deleteItem()"),
                ButtonConfig(label="Cancel", type="secondary", data_attrs=[DataAttrConfig("insight-dismiss", "modal")]),
            ],
            width=24,
        )
        """

    tag_id: str = field(metadata={"doc": _("Optional, unique tag ID for identifying the element in JavaScript.")})
    title: str = field(metadata={"doc": _("Heading of the modal dialog.")})
    description: str | list[str] = field(
        default="",
        metadata={
            "doc": _("A text in the center of the modal dialog. This can be exchanged by extending the template.")
        },
    )
    actions: list[ButtonConfig] = field(
        default_factory=list, metadata={"doc": _("List of buttons displayed at the bottom of the dialog.")}
    )
    width: int = field(
        default=32, metadata={"doc": _("The maximum width of the dialog box relative to the screen in 'rem'.")}
    )
