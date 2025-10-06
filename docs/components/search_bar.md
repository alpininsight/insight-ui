# Search Bar-Komponente (Version 0.1.0)

Eine einfaches Text-Input Feld mit einem großen Button am rechten Ende.

## Verwendung

```django
{% search_bar request_view=view_name simple=True %}
```

## Parameter

- **request_view** (_str_): Der Name der View an welche der Request gesendet werden soll.
- **simple** (_bool_): _True_ wenn die Suchleiste ohne Button und kleiner angezeigt werden soll.
- **search_query** (_str_): Ein optionaler Wert der automatisch in dem Textfeld steht.

## Verwandte Themen

- _Todo_
