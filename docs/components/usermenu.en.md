# User Menu Component (Version 0.1.0)

The user menu component displays an account dropdown with profile, settings, and logout links. It integrates with the navbar but can also be embedded elsewhere.

## Usage

```django
{% load insight_tags %}
{% include "insight_ui/components/user_dropdown.html" with user=request.user show_login=True user_dropdown_links=user_links %}
```

- `user`: current Django user object.
- `show_login`: whether to render a login button when the user is anonymous.
- `user_dropdown_links`: list of link dictionaries that populate the dropdown body.

## Link Structure

```python
user_links = [
    {
        "text": _("Profile"),
        "view_name": "profile_view",
    },
    {
        "text": _("Settings"),
        "view_name": "settings_view",
    },
]
```

## Accessibility

- Uses proper focus handling so the dropdown can be navigated with the keyboard.
- Includes aria labels describing the purpose of the menu.

## Customisation

Override `components/user_dropdown.html` to add avatars, badges, or additional sections. Keep the button markup intact to retain keyboard support.

## Related Topics

- [Navbar](navbar.md)
- [Links](links.md)
