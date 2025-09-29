# Anpassung

Unser Framework bietet verschiedene Möglichkeiten zur Anpassung, von einfachen Konfigurationsoptionen bis hin zu tiefgreifenden Anpassungen. Im Grunde ist das Insight UI Framework vor allem als Starthilfe für neue Projekte zu verstehen. Es lässt sich mit wenig Aufwand integrieren und verwenden um schnell ein Grundlegendes Layout aufzubauen. Wenn es dann zu konkreten Aufgaben kommt, wofür keine Komponente vorgefertigt wurde, müssen wieder eigene Lösungen her. Um diesen Schritt zu leichter zu gestalten, bietet unser Framework unterschiedliche Möglichkeiten, der Anpassung und Erweiterung.

## Konfiguration über settings.py

- _Todo_

## Theming (anpassen ans Corporate Design)

Unser UI Framework verwendet TailwindCSS für das Styling. Tailwind verwendet eine sog. _input.css_ Datei in welcher sich ein Theme aufbauen lässt, darunter fällt die Definition von grundlegenden Eigenschaften wie Farben, Schriftgrößen oder Fonts. Aber auch komplexere Dinge lassen sich dort definieren, wie zum Beispiel lassen sich dort Custom-CSS-Klassen erstellen oder Animationen definieren. Es lassen sich auch standard definieren, wodurch bestimmte Elemente zum Beispiel Überschriften immer gleich aussehen ohne das dafür überhaupt eine Klasse im HTML-Code angegeben werden muss.

Das Standard-Theme des Insight-UI Frameworks befindet sich in der Datei `insight_ui/utils/input.css`.

Die Datei enthält die folgenden Komponenten, alle zusammen ergeben das Theme.

DÍn der ersten Zeile befindet sich der `@import` für Tailwind, dieser wird benötigt, damit Tailwind aus dieser Datei, später das entsprechende Stylesheet generieren kann.

```css
@import "tailwindcss";
```

In der nächsten Zeile befindet sich eine `@source` Direktive. Diese sagt Tailwind, wo es nach den Template Dateien suchen soll, um die CSS-Tags, welche dort verwendet werden zu finden. I.d.R sollte Tailwind von sich aus alle Projekt spezifischen Templates finden, nur externe Pakete machen ab und zu Probleme, daher steht hier auch der Pfad zu unseren Templates.

Sollte es vorkommen, dass bestimmte Design nicht funktionieren bzw. CSS-Klassen in dem Stylesheet fehlen, kann die Ursache dafür sein, dass Tailwind die Template Dateien nicht finden kann. (_Todo_: weiter ausführen, was dann zu tun ist)

```css
@source "../templates/insight_ui/";
```

Die nächste Zeile wird benötigt für den wechseln zwischen Hell/Dunkel. (_Todo_: eventuell weiter ausführen)

```css
@custom-variant dark (&:where([data-theme=dark], [data-theme=dark] *));
```

Von Haus aus, verwendet Insight-UI den Font _Inter_. Dabei handelt es sich um kein standard System-Font, weshalb dieser explizit angegeben werden muss. Sollte ein anderen Font gewünscht sein, kann dieser an der Stelle ausgetauscht oder ergänzt werden. Der Pfad zum Font ist relative zu der _input.css_, also der Datei in welcher das definiert wird.

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

Die Zeile ` button:not(:disabled), [role="button"]:not(:disabled) { cursor: pointer; }` sorgt bspw. dafür, dass alle Buttons ein `pointer` also ein Hand-Cursor aufzeigen (seit Tailwind V.4.0 nicht mehr standard und deswegen hier angegeben).

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

In der _input.css_ sind beispielsweise Komponenten für Buttons definiert. Diese können in den Templates wie eine normale CSS-Klasse verwendet werden `<button class="btn btn-sm">`. Die Syntax hat hierbei mit klassischen CSS wenig zu tun. Stattdessen werden per `@apply` die jeweiligen Tailwind-Klassen oder auch andere Custom-Klassen hinzugefügt. Ein Vorteil für alle die bisher mit Tailwind gearbeitet haben. (_Todo_: Überprüfen, es sollte auch mit normalen CSS möglich sein.)

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

```
myapp/
  templates/
    insight_ui/
      components/
        navbar.html  # Überschreibt das standard Navbar-Template
```
