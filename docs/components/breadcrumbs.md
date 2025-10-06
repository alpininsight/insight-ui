# Breadcrumbs-Komponente (Version 0.1.0)

Breadcrumbs sind eine sekundäre Navigation, welche dazu verwendet werden, dem Nutzer Klarheit über die hierarchische Struktur einer Webseite zu verschaffen. Dies ist vor allem bei Webseiten mit einer tiefen Struktur, also mit vielen Unterseiten sinnvoll. Webseiten mit einer Tiefe von maximal zwei Stufen bspw. _Übersicht -> Produkt Details_ sollten auf Breadcrumbs verzichten.

Für eine gute Konsistenz sollten Breadcrumbs, wenn sie verwendet werden, überall verwendet werden und nicht nur sporadisch.

## Verwendung

```django
{% load insight_tags %}

{% breadcrumbs items=breadcrumb_items %}
```

## Parameter

- **items** (_list_): Eine Liste von Dictionaries mit den Breadcrumb-Elementen.

### items

Eine Liste von Dictionaries mit den Breadcrumb-Elementen.

```py
"breadcrumb_items": [
    {"text": _("Startseite"), "url": "storybook_view", "icon": {"name": "home", "size": "small"}},
    {"text": _("Demo"), "url": "storybook_view"},
    {"text": _("Komponenten"), "url": None, "active": True},
],
```

- Für mehr Details siehe [Links](links.md)

## Customization

Das Design der Breadcrumb Komponente befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/breadcrumb.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- Die Komponente verwendet ein `<nav>`-Tag mit dem entsprechenden `aria-label="Breadcrumb"`.
- Das aktive Element besitzt das Attribute `aria-current="page"`.

## Verwandte Themen

- [Links](links.md)
