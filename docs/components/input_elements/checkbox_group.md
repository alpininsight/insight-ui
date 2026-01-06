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
    "label": "Choose languages: (max. 3)",
    "as_row": True,
    "minimum_checked": 1,
    "maximum_checked": 3,
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
- **minimum_checked** (int): Die Anzahl der Checkbox-Elemente welche mindestens ausgewählt sein müssen.
- **maximum_checked** (int): Die Anzahl der Checkbox-Elemente welche gleichzeitig ausgewählt sein dürfen.
- **items**: (_list[dict]): Eine Liste der Checkbox-Elemente (siehe [Checkbox](checkbox.md)).

## Barrierefreiheit

- Siehe [Checkbox](checkbox.md)

### Tips

- Fehlermeldungen sollten immer neben dem entsprechenden Element angezeigt werden.

## Verwandte Themen

- [Checkbox](checkbox.md)
- [Radio-Gruppe](radio_group.md)
- [Toggle-Button](toggle_button.md)
