# Sidebar-Komponente (Version 0.1.0)

Die `sidebar` Komponente fügt einen Bereich an der Fensterseite hinzu. Die Sidebar kann sowohl auf der linken oder auf der rechten Seite sowie auch auf beiden Seiten gleichzeitig angewendet werden. Die Sidebar kann auch als _Drawer_ verwendet werden, in diesem Fall kann sie geschlossen werden.

## Verwendung

Eingebunden wird die Sidebar am einfachsten über das entsprechende _Template-Tag_. Für die Sidebar sind für jede Seite entsprechende Blöcke definiert, in welchem diese platziert werden sollten.

```django
{% load insight_tags %}

{% block sidebar %}
    {% sidebar sidebar_data=left_sidebar_data side="left" %}
{% endblock sidebar %}
```

Oder als _Drawer_

```django
{% load insight_tags %}

{% block drawers %}
    {% sidebar sidebar_data=right_sidebar_data side="right" static=False auto_close=True %}
{% endblock drawers %}
```

## Parameter

- **sidebar_data** (_dict_): Der Inhalt der Sidebar (Titel und Navigations-Elemente).
- **side** (_str_):  Gibt an, an welcher Seite die Sidebar dargestellt werden soll.
- **static** (_bool_): _True_ wenn die Sidebar nicht einklappbar sein soll.
- **auto_close** (_bool_): _True_ wenn die Sidebar sich automatisch schließen soll, wenn der Cursor sie verlässt.

### sidebar_data

Der Inhalt der Sidebar (Titel und Navigations-Elemente).

```py
{
    "title": _("Secondary Sidebar"),
    "icon": {"name": "home", "size": "small"},
    "categories": [
        {
            "caption": "Main",
            "icon": {"name": "home", "size": "small"},
            "items": [
                {
                    "text": _("Notifications"),
                    "icon": {"name": "home", "size": "small"},
                    "url": reverse("index_view"),
                },
                {
                    "text": _("Messages"),
                    "icon": {"name": "home", "size": "small"},
                    "url": reverse("index_view"),
                },
                {"text": _("Tasks"), "icon": {"name": "home", "size": "small"}, "url": reverse("index_view")},
                {
                    "text": _("Calender"),
                    "icon": {"name": "home", "size": "small"},
                    "url": reverse("index_view"),
                },
                {"text": _("Profile"), "icon": {"name": "home", "size": "small"}, "url": reverse("index_view")},
            ],
        }
    ],
}
```

## Customization

Das Design der Sidebar befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/sidebar.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- Die Sidebar verwendet für eine semantische Korrektheit das `<aside>`-Tag und das Attribute `role="complementary"`.
- Die Drawer Variante verwendet Focus-Trapping und besitzt ein *Schließen*-Button, um diese auch per Tastatur verwenden zu können.

## Verwandte Themen

- _Todo_
