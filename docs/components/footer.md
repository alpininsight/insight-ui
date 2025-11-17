# Footer-Komponente (Version 0.1.0)

Ein einfacher Footer bestehend aus drei Spalten mit anpassbaren Inhalt. Der Footer ist ein wichtiger Bestandteil einer jeden Webseite, er dient jedoch nicht nur dazu, die Webseite optisch abzuschließen. Er enthält i.d.R. mindestens eine Verlinkung zum Impressum und der Datenschutzerklärung. Oft befindet sich im Footer noch einmal eine Navigation zu den wichtigsten Seiten der Webseite und eine Copyright Angabe.

## Verwendung

Die Footer-komponente wird am einfachsten über das `{% footer %}` Tag eingebunden. Für den Footer ist ein entsprechender Block definiert, in welchem dieser platziert werden sollte, damit diese auch garantiert immer am Ende der Webseite erscheint.

```django
{% load insight_tags %}

{% block footer %}
    {% footer data=footer_data %}
{% endblock footer %}
```

## Parameter

- **data** (_dict_): Die Daten welche im Footer angezeigt werden sollen.

### data

Das _data_ Dictionary besteht aus zwei Komponenten. Der _description_ und den Footer-_links_. Die _description_ ist ein kurzer Text, bestehend aus einem maximal zwei Sätzen, welche die Anwendung beschreiben und einer Überschrift, i.d.R. der Titel der Anwendung. Bei den _links_ handelt es sich um Links zu den wichtigsten Seiten der Anwendung. Für Details zu Links siehe [Links](links.md).

```py
"footer_data": {
    "description": {
        "title": "Insight UI",
        "text": "Eine moderne UI-Bibliothek für Django-Anwendungen um schnell zu durchzustarten.",
    },
    "links": [
        {"text": _("Startseite"), "icon": {"name": "home", "size": "small"}, "view_name": "storybook_view"},
        {"text": _("Storybook"), "view_name": "storybook_view"},
        {"text": _("Dokumentation"), "view_name": "storybook_view"},
    ],
},
```

## Customization

Das Design des Footers befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/footer.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- Die Überschriften der drei Spalten verwenden `<h4>`-Tags wodurch ein Screenreader zwischen den Spalten wechseln kann.
- Die Auflistung der Links verwendet ein semantisch korrektes `<ul>`-Tag mit entsprechenden `<li>`-Tags.

## Verwandte Themen

- [Navbar](navbar.md)
- [Links](links.md)
