# Select-Komponente (Version 0.1.0)

Die `Select` Komponente stellt eine einfache Auswahlbox zur Verfügung.

## Verwendung

```django
{% load insight_tags %}

{% select name="test" label="Test" values=["A", "B", "C"] %}

<!-- Oder -->

{% select config=select_config %}
```

## Parameter

- **name** (_str_): Der Name des `<select>` Elements.
- **label** (_str_): Ein kurzer Titel, welche rüber dem Select angezeigt wird.
- **values** (_list[str]_ oder _dict[str, str]_): Alle Werte welche ausgewählt werden können.
- **selected_value** (_str_): Ein bereits ausgewählter Wert.
- **config** (_dict[str, Any]_): Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.

> **_Info_**: Wenn **values** eine Liste ist, dann wird die automatisch in ein _Dictionary_ umgewandelt, in welchem der _Key_ und der _Value_ identisch sind.

### config

Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.

```py
{
    "name": "test",
    "label": "Test",
    "values": ["A", "B", "C"],  # alt { "A": "A", "B": "B", "C": "C"}
}
```

## Customization

Das Design der Select Komponente befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/select.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- Todo

## Verwandte Themen

- [Multiselect](multiselect.md)
- [Generic Filter](generic_filter.md)
