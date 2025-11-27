# Range-Slider-Komponente (Version 0.1.0)

Mit der `slider`-Komponente kann ein Range-Slider in das Frontend eingebaut werden, mit welchem sich ein Wert innerhalb eines begrenzten Intervall auswählen lässt.

## Verwendung

```django
    {% load insight-tags %}

    {% slider tag_id="cpu-cores" name="cpu_core_count" value=4 minimum=2 maximum=8 step_size=2 disabled=False label="Choose amount of CPU-Cores:" items=labels %}

    # or

    {% slider config=slider_config %}
```

## Parameter

- **tag_id** (_str_): Eine eindeutige ID für die Verknüpfung von `<input>` und `<label>`, sowie JavaScript.
- **name** (_str_): Wird für eine `<form>` benötigt, als Name des Request-Parameters.
- **value** (_int_): Der Wert des Sliders.
- **minimum** (_int_): Der kleinste Wert des Sliders.
- **maximum** (_int_): Der größte Wert des Sliders.
- **step_size** (_int_): Die Größe der Schritte des Sliders.
- **label** (_str_): Ein Label-Text welcher über dem Toggle angezeigt wird.
- **disabled** (_bool_): 'True', wenn der Toggle deaktiviert sein soll, andernfalls 'False'.
- **items** (_list[str]_): Eine Liste von Texten, welche als Legende unter dem Slider angezeigt werden. 
- **config** (_dict[str, Any]_): Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.

### config

Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.

```py
{
    "tag_id": "cpu-cores",
    "name": "cpu_core_count",
    "value": 4,
    "minimum": 2,
    "maximum": 8,
    "step_size": 2
    "label": "Choose amount of CPU-Cores:,
    "disabled": False,
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
