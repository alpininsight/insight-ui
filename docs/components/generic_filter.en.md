# Generic Filter Component (Version 0.1.0)

The generic filter component renders dropdown-based filters that trigger HTMX requests whenever the selection changes. It is a simpler, predefined alternative to the [Query Builder](query_builder.md).

## Usage

```django
{% load insight_tags %}
{% generic_filter view_name="filter_view" filters=filters %}
```

## Parameters

- **view_name** (`str`): Django URL pattern name that receives the HTMX request.
- **filters** (`list[dict]`): definitions for each filter option group (see below).

### Filter Definition

Each filter entry contains:

- `text`: label shown to the user.
- `icon` (optional): icon metadata rendered via the `icon` inclusion tag.
- `name`: unique identifier submitted to the backend.
- `values`: ordered mapping of display labels to submitted values. You can insert a separator by mapping `"-----"` to `"-"`.
- `explanation` (optional): helper text displayed inside the dropdown.

```python
filters = [
    {
        "text": _("Issue Date"),
        "icon": {"name": "calendar", "size": "small"},
        "name": "issuedate_filter",
        "values": {
            _("All"): "all",
            _("Today & Yesterday"): "newest",
            _("Last 7 days"): "7days",
            _("Last 14 days"): "14days",
            _("Last 30 days"): "30days",
            _("Last 60 days"): "60days",
            _("Without release date"): "missing",
            "-----": "-",
            "2022": "2022",
            "2023": "2023",
            "2024": "2024",
        },
        "explanation": _("Filter by issue date."),
    },
]
```

Hook the HTMX endpoint up to return only the filtered result list so the component can replace the target container.

## Related Components

- [Query Builder](query_builder.md)
