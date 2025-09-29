# Table-Komponente (Version 0.1.0)

Eine einfache Tabelle zum Darstellen von Daten.

## Verwendung

```django
{% load insight_tags %}

{% table table_data=table %}
```

## Parameter

- **table_data**: Ein Dictionary welches alle relevanten Daten wie die Header und Rows enthält.

### table_data

Das Dictionary einer Tabelle ist folgendermaßen aufgebaut:

```py
"table": {
    "caption": _("Ein Beispiel einer Tabellen-Komponente."),
    "empty_msg": _("Keine Daten vorhanden!"),
    "headers": [_("Name"), _("E-Mail"), _("Status")],
    "rows": [
        [
            "Max Mustermann",
            "max@example.com",
            _("Aktiv"),
        ],
        ...
    ],
},
```

## Verwandte Themen

- _Todo_
