# Toggle-Button-Komponente (Version 0.1.0)

Mit der `toggle` Komponente lässt sich ein Toggle-Button einbauen. Dieser funktioniert im Grunde wie eine einzelne Checkbox.

## Verwendung

```django
{% load insight-tags %}

{% toggle tag_id="theme-toggle" name="toggle_theme" value="toggle_theme" checked=False disabled=False label="Dark" method="changeTheme" switch=True %}

# or
    
{% toggle config=toggle_config method="changeTheme" %}
```

## Parameter

- **tag_id** (_str_): Eine eindeutige ID für die Verknüpfung von `<input>` und `<label>`, sowie JavaScript.
- **name** (_str_): Wird für eine `<form>` benötigt, als Name des Request-Parameters.
- **value** (_str_): Der Wert des Toggles (Das ist nicht der Zustand, siehe dafür 'checked').
- **label** (_str_): Ein Label-Text welcher über dem Toggle angezeigt wird.
- **checked** (_bool_): 'True', wenn der Toggle ausgewählt sein soll, andernfalls 'False'.
- **disabled** (_bool_): 'True', wenn der Toggle deaktiviert sein soll, andernfalls 'False'.
- **switch** (_bool_): 'True', wenn der Toggle-Button wie ein typischer Switch-Select aussehen soll.
- **config** (_dict[str, Any]_): Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.
- **method** (_str_): Der Name der JavaScript Methode welche ausgeführt werden soll.

### config

Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.

```py
{
    "tag_id": "theme-toggle",
    "name": "toggle_theme",
    "value": "toggle_theme",
    "checked": False,
    "disabled": False,
    "label": "Dark",
    "switch": True,
}
```

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- [Checkbox](checkbox.md)
