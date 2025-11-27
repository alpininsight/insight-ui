# Toggle-View-Komponente (Version 0.1.0)

Die `toggle-view` Komponente kombiniert die Tabellen und die Karten-Ansicht, sowie die Karussell-Komponente. Die Komponente wird dazu verwendet, die selben Daten auf komplett unterschiedliche Art und Weise darzustellen.

## Verwendung

Die Toggle-View wird direkt über das `{% toggle_view %}` Tag eingebunden. Diese Komponente erwartet unterschiedliche Parameter, je nach dem, welche View initial eingestellt wird.

```django
{% toggle_view tag_id="test" data=toggle_table view_radio_config=view_radio_config current_view=toggle_start_view %}
```

## Parameter

- **tag_id** (_str_): Eine einzigartige ID für die Komponente. (Wird für den wechsel der Ansicht benötigt).
- **data** (_list_): Die Daten, welche angezeigt werden sollen.
- **view_radio_config** (_dict_): Die Konfiguration der Radio-Group, zum wechseln der Ansichtsart.
- **current_view** (_str_): Die anzuzeigende View-Variante (Start-View).

## Customization

Das Design der Toggle-View Komponente befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/toggle_view.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- [Tabellenansicht](table.md)
- [Karussell](carousel.md)
