# Sidebar-Komponente (Version 0.1.0)

Die Sidebar-Komponente fügt einen Bereich an der Fensterseite hinzu. Die Sidebar kann sowohl auf der linken, auf der rechten Seite als auch auf beiden Seiten gleichzeitig angewendet werden.

## Verwendung

Eingebunden wird die Sidebar am einfachsten über das entsprechende _Template-Tag_. Für die Sidebar sind für jede Seite entsprechende Blöcke definiert, in welchem diese platziert werden sollten.


```django
{% block sidebar_right %}
    {% include "insight_ui/components/sidebar.html" with title="Sekundäre Sidebar" side="right" auto_close=True sidebar_items=right_sidebar_items %}
{% endblock sidebar_right %}
{% block sidebar_left %}
    {% include "insight_ui/components/sidebar.html" with title="Primäre Sidebar" side="left" auto_close=False sidebar_items=left_sidebar_items %}
{% endblock sidebar_left %}
```

## Parameter

- **title**: Ein optionaler Titel am oberen Rand der Sidebar.
- **side**: Die Seite an welcher die Sidebar positioniert werden soll ("right" oder "left")
- **auto_close**: True wenn sich die Sidebar automatisch öffnen und schließen soll.
- **sidebar_items**: Eine Liste von Links, welche in der Sidebar angezeigt werden.

## Verwandte Themen

- _Todo_
