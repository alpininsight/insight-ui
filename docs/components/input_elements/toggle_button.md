# Toggle-Button-Komponente (Version 0.1.0)

Mit der `toggle` Komponente lässt sich ein Toggle-Button einbauen. Dieser funktioniert im Grunde wie eine einzelne Checkbox.

## Verwendung

```django
    {% toggle toggle=example_toggle %}
```

## Parameter

- **toggle** (_dict_): Beschreibt den Toggle-Button.

### toggle

Beschreibt den Toggle-Button.

```py
{
    "id": "toggle_button_example1",
    "text": _("Click me!")
}
```

## Customization

Das Design des Toggle-Buttons befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/toggle_button.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- [Checkbox](checkbox.md)
