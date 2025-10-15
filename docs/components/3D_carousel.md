# 3D Carousel-Komponente (Version 0.1.0)

Mit der `three_d_carousel` Komponente können beliebige Inhalte auf einzigartige Weise dargestellt werden. Die Inhalte werden in einem Kreis angeordnet dargestellt.

## Verwendung

```django
{% load insight_tags %}

{% three_d_carousel tag_id="threeD_carousel" velocity=300 carousel_items=3D_carousel.items %}
```

## Parameter

- **tag_id** (_str_): Eine eindeutige ID für das Karussell.
- **velocity** (_int_): Die Geschwindigkeit mit welcher sich das Karussell drehen soll.
- **face_camera** (_bool_): _True_ wenn die Karten immer in Richtung der Kamera ausgerichtet sein sollen.
- **carousel_items** (_list_): Daten welche innerhalb des Karussell angezeigt werden sollen (frei definierbar).

## Customization

Das Design das Basis-Design der 3D Karussell Komponente befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/carousel/3D_carousel.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- _Todo_
