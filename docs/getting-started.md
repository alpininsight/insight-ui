# Getting Started

This guide helps you integrate Insight UI into your Django project.

## Installation

```bash
uv add insight-ui
```

Or with pip:

```bash
pip install insight-ui
```

## Django Configuration

### 1. Add to Installed Apps

```python
INSTALLED_APPS = [
    # ...
    "insight_ui",
]
```

### 2. Include URLs (for self-documentation)

```python
from django.urls import include, path

urlpatterns = [
    # ...
    path("docs/", include("insight_ui.urls")),
]
```

### 3. Configure Static Files

Ensure Django can serve static files:

```python
STATIC_URL = "/static/"
```

Run collectstatic for production:

```bash
uv run python manage.py collectstatic
```

## First Component

Use Insight UI components in your templates:

```django
{% load insight_tags %}

<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="{% static 'insight_ui/css/tailwind.css' %}">
</head>
<body>
    {% button label="Click me" type="primary" %}

    {% alert message="Welcome!" type="info" dismissible=True %}
</body>
</html>
```

Or extend the base template:

```django
{% extends "insight_ui/base.html" %}

{% load insight_tags %}

{% block content %}
    {% button label="Click me" type="primary" %}
{% endblock %}
```

## Configuration Reference

Insight UI is configured via `settings.INSIGHT_UI`. All settings are optional and have sensible defaults.

```python
from insight_ui.configs import BrandMarkConfig, LogoConfig

INSIGHT_UI = {
    # Your configuration here
}
```

### Brand Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `brand.home_url` | str | `"/"` | URL for the brand logo link |
| `brand.mark` | BrandMarkConfig | Insight UI defaults | Brand mark with logo and text |
| `brand.footer_text` | str | Library description | Footer description text |

Example:

```python
INSIGHT_UI = {
    "brand": {
        "home_url": "/",
        "mark": BrandMarkConfig(
            primary_text="My",
            secondary_text="App",
            logo=LogoConfig(
                url="myapp/logo.svg",
                url_dark="myapp/logo-dark.svg",
                alt="My App Logo",
                height="2rem",
            ),
        ),
        "footer_text": "My awesome application.",
    }
}
```

### Favicon and Meta

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `webmanifest` | str | `"insight_ui/favicon/site.webmanifest"` | Web app manifest path for Android/PWA metadata and install icons |
| `favicon` | str | `"insight_ui/favicon/favicon.ico"` | Main favicon path |
| `favicon_32` | str | `"insight_ui/favicon/favicon-32x32.png"` | 32x32 favicon |
| `favicon_16` | str | `"insight_ui/favicon/favicon-16x16.png"` | 16x16 favicon |
| `apple_touch_icon` | str | `"insight_ui/favicon/apple-touch-icon.png"` | Apple touch icon |
| `safari_mask_icon` | str | `"insight_ui/svg/logo.svg"` | Safari pinned tab icon |
| `safari_mask_icon_color` | str | `"#5bbad5"` | Safari pinned tab icon color |
| `msapplication_TileColor` | str | `"#da532c"` | MS Edge live tile background |
| `theme_color` | str | `"#ffffff"` | Mobile browser search bar color |

`apple_touch_icon` is the home-screen icon used by iOS and iPadOS. Android and
installable PWAs discover their icons through the configured `webmanifest`.
Insight UI's default manifest includes separate `purpose: "maskable"` icons so
launchers can crop them safely. A branded consumer should provide its own
manifest and icon files, then point `webmanifest` and `apple_touch_icon` at
those static assets.

### SEO Meta Tags

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `meta.seo.description` | str | `"My indispensable app"` | Meta description |
| `meta.seo.keywords` | str | `"Django, Insight UI"` | Meta keywords |
| `meta.seo.author` | str | `"It's me"` | Meta author |

### Layout

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `navbar_fixed` | bool | `True` | Sticky navbar at top of window |
| `stylesheet` | str | `"insight_ui/css/tailwind.css"` | Main stylesheet path |

### Optional Libraries

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `load_prism` | bool | `False` | Enable Prism.js syntax highlighting |
| `load_leaflet` | bool | `False` | Enable Leaflet.js geo-maps |
| `load_echarts` | bool | `False` | Enable ECharts for charts |

### Development

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `JS_DEBUG` | bool | `False` | Enable browser console logging |
| `use_tailwind_cli` | bool | `False` | Enable Tailwind CLI for style customization |

### Assets and CDN

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `assets.use_minified` | bool | `False` | Use minified assets |
| `assets.cdn_enabled` | bool | `False` | Serve assets from CDN |
| `assets.cdn_base_url` | str | host-project setting | CDN base URL |
| `assets.cdn_prefix` | str | `"insight-ui"` | CDN path prefix |
| `assets.cdn_version` | str | `"latest"` | CDN version |

For CDN examples and the static asset build contract, see
[Static Assets](static-assets.md). Use your own CDN base URL in host
applications; this public package documentation intentionally does not describe
any organization's private CDN upload or deployment process.

## Next Steps

- [Using Components](components.md) - Learn how to use components effectively
- [Design System](design-system.md) - Understand tokens and styling
- [Static Assets](static-assets.md) - Configure local staticfiles or host-owned CDN delivery
- [Contributing](contributing.md) - Add new components
- [Testing](testing.md) - Write tests for your changes
