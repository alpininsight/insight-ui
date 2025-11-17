# Toggle-View-Komponente (Version 0.1.0)

Die `toggle-view` Komponente kombiniert die Tabellen und die Karten-Ansicht, sowie die Karussell-Komponente. Die Komponente wird dazu verwendet, die selben Daten auf komplett unterschiedliche Art und Weise darzustellen.

## Verwendung

Die Toggle-View wird direkt über das `{% toggle_view %}` Tag eingebunden. Diese Komponente erwartet unterschiedliche Parameter, je nach dem, welche View initial eingestellt wird.

```django
{% toggle_view tag_id="test" table_data=toggle_table view_options=view_options current_view=toggle_start_view %}
```

## Parameter

- **tag_id** (_str_): Eine eindeutige ID um Konflikte mit den Radio-Buttons der View-Auswahl zu vermeiden (optional, aber empfohlen).
- **table_data** (_list_): Die Daten für die Tabellen-Ansicht sofern diese als **current_view** eingestellt ist.
- **view_options** (_list_): Eine Liste der View-Varianten welche ausgewählt werden können.
- **current_view** (_str_): Die anzuzeigende View-Variante (Start-View).

## Customization

Das Design der Toggle-View Komponente befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/toggle_view.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- [Tabellenansicht](table.md)
- [Karussell](carousel.md)
