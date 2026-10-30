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
    {% button label=action_label color="primary" %}
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

Run `uv run python manage.py runserver` and visit `/`. The base template loads package CSS/JS; an individual `{% button %}` tag does not insert stylesheets. By default it also loads HTMX from jsdelivr; see [self-hosted HTMX](static-assets.md#self-hosted-htmx) for offline or strict-CSP hosts.

### Your Own Layout Classes

The packaged stylesheet is a **component stylesheet**, not a general Tailwind
build. It only contains the utilities that Insight UI's own templates, Configs
and scripts use. Common host layout classes such as `md:grid-cols-3` or
`space-y-4` may be missing, and Django will not warn you: the element simply
renders unstyled. Pick one of these for your own markup:

- Put host-only rules in your own stylesheet and load it from the
  `extra_head` block of your base template.
- Run your own Tailwind build over your templates and set `INSIGHT_UI["stylesheet"]`
  to its output. See [static assets](static-assets.md#host-layout-utilities).

The [design roles](design-system.md) (`bg-insight-surface`, `text-insight-muted`,
`rounded-insight-surface`, ...) are always available.

```django
{% extends "insight_ui/base.html" %}
{% load static %}
{% block extra_head %}<link rel="stylesheet" href="{% static 'myapp/host.css' %}">{% endblock %}
```

### Find A Component's Arguments

Each tag accepts the fields of its Config. Look them up in the
[component reference](https://django-insight-ui.com/docs/configs) or in the
installed package, as described in [Components](components.md#find-a-components-arguments).

## Navbar, Theme And Alerts

`{% navbar %}` without a Config renders the brand from `INSIGHT_UI["brand"]`
and no links. Pass `config=` with a `NavbarConfig` for links, the search bar or
`show_theme_toggle=True`. Use `{% theme_toggle %}` to place the light/dark
toggle anywhere else:

```django
{% extends "insight_ui/base.html" %}
{% load insight_tags %}
{% block navbar %}{% navbar %}{% endblock navbar %}
{% block content %}
    {% theme_toggle %}
    {% alert severity="error" message="Saving failed." dismissible=False %}
{% endblock %}
```

Without a saved choice, the base template starts in the visitor's system color
scheme (`prefers-color-scheme`). The toggle stores the choice in `localStorage`
(`insight-ui-theme`). Alerts use the semantic types `info`, `success`, `warning`
and `error`. `danger` is the button and badge color name and is rejected for
alerts. Alerts show a close button by default; pass `dismissible=False` for
messages that must stay visible.

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
| `navbar_fixed` | `False` | Stick the navbar to the top of the window; sidebars adjust their offset. |
| `stylesheet` | `"insight_ui/css/tailwind.css"` | Static path of the stylesheet; point it at your own Tailwind build. |
| `tooltip_show_delay` | `400` | Milliseconds before a tooltip appears on hover; keyboard focus shows it at once. |
| `register_url` | `""` | URL or URL name for a register button; empty hides it. |
| `content_max_width` | `""` | CSS width of the content box, e.g. `"64rem"`; empty keeps `80rem`. A page can pass `content_max_width` in its context. |
| `align_navbar_footer_to_content` | `False` | `True` puts the navbar and footer content into the content box instead of spanning the window. |
| `webmanifest`, `favicon`, `favicon_svg`, `apple_touch_icon` | packaged icons | PWA/Android manifest and browser icons; see [your app's icons](static-assets.md#host-app-icons). |
| `safari_mask_icon`, `safari_mask_icon_color`, `msapplication_TileColor`, `theme_color` | packaged values | Pinned-tab, tile and mobile browser-chrome colors. |
| `meta.seo.{description,keywords,author}` | placeholder text | `<meta>` tags rendered by the base template. |
| `load_prism`, `load_leaflet`, `load_echarts` | `False` | Opt-in third-party libraries (syntax highlighting, maps, charts). |
| `map_tiles.{url,attribution,max_zoom}` | OpenStreetMap | Tile service of `{% geo_map %}`. The OpenStreetMap tiles are for light use under their [tile usage policy](https://operations.osmfoundation.org/policies/tiles/); point `url` at your own or a commercial tile service otherwise and keep the attribution its terms require. |
| `JS_DEBUG` | `False` | Enable the package's browser console logging. |
| `use_tailwind_cli` | `False` | `True` serves the output of a project-run `django-tailwind-cli` build instead of the packaged CSS. |
| `assets.{use_minified,cdn_enabled,cdn_base_url,cdn_prefix,cdn_version}` | local, unminified | Static delivery mode; see [Static assets](static-assets.md). |
| `htmx.{src,integrity,ws_src,ws_integrity}` | jsdelivr URLs with SRI | HTMX and its WebSocket extension loaded by the base template, independent of `assets`; see [self-hosted HTMX](static-assets.md#self-hosted-htmx). |

`brand` is covered above; other keys have no effect beyond what their name states.

## Next Steps

- [Components and configuration](components.md)
- [Staticfiles, fonts, favicons and CDN options](static-assets.md)
- [Translations and RTL](i18n.md)
- [Keyboard, focus and accessible markup](accessibility.md)

[All package guides](README.md)
