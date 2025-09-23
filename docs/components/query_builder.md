# Query Builder Komponente (Version 0.1.0)

Diese Komponente stell eine alternative für die [Filter](filter.md) Komponente dar. Der Unterschied zwischen den beiden ist, dass diese Variante ähnlich funktioniert wie eine Suche mit SQL. Dieser Filter bekommt eine Liste der Modell-Felder in welchen gesucht werden kann und zu jedem Feld eine Liste der erlaubten Operationen. In speziellen Fällen können auch wie bei der anderen Variante, vordefinierte Werte angegeben werden. Dieser Aspekt macht diese Art der Filterung, u.u. wesentlich flexibler, da auf fest definierte Werte verzichtet wird.

Ähnlich wie bei der anderen Filter Variante, wird hier auch lediglich ein Dictionary mit den gewünschten Eigenschaften benötigt.

## Verwendung

```django
{% sq_builder custom_filters=custom_filters %}
```

## Parameter

- **custom_filters**: Eine Liste mit Dictionaries welches die Filter beschreibt.

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

## Verwandte Themen

- [Filter](filter.md)
