# Form-Komponente (Version 0.1.0)

Mit der `form` Komponente lässt sich ohne selbst HTML-Code editieren zu müssen, Formulare bauen.

## Verwendung

```django
{% load insight_tags %}

{% form title="Contact Form" description="Please fill out the form" fields=form_fields actions=form_actions htmx=htmx_config id="htmx-form" %}
```

## Parameter

- _Todo_

## Customization

Das Design der Form Komponente befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/form.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- _Todo__
