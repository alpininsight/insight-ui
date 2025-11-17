# Insight UI (Version 0.1.0)

Willkommen in der Dokumentation von **Insight UI**, einem modernen, erweiterbaren und unseren Gestaltungsprinzipien entsprechendes UI-Framework für Django-Projekte.

## Überblick

Das Insight UI Framework bietet eine Sammlung von UI-Komponenten und Hilfsmitteln, welche speziell für die Entwicklung von Django Webanwendungen konzipiert sind. 

Die Komponenten des Frameworks sind unter Beachtung der **Barrierefreiheit** implementiert und bieten im Bezug auf **Internationalisierung** eine Unterstützung für ein **RTL-Layout** für Sprachen, welche von rechts nach links gelesen werden.

Für Performance unterstützen entsprechende Komponenten die Verwendung von **HTMX** Requests, um nur einzelne ausschnitte des _DOM_ zu ändern, ohne einen kompletten Seiten-Reload.

## Installation

```bash
uv add insight-ui

# or

uv add "git+https://alpin-bot:a205f27ce1045d607e4cdaa7426f3b3fe5a3d5d8@git.alpininsight.com/AlpinInsight/insight-ui@fix"
```

Es kann passieren das Änderungen nicht sofort bemerkt werden, in dem Fall kann folgenden Befehl aushelfen:

```bash
uv pip install --force-reinstall "git+https://alpin-bot:a205f27ce1045d607e4cdaa7426f3b3fe5a3d5d8@git.alpininsight.com/AlpinInsight/insight-ui@fix"
```

## Schnellstart

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

## Template-Tags in den Templates aktivieren

```django
{% load insight_tags %}
```

## Komponenten in den Templates einfügen

```django
{% navbar brand="Meine App" %}

{% alert message="Willkommen bei Insight UI!" type="success" %}
```

## Beispiel Template

Der folgende Code-Ausschnitt zeigt ein typisches Template-Gerüst für eine Webseite:

```django
{% extends "insight_ui/base.html" %} {% comment %} Always extend "insight_ui/base.html" {% endcomment %}
{% load static i18n insight_tags %} {% comment %} Load tags for static files, translation and ui-elements {% endcomment %}

{% block title %}{% trans 'Project-Title' %}{% endblock %}

{% comment %} Define the navigation in the "navbar" block {% endcomment %}
{% block navbar %}
    {% navbar brand=nav_brand links=nav_links show_searchbar=True show_usermenu=True user=user show_login=True %}
{% endblock navbar %}

{% comment %} Main content of the webpage {% endcomment %}
{% block content %}
    {% comment %} Your content {% endcomment %}
{% endblock content %}

{% comment %} Define the footer in the "footer" block {% endcomment %}
{% block footer %}
    {% footer data=footer %}
{% endblock footer %}
```

## Konfiguration

Es gibt einige Einstellungen für die Insight UI, welche über die settings.py angepasst werden können:

```python
# Insight UI Einstellungen
INSIGHT_UI = {
    "theme": "light",
    "favicon": "insight_ui/favicon/favicon.ico",
    "favicon_32": "insight_ui/favicon/favicon-32x32.png",
    "favicon_16": "insight_ui/favicon/favicon-16x16.png",
    "apple_touch_icon": "insight_ui/favicon/apple-touch-icon.png",
    "safari_mask_icon": "insight_ui/svg/logo.svg",  # Used by Safari pinned tab
    "msapplication_TileColor": "#da532c",  # Sets the background color for a live tile (MS Edge only)
    "theme_color": "#ffffff",
    "stylesheet": "insight_ui/css/tailwind.css",
    "branding": {"name": "Insight UI", "logo": None},
    "meta": {
        "seo": {
            "description": "Schnellstart UI-Framework für Django-Projekte",
            "keywords": "Django, Insight UI, base template",
            "author": "Alpin Insight AI",
        }
    },
    "load_prism": True,
    "load_leaflet": True,
    "load_echarts": True,
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
