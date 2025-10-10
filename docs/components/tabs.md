# Tabs-Komponente (Version 0.1.0)

Mit der `tabs` Komponente lassen sich Tabs bzw. Registrierkarten hinzufügen. Diese Komponente besteht aus einer Reihe von Buttons, welche per HTMX-Request den Hauptinhalt der Komponente austauschen. Dadurch kann der Inhalt flexibel ausgetauscht werden, ohne das die Seite neu geladen werden muss.

## Verwendung

```django
{% load insight_tags %}

{% tabs config %}
```

## Parameter

- **config** (_dict_): Enthält die einzelnen Tabs und ein paar allgemeine Informationen über die Komponente.

### config

Enthält die einzelnen Tabs und ein paar allgemeine Informationen über die Komponente.

```py
{
    "id": "example_tabs",
    "label": "Tabs Example",
    "tabs": [
        {
            "id": "First",
            "view_name": "index",
            "title": _("First Tab"),
        }
    ]
}
```

## Customization

Das Design der Tabs Komponente befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/tabs.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- Die Komponente Unterstützt Screenreader durch die entsprechenden Rollen: `role="tablist"`, `role="tab"`, `role="tabpanel"`.
- Zusätzlich werden die Tabs und deren Inhalte mittels `aria-selected`, `aria-controls`, `aria-labelledby` miteinander Verbunden.
- Der aktuell fokussierte Tab besitzt das Attribute `tabindex="0"` alle anderen `tabindex="-1"`.
- Die Komponente unterstützt die Navigation über die Tastatur mittels der Pfeil- (links/rechts) und Home/End-Tasten.

## Verwandte Themen

- _Todo_