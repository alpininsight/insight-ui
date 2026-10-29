# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Configuration classes for data display components."""

from dataclasses import dataclass, field
from typing import Any

from django.core.paginator import Page
from django.utils.translation import gettext_lazy as _

from insight_ui.configs.base import HtmxConfig
from insight_ui.configs.types import HeadingLevel, validate_heading_level, validate_not_empty, validate_urls


@dataclass
class InfiniteScrollConfig:
    """Configuration for the infinite_scroll component.

    Renders a container that loads more content on scroll.

    Attributes:
        request_url: URL for loading more items.
        tag_id: Unique ID for JavaScript/CSS targeting.
        items: Initial items to display.
        page: Current page number.
        has_next: Whether more items are available.
        auto_fetch: If True, auto-load on scroll. If False, show button.
        threshold: Pixel threshold before loading more.
        heading_level: Heading level of the item titles.

    """

    __example__ = """
        InfiniteScrollConfig(
            request_url=reverse("news_list"),
            tag_id="news-feed",
            items=initial_items,
            page=1,
            has_next=True,
            auto_fetch=True,
            threshold=200,
        )
        """

    request_url: str = field(metadata={"doc": _("URL for loading more items.")})
    tag_id: str = field(default="", metadata={"doc": _("Unique ID for JavaScript/CSS targeting.")})
    items: list[Any] = field(default_factory=list, metadata={"doc": _("Initial items to display.")})
    page: int = field(default=1, metadata={"doc": _("Current page number.")})
    has_next: bool = field(default=True, metadata={"doc": _("Whether more items are available.")})
    auto_fetch: bool = field(default=True, metadata={"doc": _("If True, auto-load on scroll. If False, show button.")})
    threshold: int = field(default=100, metadata={"doc": _("Pixel threshold before loading more.")})
    heading_level: HeadingLevel = field(default=3, metadata={"doc": _("Heading level of the item titles.")})

    def __post_init__(self) -> None:
        """Reject an empty request_url and validate heading_level."""
        validate_urls(self)
        validate_not_empty(self, "request_url")
        validate_heading_level(self.heading_level)


@dataclass
class PaginationIppConfig:
    """Configuration for items-per-page selector in pagination.

    Attributes:
        name: Form field name.
        label: Selector label.
        options: Available page size options.
        selected_option: Currently selected value.

    """

    __example__ = """
        PaginationIppConfig(
            name="ipp",
            label="Items per Page",
            options=[10, 20, 30],
            selected_option=10,
        )
        """

    name: str = field(default="ipp", metadata={"doc": _("Form field name.")})
    label: str = field(default="Items per page", metadata={"doc": _("Selector label.")})
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
class PaginationConfig:
    """Configuration for the pagination component.

    Renders links to the neighboring pages and an optional page size selector. Without ``htmx`` the links load
    the whole page; with ``htmx`` they swap the result into the target. For an API that pages itself and only
    reports the total, pass ``Paginator(range(total), items_per_page).get_page(page)``.

    Attributes:
        request_url: URL of the list; the page parameter is added to its query string.
        current_page: Django Page object of the current page.
        tag_id: Unique ID, prefixes the IDs inside the pagination.
        htmx: Optional HTMX request for the page links and the page size selector.
        include: CSS selector of further fields sent with HTMX requests, e.g. a filter form.
        page_param: Name of the query parameter for the page number.
        on_each_side: Number of pages shown on each side of the current page.
        on_ends: Number of pages shown at the start and end.
        items_per_page: Optional configuration for the items-per-page selector.

    """

    __example__ = """
        PaginationConfig(
            request_url="/product-list/?q=chair",
            current_page=Paginator(products, 10).get_page(request.GET.get("page")),
            htmx=HtmxConfig(target="#product-list", push_url=True),
            include="#product-filter",
            items_per_page=PaginationIppConfig(options=[10, 25, 50]),
        )
        """

    request_url: str = field(metadata={"doc": _("URL of the list; the page parameter is added to its query string.")})
    current_page: Page = field(metadata={"doc": _("Django Page object of the current page.")})
    tag_id: str = field(default="pagination", metadata={"doc": _("Unique ID, prefixes the IDs inside the pagination.")})
    htmx: HtmxConfig | None = field(
        default=None, metadata={"doc": _("Optional HTMX request for the page links and the page size selector.")}
    )
    include: str = field(
        default="",
        metadata={"doc": _("CSS selector of further fields sent with HTMX requests, e.g. a filter form.")},
    )
    page_param: str = field(default="page", metadata={"doc": _("Name of the query parameter for the page number.")})
    on_each_side: int = field(default=2, metadata={"doc": _("Number of pages shown on each side of the current page.")})
    on_ends: int = field(default=1, metadata={"doc": _("Number of pages shown at the start and end.")})
    items_per_page: PaginationIppConfig | None = field(
        default=None, metadata={"doc": _("Optional configuration for the items-per-page selector.")}
    )

    def __post_init__(self) -> None:
        """Reject empty values and HTMX requests without a swap target."""
        validate_urls(self)
        validate_not_empty(self, "request_url", "tag_id", "page_param")
        if self.htmx is not None and not self.htmx.target.strip():
            raise ValueError(  # noqa: TRY003
                "PaginationConfig.htmx needs a target, e.g. the element that contains the paginated results."
            )


@dataclass
class TableConfig:
    """Configuration for the table component.

    Renders a simple data table.

    Attributes:
        headers: List of column header texts.
        rows: List of row data (each row is a list of cell values).
        caption: Optional table caption.
        empty_text: Message shown when no data available.

    """

    __example__ = """
        TableConfig(
            caption="User List",
            headers=["Name", "Email", "Status"],
            rows=[
                ["John Doe", "john@example.com", "Active"],
                ["Jane Smith", "jane@example.com", "Inactive"],
            ],
            empty_text="No users found.",
        )
        """

    headers: list[str] = field(default_factory=list, metadata={"doc": _("List of column header texts.")})
    rows: list[list[str]] = field(
        default_factory=list, metadata={"doc": _("List of row data (each row is a list of cell values).")}
    )
    caption: str = field(default="", metadata={"doc": _("Optional table caption.")})
    empty_text: str = field(
        default=_("No data available."), metadata={"doc": _("Message shown when no data available.")}
    )
