# Checkbox-Group-Komponente (Version 0.1.0)

Mit der `checkbox_group` Komponente lassen sich Gruppen von Checkbox-Elementen einbauen, welche miteinander verknüpft sind. Das erlaubt es eine Beschränkung einzuschalten, welche es zum Beispiel nicht erlaubt, dass kein Checkbox-Element ausgewählt ist.

## Verwendung

```django
    {% load insight_tags %}
    
    {% checkbox_group config=checkbox_config %}
```

## Parameter

- **config** (_dict_): Beschreibt die Checkbox-Gruppen Komponente.

### config

Beschreibt die Checkbox-Gruppen Komponente.

```py
{
    "name": "language_select",
    "label": "Choose languages:",
    "as_row": True,
    "items": [
        {"id": "english", "value": "english", "text": _("English"), "disabled": False},
        {"id": "german", "value": "german", "text": _("German"), "disabled": False},
        {"id": "italian", "value": "italian", "text": _("Italian (currently not available)"), "disabled": True},
    ],
}
```

- **name** (_str_): Wird für eine `<form>` benötigt, als Name des Request-Parameters.
- **label** (_str_): Ein Label-Text welcher über den Checkbox-Elementen angezeigt wird.
- **as_row** (_bool_): 'True', wenn die Checkbox-Elemente nebeneinander angezeigt werden sollen.
- **items**: (_list[dict]): Eine Liste der Checkbox-Elemente (siehe [Checkbox](checkbox.md)).

## Customization

Das Design der Checkbox-Gruppen Komponente befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/checkbox_group.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- Siehe [Checkbox](checkbox.md)

### Tips

- Fehlermeldungen sollten immer neben dem entsprechenden Element angezeigt werden.

## Verwandte Themen

- [Checkbox](checkbox.md)
- [Radio-Button](radio_button.md)
- [Toggle-Button](toggle_button.md)
