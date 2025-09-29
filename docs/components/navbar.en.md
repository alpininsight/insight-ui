# Navbar Component (Version 0.1.0)

The navbar component renders a responsive, fixed navigation bar that bundles several pieces of UI at the top of the viewport. Out of the box it can show the following building blocks:

- **Branding** (logo + title)
- **Navigation links**
- **Search input**
- **User/login menu**
- **Language selector**
- **Theme toggle**

## Usage

The navbar is exposed through an inclusion tag. Place it inside the predefined `navbar` block of the base template so it stays positioned correctly.

```django
{% load insight_tags %}

{% block navbar %}
    {% navbar config=nav_config user=user user_dropdown_links=user_dropdown_links show_login=True %}
{% endblock navbar %}
```

## Parameters

The inclusion tag accepts up to four parameters:

- **config**: dictionary that holds the complete navigation configuration (see below).
- **user**: current request user; needed when you want to display the user menu.
- **user_dropdown_links**: list of link dictionaries rendered inside the user menu (see [User menu](usermenu.md)).
- **show_login**: set to `True` to display a login button when no authenticated user is present (`False` by default).

### Configuration dictionary

A full configuration dictionary might look like this:

```python
{
    "brand": {
        "title": "Django Insight UI NavBar",
        "view_name": "storybook_view",
        "logo_url": "insight_ui/svg/logo.svg",
        "logo_alt": "Insight UI Logo",
    },
    "links": [
        {
            "text": _("Startseite"),
            "icon": {"name": "home", "size": "small"},
            "view_name": "storybook_view",
            "active": True,
            "need_auth": False,
            "staff_only": False,
        },
        {
            "text": _("Über"),
            "open_modal": "about-modal",
            "active": False,
            "need_auth": False,
            "staff_only": False,
        },
    ],
    "show_searchbar": True,
    "show_usermenu": True,
    "show_language_selector": True,
    "show_theme_toggle": True,
}
```

#### `brand`

Controls the logo + title area. If `logo_url` is omitted, the default Insight UI logo is used. `view_name` should contain the Django URL pattern name that is resolved via `{% url view_name %}` when the brand area is clicked.

#### `links`

Navigation link definitions (see the [Links](links.md) component for the full schema). You can mix URL-based links, dropdown triggers, and modal buttons.

#### `show_*`

- `"show_searchbar"`: display the search input after the main link list.
- `"show_usermenu"`: show the user dropdown / login button on the right (the `show_login` parameter can still hide the login button for specific pages).
- `"show_language_selector"`: render the locale switcher.
- `"show_theme_toggle"`: enable the dark/light toggle button.

## Accessibility

The navbar includes a **skip link** that allows keyboard users to jump straight to the main content area.

## Related Topics

- [User menu](usermenu.md)
- [Footer](footer.md)
- [Links](links.md)
