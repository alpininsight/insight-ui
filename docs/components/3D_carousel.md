# 3D Carousel-Komponente (Version 0.1.0)

Mit der `three_d_carousel` Komponente können beliebige Inhalte auf einzigartige Weise dargestellt werden. Die Inhalte werden in einem Kreis angeordnet dargestellt.

## Verwendung

```django
{% load insight_tags %}

{% three_d_carousel carousel_items=3D_carousel.items slides_count=3D_carousel.range_total_slides %}
```

## Parameter

- **carousel_items** (_list_): Daten welche innerhalb des Karussell angezeigt werden sollen (frei definierbar).
- **slides_count** (_range_): Die Anzahl der Seiten.

## Customization

Das Design das Basis-Design der 3D Karussell Komponente befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/carousel/3D_carousel.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- _Todo_
