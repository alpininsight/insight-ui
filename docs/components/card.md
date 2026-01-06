# Card-Komponente (Version 0.1.0)

Die `card` Komponenten werden dazu verwendet Informationsgruppen zu erstellen. Jede Karte besteht aus einer Überschrift und ihren Hauptinhalt. Dazu gibt es noch weitere Optionen, wie ein Hintergrundbild oder ein Untertitel und Aktion-Buttons.

Für die Card Komponente gibt es unterschiedliche Varianten zur Auswahl:

- **Card**: Standard Karte im 16:9 Format.
- **Horizontale Card**: Das Layout dieser Karte ist vertikal ausgerichtet wodurch dieses länger ist.
- **Flip Card**: Diese Karte dreht sich um 180° und hält auf ihrer Rückseite weiteren Inhalt bereit.

## Verwendung

```django
{% load insight_tags %}

{% card title=card.title subtitle=card.subtitle content=card.content actions=card.actions %}
{% horizontale_card title=card.title subtitle=card.subtitle content=card.content actions=card.actions %}
{% flip_card title=card.title subtitle=card.subtitle content=card.content actions=card.actions %}
```

## Parameter

- **title** (_str_): Der Title der Karte.
- **content** (_str_): Der Hauptinhalt der Karte.
- **subtitle** (_str_): Der Untertitel der Karte.
- **image** (_dict_): Informationen über das Bild der Karte.
- **actions** (_list_): Eine Liste von Aktion-Buttons.

### image

Informationen über das Bild der Karte.

```py
{
    "url": static("insight_ui/img/thumbnail.png"),
    "alt": "Card-Image"
}
```

### actions

Eine Liste von Aktion-Buttons.

```py
{
    {"text": _("Learn more"), "url": "#", "type": "secondary"},
}
```

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- [Carousel](carousel.md)
- [Toggle-View](toggle_view.md)
