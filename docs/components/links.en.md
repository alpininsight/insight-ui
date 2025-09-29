# Links Component (Version 0.1.0)

The links component provides uniform styles for link lists and button-like anchors inside Insight UI.
-
This page documents the **Links** component. Keep it in sync with `docs/de/components/links.md`.

## Available Patterns

- Inline links inside copy
- Navigation links used inside the navbar
- Footer link lists with optional icons

## Usage

Links are usually rendered via the `links` data structure that the navbar, footer, and sidebar components consume. A single entry can look like this:

```python
{
    "text": _("Dashboard"),
    "view_name": "index_view",
    "icon": {"name": "home", "size": "small"},
    "external": False,
}
```

## Styling

- CSS lives under `static/insight_ui/css/tailwind.css` and is controlled through Tailwind utilities.
- Navigation links highlight the active route by toggling `border-insight-text-link`.
- Inline links use the theme tokens `--color-insight-text-link` and `--color-insight-text-link-hover`.

## Accessibility

- Provide descriptive link text rather than “click here”.
- Use `rel="noopener"` on external links.

## Related Components

- [Navbar](navbar.md)
- [Footer](footer.md)
- [Sidebar](sidebar.md)
