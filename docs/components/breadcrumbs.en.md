# Breadcrumbs Component (Version 0.1.0)

Breadcrumbs show the current position within the application hierarchy and provide quick navigation to higher-level pages.

## Usage

```django
{% load insight_tags %}
{% breadcrumbs items=breadcrumb_items %}
```

### Data Structure

```python
breadcrumb_items = [
    {"label": _("Dashboard"), "url": "#"},
    {"label": _("Projects"), "url": "#"},
    {"label": _("Current project"), "url": None},
]
```

- `label`: translated text shown to the user.
- `url`: hyperlink target. Leave `None`/`null` for the active page.

## Accessibility

- The component renders a `<nav>` with `aria-label="Breadcrumb"`.
- The active element uses `aria-current="page"`.

## Customisation

Override `components/breadcrumbs.html` if you need to insert icons or different separators. Keep the ordered structure intact to support assistive technologies.

## Related Components

- [Navbar](navbar.md)
- [Sidebar](sidebar.md)
