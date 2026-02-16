# Steps-Komponente (Version 0.1.0)

Mit dieser Komponente kann dem Nutzer der Fortschritt eines Prozesses visuell dargestellt werden, welcher dieser selbst durchführt.  Damit sind Prozesse gemeint, wie zum Beispiel ein typischer Bezahlvorgang. Dieser besteht i.d.R. aus mehreren Schritten, wie die Adresse anzugeben, eine Zahlungsmethode auszuwählen und im Anschluss nochmal die Eingaben zu überprüfen. In diesem Fall muss der Nutzer aktiv werden, damit der Prozess voranschreitet.

## Verwendung

```django
{% load insight_tags %}

{% steps_bar steps_bar_items %}
```

## Parameter

- **items**: Eine Liste der einzelnen Schritte des Prozesses.

### items

Die Liste der einzelnen Schritte, besteht aus Dictionaries welche den jeweiligen Schritt beschreiben.

```py
[
    {"title": "Kontaktdaten", "description": "Informationen zur Person und Anschrift.", "completed": True},
    {"title": "Zahlungsmethode", "description": "Art der Bezahlung.", "completed": False, "current": True},
    {"title": "Überprüfen", "description": "Prüfen der Angaben und Bezahlen.", "completed": False},
],
```

- **title**: Der Titel des jeweiligen Schritts.
- **description**: Eine kurze Beschreibung des jeweiligen Schritts.
- **completed**: _True_ wenn dieser Schritt bereits absolviert wurde.
- **current**: _True_ wenn es sich um den aktuellen Schritt handelt.

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- [Bullet Point List](bullet_point_list.md)
