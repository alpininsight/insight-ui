# Pagination-Komponente (Version 0.1.0)

Mit der 'paginated_list' Komponente lässt sich eine Liste auf mehrere Seiten aufteilen, welche mittels der durch diese Komponente dargestellte Pagination am Ende der Liste gewechselt werden kann. Dies ist praktisch für große Datenmengen und bietet eine alternative zur [Infinite Scroll](infinite_scroll.md) Komponente.

## Verwendung

```django
{% load insight_tags %}

{% paginated_list current_page=start_page surrounding_pages=surrounding_pages %}
```

## Parameter

- **current_page** (_Page_): Ein von Django erzeugtes Pagination-Objekt der aktuellen Seite.
- **surrounding_pages** (_list_): Eine liste der benachbarten Seiten.

### current_page

Ein von Django erzeugtes Pagination-Objekt der aktuellen Seite.

_Todo_

### surrounding_pages

Eine liste der benachbarten Seiten.

_Todo_

## Customization

Das Design der Pagination befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/pagination.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- [Infinite Scroll](infinite_scroll.md)
