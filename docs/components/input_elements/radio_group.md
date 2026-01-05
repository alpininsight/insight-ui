# Radio-Group-Komponente (Version 0.1.0)

Mit der `radio_group` oder alternativ mit der `radio_block` Komponente lassen sich Gruppen von Radio-Buttons einbauen. Bei der `radio_group` Variante handelt es sich um eine Variante mit normalen Radio-Buttons für ein Formular o.ä.. Bei der `radio_block` Variante handelt es sich hingegen, um eine grafisch anspruchsvollere Variante und die Radio-Buttons können dazu verwendet werden, einen Request zu starten, um zum Beispiel die Seite zu wechseln (siehe [Carousel](../carousel.md)).

## Verwendung

```django
{% load insight_tags %}

{% radio_group config=example_radio current_value=current_view %}
```

Oder als Block

```django
{% load insight_tags %}

{% radio_block config=example_radio current_value=current_view %}
```

## Parameter

- **config** (_dict_): Beschreibt die Radio Komponente und deren Items.
- **current_value** (_str_): Der Name der aktuell ausgewählten Wertes.

### Nur radio_block

- **view_name** (_str_): (Optional) Der Name der View an welchen der Request beim wechseln, gesendet werden soll.
- **query_params** (_str_): (Optional) Ein String von Query-Parametern.
- **target_id** (_str_): (Optional) Die ID des HTML-Tags, welches bei wechseln des Wertes ausgetauscht werden soll.
- **method** (_str_): (Optional) Der Name der JavaScript Methode welche ausgeführt werden soll.
- **integrated** (_bool_): _False_ wenn die Komponente ihr eigenes `<form>` Element haben soll.

### config

Beschreibt die Radio Komponente und deren Items.

```py
{
    "name": "radio-example1",
    "label": "Model auswählen",
    "as_row": True,
    "items": [
        {"id": "model1", "value": "BERT", "text": _("BERT"), "disabled": False},
        {"id": "model2", "value": "PaLM 2", "text": _("PaLM 2"), "disabled": False},
        {"id": "model3", "value": "LLaMA 2", "text": _("LLaMA 2 (currently not available)"), "disabled": True},
    ],
}
```

## Customization

Das Design der Radio-Group befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/radio_group.html`, das der Radio-Blocks in dieser Datei: `insight_ui/templates/insight_ui/components/radio_block.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- _Todo_
