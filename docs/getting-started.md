<!--
SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
SPDX-License-Identifier: AGPL-3.0-only
-->

# Getting Started

This guide integrates the reusable package into **your existing Django project**.
For a source checkout and a one-component preview, use
[the contributor workflow](../CONTRIBUTING.md) instead. Neither path needs the
separate documentation application.

## Install The Package

Use the supported Python/Django versions in [README.md](../README.md).
Stable releases are available on [PyPI](https://pypi.org/project/insight-ui/).
Install the package in the host project's environment:

```bash
uv add insight-ui
```

For local development against an unpublished change, use your reviewed source checkout:

```bash
uv add --editable /absolute/path/to/insight-ui
```

That path is local development configuration, not a production dependency pin.
For editable source, first build package assets as described in
[Static assets](static-assets.md). A released wheel provides readable assets.

## Configure The Host

The examples assume an existing app named `myapp`, already registered in the
host, with DjangoTemplates and `APP_DIRS=True`. Keep your other installed apps
and middleware. Add `insight_ui` and ensure staticfiles is enabled:

```python
INSTALLED_APPS = [
    # Keep your existing project apps here, including myapp.
    "django.contrib.staticfiles",
    "insight_ui",
]
STATIC_URL = "/static/"
INSIGHT_UI = {
    "navbar_fixed": False,  # This first page has no navbar.
    "assets": {"cdn_enabled": False, "use_minified": False},
}
```

Do not add a `documentation` app or documentation URL routes. A package install
does not supply them. Default icons are shipped with the package. Keep
production manifest validation strict rather than disabling it to hide missing
files. Override icon settings only with assets supplied by your host.

The base template needs the resolved `INSIGHT_UI` context. In
`myapp/context_processors.py`, wrap the package config helper:

```python
from insight_ui.config import get_config


def insight_ui_settings(request):
    return get_config()
```

Append `"myapp.context_processors.insight_ui_settings"` to the existing
`TEMPLATES[0]["OPTIONS"]["context_processors"]`. Keep Django's `request`,
`i18n` and, when used, authentication context processors. Do not register
`get_config` itself as a context processor: its argument is a config key,
not an HTTP request.

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

In your host URL configuration, add a route using Django's `TemplateView`:

```python
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    # Keep your existing routes.
    path("", TemplateView.as_view(template_name="myapp/home.html"), name="home"),
]
```

Run the host's `uv run python manage.py runserver` and visit `/`. The base
template loads package CSS/JS; an individual `{% button %}` tag does not insert
stylesheets. This host base template also loads external HTMX scripts. The
source-only `devtools` preview is the separate local-assets-only option.

## Brand Defaults And Explicit Composition

Add brand settings to the same `INSIGHT_UI` mapping, using the current Config
classes rather than obsolete top-level `brand.logo` / `brand.title` keys:

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

For your brand, replace those example asset paths with files supplied by the
host. Set the page title through the `title` block, as above.
The helpers in [brand.py](../insight_ui/brand.py) turn settings into brand or
footer-description Configs. They do not automatically build your navigation:

```python
from insight_ui.brand import get_navbar_brand_defaults
from insight_ui.configs import NavbarConfig

navbar_config = NavbarConfig(brand=get_navbar_brand_defaults(), links=[])
```

Pass that Config to `{% navbar config=navbar_config %}` in the `navbar` block
and enable `navbar_fixed` if your layout uses a fixed navbar. Provide your own
links and authentication routes. **Explicit component Configs win:** the navbar
and footer tags render the supplied Config; they do not overwrite it from
settings. Use the default helpers only where defaults are wanted.

## Next Steps

- [Components and configuration](components.md)
- [Staticfiles, fonts, favicons and CDN options](static-assets.md)
- [Translations and RTL](i18n.md)
- [Keyboard, focus and accessible markup](accessibility.md)

[All package guides](README.md)
