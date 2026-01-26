# Websocket-Komponente (Version 0.1.0)

Mit der `websocket` kann eine Verbindung mit einem anderen Websocket aufgebaut werden, um automatisch Daten zu empfangen. Die empfangenen Daten werden mittels HTMX in dem Container der Komponente eingesetzt. Es wird kein Neuladen der Seite oder irgendeine andere Form von Interaktion benötigt.

## Verwendung

```django
{% load insight_tags %}

{% websocket html_tag_id="websocket" ws_url="/websocket-service/" initial_content="" %}
```

## Parameter

- **html_tag_id** (_str_): Eine eindeutige ID für den Container.
- **ws_url** (_str_): Die URL des Websocket-Service mit welchem eine Verbindung aufgebaut werden soll.
- **initial_content** (_str_): Initialer Inhalt.
- **kwargs**: Zusätzliche Optionen ('id' = Tag-ID).

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- [Live-Content](live_content.md)
