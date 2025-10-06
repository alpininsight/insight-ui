# Live-Content-Komponente (Version 0.1.0)

Die `live_content` Komponente aktualisiert ein Fragment regelmäßig mithilfe von HTMX-Abfragen. Sie eignet sich ideal für Dashboards oder Statusansichten, die häufig aktualisiert werden müssen, ohne dass die gesamte Seite neu geladen werden muss.

## Verwendung

```django
    {% load insight_tags %}

    {% live_content url="/api/live-data/" interval=10 id="live-content" %}
```

## Parameter

- **url** (_str_): Die URL an welche der Request für das updaten des Inhalts gesendet werden soll.
- **interval** (_int_): Das Intervall für automatische Updates in Sekunden.
- **initial_content** (_str_): Initialer Inhalt.
- **kwargs**: Zusätzliche Optionen ('id' = Tag-ID).

## Customization

Das Design der Live-Content Komponente befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/live_content.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- [Websocket](websocket.md)
