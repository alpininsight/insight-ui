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

- **html_tag_id** _(str)_: Eine eindeutige ID für das Modal-Element.
- **title** _(str)_: Ein aussagekräftiger Titel für das Dialogfenster.
- **description** _(str)_: Der hauptinhalt des Dialogs.

## Verwandte Themen

- [Popover](popover.md)
