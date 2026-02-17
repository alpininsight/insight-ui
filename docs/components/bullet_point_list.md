# Bullet Point List-Komponente (Version 0.1.0)

Die Bullet-Point List Komponente stellt eine Liste dar, welche mit deutlichen _Bullet_ und Linien welche diese Verbinden dargestellt wird. Diese Liste ist vor allem für chronologische Listen gedacht, kann aber auch für ungeordnete Listen verwendet werden.

## Verwendung

- Todo

```django
{% load insight_tags %}

{% bullet_point_list items=bulletpoints %}
```

## Parameter

- **items**: Ein Liste der einzelnen Punkte der Bullet Point Liste.

### items

Ein Liste der einzelnen Punkte der Bullet Point Liste.

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

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- [Step Bar](step_bar.md)
