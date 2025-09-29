# Infinite-Scroll-Komponente (Version 0.1.0)

Ein _Infinite Scroll_ ist eine gängige Alternative zu einer Pagination und kann dazu verwendet werden, eine große Menge Daten darzustellen. Anstatt von Seite zu Seite zu wechseln, lädt der Infinite Scroll nach dem ein bestimmter Schwellwert beim Scrollen erreicht wurde, weitere Daten aus dem Backend und fügt diese mittels HTMX an das Ende an. 

## Verwendung

```django
{% infinite_scroll items=scroll_items request_view="more_items" %}
```

## Parameter

- **scroll_items**: Eine Liste der bereits geladenen Elemente.
- **request_view**: Der Name der View vom welcher die Daten abgefragt werden sollen.

## Verwandte Themen

- [Pagination](pagination.md)
