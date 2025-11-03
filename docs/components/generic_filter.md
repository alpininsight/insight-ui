# Filter Komponente (Version 0.1.0)

Mit der `generic_filter` Komponente lassen sich relativ einfach standard Filter, bestehend aus `<select>`-Tags, bauen. Der Filter macht bei einer Änderung automatisch einen Request an den entsprechenden Endpunkt und aktualisiert den Datenbereich mittels HTMX.

Eine alternative hierzu stellt der flexiblere, aber auch kompliziertere [Query Builder](query_builder.md) dar.

## Verwendung

```django
{% generic_filter view_name="filter_view" filters=filters %}
```

## Parameter

- **view_name** (_str_): Der Name der View an welche der Request gesendet werden soll.
- **filters** (_list_): Definitionen der einzelnen Filter.

### filters

Mit diesem Parameter werden die einzelnen Filter definiert. Jeder Filter hat zunächst einen **Anzeigetext** und ein **optionales Icon** für die Darstellung im Frontend. Für die Verarbeitung im Backend, bekommt jeder Filter einen **Namen**, sowie eine Liste mit möglichen **Werten**. Um den Benutzer hilfreiche Informationen über die Filter bereitzustellen, kann jeder Filter einen **Erklärungstext** haben.

```py
[
    {
        "text": _("Issue Date"),
        "icon": {"name": "home", "size": "small"},
        "name": "issuedate_filter",
        "values": {
            _("All"): "all",
            _("Today & Yesterday"): "newest",
            _("Last 7 days"): "7days",
            _("Last 14 days"): "14days",
            _("Last 30 days"): "30days",
            _("Last 60 days"): "60days",
            _("Without release date"): "missing",
            "-----": "-",  # no actual value, used as a divider
            "2020": "2020",
            "2021": "2021",
            "2022": "2022",
            "2023": "2023",
            "2024": "2024",
            "2025": "2025",
        },
        "explanation": _("To filter by the issue date."),
    },
    {
        "text": _("Deadline"),
        "icon": {"name": "home", "size": "small"},
        "name": "expiration_filter",
        "values": {
            _("All"): "all",
            _("Expires today"): "today",
            _("Expires in 7 days at the earliest"): "7days",
            _("Expires in 14 days at the earliest"): "14days",
            _("Expires in 30 days at the earliest"): "30days",
            _("Expires in 60 days at the earliest"): "60days",
            _("Expires in 120 days at the earliest"): "120days",
            _("Without deadline"): "missing",
            "-----": "-",  # no actual value, used as a divider
            "2020": "2020",
            "2021": "2021",
            "2022": "2022",
            "2023": "2023",
            "2024": "2024",
            "2025": "2025",
        },
        "explanation": _("To filter by the deadline."),
    },
    {
        "text": _("Reward in €"),
        "icon": {"name": "home", "size": "small"},
        "name": "reward_filter",
        "values": {
            _("All"): "all",
            "> 200.000€": "gt_200",
            "> 100.000€": "gt_100",
            "> 50.000€": "gt_50",
            "<= 1,0€": "lt_one",
        },
        "explanation": _("To filter by the reward."),
    },
]
```

## Customization

Das Design der Filter-Komponente befindet sich in dieser Datei: `insight_ui/templates/insight_ui/generic_filter.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- [Query Builder](query_builder.md)
