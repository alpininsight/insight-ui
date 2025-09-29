# Footer Component (Version 0.1.0)

The footer component renders a three-column page footer with optional description text, link lists, and contact details.

## Usage

```django
{% load insight_tags %}
{% footer data=footer_data %}
```

The inclusion tag expects a `footer_data` dictionary.

## Data Structure

```python
footer_data = {
    "description": {
        "title": "Insight UI",
        "text": "Reusable UI building blocks for Django.",
    },
    "links": [
        {
            "text": "Start page",
            "view_name": "storybook_view",
        },
        {
            "text": "Components",
            "view_name": "component_detail_page_view",
            "view_kwargs": {"component_name": "navbar"},
        },
    ],
}
```

- **description** (optional): headline and short paragraph.
- **links**: list of link objects (see [Links](links.md)). Each entry may include icons or external URLs.

## Accessibility

- Headings are rendered as `<h4>` so screen readers can skip through sections.
- Link lists use semantic `<ul>` markup.

## Customisation

Override `templates/insight_ui/components/footer.html` in your project to adjust layout or add additional blocks (e.g. newsletter signup). Remember to keep translation strings wrapped in `{% trans %}`.

## Related Components

- [Navbar](navbar.md)
- [Links](links.md)
- [User menu](usermenu.md)
