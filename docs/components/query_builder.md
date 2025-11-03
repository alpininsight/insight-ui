# Query Builder Komponente (Version 0.1.0)

Diese Komponente stellt eine Alternative zur [Generic Filter](generic_filter.md) Komponente dar. 

Der Query Builder ist weitaus flexibler aber auch komplexer in der Nutzung als übliche Filter Methoden. Der Query Builder ist im Grunde eine Art grafische Darstellung einer SQL-Query. Der Query Builder bekommt eine Liste der Modell-Felder in welchen gesucht werden kann und zu jedem Feld eine Liste der erlaubten Operationen. Bspw.: `{ "field": "name", "type": "text", "operations": ["iexact", "icontains"]}`.

In speziellen Fällen können auch wie bei der anderen Variante, vordefinierte Werte angegeben werden. Dieser Aspekt macht diese Art der Filterung, u.u. wesentlich flexibler, da auf fest definierte Werte verzichtet wird.

Ähnlich wie bei der anderen Filter Variante, wird hier auch lediglich ein Dictionary mit den gewünschten Eigenschaften benötigt.

## Verwendung

```django
{% sq_builder custom_filters=custom_filters %}
```

## Parameter

- **custom_filters** (_list_): Eine Liste mit Dictionaries welches die Filter beschreibt.

### custom_filters

Dieser Parameter beschreibt alle Filter, welche mit dem Query Builder gebaut werden können. Jeder Filter besteht aus einem **Modell-Feld** Namen und dessen **Datentyp** und einem Platzhalter Text. Des weiteren, muss für jeden Filter eine Gruppe der möglichen **Operatoren** definiert werden, welche auf das entsprechende Feld angewendet werden können. Optional können auch für jedes Feld, bestimmte **Werte** definiert werden.

```py
[
    {
        "field": "title",
        "name": _("Title"),
        "type": "text",
        "operations": {
            "iexact": _("is exact"),
            "icontains": _("contains"),
            "contains": _("contains (case sensitive)"),
            "istartswith": _("starts with"),
            "iendswith": _("ends with"),
        },
        "values": {},
    },
    {
        "field": "description",
        "name": _("Description"),
        "type": "text",
        "operations": {"icontains": _("contains"), "contains": _("contains (case sensitive)")},
        "values": {},
    },
    {
        "field": "short_description",
        "name": _("Short Description"),
        "type": "text",
        "operations": {"icontains": _("contains"), "contains": _("contains (case sensitive)")},
        "values": {},
    },
    {
        "field": "release_date",
        "name": _("Release Date"),
        "type": "date",
        "operations": {"date": _("is exact"), "date__gte": _("is not before"), "date__lte": _("is not after")},
        "values": {},
    },
    {
        "field": "deadline",
        "name": _("Deadline"),
        "type": "date",
        "operations": {"date": _("is exact"), "date__gte": _("is not before"), "date__lte": _("is not after")},
        "values": {},
    },
    {
        "field": "client__name",
        "name": _("Client"),
        "type": "text",
        "operations": {
            "iexact": _("is exact"),
            "icontains": _("contains"),
            "istartswith": _("starts with"),
            "iendswith": _("ends with"),
        },
        "values": {},
    },
]
```

## Customization

Das Design des Query Builder befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/search_query_builder/sq_builder.html`. Das Design der Filterzeile befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/search_query_builder/sq_builder_filter.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- [Generic Filter](generic_filter.md)
