# Insight UI (Version 0.1.0)

Welcome to the **Insight UI** documentation – a modern, extensible UI framework for Django projects that ships with accessible components, opinionated defaults, and productivity tooling.

## What You Get

- **Reusable components** built with Django templates, HTMX, and Tailwind CSS.
- **Accessibility first**: every component follows WCAG 2.1 AA guidelines.
- **Internationalisation ready**: RTL layouts, locale-aware strings, and language switchers.
- **Performance minded**: partial updates through HTMX requests instead of full page reloads.

## Installation

```bash
uv add insight-ui

# Install a specific branch
uv add "git+https://github.com/alpininsight/insight-ui@main"
```

Need to refresh the package after local changes?

```bash
uv pip install --force-reinstall "git+https://github.com/alpininsight/insight-ui@main"
```

## Quickstart

1. Add the app to your Django project:

   ```python
   INSTALLED_APPS = [
       # ...
       "insight_ui",
       # ...
   ]
   ```

2. Configure Insight UI in `settings.py` (see the configuration section below).

3. Decide how you want to work with Tailwind CSS:

   - **Use the prebuilt bundle**
     ```bash
     python manage.py collectstatic
     python manage.py runserver
     ```

   - **Extend the design**
     ```bash
     uv add django-tailwind-cli

     python manage.py tailwind setup   # one-time download (~120 MB)
     python manage.py tailwind runserver
     ```

## Template Tags

Enable the template tags in any template where you use Insight UI components:

```django
{% load insight_tags %}
```

Example component usage:

```django
{% navbar brand=my_brand links=my_links show_searchbar=True %}
{% alert message="Welcome to Insight UI" type="success" %}
```

## Example Layout

```django
{% extends "insight_ui/base.html" %}
{% load static i18n insight_tags %}

{% block title %}{% trans "Project title" %}{% endblock %}

{% block navbar %}
    {% navbar brand=nav_brand links=nav_links show_searchbar=True show_usermenu=True %}
{% endblock %}

{% block content %}
    {# Your content goes here #}
{% endblock %}

{% block footer %}
    {% footer data=footer %}
{% endblock %}
```

## Configuration

```python
INSIGHT_UI = {
    "theme": "light",
    "favicon": "insight_ui/favicon/favicon.ico",
    "favicon_32": "insight_ui/favicon/favicon-32x32.png",
    "favicon_16": "insight_ui/favicon/favicon-16x16.png",
    "apple_touch_icon": "insight_ui/favicon/apple-touch-icon.png",
    "safari_mask_icon": "insight_ui/svg/logo.svg",
    "msapplication_TileColor": "#da532c",
    "theme_color": "#ffffff",
    "stylesheet": "insight_ui/css/tailwind.css",
    "branding": {"name": "Insight UI", "logo": None},
    "meta": {
        "seo": {
            "description": "Starter UI framework for Django projects",
            "keywords": "Django, Insight UI, base template",
            "author": "Alpin Insight AI",
        }
    },
}
```

## Login Page

Insight UI provides a reusable login template. Wire it up by extending Django’s auth URLs and referencing `insight_ui/login.html`:

```python
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="insight_ui/login.html",
            extra_context=get_nav_and_footer_context(),
        ),
        name="login",
    ),
]
```

## Next Steps

- [Components](components/index.md) – browse each UI element.
- [Customization](guides/customization.md) – tailor the theme, branding, and settings.
- [Contributor Guide](contributing.md) – learn how to extend Insight UI safely.
