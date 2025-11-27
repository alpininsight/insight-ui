# Checkbox-Komponente (Version 0.1.0)

Mit der `checkbox` Komponente lassen sich einzelne Checkbox-Elemente einbauen. Für eine Gruppe von miteinander Verbundenen Checkbox-Elementen siehe [Checkbox-Gruppe](checkbox_group.md).

## Verwendung

```django
    {% load insight_tags %}
    {% checkbox tag_id="agb-box" name="accept_agb" value="accept_agb" checked=False disabled=False label="Accept AGBs" %}

    # or

    {% checkbox config=checkbox_config %}
```

## Parameter

- **tag_id** (_str_): Eine optionale, eindeutige ID für JavaScript.
- **name** (_str_): Wird für eine `<form>` benötigt, als Name des Request-Parameters.
- **value** (_str_): Der Wert der Checkbox (Das ist nicht der Zustand, siehe dafür 'checked').
- **label** (_str_): Ein Label-Text welcher über der Checkbox angezeigt wird.
- **checked** (_bool_): 'True', wenn die Checkbox ausgewählt sein soll, andernfalls 'False'.
- **disabled** (_bool_): 'True', wenn die Checkbox deaktiviert sein soll, andernfalls 'False'.
- **config** (_dict[str, Any]_): Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.

### config

Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.

```py
{
    "id": "agb-box",
    "name": "accept_agb",
    "value": "accept_agb",
    "checked": False,
    "disabled": False,
    "label": "Accept AGBs",
}
```

## Customization

Das Design der Checkbox Komponente befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/checkbox.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- Das `<label>` und der dazugehörige `<input>` sind mit `for` / `id` miteinander verknüpft.

### Tips

- Fehlermeldungen sollten immer neben dem entsprechenden Element angezeigt werden.

## Verwandte Themen

- [Checkbox-Gruppe](checkbox_group.md)
- [Radio-Button](radio_button.md)
- [Toggle-Button](toggle_button.md)
