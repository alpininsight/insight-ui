# Anpassung

Unser UI Framework bietet nicht nur eine reihe von nützlichen Komponenten, sondern lässt sich auch vollkommen nach allen Wünschen anpassen. Farben und immer wiederkehrende Elemente, wie das Aussehen von Überschriften lassen sich an nur einer Stelle anpassen und sofort passt sich das Design an. Es lassen sich aber auch neue Komponenten hinzufügen und bestehende Komponenten anpassen. Sollte also eine Komponente nicht komplett passen, lässt sich diese mit relativ wenig Aufwand entsprechende anpassen.

In den folgenden Abschnitten werden die unterschiedlichen Möglichkeiten der Anpassung beschrieben.

## Konfiguration über settings.py

Es gibt eine Reihe von Einstellungen, welche über die `settings.py` definiert werden können.

```python
INSIGHT_UI = {
    "favicon": "insight_ui/favicon/favicon.ico",
    "favicon_32": "insight_ui/favicon/favicon-32x32.png",
    "favicon_16": "insight_ui/favicon/favicon-16x16.png",
    "apple_touch_icon": "insight_ui/favicon/apple-touch-icon.png",
    "safari_mask_icon": "insight_ui/svg/logo.svg",  # Used by Safari pinned tab
    "msapplication_TileColor": "#da532c",  # Sets the background color for a live tile (MS Edge only)
    "theme_color": "#ffffff",  # For the search bar on mobile devices
    "stylesheet": "insight_ui/css/tailwind.css",  # Only change in case of using alternative stylesheet (currently not supported)
    "meta": {
        "seo": {
            "description": "My indispensable app",
            "keywords": "Django, Insight UI",
            "author": "It's me",
        }
    },
    "load_prism": False,  # Turn to 'True' to use syntax highlighting
    "load_leaflet": False,  # Turn to 'True' to use geo-maps
    "load_echarts": False,  # Turn to 'True' to use Chart-Components
	"JS_DEBUG": False,  # Turn to 'True' to enable build in browser console logging
}
```

## Theming (anpassen ans Corporate Design)

