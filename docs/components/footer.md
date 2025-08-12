# Footer-Komponente (Version 0.1.0)

- Ein Footer sollte immer vorhanden sein, da er eine Webseite optisch abschließt und i.d.R. das Impressum enthält. 

## Verwendung

Eingebunden wird die Navbar am einfachsten über das `{% footer %}` Tag. Für den Footer ist ein entsprechender Block definiert, in welchem dieser platziert werden sollte.

```django
{% load insight_tags %}

{% block footer %}
    {% footer data=footer_data %}
{% endblock footer %}
```

## Parameter

- **data**: Ein Dictionary mit den Daten, welche im Footer angezeigt werden sollen.

### data

Das _data_ Dictionary besteht aus zwei Komponenten. Der _description_ und den Footer-_links_. Die _description_ ist ein kurzer Text, bestehend aus einem maximal zwei Sätzen, welche die Anwendung beschreiben und einer Überschrift, i.d.R. der Titel der Anwendung. Bei den _links_ handelt es sich um Links zu den wichtigsten Seiten der Anwendung. Für Details zu Links siehe [Links](links.md).

```py
"footer_data": {
    "description": {
        "title": "Django Insight UI",
        "text": "Eine moderne UI-Bibliothek für Django-Anwendungen mit Fokus auf Barrierefreiheit und Benutzerfreundlichkeit.",
    },
    "links": [
        {"text": _("Startseite"), "icon": {"name": "home", "size": "small"}, "view_name": "storybook_view"},
        {"text": _("Storybook"), "view_name": "storybook_view"},
        {"text": _("Dokumentation"), "view_name": "storybook_view"},
    ],
},
```

## Verwandte Themen

- [Navbar](navbar.md)
- [Links](links.md)
