# Alert-Komponente (Version 0.1.0)

Die Alert-Komponente bietet eine Möglichkeit, Benutzern wichtige Informationen, Warnungen oder Erfolgsmeldungen anzuzeigen.

## Verwendung

```django
{% load insight_tags %}

{% alert message="Ihre Änderungen wurden gespeichert." type="success" dismissible=True %}
```

## Parameter

- **message** (_str_): Die Hauptnachricht der Benachrichtigung.
- **type** (_str_): Der Typ der Benachrichtigung. Mögliche Werte: (`"info"`, `"success"`, `"warning"`, `"error"`).
- **dismissible** (_bool_): _True_ wenn die Benachrichtigung schließbar sein soll.
- **kwargs**: Weitere optionale Parameter ('id' = Tag-ID).

## Barrierefreiheit

- Die Alert-Box besitzt das Attribute `role="alert"` für die Unterstützung eines Screenreader.
- Der Button zum Schließen ist mit der Tastatur ansteuerbar und besitzt ein entsprechendes `aria-label`.

## Verwandte Themen

- _Todo_
