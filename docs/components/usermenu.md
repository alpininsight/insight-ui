# Usermenu-Komponente (Version 0.1.0)

Das Benutzermenü beinhaltet ein Dropdown-Menü mit weitere Navigationselementen, welche Frei konfiguriert werden können. Sollte der Nutzer nicht angemeldet sein, wird anstelle des Menüs ein Button zum Anmelden angezeigt.

Das Benutzermenü ist bereits in der Navbar integriert, kann aber auch separat an anderer Stelle eingebunden werden.

## Verwendung

Eingebunden wird das Benutzermenü am einfachsten über das `{% include %}` Tag.

```django
{% load insight-tags %}

{% include "insight_ui/components/user_dropdown.html" with user=user show_login=show_login user_dropdown_links=user_dropdown_links %}
```

## Parameter

Das Benutzermenü bekommt so wie die Navbar drei Parameter.

- **user**: Das *user* Objekt des Requests (sollte eigentlich immer verfügbar sein).
- **show_login**: _True_ wenn ein Button zum Anmelden angezeigt werden soll (standardmäßig aus, also `False`).
- **user_dropdown_links**: Eine Liste mit den Links welche in dem Benutzermenü angezeigt werden sollen.

### user_dropdown_links

Die Liste der Links besteht aus Dictionaries, welche die Links beschreiben.

Eine mögliche Liste sieht folgendermaßen aus:

```py
"user_dropdown_links": [
    {
        "text": _("Einstellungen"),
        "view_name": "storybook_view",
        "staff_only": False,
        "icon": {"name": "cog", "size": "small"},
    },
    {
        "text": _("Administration"),
        "view_name": "admin:index",
        "staff_only": True,
        "icon": {"name": "home", "size": "small"},
    },
],
```

- Für mehr Details siehe [Links](links.md)

> **_Info_**: Ein Button zum Abmelden ist intern bereits vorhanden und muss nicht manuell hinzugefügt werden!

## Barrierefreiheit

- Todo

## Verwandte Themen

- [Navbar](navbar.md)
- [Links](links.md)
