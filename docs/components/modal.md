# Modal-Komponente (Version 0.1.0)

Mit der Modal Komponente lassen sich anpassbare Dialoge einbauen. Diese können verwendet werden um dem Nutzer zusätzliche Informationen anzuzeigen oder als Bestätigungsdialoge für diverse Aktionen verwendet werden.

## Verwendung

```django
{% load insight_tags %}

<button class="btn btn-primary" data-insight-toggle="modal" data-insight-target="demo-modal">
    {% trans "Open Modal" %}
</button>
{% modal html_tag_id="demo-modal" title=_("Demo Modal") description=_("Dies ist ein Beispiel-Modal mit Standard-Styling!") %}
```

## Parameter

- **html_tag_id** (_str_): Eine eindeutige ID für das Modal.
- **title** (_str_): Der Titel des Modals.
- **description** (_str_): Eine optionale Beschreibung des Modals.
- **content** (_str_): Der Inhalt des Modals (frei definierbarer HTML-Code).
- **actions** (_list_): Eine Liste von Aktion-Buttons.

### actions

Eine Liste von Aktion-Buttons.

```py
{
    {"text": _("Learn more"), "url": "#", "type": "secondary"},
}
```

## Customization

Das Design der Modal Komponente befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/modal.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- Das Modal wird semantisch korrekt als Dialogfenster definiert, durch die Attribute `role="dialog"` und `aria-modal="true"`.
- Für Screenreader bietet das Modal einen Titel und eine (jedoch optionale) Beschreibung, welche mit `aria-labelledby` und `aria-describedby` verlinkt werden
- Das Dialogfenster verwendet Focus-Trapping und besitzt ein *Schließen*-Button, um dieses auch per Tastatur verwenden zu können.

## Verwandte Themen

- [Popover](popover.md)
