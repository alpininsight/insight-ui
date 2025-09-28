# Query Builder Component (Version 0.1.0)

The query builder component offers an SQL-like filtering interface. Instead of selecting from pre-defined drop-down lists, users can pick fields, operators, and values dynamically.

## Usage

```django
{% load insight_tags %}
{% sq_builder custom_filters=custom_filters %}
```

### Parameters
- **custom_filters** (`list[dict]`): field definitions, allowed operations, and optional value presets (see below).

### Filter Definition

```python
custom_filters = [
    {
        "field": "title",
        "name": _("Title"),
        "type": "text",
        "operations": {
            "iexact": _("is exact"),
            "icontains": _("contains"),
            "contains": _("contains (case sensitive)"),
            "istartswith": _("starts with"),
            "iendswith": _("ends with"),
        },
        "values": {},
    },
]
```

Each entry includes:
- `field`: model field or lookup expression (supports relations such as `client__name`).
- `name`: label displayed in the UI.
- `type`: influences the widget (e.g., `text`, `date`).
- `operations`: mapping between Django lookups and human-readable labels.
- `values` (optional): restrict choices to predefined options.

## When to Use
- Complex reporting interfaces with multiple filterable fields.
- Power-user dashboards where standard drop-down filters are too limiting.

## Related Components
- [Generic filter](generic_filter.en.md)
