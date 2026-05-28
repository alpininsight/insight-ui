"""Configuration classes for popup components."""

from dataclasses import dataclass, field
from typing import Literal

from insight_ui.configs.base import ActionConfig


@dataclass
class AlertConfig:
    """
    Configuration for the alert component.

    Renders a notification/alert box.

    Attributes:
        tag_id: Unique ID for JavaScript/CSS targeting.
        message: Alert message text.
        type: Alert type/severity.
        dismissible: Whether alert can be closed.

    Example:
        >>> success_alert = AlertConfig(
        ...     message="Your changes have been saved successfully!",
        ...     type="success",
        ...     dismissible=True,
        ... )

    """

    tag_id: str = ""
    message: str = ""
    type: Literal["info", "success", "warning", "error"] = "info"
    dismissible: bool = True


@dataclass
class ModalConfig:
    """
    Configuration for the modal component.

    Renders an accessible modal dialog.

    Attributes:
        tag_id: Unique ID for the modal (required for triggering).
        title: Modal title.
        description: Modal description (string or list of paragraphs).
        actions: List of action buttons.
        width: Maximum width in rem.

    Example:
        >>> confirm_modal = ModalConfig(
        ...     tag_id="delete-confirm",
        ...     title="Confirm Deletion",
        ...     description="Are you sure you want to delete this item? This action cannot be undone.",
        ...     actions=[
        ...         ActionConfig(text="Delete", type="danger", onclick="deleteItem()"),
        ...         ActionConfig(text="Cancel", type="cancel", dismiss=True),
        ...     ],
        ...     width=24,
        ... )

    """

    tag_id: str
    title: str
    description: str | list[str] = ""
    actions: list[ActionConfig] = field(default_factory=list)
    width: int = 32
