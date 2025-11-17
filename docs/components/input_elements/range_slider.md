# Range-Slider-Komponente (Version 0.1.0)

Mit der `slider`-Komponente kann ein Range-Slider in das Frontend eingebaut werden, mit welchem sich ein Wert innerhalb eines begrenzten Intervall auswählen lässt.

## Verwendung

```django
    {% slider slider=example_slider %}
```

## Parameter

- **slider** (_dict_): Beschreibt den Range-Slider.

### slider

Beschreibt den Range-Slider.

```py
{
    "id": "range_slider_example1",
    "title": "Range Slider Title",
    "value": 1000,
    "min": 100,
    "max": 1500,
    "items": [_("100€ (minimum)"), "500€", "750€", "1000€", _("1500€ (maximum)")],
}
```

## Customization

Das Design des Range-Sliders befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/range_slider.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- _Todo_
