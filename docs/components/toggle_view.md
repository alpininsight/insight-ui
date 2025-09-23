# Toggle-View-Komponente (Version 0.1.0)

Diese Komponente kombiniert die Tabellen und die Karten-Ansicht, sowie die Karussell-Komponente. Diese Komponente wird dazu verwendet, die selben Daten auf komplett unterschiedliche Art und Weise darzustellen.

## Verwendung

Die Toggle-View wird direkt über das `{% toggle_view %}` Tag eingebunden. Diese Komponente erwartet unterschiedliche Parameter, je nach dem, welche View initial eingestellt wird.

```django
{% toggle_view tag_id="test" table_data=toggle_table view_options=view_options current_view=toggle_start_view %}
```

## Parameter

- **tag_id**: Eine eindeutige ID um Konflikte mit den Radio-Buttons der View-Auswahl zu vermeiden (optional, aber empfohlen).
- **table_data**: Die Daten für die Tabellen-Ansicht sofern diese als current_view_ eingestellt ist.
- **view_options**: Eine Liste der View-Varianten welche ausgewählt werden können.
- **current_view**: Die anzuzeigende View-Variante (Start-View).

## Verwandte Themen

- [Tabellenansicht](table.md)
- [Karussell](carousel.md)
