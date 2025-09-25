# Sidebar-Komponente (Version 0.1.0)

Die Sidebar-Komponente fügt einen Bereich an der Fensterseite hinzu. Die Sidebar kann sowohl auf der linken, auf der rechten Seite als auch auf beiden Seiten gleichzeitig angewendet werden.

## Verwendung

Eingebunden wird die Sidebar am einfachsten über das entsprechende _Template-Tag_. Für die Sidebar sind für jede Seite entsprechende Blöcke definiert, in welchem diese platziert werden sollten.

```django
{% block sidebar %}
    {% sidebar sidebar_data=left_sidebar_data side="left" %}
{% endblock sidebar %}
```

Oder als _Drawer_

```django
{% block drawers %}
    {% sidebar sidebar_data=right_sidebar_data side="right" static=False auto_close=True %}
{% endblock drawers %}
```

## Parameter

- **title**: Ein optionaler Titel am oberen Rand der Sidebar.
- **side**: Die Seite an welcher die Sidebar positioniert werden soll ("right" oder "left")
- **auto_close**: True wenn sich die Sidebar automatisch öffnen und schließen soll.
- **sidebar_items**: Eine Liste von Links, welche in der Sidebar angezeigt werden.

## Verwandte Themen

- _Todo_
