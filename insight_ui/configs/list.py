"""Configuration classes for data display components."""

from dataclasses import dataclass, field
from typing import Any

from django.utils.translation import gettext_lazy as _


@dataclass
class InfiniteScrollConfig:
    """
    Configuration for the infinite_scroll component.

    Renders a container that loads more content on scroll.

    Attributes:
        tag_id: Unique ID for JavaScript/CSS targeting.
        request_url: URL for loading more items.
        items: Initial items to display.
        page: Current page number.
        has_next: Whether more items are available.
        auto_fetch: If True, auto-load on scroll. If False, show button.
        threshold: Pixel threshold before loading more.

    """

    __example__ = """
        InfiniteScrollConfig(
            tag_id="news-feed",
            request_url=reverse("news_list"),
            items=initial_items,
            page=1,
            has_next=True,
            auto_fetch=True,
            threshold=200,
        )
        """

    tag_id: str = field(default="", metadata={"doc": _("Unique ID for JavaScript/CSS targeting.")})
    request_url: str = field(default="", metadata={"doc": _("URL for loading more items.")})
    items: list[Any] = field(default_factory=list, metadata={"doc": _("Initial items to display.")})
    page: int = field(default=1, metadata={"doc": _("Current page number.")})
    has_next: bool = field(default=True, metadata={"doc": _("Whether more items are available.")})
    auto_fetch: bool = field(default=True, metadata={"doc": _("If True, auto-load on scroll. If False, show button.")})
    threshold: int = field(default=100, metadata={"doc": _("Pixel threshold before loading more.")})


@dataclass
class PaginationIppConfig:
    """
    Configuration for items-per-page selector in pagination.

    Attributes:
        name: Form field name.
        label: Selector label.
        explanation: Tooltip explanation text.
        options: Available page size options.
        selected_option: Currently selected value.

    """

    name: str = field(default="ipp", metadata={"doc": _("Form field name.")})
    label: str = field(default="Items per page", metadata={"doc": _("Selector label.")})
    explanation: str = field(default="", metadata={"doc": _("Tooltip explanation text.")})
    options: list[int] = field(
        default_factory=lambda: [10, 20, 30], metadata={"doc": _("Available page size options.")}
    )
    selected_option: int | None = field(default=None, metadata={"doc": _("Currently selected value.")})

    def __post_init__(self) -> None:
        """Check whether 'selected_option' is included in 'options'."""
        if self.selected_option is None:
            self.selected_option = self.options[0]

        if self.selected_option not in self.options:
            raise ValueError("'selected_option' must be included in 'options'.")  # noqa: TRY003


@dataclass
class TableConfig:
    """
    Configuration for the table component.

    Renders a simple data table.

    Attributes:
        headers: List of column header texts.
        rows: List of row data (each row is a list of cell values).
        caption: Optional table caption.
        empty_msg: Message shown when no data available.

    """

    __example__ = """
        TableConfig(
            caption="User List",
            headers=["Name", "Email", "Status"],
            rows=[
                ["John Doe", "john@example.com", "Active"],
                ["Jane Smith", "jane@example.com", "Inactive"],
            ],
            empty_msg="No users found.",
        )
        """

    headers: list[str] = field(default_factory=list, metadata={"doc": _("List of column header texts.")})
    rows: list[list[str]] = field(
        default_factory=list, metadata={"doc": _("List of row data (each row is a list of cell values).")}
    )
    caption: str = field(default="", metadata={"doc": _("Optional table caption.")})
    empty_msg: str = field(
        default=_("No data available."), metadata={"doc": _("Message shown when no data available.")}
    )
