# Checkbox-Komponente (Version 0.1.0)

Mit der `checkbox` Komponente lassen sich einzelne oder Gruppen von Checkbox-Elementen einbauen.

## Verwendung

```django
    {% checkbox checkbox=example_checkbox %}
```

## Parameter

- **checkbox** (_dict_): Beschreibt die Checkbox Komponente.

### checkbox

Beschreibt die Checkbox Komponente.

```py
{
    "name": "checkbox-example1",
    "items": [
        {"id": "english", "value": "english", "text": _("English"), "disabled": False},
        {"id": "german", "value": "german", "text": _("German"), "disabled": False},
        {"id": "italian", "value": "italian", "text": _("Italian (currently not available)"), "disabled": True},
    ],
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

- [Radio-Button](radio_button.md)
- [Toggle-Button](toggle_button.md)
