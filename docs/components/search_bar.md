# Search Bar-Komponente (Version 0.1.0)

Ein einfaches Textinput-Feld mit einem großen Button am rechten Ende. Beim absenden wird ein Request an den angegebenen Endpunkt geschickt. Die `search_bar` Komponente unterstützt auch HTMX Requests.

## Verwendung

```django
{% load insight_tags %}

{% search_bar request_view=view_name simple=True %}
```

## Parameter

- **request_view** (_str_): Der Name der View an welche der Request gesendet werden soll.
- **simple** (_bool_): _True_ wenn die Suchleiste ohne Button und kleiner angezeigt werden soll.
- **search_query** (_str_): Ein optionaler Wert der automatisch in dem Textfeld steht.

## Customization

Das Design der Search Bar befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/search_bar.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- Das Textinput-Feld besitzt ein extra Title ("Suche") für Screenreader.

## Verwandte Themen

- _Todo_
