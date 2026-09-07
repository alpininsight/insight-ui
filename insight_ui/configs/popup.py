"""Configuration classes for popup components."""

from dataclasses import dataclass, field

from django.utils.translation import gettext_lazy as _

from insight_ui.configs.types import AlertType, validate_alert_type


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
