# Dropdown-Komponente (Version 0.1.0)

Ein Dropdown-Menü bietet die Möglichkeit eine Gruppe von Buttons in einem sich ein- und ausklappbaren Menü zu verstauen. Das ist immer dann sehr nützlich, wenn entweder nur wenig Platz zu Verfügung steht oder die Anzahl der Elemente sonst zu groß und unübersichtlich wäre.

Bei der Verwendung von Dropdown-Menüs ist dennoch zu beachten, das diese nicht überladen werden. In der Regel sollte ein Menü nicht mehr als sieben Elemente besitzen und auch verschachtelte Menüs, also ein Dropdown-Menü in einem Dropdown-Menü sollten vermieden werden.

## Verwendung

```django
{% load insight_tags %}

{% dropdown config=user_dropdown %}
```

## Parameter

- **config** (_dict_): Ein Dictionary welches das Dropdown Menü beschreibt.

### config

Ein Dictionary welches das Dropdown Menü beschreibt.

```py
{
    "tag_id": "user-menu",
    "title": _("User"),
    "show_arrow": True,
    "items": [
        {
            "text": _("Profile"),
            "view_name": "user_profile_view",
            "icon": {"name": "user", "size": "small"},
        },
        ...
    ],
}
```

- **tag_id**: Eine eindeutige ID für das HTML-Tag des Dropdown-Containers.
- **title**: Die Beschriftung des Dropdown-Buttons.
- **show_arrow**: _True_ wenn ein Pfeil neben dem Titel angezeigt werden soll.
- **item**: Eine Liste der Dropdown-Elemente.
    - **text**: Der angezeigte Text des jeweiligen Elements.
    - **view_name**: Der Name der View zu wessen Endpunkt der Request gesendet werden soll.
    - **icon**: Ein optionales Icon welches vor dem Text angezeigt wird.

## Customization

Das Design des Dropdown Menüs befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/dropdown.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- _Todo_
