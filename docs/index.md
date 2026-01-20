# Insight UI

Willkommen in der Dokumentation von **Insight UI**, einem modernen, erweiterbaren und nach dem WCAG Prinzipien gestaltetes UI-Framework für Django-Projekte.

## Warum sollte ich das brauchen?

Nun...

Du möchtest deiner Django Anwendung ein möglichst hübsches und modernes Frontend verpassen, aber hast keine Lust auf:
- JavaScript und CSS
- das Basteln von Utilities wie Dropdowns oder Accordions, etc.
- das Design auch für Smartphones anzupassen
- und vor allem, sich mit den Grundlagen der Barrierefreiheit zu beschäftigen?

Dann ist das die Antwort, denn alle diese Sachen erledigt unser Framework für dich. Das einziege was du tun musst, ist dein Layout zusammenbasteln und deinen Inhalt einbauen. Sorry, aber das bisschen HTML können wir dir leider echt nicht ersparen.

## Überblick

Das Insight UI Framework bietet eine Sammlung von UI-Komponenten und Hilfsmitteln, welche speziell für die Entwicklung von Django Webanwendungen konzipiert sind. 

Die Komponenten des Frameworks sind unter Beachtung der **Barrierefreiheit** implementiert und bieten im Bezug auf **Internationalisierung** eine Unterstützung für ein **RTL-Layout** für Sprachen, welche von rechts nach links gelesen werden.

Für Performance unterstützen entsprechende Komponenten die Verwendung von **HTMX** Requests, um nur einzelne ausschnitte des _DOM_ zu ändern, ohne einen kompletten Seiten-Reload.

## Installation

```bash
uv add insight-ui

# oder die Git-Quelle verwenden

uv add "git+https://github.com/alpininsight/insight-ui@main"
```

## Schnellstart

1. 'insight_ui' zu INSTALLED_APPS in der settings.py hinzufügen:

```python
INSTALLED_APPS = [
    # ...
    'insight_ui',
    # ...
]
```

2. Konfiguration in settings.py hinzufügen und anpassen (siehe Konfiguration)
	- Die Konfiguration muss über `from insight_ui.config import get_config` an den `Context` der View übergeben werden.

3. (A) Projekt starten ohne Änderungen am Frontend vornehmen zu wollen
    - `python manage.py collectstatic` um das u.a. das insight-ui Stylesheet einzusammeln
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
        STATICFILES_DIRS = [BASE_DIR / "static"]
		
		# Tailwind source file
		TAILWIND_CLI_SRC_CSS = BASE_DIR / ".venv/Lib/site-packages/insight_ui/utils/input.css"

        # Tailwind dist file
        TAILWIND_CLI_DIST_CSS = "insight_ui/css/tailwind.css"
		
		# Prevent automatic updating (recommended)
		# Why? Because this is a silent process that can lead to silent problems if the process is terminated too quickly.
		TAILWIND_CLI_AUTOMATIC_DOWNLOAD = False
    ```
    - `python manage.py tailwind setup` Für initiales Setup von Tailwind ausführen (lädt u.a. das Tailwind-CLI runter ~120MB)
    - `python manage.py tailwind runserver` Startet den development Server und aktualisiert automatisch das Stylesheet (ACHTUNG: eventuelle Fehler der Tailwind-CLI werden nicht geloggt!)

## Änderungen der Konfiguration

Die Konfiguration von `STATICFILES_DIRS`, `TAILWIND_CLI_SRC_CSS` und `TAILWIND_CLI_DIST_CSS` kann im Nachhinein angepasst werden,
jedoch muss anschließend `python manage.py tailwind setup` erneut ausgeführt werden.

## Verwendung

Nach der Installation und Konfiguration können einzelne **Komponenten** und das **Basis-Template** verwendet werden.

### Zugriff auf Komponenten

> Bevor die Komponenten verwendet werden können, muss das **Insight-UI Stylesheet** geladen werden.

Um eine der Frontend Komponenten verwenden zu können, müssen zuvor die `insight_tags` geladen werden:

```django
{% load insight_tags %}
```

Anschließend können einige Komponenten direkt verwendet werden:

```django
{% navbar brand="Meine App" %}

{% alert message="Willkommen bei Insight UI!" type="success" %}
```

Manche Komponenten benötigen jedoch das laden weiterer JavaScript Dateien. Am einfachsten ist die Verwendung des **Basis Templates**.

### Basis Template

Das Basis Template bietet eine Strukturierte Vorlage, welche sämtliche Scripte und Stylesheets bereits lädt.

Die Verwendung erfolgt einfach über `{% extends %}`:

```django
{% extends "insight_ui/base.html" %}
```

Für eine detaillierte Erklärung, siehe [Basis Template](base_template.md).

## Konfiguration

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
    "navbar_fixed": True,  # Should the navigation stick at the top of the window (has impact on the sidebars as well)
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

## Login Screen

Das Framework stell bereits ein standard Login-Screen bereit. Um diesen zu verwenden müssen jedoch ein paar Dinge eingestellt werden.

Die build-in Views von Django's Authentication-Systems müssen zu den Projekt URL's hinzugefügt werden. Anschließend, muss um den Login Screen verwenden zu können, eine weitere URL hinzugefügt werden. Diese kann auf einen beliebigen Endpunkt zeigen, sinnvollerweise sollte es aber irgendetwas wie **login/** sein. Das Template, welches verwendet werden soll, muss **insight_ui/login.html** lauten und damit die navigation und der Footer korrekt gefüllt werden können, müssen die entsprechenden Kontext-Variablen übergeben werden.

```py
from django.urls import include, path

urlpatterns = [
    # ...
    path("accounts/", include("django.contrib.auth.urls")),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="insight_ui/login.html", extra_context=get_nav_and_footer_context()),
        name="login",
    ),
    # ...
]
```

## Nächste Schritte

- [Komponenten](components/index.md): Eine Übersicht über alle UI-Komponenten
- [Anpassung](guides/customization.md): Eine Anleitung zum Konfigurieren und Anpassen des Erscheinungsbildes
- [Barrierefreiheit](guides/accessibility.md): Hilfreiche Informationen zum Thema Barrierefreiheit
