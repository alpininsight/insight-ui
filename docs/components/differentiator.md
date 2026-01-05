# Differentiator-Komponente (Version 0.1.0)

Mit dem Differentiator lassen sich Unterschiede zwischen zwei Texten grafisch darstellen, was vor allem bei längeren Texten mit nur kleinen Änderungen, eine sehr gute Hilfe bieten kann. Für Texte welche sich mehr oder weniger komplett voneinander unterscheiden, ist diese Komponente wahrscheinlich weniger nützlich.

## Verwendung

```django
{% load insight_tags %}

{{ textA|diff:textB|safe }}
```

## Parameter

- **textA** (_str_): Die ursprüngliche Version des Textes.
- **textB** (_str_): Die veränderte Version des Textes.

## Customization

- _Todo_

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- _Todo_
