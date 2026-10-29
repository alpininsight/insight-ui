# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for reading query builder filters and turning them into a Django query."""

import zoneinfo
from datetime import date, datetime, time
from decimal import Decimal

import pytest
from django.db.models import Q
from django.http import QueryDict
from django.test import override_settings
from django.utils import translation
from insight_ui.configs import QueryBuilderConfig, QueryBuilderFieldConfig, QueryBuilderFilterConfig
from insight_ui.utils.query_builder import build_query, describe_filters, format_value, parse_filters

FIELDS = [
    QueryBuilderFieldConfig(field="title", label="Title", operations={"icontains": "contains", "iexact": "is"}),
    QueryBuilderFieldConfig(field="pages", label="Pages", type="number", operations={"gte": "at least"}),
    QueryBuilderFieldConfig(field="published", label="Published", type="date", operations={"gte": "after"}),
    QueryBuilderFieldConfig(field="updated", label="Updated", type="datetime", operations={"lte": "before"}),
    QueryBuilderFieldConfig(field="opens", label="Opens", type="time", operations={"lt": "before"}),
    QueryBuilderFieldConfig(field="available", label="Available", type="boolean", operations={"exact": "is"}),
    QueryBuilderFieldConfig(
        field="status", label="Status", type="choice", operations={"exact": "is"}, values={"draft": "Draft"}
    ),
]

CONFIG = QueryBuilderConfig(fields=FIELDS)


def query(**params: str) -> QueryDict:
    """Build submitted data; keyword names use "_" for the "-" of the parameter names."""
    data = QueryDict(mutable=True)
    for key, value in params.items():
        data[key.replace("_", "-")] = value
    return data


def test_parse_filters_reads_filters_in_submitted_order() -> None:
    """Rows are ordered by their index, not by the order of the parameters."""
    data = query(
        filters_1_field="title",
        filters_1_operator="iexact",
        filters_1_value="Dune",
        filters_1_logic="OR",
        filters_0_field="title",
        filters_0_operator="icontains",
        filters_0_value="sand",
    )

    assert parse_filters(data, CONFIG) == [
        QueryBuilderFilterConfig(field="title", operator="icontains", value="sand"),
        QueryBuilderFilterConfig(field="title", operator="iexact", value="Dune", logic="OR"),
    ]


@pytest.mark.parametrize(
    ("field", "operator", "value"),
    [
        pytest.param("password", "icontains", "x", id="unknown-field"),
        pytest.param("title__author__password", "icontains", "x", id="lookup-path-not-configured"),
        pytest.param("title", "regex", ".*", id="operator-not-allowed"),
        pytest.param("title", "icontains__x", "x", id="operator-with-lookup"),
        pytest.param("title", "icontains", "", id="empty-value"),
        pytest.param("status", "exact", "deleted", id="value-not-allowed"),
        pytest.param("available", "exact", "maybe", id="boolean-not-allowed"),
        pytest.param("pages", "gte", "many", id="not-a-number"),
        pytest.param("pages", "gte", "NaN", id="not-finite"),
        pytest.param("published", "gte", "yesterday", id="not-a-date"),
        pytest.param("opens", "lt", "noon", id="not-a-time"),
    ],
)
def test_parse_filters_drops_filters_the_fields_do_not_allow(field: str, operator: str, value: str) -> None:
    """Only configured fields, their operations and values of the field type reach the query."""
    data = query(filters_0_field=field, filters_0_operator=operator, filters_0_value=value)

    assert parse_filters(data, CONFIG) == []


@pytest.mark.parametrize(
    ("field", "operator", "value", "expected"),
    [
        pytest.param("pages", "gte", "300", Decimal(300), id="number"),
        pytest.param("published", "gte", "2026-10-23", date(2026, 10, 23), id="date"),
        pytest.param("opens", "lt", "09:30", time(9, 30), id="time"),
        pytest.param("available", "exact", "false", False, id="boolean"),
        pytest.param("status", "exact", "draft", "draft", id="choice"),
    ],
)
def test_parse_filters_converts_values_to_the_field_type(
    field: str, operator: str, value: str, expected: object
) -> None:
    """Values arrive as the field's Python type."""
    data = query(filters_0_field=field, filters_0_operator=operator, filters_0_value=value)

    assert parse_filters(data, CONFIG)[0].value == expected


