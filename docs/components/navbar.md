# Navbar-Komponente (Version 0.1.0)

Die Navbar-Komponente stellt eine anpassbare Navigationsleiste mit verschiedenen Komponenten zur Verfügung. Die Navigation ist fixiert am oberen Rand des Browserfenstern und bewegt sich beim nach unten Scrollen mit. Die Navigationsleiste besteht aus den folgenden Komponenten:

- **Logo und Titel**
- **Navigationslinks**
- **Suchleiste**
- **Login/Benutzermenü**
- **Sprachauswahl**
- **Theme-Toggle Button**

## Verwendung

Eingebunden wird die Navbar am einfachsten über das entsprechende _Template-Tag_. Für die Navbar ist ein entsprechender Block definiert, in welchem diese platziert werden sollte.

```django
{% load insight_tags %}

{% block navbar %}
    {% navbar config=nav_config user=user user_dropdown_links=user_dropdown_links show_login=True %}
{% endblock navbar %}
```

## Parameter

Die Navbar bekommt bis zu vier Parameter.

- **navbar**: Ein Dictionary mit der gesamten Konfiguration der Navigationsleiste (mehr dazu gleich).
- **user**: Das *user* Objekt des Requests (sollte eigentlich immer verfügbar sein).
- **user_dropdown_links**: Eine Liste mit den Links welche in dem Benutzermenü angezeigt werden sollen.
    - siehe [Benutzermenü](usermenu.md)
- **show_login**: _True_ wenn ein Button zum Anmelden angezeigt werden soll (standardmäßig aus, also `False`).

### Konfiguration

Das Dictionary mit der Navbar Konfiguration ist etwas größer und wird hier einmal näher erläutert.

Eine komplette Konfiguration sieht folgendermaßen aus:

```py
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

#### brand

Beinhaltet die Einstellungen für den Titel und das daneben stehende Logo. Das Logo ist optional und wenn kein Pfad angegeben werden sollte, wird das standard Logo verwendet. Die Variable **view_name** wird verwendet, um den Nutzer auf die entsprechende Seite zu schicken, sollte dieser auf den Titel klicken. Erwartet wird der Name der View keine URL, da der Wert intern mit `{% url view_name %}` aufgelöst wird.

#### links

- siehe [Links](links.md)

#### show_...

- `"show_searchbar"`: _True_ wenn eine Suchleiste nach den Links angezeigt werden soll
- `"show_usermenu"`: _True_ wenn ein Benutzermenü/Login an der rechten Seite angezeigt werden soll (der externe Parameter **show_login** wird nur zum verstecken des Login's auf bestimmten Seiten verwendet)
- `"show_language_selector"`: _True_ wenn eine Sprachauswahl an der rechten Seite angezeigt werden soll
- `"show_theme_toggle"`: _True_ wenn der Theme-Toggle (hell/dunkel) an der rechten Seite angezeigt werden soll

## Barrierefreiheit

Die Navbar-Komponente enthält einen **Skip-Link** zum *Hauptinhalt*.

## Verwandte Themen

- [Benutzermenü](usermenu.md)
- [Footer](footer.md)
- [Links](links.md)
