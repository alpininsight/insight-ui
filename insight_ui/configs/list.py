"""Configuration classes for data display components."""

from dataclasses import dataclass, field
from typing import Any

from django.utils.translation import gettext as _


@dataclass
class InfiniteScrollConfig:
    """
    Configuration for the infinite_scroll component.

    Renders a container that loads more content on scroll.

    Attributes:
        tag_id: Unique ID for JavaScript/CSS targeting.
        request_url: Url for loading more items.
        items: Initial items to display.
        page: Current page number.
        has_next: Whether more items are available.
        auto_fetch: If True, auto-load on scroll. If False, show button.
        threshold: Pixel threshold before loading more.

    Example:
        >>> feed = InfiniteScrollConfig(
        ...     tag_id="news-feed",
        ...     request_url=reverse("news_list"),
        ...     items=initial_items,
        ...     page=1,
        ...     has_next=True,
        ...     auto_fetch=True,
        ...     threshold=200,
        ... )

    """

    tag_id: str = ""
    request_url: str = ""
    items: list[Any] = field(default_factory=list)
    page: int = 1
    has_next: bool = True
    auto_fetch: bool = True
    threshold: int = 100


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

    name: str = "ipp"
    label: str = "Items per page"
    explanation: str = ""
    options: list[int] = field(default_factory=lambda: [10, 20, 30])
    selected_option: int | None = None

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

    Example:
        >>> users_table = TableConfig(
        ...     caption="User List",
        ...     headers=["Name", "Email", "Status"],
        ...     rows=[
        ...         ["John Doe", "john@example.com", "Active"],
        ...         ["Jane Smith", "jane@example.com", "Inactive"],
        ...     ],
        ...     empty_msg="No users found.",
        ... )

    """

    headers: list[str] = field(default_factory=list)
    rows: list[list[str]] = field(default_factory=list)
    caption: str = ""
    empty_msg: str = _("No data available.")
