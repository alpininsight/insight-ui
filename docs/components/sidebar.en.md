# Sidebar Component (Version 0.1.0)

The sidebar component presents grouped navigation links along the left or right edge of the layout.

## Usage

```django
{% load insight_tags %}
{% sidebar sidebar_data=sidebar_data side="left" static=False auto_close=True %}
```

### Parameters
- **sidebar_data** (`dict`): categories and entries to display (see below).
- **side** (`"left"` or `"right"`): placement of the sidebar (defaults to `"right"`).
- **static** (`bool`): when `True`, renders as a fixed column; when `False`, it can slide in/out.
- **auto_close** (`bool`): auto-hide when focus leaves the panel (only when `static=False`).

### Data Structure

```python
sidebar_data = {
    "title": "Navigation",
    "categories": [
        {
            "caption": "Components",
            "icon": {"name": "collection"},
            "items": [
                {"text": "Navbar", "url": "/docs/components/navbar/"},
                {"text": "Footer", "url": "/docs/components/footer/"},
            ],
        },
    ],
}
```

Each item supports optional `icon` metadata, HTMX attributes, and external links.

## Accessibility
- Sidebar uses ARIA attributes to describe its role (complementary) and supports keyboard toggling.

## Customisation
- Override `components/sidebar.html` to adjust spacing or add nested levels.
- Tailor the toggle buttons or animations by editing the template or accompanying JavaScript `static/insight_ui/js/sidebar.js`.

## Related Components
- [Navbar](navbar.en.md)
- [Generic filter](generic_filter.en.md)
