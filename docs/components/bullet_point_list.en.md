# Bullet Point List Component (Version 0.1.0)

The bullet point list component renders a styled list of items with icon support and spacing tailored to Insight UI.

## Usage

```django
{% load insight_tags %}
{% bullet_point_list items=list_items %}
```

### Data Structure

```python
list_items = [
    {"text": _("Fast implementation"), "icon": {"name": "bolt"}},
    {"text": _("Accessible by default"), "icon": {"name": "accessibility"}},
    {"text": _("Theming with Tailwind"), "icon": None},
]
```

## Customisation

- Override `components/bullet_point_list.html` to change spacing, icons, or layout.
- Icons are rendered via the `icon` inclusion tag; supply any icon supported in `components/icons.html`.

## Related Components
- [Card](card.md) – bullet lists are often embedded in cards.
- [Sidebar](sidebar.md)
