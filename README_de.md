# Insight UI (Version 0.1.0)

> Eine englische Version dieses Dokuments findest du in [README.md](README.md).

Ein modernes und erweiterbares UI-Framework für Django Projekte, das wiederverwendbare, WCAG 2.1 AA-konforme Komponenten und Entwicklungs-Best-Practices bietet.

## Überblick

Das Insight UI Framework bietet eine Sammlung von UI-Komponenten und Hilfsmitteln, welche speziell für die Entwicklung von Django Webanwendungen konzipiert sind.

Die Komponenten des Frameworks sind unter Beachtung der **Barrierefreiheit** implementiert und bieten im Bezug auf **Internationalisierung** eine Unterstützung für ein **RTL-Layout** für Sprachen, welche von rechts nach links gelesen werden.

Für Performance unterstützen entsprechende Komponenten die Verwendung von **HTMX** Requests, um nur einzelne ausschnitte des _DOM_ zzu ändern, ohne einen kompletten Seiten-Reload.

## Entwicklung

```bash
uv sync --all-groups

python manage.py migrate
python manage.py runserver
```

### Websocket

Um das Beispiel der Websocket Kommunikation zu verwenden muss ein weiterer Prozess gestartet werden. Dieser befindet sich in dem Verzeichnis _/utils_.

```bash
uv run ./utils/main.py
```

In dem Verzeichnis _/utils_ gibt es eine extra Readme mit weiteren Informationen.

## Installation (in externes Projekt)

```bash
uv add "git+https://alpin-bot:a205f27ce1045d607e4cdaa7426f3b3fe5a3d5d8@git.alpininsight.com/AlpinInsight/insight-ui@fix"

# or later with

uv add insight-ui
```

1. 'insight_ui' zu INSTALLED_APPS in settings.py hinzufügen:

```python
INSTALLED_APPS = [
    # ...
    'insight_ui',
    # ...
]
```

2. Konfiguration in settings.py hinzufügen und anpassen (siehe Konfiguration)

3. (A) Projekt starten ohne Änderungen am Frontend vornehmen zu wollen
    - `python manage.py collectstatic` um das vorkompilierte insight-ui Stylesheet einzusammeln
    - `python manage.py runserver` Startet den development Server

3. (B) Projekt aufsetzen und starten, wenn das Frontend weiter entwickelt werden soll
    - Django-Tailwind-CLI zu Projekt hinzufügen (`uv add django-tailwind-cli`)
    - Zu `INSTALLED_APPS` hinzufügen, `STATICFILES_DIRS`, `TAILWIND_CLI_SRC_CSS` und `TAILWIND_CLI_DIST_CSS` definieren
    ```py
        INSTALLED_APPS = [
            # ...
            "django_tailwind_cli",
            # ...
        ]

        # Configure static files directory
        STATICFILES_DIRS = [BASE_DIR / "assets"]

		# Tailwind source file
		TAILWIND_CLI_SRC_CSS = BASE_DIR / ".venv/Lib/site-packages/insight_ui/static/insight_ui/css/input.css"

        # Tailwind dist file
        TAILWIND_CLI_DIST_CSS = "insight_ui/css/tailwind.css"
    ```
    - `python manage.py tailwind setup` Für initiales Setup von Tailwind ausführen (lädt u.a. das Tailwind-CLI runter ~120MB)
    - `python manage.py tailwind runserver` Startet den development Server mit hot reload

## Komponenten

Eine Liste aller Komponenten befindet sich in der Documentation [docs/components](docs/components).

### Geplant Verbesserungen und neue Komponenten

- Mehr Varianten für Karten/Kacheln
- Layout: Text + Tags
- Sortierung
    - Einfach (nur eine Parameter)
    - Komplex (nach mehreren Parametern)
- Tabellenspaltengröße vom Nutzer anpassbar

## Dokumentation

Ausführliche Dokumentation befindet sich unter [docs/](docs/).

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz.
