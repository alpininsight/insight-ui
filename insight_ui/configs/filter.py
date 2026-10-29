# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Configuration classes for data filter components."""

import warnings
from dataclasses import dataclass, field as dc_field
from typing import Any

from django.utils.translation import gettext_lazy as _

from insight_ui.configs.base import HtmxConfig, IconConfig
from insight_ui.configs.types import (
    FilterFieldType,
    QueryLogic,
    validate_filter_field_type,
    validate_not_empty,
    validate_query_logic,
    validate_urls,
)


@dataclass
class SearchBarConfig:
    """Configuration for the search_bar component.

    Attributes:
        request_url: URL for form action. Do not use together with htmx; use htmx.request_url instead for HTMX requests.
        simple: If True, render compact/minimal style.
        search_query: Initial search query value.
        placeholder: Placeholder text for the search input.
        button_label: Label for the search button.
        htmx: HTMX configuration for AJAX requests.
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
                "URL for form action. Do not use together with htmx; use htmx.request_url instead for HTMX requests."
            )
        },
    )
    simple: bool = dc_field(default=False, metadata={"doc": _("If True, render compact/minimal style.")})
    search_query: str = dc_field(default="", metadata={"doc": _("Initial search query value.")})
    placeholder: str = dc_field(default="", metadata={"doc": _("Placeholder text for the search input.")})
    button_label: str = dc_field(default="", metadata={"doc": _("Label for the search button.")})
    htmx: HtmxConfig | None = dc_field(default=None, metadata={"doc": _("HTMX configuration for AJAX requests.")})
    enable_search: bool = dc_field(
        default=False, metadata={"doc": _("If True, enable client-side documentation search with Fuse.js.")}
    )
    search_index_url: str = dc_field(
        default="",
        metadata={"doc": _("Optional URL for the client-side documentation search index.")},
    )

    def __post_init__(self) -> None:
        """Validate that request_url and htmx.request_url are not both set."""
        validate_urls(self)
        if self.request_url and self.htmx and self.htmx.request_url:
            warnings.warn(
                f"SearchBarConfig ({self.request_url}) has both 'request_url' and 'htmx.request_url' set. "
                "This may cause conflicting behavior. Use 'request_url' for form action, or "
                "'htmx.request_url' for HTMX requests, but not both.",
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
        help_text: Hint shown below the field.
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
    help_text: str = dc_field(default="", metadata={"doc": _("Hint shown below the field.")})
    icon: IconConfig | None = dc_field(default=None, metadata={"doc": _("Optional filter icon.")})
    selected_option: str = dc_field(default="", metadata={"doc": _("Currently selected value.")})

    @property
    def message_id(self) -> str:
        """Id prefix of the help text, taken from the name."""
        return self.name

    def __post_init__(self) -> None:
        """Require a name and validate that selected_option is included in options, if both are set."""
        validate_not_empty(self, "name")
        if self.selected_option and self.options and self.selected_option not in self.options:
            raise ValueError(f"selected_option '{self.selected_option}' must be included in 'options'.")  # noqa: TRY003


@dataclass
class GenericFilterConfig:
    """Configuration for the generic_filter component.

    Renders a filter bar with multiple select elements.

    Attributes:
        filters: List of filter configurations.
        request_url: URL for form action. Do not use together with htmx; use htmx.request_url instead for HTMX requests.
        vertical: If True, arrange filters vertically.
        htmx: HTMX configuration for AJAX requests.

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
            htmx=HtmxConfig(target="#results", swap_method="innerHTML"),
        )
        """

    filters: list[FilterConfig] = dc_field(default_factory=list, metadata={"doc": _("List of filter configurations.")})
    request_url: str = dc_field(
        default="",
        metadata={
            "doc": _(
                "URL for form action. Do not use together with htmx; use htmx.request_url instead for HTMX requests."
            )
        },
    )
    vertical: bool = dc_field(default=False, metadata={"doc": _("If True, arrange filters vertically.")})
    htmx: HtmxConfig | None = dc_field(default=None, metadata={"doc": _("HTMX configuration for AJAX requests.")})

    def __post_init__(self) -> None:
        """Validate that request_url and htmx.request_url are not both set."""
        validate_urls(self)
        if self.request_url and self.htmx and self.htmx.request_url:
            warnings.warn(
                f"GenericFilterConfig ({self.request_url}) has both 'request_url' and 'htmx.request_url' set. "
                "This may cause conflicting behavior. Use 'request_url' for form action, or "
                "'htmx.request_url' for HTMX requests, but not both.",
                UserWarning,
                stacklevel=2,
            )


@dataclass
class QueryBuilderFieldConfig:
    """Configuration for a field in the query builder.

    Attributes:
        field: Model field or lookup path, e.g. "author__name".
        label: Display name.
        type: Field type; selects the value input.
        operations: Allowed lookups, mapped to their labels.
        values: Allowed values, mapped to their labels; renders a select.

    """

    __example__ = """
        QueryBuilderFieldConfig(
            field="title",
            label="Title",
            type="text",
            operations={
                "iexact": "is exactly",
                "icontains": "contains",
                "istartswith": "starts with",
            },
        )
        """

    field: str = dc_field(metadata={"doc": _('Model field or lookup path, e.g. "author__name".')})
    label: str = dc_field(metadata={"doc": _("Display name.")})
    type: FilterFieldType = dc_field(default="text", metadata={"doc": _("Field type; selects the value input.")})
    operations: dict[str, str] = dc_field(
        default_factory=dict, metadata={"doc": _("Allowed lookups, mapped to their labels.")}
    )
    values: dict[str, str] = dc_field(
        default_factory=dict, metadata={"doc": _("Allowed values, mapped to their labels; renders a select.")}
    )

    def __post_init__(self) -> None:
        """Require a field name and operations and validate the type."""
        validate_not_empty(self, "field", "operations")
        validate_filter_field_type(self.type, "type")
        if self.type == "choice" and not self.values:
            msg = f"QueryBuilderFieldConfig {self.field!r} of type 'choice' needs values."
            raise ValueError(msg)


@dataclass
class QueryBuilderFilterConfig:
    """An active filter of the query builder.

    Attributes:
        field: Field name of a QueryBuilderFieldConfig.
        operator: Lookup of the field, e.g. "icontains".
        value: Value to compare with.
        logic: Combination with the previous filter.

    """

    __example__ = """
        QueryBuilderFilterConfig(field="title", operator="icontains", value="report", logic="AND")
        """

    field: str = dc_field(metadata={"doc": _("Field name of a QueryBuilderFieldConfig.")})
    operator: str = dc_field(metadata={"doc": _('Lookup of the field, e.g. "icontains".')})
    value: Any = dc_field(default="", metadata={"doc": _("Value to compare with.")})
    logic: QueryLogic = dc_field(default="AND", metadata={"doc": _("Combination with the previous filter.")})

    def __post_init__(self) -> None:
        """Validate the logic."""
        validate_query_logic(self.logic, "logic")


@dataclass
class QueryBuilderConfig:
    """Configuration for the query_builder component.

    Renders a form to combine filters on model fields. Read the submitted filters with
    insight_ui.utils.query_builder.parse_filters and turn them into a Q object with build_query.

    Attributes:
        tag_id: Unique ID; prefixes the IDs of the filter controls.
        fields: Fields that can be filtered.
        filters: Active filters, rendered as filter rows.
        request_url: URL the form is sent to; empty sends it to the current page.
        param_name: Prefix of the submitted query parameters.
        max_filters: Maximum number of filters; parse_filters ignores further ones.
        htmx: HTMX configuration for sending the form without a page load.
        show_summary: If True, show the active filters as a sentence below the form.

    """

    __example__ = """
        QueryBuilderConfig(
            tag_id="book-filter",
            fields=[
                QueryBuilderFieldConfig(
                    field="title",
                    label="Title",
                    type="text",
                    operations={"iexact": "is exactly", "icontains": "contains"},
                ),
                QueryBuilderFieldConfig(
                    field="published",
                    label="Published",
                    type="date",
                    operations={"gte": "on or after", "lte": "on or before"},
                ),
            ],
        )
        """

    tag_id: str = dc_field(
        default="query-builder", metadata={"doc": _("Unique ID; prefixes the IDs of the filter controls.")}
    )
    fields: list[QueryBuilderFieldConfig] = dc_field(
        default_factory=list, metadata={"doc": _("Fields that can be filtered.")}
    )
    filters: list[QueryBuilderFilterConfig] = dc_field(
        default_factory=list, metadata={"doc": _("Active filters, rendered as filter rows.")}
    )
    request_url: str = dc_field(
        default="", metadata={"doc": _("URL the form is sent to; empty sends it to the current page.")}
    )
    param_name: str = dc_field(default="filters", metadata={"doc": _("Prefix of the submitted query parameters.")})
    max_filters: int = dc_field(
        default=20, metadata={"doc": _("Maximum number of filters; parse_filters ignores further ones.")}
    )
    htmx: HtmxConfig | None = dc_field(
        default=None, metadata={"doc": _("HTMX configuration for sending the form without a page load.")}
    )
    show_summary: bool = dc_field(
        default=False, metadata={"doc": _("If True, show the active filters as a sentence below the form.")}
    )

    def __post_init__(self) -> None:
        """Require an ID and a parameter name; reject a request_url with a scheme that is not allowed."""
        validate_urls(self)
        validate_not_empty(self, "tag_id", "param_name")
        if self.max_filters < 1:
            msg = f"QueryBuilderConfig {self.tag_id!r} needs max_filters of at least 1."
            raise ValueError(msg)
