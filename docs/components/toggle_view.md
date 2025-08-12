# Toggle-View-Komponente (Version 0.1.0)

Diese Komponente kombiniert die Tabellen und die Karten-Ansicht, sowie die Karussell-Komponente. Diese Komponente wird dazu verwendet, die selben Daten auf komplett unterschiedliche Art und Weise darzustellen.

## Verwendung

Die Toggle-View wird direkt über das `{% include "insight_ui/components/toggle_view.html" %}` eingebunden. Diese Komponente erwartet unterschiedliche Parameter, je nach dem, welche View initial eingestellt wird.

```django
{% include "insight_ui/components/toggle_view.html" with table_headers=toggle_table_headers table_rows=toggle_table_rows current_view=toggle_current_view %}
```

## Parameter

- _Todo_

## Verwandte Themen

- [Tabellenansicht](table.md)
- [Karussell](carousel.md)
