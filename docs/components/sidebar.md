# Sidebar-Komponente (Version 0.1.0)

Die Sidebar-Komponente fügt einen Bereich an der Fensterseite hinzu. Die Sidebar kann sowohl auf der linken, auf der rechten Seite als auch auf beiden Seiten gleichzeitig angewendet werden.

## Verwendung

Eingebunden wird die Sidebar am einfachsten über das entsprechende _Template-Tag_. Für die Sidebar sind für jede Seite entsprechende Blöcke definiert, in welchem diese platziert werden sollten.


```django
{% block sidebar_right %}
    {% include "insight_ui/components/sidebar.html" with title="Sekundäre Sidebar" side="right" auto_close=True collapsible=True sidebar_items=right_sidebar_items %}
{% endblock sidebar_right %}
{% block sidebar_left %}
    {% include "insight_ui/components/sidebar.html" with title="Primäre Sidebar" side="left" auto_close=False collapsible=True sidebar_items=left_sidebar_items %}
{% endblock sidebar_left %}
```

## Parameter

- **title**:
- **side**:
- **auto_close**:
- **collapsible**:
- **sidebar_items**:

## Verwandte Themen

- _Todo_
