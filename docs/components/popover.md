# Popover-Komponente (Version 0.1.0)

In manchen Fällen ist es notwendig weitere jedoch eher optionale Informationen anzuzeigen, welche jedoch das gesamtbild stören würden oder für welche einfach nicht genug Platz vorhanden ist. Für diesen Fall sind _Popover_ eine nützliche Komponente. Ähnlich wie ein _Tooltip_ werden auch Popover getrennt vom restlichen Layout dargestellt und stören insofern nicht den Fluss des Layouts. Bei einem Popover handelt es sich um eine Bereich für zusätzliche Informationen, welcher nur angezeigt wird, wenn der Nutzer sich mit dem Mauszeiger über einem bestimmten Element befindet. Im gegensatz zum Tooltip, kann der Nutzer mit dem Mauszeiger auf das Popover gehen, ohne das dieses sich schließt. Dadurch können mit einem Popover auch interaktive Elemente angezeigt werden.

Wenn nur ein kurzer Informationstext angezeigt werden soll, um ein Element mit ein, zwei Wörter zu erklären, sollte stattdessen die [Tooltip-Komponente](tooltip.md) verwendet werden.

## Verwendung

Dieses Element besitzt kein `insight-tag`, da es lediglich ein Auslöser braucht und ein Ziel-Element. Das Ziel-Element kann komplett selbst definiert werden, lediglich die Verbindung durch die **Tag-ID** ist zu beachten.

```html
<button data-popover-trigger="demo-popover" data-position="top" class="btn btn-primary">{% trans "Hover me!" %}</button>
<div id="demo-popover" class="bg-white dark:bg-gray-500 w-64 border border-gray-300 dark:border-0 rounded-sm shadow">
    <!-- Arrow -->
    <div class="popover-arrow absolute left-1/2 -top-2 -translate-x-1/2 w-0 h-0 border-10 border-t-0 border-transparent border-b-white dark:border-b-gray-600"></div>
    <!-- Content -->
</div>
```

> **_Info_**: Der Pfeil kann ausgeschaltet werden, indem der `<div>`-Container unter dem `<!-- Arrow -->` Kommentar entfernt wird.

## data-* Attribute

- **data-popover-trigger=<tooltip_ID>**: Setzt den Auslöser für den Popover auf das Element mit der entsprechenden ID.
- **data-position**: Bestimmt wo im Bezug auf das Element, der Popover angezeigt werden soll. Mögliche Werte sind: `top`, `bottom`, `right` und `left`.

## Parameter

- N.a.

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- [Tooltip](tooltip.md)
- [Modal](modal.md)
