"""Configuration classes for data filter components."""

from dataclasses import dataclass, field
from typing import Literal

from insight_ui.configs.base import HtmxConfig, IconConfig


@dataclass
class SearchBarConfig:
    """
    Configuration for the search_bar component.

    Attributes:
        request_url: Url for search requests.
        simple: If True, render compact/minimal style.
        search_query: Initial search query value.
        htmx_config: HTMX configuration for AJAX requests.

    """

    request_url: str
    simple: bool = False
    search_query: str = ""
    htmx_config: HtmxConfig | None = None


@dataclass
class FilterConfig:
    """
    Configuration for a single filter in generic_filter.

    Attributes:
        name: Filter field name.
        label: Filter label.
        options: Available filter options (dict maps value→label).
        explanation: Tooltip explanation text.
        icon: Optional filter icon.
        selected_option: Currently selected value.

    """

    name: str
    label: str = ""
    options: dict[str, str] = field(default_factory=dict)
    explanation: str = ""
    icon: IconConfig | None = None
    selected_option: str = ""


@dataclass
class GenericFilterConfig:
    """
    Configuration for the generic_filter component.

    Renders a filter bar with multiple select elements.

    Attributes:
        filters: List of filter configurations.
        request_url: URL for filter requests.
        vertical: If True, arrange filters vertically.
        htmx_config: HTMX configuration for AJAX requests.

    Example:
        >>> filter_bar = GenericFilterConfig(
        ...     filters=[
        ...         FilterConfig(
        ...             name="status",
        ...             label="Status",
        ...             options={"": "All", "active": "Active", "inactive": "Inactive"},
        ...         ),
        ...         FilterConfig(
        ...             name="category",
        ...             label="Category",
        ...             options={"": "All", "tech": "Technology", "science": "Science"},
        ...         ),
        ...     ],
        ...     htmx_config=HtmxConfig(target="#results", swap="innerHTML"),
        ... )

    """

    filters: list[FilterConfig] = field(default_factory=list)
    request_url: str = ""
    vertical: bool = False
    htmx_config: HtmxConfig | None = None


@dataclass
class QueryBuilderFieldConfig:
    """
    Configuration for a field in the query builder.

    Attributes:
        field: Database field name.
        label: Display name.
        type: Field type (text, date, number).
        operations: Available operations (maps operation→label).
        values: Predefined values (optional).

    Example:
        >>> title_field = QueryBuilderFieldConfig(
        ...     field="title",
        ...     label="Title",
        ...     type="text",
        ...     operations={
        ...         "iexact": "is exact",
        ...         "icontains": "contains",
        ...         "istartswith": "starts with",
        ...     },
        ... )

    """

    field: str
    label: str
    type: Literal["text", "date", "number"] = "text"
    operations: dict[str, str] = field(default_factory=dict)
    values: dict[str, str] = field(default_factory=dict)
