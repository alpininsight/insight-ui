# Bullet Point List-Komponente (Version 0.1.0)

- Todo

## Verwendung

- Todo

```django
{% load insight_tags %}

{% bullet_point_list items=bulletpoints %}
```

## Parameter

- **items**: Ein Liste der einzelnen Punkte der Bullet Point Liste.

### items

```py
[
    {
        "title": _("Kontaktdaten"),
        "description": _("Informationen zur Person und Anschrift."),
        "completed": True,
    },
    {"title": _("Zahlungsmethode"), "description": _("Art der Bezahlung auswählen."), "current": True},
    {"title": _("Überprüfen"), "description": _("Prüfen der Angaben und Bezahlen.")},
]
```

## Verwandte Themen

- [Navbar](step_bar.md)