@override_settings(USE_TZ=True, TIME_ZONE="Europe/Berlin")
def test_parse_filters_reads_datetimes_in_the_current_time_zone() -> None:
    """A datetime-local value has no offset and means local time."""
    data = query(filters_0_field="updated", filters_0_operator="lte", filters_0_value="2026-10-23T14:30")

    value = parse_filters(data, CONFIG)[0].value

    assert value == datetime(2026, 10, 23, 14, 30, tzinfo=zoneinfo.ZoneInfo("Europe/Berlin"))
    assert format_value(value) == "2026-10-23T14:30"


def test_parse_filters_ignores_logic_of_the_first_filter() -> None:
    """The first filter has nothing to be combined with."""
    data = query(filters_3_field="title", filters_3_operator="iexact", filters_3_value="Dune", filters_3_logic="OR")

    assert parse_filters(data, CONFIG)[0].logic == "AND"


def test_parse_filters_uses_param_name_and_max_filters() -> None:
    """Only names with param_name count, and at most max_filters filters are read."""
    data = query(
        books_0_field="title",
        books_0_operator="iexact",
        books_0_value="Dune",
        books_1_field="title",
        books_1_operator="iexact",
        books_1_value="Emma",
        filters_0_field="title",
        filters_0_operator="iexact",
        filters_0_value="Ulysses",
    )

    filters = parse_filters(data, QueryBuilderConfig(fields=FIELDS, param_name="books", max_filters=1))

    assert [item.value for item in filters] == ["Dune"]


def test_build_query_binds_and_tighter_than_or() -> None:
    """A AND B OR C AND D becomes (A AND B) OR (C AND D), in the submitted order."""
    filters = [
        QueryBuilderFilterConfig(field="title", operator="icontains", value="a"),
        QueryBuilderFilterConfig(field="pages", operator="gte", value=100),
        QueryBuilderFilterConfig(field="title", operator="icontains", value="c", logic="OR"),
        QueryBuilderFilterConfig(field="available", operator="exact", value=True),
    ]

    expected = (Q(title__icontains="a") & Q(pages__gte=100)) | (Q(title__icontains="c") & Q(available__exact=True))
    assert build_query(filters) == expected


def test_build_query_without_filters_matches_everything() -> None:
    """No filters means no restriction."""
    assert build_query([]) == Q()


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(True, "true", id="boolean"),
        pytest.param(date(2026, 10, 23), "2026-10-23", id="date"),
        pytest.param(time(9, 30), "09:30:00", id="time"),
        pytest.param(Decimal("2.5"), "2.5", id="number"),
    ],
)
def test_format_value_matches_the_browser_controls(value: object, expected: str) -> None:
    """Restored values fit the value attribute of the matching input type."""
    assert format_value(value) == expected


def test_describe_filters_reads_as_a_sentence() -> None:
    """Labels replace lookups and values; the comma before "or" closes an AND group; no leading logic."""
    filters = [
        QueryBuilderFilterConfig(field="title", operator="iexact", value="Dune"),
        QueryBuilderFilterConfig(field="pages", operator="gte", value=Decimal(300)),
        QueryBuilderFilterConfig(field="status", operator="exact", value="draft", logic="OR"),
        QueryBuilderFilterConfig(field="available", operator="exact", value=True),
    ]

    with translation.override("en"):
        summary = describe_filters(filters, FIELDS)

    assert summary == "Title is “Dune” and Pages at least 300, or Status is Draft and Available is Yes"


def test_describe_filters_leaves_out_unknown_fields() -> None:
    """A filter the fields do not describe is not shown, and no filters give an empty text."""
    filters = [QueryBuilderFilterConfig(field="password", operator="exact", value="x")]

    assert describe_filters(filters, FIELDS) == ""
    assert describe_filters([], FIELDS) == ""
