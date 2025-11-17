# Radio-Button-Komponente (Version 0.1.0)

Mit der `radio` oder alternativ mit der `radio_group` Komponente lassen sich Gruppen von Radio-Buttons einbauen. Bei der `radio` Variante handelt es sich um eine Variante mit normalen Radio-Buttons für ein Formular o.ä.. Bei der `radio_group` Variante handelt es sich hingegen, um eine grafisch anspruchsvollere Variante und die Radio-Buttons können dazu verwendet werden, einen Request zu starten, um zum Beispiel die Seite zu wechseln (siehe [Carousel](../carousel.md)).

## Verwendung

```django
    {% radio radio_group=example_radio current_value=current_view %}
```

Oder als Block

```django
    {% radio_group radio_group=example_radio current_value=current_view %}
```

## Parameter

- **radio_group** (_dict_): Beschreibt die Radio Komponente und deren Items.
- **current_value** (_str_): Der Name der aktuell ausgewählten Wertes.
- **view_name** (_str_): (Optional) Der Name der View an welchen der Request beim wechseln, gesendet werden soll (nur radio_group).
- **query_params** (_str_): (Optional) Ein String von Query-Parametern (nur radio_group).
- **target_id** (_str_): (Optional) Die ID des HTML-Tags, welches bei wechseln des Wertes ausgetauscht werden soll (nur radio_group).

### radio_group

Beschreibt die Radio Komponente und deren Items.

```py
{
    "name": "radio-example1",
    "items": [
        {"id": "model1", "value": "BERT", "text": _("BERT"), "disabled": False},
        {"id": "model2", "value": "PaLM 2", "text": _("PaLM 2"), "disabled": False},
        {"id": "model3", "value": "LLaMA 2", "text": _("LLaMA 2 (currently not available)"), "disabled": True},
    ],
}
```

## Customization

Das Design des Radio-Buttons befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/radio_button.html`, das der Radio-Blocks in dieser Datei: `insight_ui/templates/insight_ui/components/radio_group.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- _Todo_
