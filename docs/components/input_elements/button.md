# Button-Komponente (Version 0.1.0)

Für einen gewöhnlichen Button stellt unser UI-Framework eine Reihe von CSS-Klassen zur Verfügung. Damit lassen sich Buttons für unterschiedliche Szenarien ohne großen Aufwand mit gängigen CSS-Klassen einbauen.

## Verwendung

```django
    <button class="btn btn-primary">{% trans "Primary" %}</button>
```

Die Klasse **btn** gibt dem Button seine Form, aber weder Farbe noch Effekte.

### Farbe / Hover-Effekte

Für die Auswahl der Farbe, gibt es die folgenden Varianten:

- **btn-primary**: Für die primären und damit wichtigsten Buttons.
- **btn-secondary**: Für die etwas weniger wichtigen Buttons.
- **btn-info**: Für rein informative Buttons.
- **btn-success** Für Buttons zum Bestätigen von etwas positiven.
- **btn-warning**: Für Buttons welche eine möglicherweise gefährliche Aktion ausführen.
- **btn-danger**: Für Buttons die eine definitiv gefährliche Aktion ausführen (z.b.: Account Löschen).

### Outline

Für Buttons ohne Füllung gibt es die gleichen Varianten mit **outline** in der Mitte, also bspw. **btn-outline-primary**.

### Größe

Um die Größe eines Buttons anzupassen, kann eine der folgende Klassen hinzugefügt werden:

- **btn-large**: Groß.
- **btn-sm**: Klein.
- **btn-xs**: Sehr Klein.

### Icon

Für ein Button ohne Text gibt es eine extra Klasse, welche einen quadratischen Button darstellt:

- **btn-icon**: Quadratisch und enthält nur ein Icon.

## Customization

Alle `btn-*`-Klassen sind in der Datei `insight_ui/utils/input.css` innerhalb des `@layer components` Bereichs definiert und können dort nach belieben angepasst werden.

## Barrierefreiheit

### Tips

- Buttons welche lediglich ein Icon besitzen und keinen Text, sollten ein beschreibendes `aria-label` besitzen.
- Ein Button sollte so wie der Rest der Webseite, immer auch mit der Tastatur ansteuer- und bedienbar sein.
- Für die korrekten Einhaltung der Semantik, ist ein `<button>` einem interaktivem `<div>`-Container immer vorzuziehen.

## Verwandte Themen

- _Todo_
