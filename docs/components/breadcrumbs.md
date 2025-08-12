# Breadcrumbs-Komponente (Version 0.1.0)

Breadcrumbs sind eine sekundäre Navigation, welche dazu verwendet werden, dem Nutzer Klarheit über die hierarchische Struktur einer Webseite zu verschaffen. Dies ist vor allem bei Webseiten mit einer tiefen Struktur, also mit vielen Unterseiten sinnvoll. Webseiten mit einer Tiefe von maximal zwei Stufen bspw. _Übersicht -> Produkt Details_ sollten auf Breadcrumbs verzichten.

Für eine gute Konsistenz sollten Breadcrumbs, wenn sie verwendet werden, überall verwendet werden und nicht nur sporadisch.

## Verwendung

```django
{% load insight_tags %}

{% breadcrumbs items=breadcrumb_items %}
```

## Parameter

- **items**: Eine Liste mit Links.

### items

Eine Liste von Links für eine mögliche Breadcrumb Anzeige sieht folgendermaßen aus:

```py
"breadcrumb_items": [
    {"text": _("Startseite"), "url": "storybook_view", "icon": {"name": "home", "size": "small"}},
    {"text": _("Demo"), "url": "storybook_view"},
    {"text": _("Komponenten"), "url": None, "active": True},
],
```

- Für mehr Details siehe [Links](links.md)

## Verwandte Themen

- [Links](links.md)
