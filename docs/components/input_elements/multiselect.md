# Multiselect-Komponente (Version 0.1.0)

Die `multiselect` Komponente stellt eine Auswahlbox zur Verfügung, welche die Auswahl mehrere Werte erlaubt. Zusätzlich hat das Multiselect eine Suchleiste integriert um schnell nach bestimmten Werten suchen zu können.

## Verwendung

```django
{% load insight_tags %}

{% multiselect name="test" label="Test" maximum=0 show_buttons=True values=["A", "B", "C"] %}

<!-- Oder -->

{% multiselect config=multiselect_config %}
```

## Parameter

- **name** (_str_): Der Name des Multiselect Elements.
- **label** (_str_): Ein kurzer Titel, welche rüber dem Multiselect angezeigt wird.
- **maximum** (_int_): Gibt an wie viele Werte maximal ausgewählt sein dürfen.
- **show_buttons** (_bool_): _True_ zeigt zusätzlich "Alle Auswählen" und "Alle Abwählen" Buttons an.
- **values** (_list[str]_ oder _dict[str, str]_): Alle Werte welche ausgewählt werden können.
- **selected_values** (_list[str]_): Alle Werte welche bereits ausgewählt sein sollen.
- **config** (_dict[str, Any]_): Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.

> **_Info_**: Wenn **values** eine Liste ist, dann wird die automatisch in ein _Dictionary_ umgewandelt, in welchem der _Key_ und der _Value_ identisch sind.

### config

Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.

```py
{
    "name": "test",
    "label": "Test",
    "maximum": 0,
    "show_buttons": True,
    "values": ["A", "B", "C"],  # alt { "A": "A", "B": "B", "C": "C"}
}
```

## Customization

Das Design der Multiselect Komponente befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/multiselect.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- Die Komponente Unterstützt Screenreader durch die entsprechenden ARIA-Attribute: `role="combobox"`, `aria-expanded"`, `aria-selected"`.
- Die Komponente unterstützt die Navigation über die Tastatur mittels der Pfeiltasten (hoch/runter).

## Verwandte Themen

- [Select](select.md)
- [Generic Filter](generic_filter.md)
