"""Configuration classes for data filter components."""

from dataclasses import dataclass, field as dc_field
from typing import Literal

from django.utils.translation import gettext_lazy as _

from insight_ui.configs.base import HtmxConfig, IconConfig


@dataclass
class SearchBarConfig:
    """
    Configuration for the search_bar component.

    Attributes:
        request_url: URL for search requests.
        simple: If True, render compact/minimal style.
        search_query: Initial search query value.
        htmx_config: HTMX configuration for AJAX requests.

    """

    __example__ = """
        SearchBarConfig(
            request_url="/search_products/",
            simple=False,
        )
        """

    request_url: str = dc_field(metadata={"doc": _("URL for search requests.")})
    simple: bool = dc_field(default=False, metadata={"doc": _("If True, render compact/minimal style.")})
    search_query: str = dc_field(default="", metadata={"doc": _("Initial search query value.")})
    htmx_config: HtmxConfig | None = dc_field(
        default=None, metadata={"doc": _("HTMX configuration for AJAX requests.")}
    )


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

    __example__ = """
        FilterConfig(
            name="status",
            label="Status",
            options={"": "All", "active": "Active", "inactive": "Inactive"},
        )
        """

    name: str = dc_field(metadata={"doc": _("Filter field name.")})
    label: str = dc_field(default="", metadata={"doc": _("Filter label.")})
    options: dict[str, str] = dc_field(
        default_factory=dict, metadata={"doc": _("Available filter options (dict maps value→label).")}
    )
    explanation: str = dc_field(default="", metadata={"doc": _("Tooltip explanation text.")})
    icon: IconConfig | None = dc_field(default=None, metadata={"doc": _("Optional filter icon.")})
    selected_option: str = dc_field(default="", metadata={"doc": _("Currently selected value.")})


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

    """

    __example__ = """
        GenericFilterConfig(
            filters=[
                FilterConfig(
                    name="status",
                    label="Status",
                    options={"": "All", "active": "Active", "inactive": "Inactive"},
                ),
                FilterConfig(
                    name="category",
                    label="Category",
                    options={"": "All", "tech": "Technology", "science": "Science"},
                ),
            ],
            htmx_config=HtmxConfig(target="#results", swap="innerHTML"),
        )
        """

    filters: list[FilterConfig] = dc_field(default_factory=list, metadata={"doc": _("List of filter configurations.")})
    request_url: str = dc_field(default="", metadata={"doc": _("URL for filter requests.")})
    vertical: bool = dc_field(default=False, metadata={"doc": _("If True, arrange filters vertically.")})
    htmx_config: HtmxConfig | None = dc_field(
        default=None, metadata={"doc": _("HTMX configuration for AJAX requests.")}
    )


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

    """

    __example__ = """
        QueryBuilderFieldConfig(
            field="title",
            label="Title",
            type="text",
            operations={
                "iexact": "is exact",
                "icontains": "contains",
                "istartswith": "starts with",
            },
        )
        """

    field: str = dc_field(metadata={"doc": _("Database field name.")})
    label: str = dc_field(metadata={"doc": _("Display name.")})
    type: Literal["text", "date", "number"] = dc_field(
        default="text", metadata={"doc": _("Field type (text, date, number).")}
    )
    operations: dict[str, str] = dc_field(
        default_factory=dict, metadata={"doc": _("Available operations (maps operation→label).")}
    )
    values: dict[str, str] = dc_field(default_factory=dict, metadata={"doc": _("Predefined values (optional).")})


@dataclass
class QueryBuilderConfig:
    """
    Configuration for the query_builder component.

    Renders a filter for constructing custom search queries.

    Attributes:
        model_fields: List of model fields with possible operators.

    """

    __example__ = """
        QueryBuilderConfig(
            model_fields=[
                QueryBuilderFieldConfig(
                    field="title",
                    label="Title",
                    type="text",
                    operations={"iexact": "is exact", "icontains": "contains"},
                ),
                QueryBuilderFieldConfig(
                    field="created_at",
                    label="Created At",
                    type="date",
                    operations={"gte": "after", "lte": "before"},
                ),
            ],
        )
        """

    model_fields: list[QueryBuilderFieldConfig] = dc_field(
        default_factory=list, metadata={"doc": _("List of model fields with possible operators.")}
    )