Unser UI Framework verwendet [TailwindCSS](https://tailwindcss.com/) für das Styling. Tailwind verwendet eine sog. _input.css_ Datei, in welcher sich ein Theme aufbauen lässt. Darunter fällt die Definition von grundlegenden Eigenschaften wie Farben, Schriftgrößen oder Fonts, aber auch Custom-CSS-Klassen erstellen oder Animationen lassen sich dort definieren. Dank Tailwinds Preflight Funktion lassen sich auch Standards definieren, wodurch bestimmte Elemente zum Beispiel Überschriften immer gleich aussehen ohne das dafür überhaupt eine Klasse im HTML-Code angegeben werden muss. Die einzelnen Möglichkeiten und Bereiche der _input.css_ werden in den nächsten Abschnitten näher erläutert.

Das Standard-Theme des Insight-UI Frameworks befindet sich in der Datei `insight_ui/utils/input.css`.

### Customization

Um das Theming anzupassen muss diese Datei kopiert werden und anschließend in der Konfiguration von _Insight-UI_ in den `settings.py` angeben werden.

```py
TAILWIND_CLI_SRC_CSS = "my-path/to/input.css"
```

In dieser muss der Pfad zu den _Insight-UI_ Templates angepasst werden:

```css
@source "../templates/insight_ui/";
```

ersetzen durch:

```css
@source ".venv/Lib/site-packages/insight_ui/templates/insight_ui";
```

Anschließend muss `python manage.py tailwind setup` ausgeführt werden.

### Inhalt der input.css

Die Datei enthält die folgenden Komponenten, alle zusammen ergeben das Theme.

In der ersten Zeile befindet sich der `@import` für Tailwind, dieser wird benötigt, damit Tailwind aus dieser Datei, später das entsprechende Stylesheet generieren kann.

```css
@import "tailwindcss";
```

In der nächsten Zeile befindet sich eine `@source` Direktive. Diese sagt Tailwind, wo es nach den Template Dateien suchen soll, um die CSS-Tags, welche dort verwendet werden zu finden. I.d.R sollte Tailwind von sich aus alle Projekt spezifischen Templates finden, nur externe Pakete machen ab und zu Probleme, daher steht hier auch der Pfad zu unseren Templates.

```css
@source "../templates/insight_ui/";
```

Die nächste Zeile wird benötigt für den wechseln zwischen Hell/Dunkel.

```css
@custom-variant dark (&:where([data-theme=dark], [data-theme=dark] *));
```

Von Haus aus, verwendet Insight-UI den Font [Inter](https://fonts.google.com/specimen/Inter). Dabei handelt es sich um kein standard System-Font, weshalb dieser explizit angegeben werden muss. Sollte ein anderen Font gewünscht sein, kann dieser an der Stelle ausgetauscht oder ergänzt werden. Der Pfad zum Font ist relative zu der _input.css_, also der Datei in welcher das definiert wird.

```css
@font-face {
    font-family: "Inter";
    src: url("../font/Inter.ttf");
}
```

Das ist ja alles ganz nett, aber wo sind die Farben? Nun, bis auf den Font sind die bisherigen Schritte notwendig und sollten auch nicht ohne Grund verändert werden. Das eigentliche Theme kommt jetzt erst. Passenderweise wird der Block mit `@theme` deklariert. In diesem Block werden all die Theme spezifischen Variablen definiert. Darunter auch Farben.

Doch zunächst nochmal der Font. In dem Theme-Block lässt sich auch ein Default-Font einstellen, welcher für alle Texte im gesamten Projekt verwendet wird, ohne in jedes mal explizit angeben zu müssen. Die Direktive `--font-sans: "Inter", sans-serif;` sagt, dass jeder Text, der keine Serifen besitzen soll, den Font _Inter_ verwenden soll. (_Todo_: ist das tatsächlich die beste Variante und was ist mit mehreren Fonts?)

```css
@theme {
  --font-sans: "Inter", sans-serif;

  --color-insight-primary: #3b82f6;
  ...
  --color-insight-text-link-hover: #93c5fd;

  --animate-blink: blink 2s step-start infinite;

  @keyframes blink {
    0%, 100% {
      opacity: 0;
    }
    50% {
      opacity: 100;
    }
  }
}
```

Während die Variablen welche in dem Theme-Block definiert wurden, sich manuell auf Elemente anwenden lassen und jeweils eine Eigenschaft anpassen, können auch komplette Designs für bestimmte HTML-Tags vordefiniert werden. Dies funktioniert mittels Tailwinds _Preflight_ Modul. Dieses entfernt vor allem alle Default Styles der HTML-Elemente wodurch beispielsweise alle `<h>` gleich aussehen. Das passiert, u.a. um die verschiedenen Browser-Defaults zu entfernen, damit die Seite in jedem Browser gleich aussieht. Zum anderen lassen sich darüber aber auch direkt Styles für bestimmte Elemente hinzufügen.

Die Zeile `button:not(:disabled), [role="button"]:not(:disabled) { cursor: pointer; }` sorgt bspw. dafür, dass alle Buttons ein `pointer` also ein Hand-Cursor aufzeigen (seit Tailwind V.4.0 nicht mehr standard und deswegen hier angegeben).

Die direktive drunter für das `<h1>` Tag, gibt an dass die dort aufgelistet CSS-Klassen auf jedes `<h1>` Tag angewendet werden sollen. Dadurch müssen nicht bei jedem Tag, diese Klassen manuell hinzugefügt werden. Sollte es mal zu ausnahmen kommen, können im Template trotzdem noch weitere CSS-klassen ergänzt werden oder überschrieben werden. So werden Überschriften mit `<h1 class="text-red-500>` trotzdem in Rot dargestellt.

```css
@layer base {
  button:not(:disabled), [role="button"]:not(:disabled) { cursor: pointer; }

  h1 {
      @apply text-3xl font-bold text-insight-text-primary dark:text-white mb-4;
  }
}
```

Der nächste Block heißt `components` und enthält sozusagen Custom-CSS-Klassen. Warum keine Custom-CSS-Klassen in dem eigentlichen Stylesheet? Theoretisch gibt es kein konventionelles Stylesheet, da dieses von Tailwind erzeugt wird und zwar jedes mal wenn sich etwas an den Templates ändert. Insofern der Tailwind-Compiler läuft. Dabei wird jedes mal die gesamte Datei neu erstellt und alle manuell hinzugefügten Klassen gehen verloren. Um trotzdem vorgefertigte Konstrukte verwenden zu können, ohne jedes mal zwanzig CSS-klassen kopieren zu müssen, lassen sich `components` definieren. 

In der _input.css_ sind beispielsweise Komponenten für Buttons definiert. Diese können in den Templates wie eine normale CSS-Klasse verwendet werden `<button class="btn btn-sm">`. Die Syntax hat hierbei mit klassischen CSS wenig zu tun. Stattdessen werden per `@apply` die jeweiligen Tailwind-Klassen oder auch andere Custom-Klassen hinzugefügt. Ein Vorteil für alle die bisher mit Tailwind gearbeitet haben.

```css
@layer components {
  .btn {
    @apply flex gap-2 items-center justify-center border-2 rounded-sm text-white px-5 py-1.5;
  }
  ...
}
```

## Template überschreiben

Es besteht die Möglichkeit, die bereitgestellten Komponenten anzupassen. Dafür muss lediglich das entsprechende Template der Komponente in das eigene Projekt-Verzeichnis kopiert werden.

Wichtig ist nur, dass das kopierte Template in diesem Pfad `templates/insight_ui/components/` abgelegt wird. Das Verzeichnis muss sich im Root-Verzeichnis des Projektes befinden.

Beispiel:

```bash
myapp/
  templates/
    insight_ui/
      components/
        navbar.html  # Überschreibt das standard Navbar-Template
```
