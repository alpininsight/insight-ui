"""Configuration classes for data filter components."""

import warnings
from dataclasses import dataclass, field as dc_field

from django.utils.translation import gettext_lazy as _

from insight_ui.configs.base import HtmxConfig, IconConfig
from insight_ui.configs.types import FilterFieldType, validate_filter_field_type


@dataclass
class SearchBarConfig:
    """Configuration for the search_bar component.

    Attributes:
        request_url: URL for form action. Do not use together with htmx_config; use htmx_config.request_url instead for HTMX requests.
        simple: If True, render compact/minimal style.
        search_query: Initial search query value.
        placeholder: Placeholder text for the search input.
        button_label: Label for the search button.
        htmx_config: HTMX configuration for AJAX requests.
        enable_search: If True, enable client-side documentation search with Fuse.js.
        search_index_url: Optional URL for the client-side documentation search index.

    """

    __example__ = """
        SearchBarConfig(
            request_url="/search_products/",
            placeholder="Search products...",
            button_label="Find",
            simple=False,
        )
        """

    request_url: str = dc_field(
        default="",
        metadata={
            "doc": _(
                "URL for form action. Do not use together with htmx_config; "
                "use htmx_config.request_url instead for HTMX requests."
            )
        },
    )
    simple: bool = dc_field(default=False, metadata={"doc": _("If True, render compact/minimal style.")})
    search_query: str = dc_field(default="", metadata={"doc": _("Initial search query value.")})
    placeholder: str = dc_field(default="", metadata={"doc": _("Placeholder text for the search input.")})
    button_label: str = dc_field(default="", metadata={"doc": _("Label for the search button.")})
    htmx_config: HtmxConfig | None = dc_field(
        default=None, metadata={"doc": _("HTMX configuration for AJAX requests.")}
    )
    enable_search: bool = dc_field(
        default=False, metadata={"doc": _("If True, enable client-side documentation search with Fuse.js.")}
    )
    search_index_url: str = dc_field(
        default="",
        metadata={"doc": _("Optional URL for the client-side documentation search index.")},
    )

    def __post_init__(self) -> None:
        """Validate that request_url and htmx_config.request_url are not both set."""
        if self.request_url and self.htmx_config and self.htmx_config.request_url:
            warnings.warn(
                f"SearchBarConfig ({self.request_url}) has both 'request_url' and 'htmx_config.request_url' set. "
                "This may cause conflicting behavior. Use 'request_url' for form action, or "
                "'htmx_config.request_url' for HTMX requests, but not both.",
                UserWarning,
                stacklevel=2,
            )


@dataclass
class FilterConfig:
    """Configuration for a single filter in generic_filter.

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

    def __post_init__(self) -> None:
        """Validate that selected_option is included in options, if both are set."""
        if self.selected_option and self.options and self.selected_option not in self.options:
            raise ValueError(f"selected_option '{self.selected_option}' must be included in 'options'.")  # noqa: TRY003


@dataclass
class GenericFilterConfig:
    """Configuration for the generic_filter component.

    Renders a filter bar with multiple select elements.

    Attributes:
        filters: List of filter configurations.
        request_url: URL for form action. Do not use together with htmx_config; use htmx_config.request_url instead for HTMX requests.
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
            htmx_config=HtmxConfig(target="#results", swap_method="innerHTML"),
        )
        """

    filters: list[FilterConfig] = dc_field(default_factory=list, metadata={"doc": _("List of filter configurations.")})
    request_url: str = dc_field(
        default="",
        metadata={
            "doc": _(
                "URL for form action. Do not use together with htmx_config; "
                "use htmx_config.request_url instead for HTMX requests."
            )
        },
    )
    vertical: bool = dc_field(default=False, metadata={"doc": _("If True, arrange filters vertically.")})
    htmx_config: HtmxConfig | None = dc_field(
        default=None, metadata={"doc": _("HTMX configuration for AJAX requests.")}
    )

    def __post_init__(self) -> None:
        """Validate that request_url and htmx_config.request_url are not both set."""
        if self.request_url and self.htmx_config and self.htmx_config.request_url:
            warnings.warn(
                f"GenericFilterConfig ({self.request_url}) has both 'request_url' and 'htmx_config.request_url' set. "
                "This may cause conflicting behavior. Use 'request_url' for form action, or "
                "'htmx_config.request_url' for HTMX requests, but not both.",
                UserWarning,
                stacklevel=2,
            )


@dataclass
class QueryBuilderFieldConfig:
    """Configuration for a field in the query builder.

    Attributes:
        field: Database field name.
        label: Display name.
        type: Field type for filtering.
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
    type: FilterFieldType = dc_field(default="text", metadata={"doc": _("Field type for filtering.")})
    operations: dict[str, str] = dc_field(
        default_factory=dict, metadata={"doc": _("Available operations (maps operation→label).")}
    )
    values: dict[str, str] = dc_field(default_factory=dict, metadata={"doc": _("Predefined values (optional).")})

    def __post_init__(self) -> None:
        """Validate type after initialization."""
        validate_filter_field_type(self.type, "type")


@dataclass
class QueryBuilderConfig:
    """Configuration for the query_builder component.

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
