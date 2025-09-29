# Table Component (Version 0.1.0)

The table component renders responsive data tables with support for empty states and basic styling.

## Usage

```django
{% load insight_tags %}
{% table table_data=table_data %}
```

### Data Structure

```python
table_data = {
    "caption": "Example table",
    "empty_msg": "No data available",
    "headers": ["Name", "Email", "Status"],
    "rows": [["Jane Doe", "jane@example.com", "Active"]],
}
```

## Features
- Renders captions and accessible headers.
- Displays an empty-state message when no rows exist.
- Works well with HTMX updates or pagination.

## Customisation
- Override `components/table.html` to add sorting icons, zebra stripes, or interactive rows.

## Related Components
- [Pagination](pagination.en.md)
- [Toggle view](toggle_view.en.md)
