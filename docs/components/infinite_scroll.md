# Infinite-Scroll-Komponente (Version 0.1.0)

Die `infinite_scroll` Komponente stellt eine Alternative zu einer Pagination dar und kann dazu verwendet werden, eine große Menge Daten darzustellen. Anstatt von Seite zu Seite zu wechseln, lädt der Infinite Scroll nach dem ein bestimmter Schwellwert beim Scrollen erreicht wurde, weitere Daten aus dem Backend und fügt diese mittels HTMX an das Ende an.

Die Komponente wird in zwei Varianten zur Verfügung gestellt, eine mit automatischer Erweiterung und eine zweite, wobei zum Laden neuer Elemente aktiv ein Button _Lade weitere_ geklickt werden muss.

## Verwendung

```django
{% load insight_tags %}

{% infinite_scroll items=scroll_items view_name="more_items" auto_fetch=False %}
```

## Parameter

- **items** (_list_): Eine Liste der bereits geladenen Elemente.
- **view_name** (_str_): Der Name der View vom welcher die Daten abgefragt werden sollen.
- **auto_fetch** (_bool_): False wenn der Nutzer aktiv weitere Elemente per Button anfordern soll.
- **threshold** (_int_): Der Pixel-Schwellenwert für das Laden weiterer Elemente (nur wenn **auto_fetch=False**).
- **kwargs**: Zusätzliche Optionen ('id' = Tag-ID).

## Customization

Das Design der Infinite Scroll Komponente befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/infinite_scroll.html`. Das Design der Elemente befindet sich in einer separaten Datei: `insight_ui/templates/insight_ui/components/infinite_scroll_items`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- [Pagination](pagination.md)
