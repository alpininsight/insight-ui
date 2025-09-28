# Dropdown Component (Version 0.1.0)

Dropdown menus group related actions in a collapsible list. Use them when space is limited or when displaying secondary actions.

## Usage

```django
{% load insight_tags %}
{% dropdown dropdown_menu=user_dropdown %}
```

### Configuration

```python
user_dropdown = {
    "tag_id": "dd_user",
    "title": _("User"),
    "show_arrow": True,
    "items": [
        {"text": _("Profile"), "view_name": "profile_view", "icon": {"name": "user"}},
        {"text": _("Settings"), "view_name": "settings_view", "icon": {"name": "cog"}},
        {"text": _("Logout"), "view_name": "logout_view", "icon": {"name": "log-out"}},
    ],
}
```

- `tag_id`: unique HTML ID for the dropdown container.
- `title`: button label visible in the navbar or toolbar.
- `show_arrow`: whether to render the chevron indicator.
- `items`: list of entry dictionaries (each can define `text`, `view_name`, `icon`, or raw `url`).

## Best Practices
- Keep menus short—ideally fewer than seven items.
- Avoid nested dropdowns; consider modal dialogs or dedicated pages for complex interactions.

## Customisation
- Override `components/dropdown.html` to change animation, layout, or add sections.
- Icons are rendered by the `icon` inclusion tag; ensure new icons exist in `components/icons.html`.

## Related Components
- [Navbar](../navbar.en.md)
- [User menu](../usermenu.en.md)
