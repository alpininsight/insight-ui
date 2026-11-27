# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Read the filters of a query_builder form and turn them into a Django query.

Example:
    fields = [QueryBuilderFieldConfig(field="title", label="Title", operations={"icontains": "contains"})]
    config = QueryBuilderConfig(tag_id="book-filter", fields=fields)
    config.filters = parse_filters(request.GET, config)
    books = Book.objects.filter(build_query(config.filters))

"""

import re
from collections.abc import Callable, Mapping, Sequence
from datetime import date, datetime, time
from decimal import Decimal, InvalidOperation
from typing import TYPE_CHECKING, Any

from django.conf import settings
from django.db.models import Q
from django.utils import formats, timezone
from django.utils.translation import gettext, gettext_lazy as _, pgettext

from insight_ui.configs.filter import QueryBuilderConfig, QueryBuilderFieldConfig, QueryBuilderFilterConfig

if TYPE_CHECKING:
    from insight_ui.configs.types import QueryLogic

# HTML input type of the value control per field type; types without one render a select.
INPUT_TYPES = {"text": "text", "number": "number", "date": "date", "datetime": "datetime-local", "time": "time"}

PARTS = ("field", "operator", "value", "logic")


def choices(field: QueryBuilderFieldConfig) -> dict[str, Any]:
    """Return the options of a field's value select, or an empty dict for a free input.

    Args:
        field: The field definition.

    Returns:
        The allowed values mapped to their labels.

    """
    if field.values:
        return dict(field.values)
    if field.type == "boolean":
        return {"true": _("Yes"), "false": _("No")}
    return {}


def field_definition(field: QueryBuilderFieldConfig) -> dict[str, Any]:
    """Describe a field for the browser, which builds the operator and value controls from it.

    Args:
        field: The field definition.

    Returns:
        Name, label, operators, value options and input type of the field.

    """
    return {
        "field": field.field,
        "label": field.label,
        "operations": dict(field.operations),
        "choices": choices(field),
        "input_type": INPUT_TYPES.get(field.type, "text"),
    }


type FilterValue = str | bool | Decimal | date | datetime | time


def _to_number(raw: str) -> Decimal:
    """Convert a submitted number; reject NaN and infinity."""
    try:
        number = Decimal(raw)
    except InvalidOperation as error:
        raise ValueError(raw) from error
    if not number.is_finite():
        raise ValueError(raw)
    return number


def _to_datetime(raw: str) -> datetime:
    """Convert a submitted date and time; it is in the current time zone if time zones are active."""
    value = datetime.fromisoformat(raw)
    if settings.USE_TZ and timezone.is_naive(value):
        value = timezone.make_aware(value)
    return value


CONVERTERS: dict[str, Callable[[str], FilterValue]] = {
    "boolean": lambda raw: raw == "true",
    "number": _to_number,
    "date": date.fromisoformat,
    "datetime": _to_datetime,
    "time": time.fromisoformat,
}


def _convert(field: QueryBuilderFieldConfig, raw: str) -> FilterValue:
    """Convert a submitted value to the field's Python type.

    Args:
        field: The field definition.
        raw: The submitted value.

    Returns:
        The converted value.

    Raises:
        ValueError: If the value is empty, not an allowed choice or cannot be converted.

    """
    if raw == "":
        msg = "empty value"
        raise ValueError(msg)
    allowed = choices(field)
    if allowed and raw not in allowed:
        msg = f"{raw!r} is not an allowed value"
        raise ValueError(msg)
    converter = CONVERTERS.get(field.type)
    return converter(raw) if converter else raw


def format_value(value: object) -> str:
    """Format a filter value for the value control of the form.

    Args:
        value: A value as returned by parse_filters, or a string.

    Returns:
        The value as the browser control expects it.

    """
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, datetime):
        if timezone.is_aware(value):
            value = timezone.localtime(value).replace(tzinfo=None)
        return value.isoformat(timespec="minutes")
    if isinstance(value, date | time):
        return value.isoformat()
    return str(value)


def parse_filters(query_dict: Mapping[str, Any], config: QueryBuilderConfig) -> list[QueryBuilderFilterConfig]:
    """Read the submitted filters and keep only those the fields of the config allow.

    A filter is dropped if its field is not in config.fields, its operator is not one of the field's
    operations, or its value is empty, not an allowed value or does not match the field type.
    Names follow config.param_name; at most config.max_filters filters are read.

    Args:
        query_dict: The submitted data, usually request.GET.
        config: The query builder the form was rendered with.

    Returns:
        The valid filters in the submitted order, values converted to the field type.

    """
    pattern = re.compile(rf"^{re.escape(config.param_name)}-(\d{{1,4}})-({'|'.join(PARTS)})$")
    rows: dict[int, dict[str, str]] = {}
    for key in query_dict:
        match = pattern.match(key)
        if match:
            value = query_dict[key]
            rows.setdefault(int(match.group(1)), {})[match.group(2)] = value if isinstance(value, str) else ""

    by_name = {field.field: field for field in config.fields}
    filters: list[QueryBuilderFilterConfig] = []
    for index in sorted(rows):
        row = rows[index]
        field = by_name.get(row.get("field", ""))
        operator = row.get("operator", "")
        if field is None or operator not in field.operations:
            continue
        try:
            value = _convert(field, row.get("value", "").strip())
        except ValueError:
            continue
        logic: QueryLogic = "OR" if row.get("logic") == "OR" and filters else "AND"
        filters.append(QueryBuilderFilterConfig(field=field.field, operator=operator, value=value, logic=logic))
        if len(filters) == config.max_filters:
            break
    return filters


def build_query(filters: Sequence[QueryBuilderFilterConfig]) -> Q:
    """Combine filters into a Q object; AND binds tighter than OR.

    "A AND B OR C" becomes "(A AND B) OR C", as in SQL. Pass only filters from parse_filters
    or from your own code: field and operator become a lookup without further checks.

    Args:
        filters: The filters in their order.

    Returns:
        The combined query; an empty Q matches everything.

    """
    query = Q()
    group = Q()
    for index, item in enumerate(filters):
        term = Q(**{f"{item.field}__{item.operator}": item.value})
        if index and item.logic == "OR":
            query |= group
            group = term
        else:
            group &= term
    return query | group


def _describe_value(field: QueryBuilderFieldConfig, value: object) -> str:
    """Return the value as the user chose it: the label of a choice, a localized date or number, or quoted text."""
    label = choices(field).get(format_value(value))
    if label is not None:
        return str(label)
    if isinstance(value, datetime) and timezone.is_aware(value):
        value = timezone.localtime(value)
    if isinstance(value, date | time | Decimal):
        return str(formats.localize(value))
    return gettext("“%(value)s”") % {"value": value}


def describe_filters(filters: Sequence[QueryBuilderFilterConfig], fields: Sequence[QueryBuilderFieldConfig]) -> str:
    """Describe filters as a sentence with the labels of fields, operators and values.

    "Title contains “dune” and Pages at least 300, or Genre is Science fiction".
    The comma before "or" marks where the AND groups end. Filters on unknown fields are left out.

    Args:
        filters: The filters in their order.
        fields: The fields of the query builder.

    Returns:
        The sentence, or an empty string without filters.

    """
    by_name = {field.field: field for field in fields}
    groups: list[list[str]] = []
    for item in filters:
        field = by_name.get(item.field)
        if field is None or item.operator not in field.operations:
            continue
        term = gettext("%(field)s %(operator)s %(value)s") % {
            "field": field.label,
            "operator": field.operations[item.operator],
            "value": _describe_value(field, item.value),
        }
        if groups and item.logic == "AND":
            groups[-1].append(term)
        else:
            groups.append([term])
    and_word = pgettext("query builder", "and")
    or_word = pgettext("query builder", "or")
    return f", {or_word} ".join(f" {and_word} ".join(group) for group in groups)
