# Accordion-Komponente (Version 0.1.0)

Mit der `accordion` Komponente lassen sich ausklappbare Bereiche für weitere Informationen hinzufügen. Ein Accordion kann entweder ein oder mehrere Bereiche gleichzeitig geöffnet haben. Es besteht die Möglichkeit, dass beim öffnen eines Bereich, ein Anker gesetzt wird. Dadurch lassen sich über die URL bestimmte Bereiche beim aufrufen der Seite aufklappen und die Ansicht scrollt automatisch bis zu dem geöffneten Bereich.

## Verwendung

```django
{% load insight_tags %}

{% accordion id="faq-exclusive" items=accordion_items exclusive=True %}
```

## Parameter

- **id** (_str_): Eine eindeutige ID für das Accordion.
- **items** (_list_): Die einzelnen Bereiche des Accordion.
- **exclusive** (_bool_): _True_ wenn nur ein Element zur selben Zeit geöffnet sein darf.

### items

Die einzelnen Bereiche des Accordion.

```py
[
    {"question": "Was ist Django?", "answer": "Django ist ein Webframework für Python."},
    {"question": "Was ist Tailwind?", "answer": "Tailwind ist ein CSS-Utility-Framework."},
    {"question": "Was ist ARIA?", "answer": "ARIA steht für Accessible Rich Internet Applications."},
]
```

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- _Todo_