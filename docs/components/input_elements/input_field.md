# Input-Field-Komponente (Version 0.1.0)

Mit der `input_field` Komponente lassen sich einzelne `<input>`-Elemente einbauen.

## Verwendung

```django
{% load insight_tags %}
    
{% input_field tag_id="expiration-date" name="expiration_date" input_type="date" value="expiration_date" label="Choose expiration date:" %}

# or

{% input_field config=input_config %}
```

## Parameter

- **tag_id** (_str_): Eine optionale, eindeutige ID für JavaScript.
- **name** (_str_): Wird für eine `<form>` benötigt, als Name des Request-Parameters.
- **input_type** (_str_): Der Type des Input-Feldes bspw.: "text", "password", "date", etc..
- **placeholder** (_str_): Ein platzhalter Text.
- **value** (_str_): Der Wert des Input-Feldes (Bei type="checkbox", siehe 'checked').
- **minimum** (_int_): Bestimmt den minimalen Wert der Eingabe.
- **maximum** (_int_): Bestimmt den maximalen Wert der Eingabe.
- **min_length** (_int_): Bestimmt die minimale Anzahl an Zeichen in einem Textfeld.
- **max_length** (_int_): Bestimmt die maximale Anzahl an Zeichen in einem Textfeld.
- **checked** (_bool_): 'True', wenn type="checkbox" und die Checkbox ausgewählt sein soll.
- **required** (_bool_): 'True' wenn das Feld ausgefüllt werden muss.
- **disabled** (_bool_): 'True', wenn das Feld deaktiviert sein soll, andernfalls 'False'.
- **label** (_str_): Ein Label-Text welcher über dem Input-Feld angezeigt wird.
- **config** (_dict[str, Any]_): Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.

### config

Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.

```py
{
    "id": "expiration-date",
    "name": "expiration_date",
    "input_type": "date",
    "value": "01.01.2026",
    "checked": False,
    "disabled": False,
    "label": "Choose expiration date:",
}
```

## Customization

Das Design der Input Komponente befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/input.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- Das `<label>` und der dazugehörige `<input>` sind mit `for` / `id` miteinander verknüpft.

### Tips

- Fehlermeldungen sollten immer neben dem entsprechenden Element angezeigt werden.

## Verwandte Themen

- [Checkbox](checkbox.md)
- [Checkbox-Gruppe](checkbox_group.md)
- [Radio-Gruppe](radio_group.md)
- [Toggle-Button](toggle_button.md)
