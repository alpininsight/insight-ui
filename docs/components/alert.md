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

## Barrierefreiheit

Die Alert-Komponente enthält:

- `role="alert"` für Screenreader
