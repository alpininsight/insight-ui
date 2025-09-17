# Carousel-Komponente (Version 0.1.0)

Mit einem Karussell können Daten aber vor allem Bilder auf eine spezielle Art, Platzsparend und interaktiv angezeigt werden.

## Verwendung

```django
{% load insight_tags %}

{% carousel carousel_items=carousel_items show_index=True slides_count=range_total_slides items_per_slide=2 %}
```

## Parameter

- **carousel_items** (_list_): Daten welche innerhalb des Karussell angezeigt werden sollen (frei definierbar).
- **show_index** (_bool_): 'True' wenn in der unteren rechten Ecke die aktuelle Seite angezeigt werden soll.
- **show_dots** (_bool_): 'True' wenn unter dem Karussell-Inhalt eine einfache Pagination angezeigt werden soll.
- **autoplay** (_bool_): 'True' wenn das Karussell von alleine durch den Inhalt iterieren soll.
- **slides_count** (_range_): Die Anzahl der Seiten.
- **items_per_slide** (_int_): Die Anzahl an Objekten pro Seite.

## Eigener Inhalt

Es sind zwei Varianten für Karussell Komponente vorgefertigt. Eine für die Darstellung von Bildern und eine für Karten. Die Komponente ist jedoch so gebaut, dass (beinahe) jeder Inhalt dort eingefügt werden könnte. Dazu muss lediglich ein neues Template erstellt werden, welches das Karussell-Template erweitert `{% extends "insight_ui/components/carousel.html" %}`.

In dem neuen Template muss der Block `{% block carousel_content %}` definiert werden. In diesem Block kann dann der gewünschte Inhalt des Karussells definiert werden.

Das Basis-Template des Karussell durchläuft bereits die Schleife, welche durch die `items` iteriert. Daher muss bzw. sollte dies nicht nochmal in dem abgeleiteten Template gemacht werden. Das einzelne Daten-Objekt steht als `item` zur Verfügung. Für mehr Details siehe [Karussell-Template](../../insight_ui/templates/insight_ui/components/carousel.html).

So könnte ein Karussell mit eigenen Inhalt aussehen:

```django
{% extends "insight_ui/components/carousel.html" %}

{% load insight_tags %}

{% block carousel_content %}
    <div>
        <h2>{{ item.titel }}</h2>
        <span>{{ item.subtitel }}</span>

        <p>{{ item.content }}</p>
    </div>
{% endblock carousel_content %}
```

Und so kann anschließend das Karussell eingebunden werden. Über die Parameter können wie zuvor beschrieben, die Grund-Eigenschaften des Karussell gesteuert werden und bei `carousel_items` können beliebige Daten übergeben werden.

```django
{% include "my_carousel.html" with carousel_items=image_carousel_items show_dots=True show_index=True slides_count=range_total_slides items_per_slide=1 %}
```

## Template Datei

- [Template](../../insight_ui/templates/insight_ui/components/carousel.html)

## Verwandte Themen

- _Todo_
