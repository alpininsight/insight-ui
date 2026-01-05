# Filter Komponente (Version 0.2.0)

Mit der `generic_filter` Komponente lassen sich relativ einfach standard Filter, bestehend aus `<select>`-Tags, bauen. Der Filter macht bei einer Änderung automatisch einen Request an den entsprechenden Endpunkt und aktualisiert den Datenbereich mittels HTMX.

Eine alternative hierzu stellt der flexiblere, aber auch kompliziertere [Query Builder](query_builder.md) dar.

## Verwendung

```django
{% load insight_tags %}

{% generic_filter filters=filters view_name=filter_view_name hx_target="#data" hx_push_url="true" vertical=False query_params=request.GET %}
```

## Parameter

- **view_name** (_str_): Der Name der View an welche der Request gesendet werden soll.
- **hx_target** (_str_): Die ID des Containers, dessen Inhalt vom Response ausgetauscht werden soll.
- **hx_push_url** (_str_): "true" wenn die ausgewählten Filterwerte in der URL abgebildet werden sollen, ansonsten "false".
- **filters** (_list_): Definitionen der einzelnen Filter.
- **vertical** (_bool_): _True_ wenn die Filter übereinander angeordnet sein sollen.
- **query_params** (dict): Ein Dictionary um die Werte der Filter zu setzen.

### filters

Mit diesem Parameter werden die einzelnen Filter definiert. Jeder Filter hat zunächst einen **Anzeigetext** und ein **optionales Icon** für die Darstellung im Frontend. Für die Verarbeitung im Backend, bekommt jeder Filter einen **Namen**, sowie eine Liste mit möglichen **Werten**. Um den Benutzer hilfreiche Informationen über die Filter bereitzustellen, kann jeder Filter einen **Erklärungstext** haben.

```py
[
    {
        "text": _("AI model type"),
        "icon": {"name": "rocket", "size": "small"},
        "name": "model_type_filter",
        "values": {
            "placeholder": "-- Select model --",
            "language": "Language Model",
            "vision": "Vision Model",
            "multimodal": "Multimodal Model",
            "audio": "Audio / Speech Processing",
            "recommendation": "Recommendation System",
            "generative": "Generative Model",
        },
        "explanation": _("To filter by the type of AI-Model."),
    },
    {
        "text": _("Runtime"),
        "icon": {"name": "clock", "size": "small"},
        "name": "runtime_filter",
        "values": {
            "placeholder": "-- Select runtime --",
            "cloud": "Cloud (API-based)",
            "edge": "Edge / On-Device",
            "local": "Local (Self-hosted)",
            "hybrid": "Hybrid (Cloud + Local)",
            "serverless": "Serverless Deployment",
        },
        "explanation": _("To filter by the runtime."),
    },
    {
        "text": _("License"),
        "icon": {"name": "doc", "size": "small"},
        "name": "license_filter",
        "values": {
            "placeholder": "-- Select license --",
            "free": "Free / Open Source",
            "freemium": "Freemium",
            "subscription": "Subscription",
            "pay_per_use": "Pay per Use",
            "enterprise": "Enterprise License",
        },
    },
]
```

> **_Info_**: Bei den Filter `values` dient der Wert `-` als Trennlinie, welche nicht anklickbar ist. Der Wert `placeholder` dient als Platzhalter.

## Customization

Das Design der Filter-Komponente befindet sich in dieser Datei: `insight_ui/templates/insight_ui/generic_filter.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- [Query Builder](query_builder.md)
