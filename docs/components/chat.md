# Chat-Komponente (Version 0.1.0)

Die Chat Komponente bietet ein einfaches Frontend für eine Chat-Anwendung. Die Komponente besteht aus einem Text-Input und einem Bereich für die Nachrichten. Der Inhalt des Nachrichtenbereichs wird mittels HTMX bei jedem Response erweitert, ohne dass die Seite neu geladen wird.

## Verwendung

```django
{% load insight_tags %}

{% chat view_name=view_name %}
```

## Parameter

- **view_name** (_str_): Der Name der View an welchen der Request gesendet werden soll.

## Customization

Das Design der Chat Komponente befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/chat.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- _Todo_
