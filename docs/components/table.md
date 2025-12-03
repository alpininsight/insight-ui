# Table-Komponente (Version 0.1.0)

Mit der `table` Komponente lässt sich eine einfache Tabelle für beliebige Daten darstellen. Das Layout ist responsive Gestaltet, sollte der Platz nicht ausreichen wird eine horizontale Scrollbar eingeblendet.

## Verwendung

```django
{% load insight_tags %}

{% table data=user_data %}
```

## Parameter

- **data** (_dict_): Enthält die Daten für die Header und Rows, sowie einer Überschrift und einer Nachricht für den Fall, dass keine Daten vorhanden sind.

### data

Enthält die Daten für die Header und Rows, sowie einer Überschrift und einer Nachricht für den Fall, dass keine Daten vorhanden sind.

```py
{
    "caption": _("Alle registrierten Nutzer und ihr aktueller Status."),
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
}
```

## Customization

Das Design der Tabelle befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/table.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- [List](pagination.md)
- [Carousel](carousel.md)
