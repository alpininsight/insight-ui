# Tooltip-Komponente (Version 0.1.0)

Manchmal ist die Beschriftung oder das Icon eines Buttons o.ä. nicht eindeutig genug und lässt Raum für Interpretationen, was im schlimmsten Fall zu Verwirrung führen kann. In solchen Fällen ist es hilfreich und wichtig, zusätzliche Informationen anzuzeigen. Um nicht den Fluss der Weboberfläche zu stören, eignen sich _Tooltips_. Diese werden nur angezeigt, wenn der Nutzer sich mit dem Mauszeiger über dem entsprechenden Element befindet. Der Tooltip wird getrennt wom restlichen Layout über allen anderen Elementen angezeigt und ist damit immer sichtbar und stört nicht das gesamtbild.

Ein Tooltip sollte nur für kurze Informationstexte (meist nur ein Wort) verwendet werden, wenn mehr Informationen angezeigt werden sollen, sollte stattdessen die [Popover-Komponente](popover.md) verwendet werden.

## Verwendung

```django
<button data-tooltip-trigger="tt-demo-bottom" data-position="bottom" class="btn btn-primary">{% trans "Click me!" %}</button>
{% include "insight_ui/components/tooltip.html" with text=_("This is a tooltip.") tag_id="tt-demo-bottom" %}
```

## data-* Attribute

- **data-tooltip-trigger=<tooltip_ID>**: Setzt den Auslöser für den Tooltip auf das Element mit der entsprechenden ID.
- **data-position**: Bestimmt wo im Bezug auf das Element, der Tooltip angezeigt werden soll. Mögliche Werte sind: `top`, `bottom`, `right` und `left`.

## Parameter

- **text**: Der anzuzeigende Text.
- **tag_id**: Eine einzigartige ID für den Tooltip, diese muss bei dem auslösenden Element ebenfalls angegeben werden.

## Customization

Das Design der Tooltip Komponente befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/tooltip.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- [Popover](popover.md)
