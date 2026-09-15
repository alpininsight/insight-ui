<!--
SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
SPDX-License-Identifier: AGPL-3.0-only
-->

# Getting Started

This guide integrates the reusable package into **your existing Django project**. If you want to work on Insight UI itself instead, see [CONTRIBUTING.md](../CONTRIBUTING.md).

## Install The Package

Use the supported Python/Django versions in [README.md](../README.md). Stable releases are available on [PyPI](https://pypi.org/project/insight-ui/). Install the package into your project's environment:

```bash
uv add insight-ui
```

For local development against an unpublished change, use your reviewed source checkout:

```bash
uv add --editable /absolute/path/to/insight-ui
```

For editable source, first build package assets as described in [Static assets](static-assets.md). A released wheel provides readable assets.

## Configure Your Project

The examples assume an existing app named `myapp`, already registered in your project, with DjangoTemplates and `APP_DIRS=True`. Keep your other installed apps and middleware. Add `insight_ui` and ensure staticfiles is enabled:

```python
INSTALLED_APPS = [
    # Keep your existing project apps here, including myapp.
    "django.contrib.staticfiles",
    "insight_ui",
]
STATIC_URL = "/static/"
INSIGHT_UI = {
    "navbar_fixed": False,
    "assets": {"cdn_enabled": False, "use_minified": False},
}
```

Default icons are shipped with the package. Override icon settings only with your own assets, and keep production manifest validation strict rather than disabling it to hide missing files.

The base template needs the resolved `INSIGHT_UI` context. The package ships a ready-to-use context processor for this; append it to the existing `TEMPLATES[0]["OPTIONS"]["context_processors"]`:

```python
TEMPLATES = [
    {
        # Keep your other TEMPLATES options.
        "OPTIONS": {
            "context_processors": [
                # Keep Django's request, i18n and, when used, authentication
                # context processors.
                "insight_ui.context_processors.insight_ui_context",
            ],
        },
    },
]
```

## Render A First Page

Create `myapp/templates/myapp/home.html`:

```django
{% extends "insight_ui/base.html" %}
{% load insight_tags i18n %}

{% block title %}My application{% endblock %}
{% block content %}
    {% translate "Get started" as action_label %}
    {% button label=action_label type="primary" %}
{% endblock %}
```

In your URL configuration, add a route using Django's `TemplateView`:

```python
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    # Keep your existing routes.
    path("", TemplateView.as_view(template_name="myapp/home.html"), name="home"),
]
```

Run `uv run python manage.py runserver` and visit `/`. The base template loads package CSS/JS; an individual `{% button %}` tag does not insert stylesheets. It also loads external HTMX scripts.

## Brand Defaults And Explicit Composition

Add brand settings to the same `INSIGHT_UI` mapping, using the current Config:

```python
from insight_ui.configs import BrandMarkConfig, LogoConfig

INSIGHT_UI["brand"] = {
    "home_url": "/",
    "mark": BrandMarkConfig(
        primary_text="Example",
        secondary_text="App",
        logo=LogoConfig(
            url="insight_ui/svg/insight-ui-logo.svg",
            url_dark="insight_ui/svg/insight-ui-logo.svg",
            alt="Example app",
            height="2rem",
        ),
    ),
    "footer_text": "An application built with Insight UI.",
}
```

For your brand, replace those example asset paths with your own files. Set the page title through the `title` block, as above. The helpers in [brand.py](../insight_ui/brand.py) turn settings into brand or footer-description Configs. They do not automatically build your navigation:

```python
from insight_ui.brand import get_navbar_brand_defaults
from insight_ui.configs import NavbarConfig

navbar_config = NavbarConfig(brand=get_navbar_brand_defaults(), links=[])
```

Pass that Config to `{% navbar config=navbar_config %}` in the `navbar` block and enable `navbar_fixed` if your layout uses a fixed navbar. Provide your own links and authentication routes. **Explicit component Configs win:** the navbar and footer tags render the supplied Config; they do not overwrite it from settings. Use the default helpers only where defaults are wanted.

## Settings Reference

All `INSIGHT_UI` keys are optional; your mapping is deep-merged over the package defaults in [config.py](../insight_ui/config.py):

| Key | Default | Purpose |
| --- | --- | --- |
| `navbar_fixed` | `True` | Stick the navbar to the top of the window. |
| `register_url` | `""` | URL or URL name for a register button; empty hides it. |
| `webmanifest`, `favicon`, `favicon_svg`, `apple_touch_icon` | packaged icons | PWA/Android manifest and browser icons; see [your app's icons](static-assets.md#host-app-icons). |
| `safari_mask_icon`, `safari_mask_icon_color`, `msapplication_TileColor`, `theme_color` | packaged values | Pinned-tab, tile and mobile browser-chrome colors. |
| `meta.seo.{description,keywords,author}` | placeholder text | `<meta>` tags rendered by the base template. |
| `load_prism`, `load_leaflet`, `load_echarts` | `False` | Opt-in third-party libraries (syntax highlighting, maps, charts). |
| `JS_DEBUG` | `False` | Enable the package's browser console logging. |
| `use_tailwind_cli` | `False` | Serve packaged CSS instead of a project-run Tailwind CLI build. |
| `assets.{use_minified,cdn_enabled,cdn_base_url,cdn_prefix,cdn_version}` | local, unminified | Static delivery mode; see [Static assets](static-assets.md). |

`brand` is covered above; other keys have no effect beyond what their name states.

## Next Steps

- [Components and configuration](components.md)
- [Staticfiles, fonts, favicons and CDN options](static-assets.md)
- [Translations and RTL](i18n.md)
- [Keyboard, focus and accessible markup](accessibility.md)

[All package guides](README.md)
