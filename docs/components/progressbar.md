# Progressbar-Komponente (Version 0.1.0)

> **_Info_**: Diese Komponente befindet sich noch in Bearbeitung!

Die `progress_bar` Komponente wird dafür verwendet dem Nutzer den Fortschritt eines im Hintergrund laufenden Prozesses visuell darzustellen. Ein gängiges Szenario für solche Komponenten sind zum Beispiel Downloads.

Für eine Fortschrittsanzeige wo der Fortschritt durch aktives Zutun des Nutzers entsteht, eignet sich unsere [Step Bar](step_bar.md) Komponente.

## Verwendung

```django
{% include "insight_ui/components/progress_bar.html" %}
```

## Parameter

- N.a.

## Customization

Das Design der Progressbar Komponente befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/progress_bar.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- [Step Bar](step_bar.md)
