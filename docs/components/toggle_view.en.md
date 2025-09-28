# Toggle View Component (Version 0.1.0)

The toggle view component lets users switch between multiple visualisations of the same data (e.g., table vs. cards vs. carousel).

## Usage

```django
{% load insight_tags %}
{% toggle_view tag_id="list-view" table_data=table_rows view_options=view_options current_view="table" %}
```

### Parameters
- **tag_id**: unique identifier used by the JavaScript toggle logic.
- **table_data**: data fed into the table view (see [Table](table.en.md)).
- **view_options**: configuration defining available view modes.
- **current_view**: initial view (`"table"`, `"card"`, `"carousel"`, etc.).

`view_options` usually takes this shape:

```python
view_options = {
    "name": "view-options",
    "param_name": "view",
    "options": [
        {"id": "card-view", "value": "card", "icon": {"name": "cards"}},
        {"id": "table-view", "value": "table", "icon": {"name": "list"}},
        {"id": "carousel-view", "value": "carousel", "icon": {"name": "carousel"}},
    ],
}
```

## Customisation
- Extend `components/toggle_view.html` to add custom view types or change icons.
- Combine with HTMX to fetch data lazily when switching views.

## Related Components
- [Table](table.en.md)
- [Carousel](carousel.en.md)
- [Card](card.en.md)
