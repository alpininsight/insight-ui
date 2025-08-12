# Alert-Komponente (Version 0.1.0)

Die Alert-Komponente bietet eine Möglichkeit, Benutzern wichtige Informationen, Warnungen oder Erfolgsmeldungen anzuzeigen.

## Verwendung

```django
{% load insight_tags %}

{% alert message="Ihre Änderungen wurden gespeichert." type="success" dismissible=True %}
```

## Parameter

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `message` | `str` | `""` | Die Hauptnachricht der Benachrichtigung |
| `type` | `str` | `"info"` | Der Typ der Benachrichtigung (`"info"`, `"success"`, `"warning"`, `"error"`) |
| `dismissible` | `bool` | `True` | Ob die Benachrichtigung schließbar sein soll |
| `details` | `str` | `""` | Zusätzliche Details zur Hauptnachricht |
| `id` | `str` | `""` | Eine optionale ID für das Alert-Element |

## Beispiel

```django
{% alert
   message="Es ist ein Fehler aufgetreten."
   type="error"
   details="Bitte versuchen Sie es später erneut oder kontaktieren Sie den Support."
%}
```

## JavaScript-Integration

- _Todo_

## Barrierefreiheit

Die Alert-Komponente enthält:

- `role="alert"` für Screenreader
