<div align="center">

<br>

<img src="https://raw.githubusercontent.com/alpininsight/insight-ui/develop/.github/assets/hero-title.svg" alt="Insight UI" width="400">

<br>

**The Modern Django Component Framework with built-in Accessibility**

65+ accessible, WCAG 2.2 AA-compliant UI components<br>
HTMX-powered · Tailwind-based · RTL & i18n ready

<br>

[Live Demo](https://insight-ui.com) · [Get Started](docs/getting-started.md) · [Components](https://insight-ui.com/docs/configs)

<br>

[![PyPI](https://img.shields.io/pypi/v/insight-ui.svg)](https://pypi.org/project/insight-ui/)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue?logo=python&logoColor=white)](pyproject.toml)
[![Django](https://img.shields.io/badge/django-5.2%20to%206.x-092E20?logo=django&logoColor=white)](pyproject.toml)
[![License: AGPL-3.0](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)](LICENSE)

</div>

<br>

Insight UI is a reusable Django component library that provides production-ready
UI building blocks. Components are implemented as Django template tags with typed
configuration dataclasses, styled with Tailwind CSS, and enhanced with HTMX for
interactivity — no JavaScript framework required.

## Features

- **Accessible by default** — Navigation, forms, tables, modals, and more, all WCAG 2.2 AA-compliant
- **HTMX integration** — Partial updates without full page reloads
- **Tailwind design system** — Customizable semantic tokens for fast brand alignment
- **RTL & i18n ready** — Right-to-left layouts and localization included
- **Light & dark themes** — Automatic theme switching with CSS custom properties

## Quick Start

Install the package:

```bash
uv add insight-ui
```

Add to your Django settings:

```python
INSTALLED_APPS = [
    # Your apps...
    "django.contrib.staticfiles",
    "insight_ui",
]

TEMPLATES = [
    {
        # ...
        "OPTIONS": {
            "context_processors": [
                # ...
                "insight_ui.context_processors.insight_ui_context",
            ],
        },
    },
]
```

Use components in your templates:

```django
{% extends "insight_ui/base.html" %}
{% load insight_tags %}

{% block title %}My application{% endblock %}

{% block content %}
    {% button label="Get started" type="primary" %}
    {% card title="Welcome" subtitle="Your first card" content="Card content goes here." %}
    {% alert type="success" message="Component rendered successfully." %}
{% endblock %}
```

See [Getting Started](docs/getting-started.md) for complete setup including static assets.

## Documentation

| Guide | Description |
|-------|-------------|
| [Getting Started](docs/getting-started.md) | Installation and configuration |
| [Components](docs/components.md) | Template tag API and patterns |
| [Design System](docs/design-system.md) | Tokens, theming, and customization |
| [Static Assets](docs/static-assets.md) | Staticfiles and CDN configuration |
| [Accessibility](docs/accessibility.md) | WCAG compliance guidelines |
| [Internationalization](docs/i18n.md) | i18n and RTL support |

Full component reference and live examples at [insight-ui.com](https://insight-ui.com).

## Contributing

```bash
git clone https://github.com/alpininsight/insight-ui.git
cd insight-ui
uv sync --all-groups
npm install
npm run build:static-all
uv run pytest
```

The `devtools` app provides a local playground for component development:

```bash
uv run python manage.py runserver
```

Edit `devtools/views.py` to add component configs, then open http://127.0.0.1:8000/.

To scaffold a new component:

```bash
uv run python manage.py create_component --name "My Widget" --category input
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow.

## Package Scope

This repository contains the `insight_ui` Python package. The documentation website,
component catalog, and examples are maintained in a separate repository.

## License

[GNU Affero General Public License v3.0](LICENSE).
For commercial licensing see [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md).

Licensing metadata follows [REUSE](https://reuse.software). Third-party notices
are in [NOTICE](NOTICE) and [insight_ui/THIRD_PARTY_NOTICES.md](insight_ui/THIRD_PARTY_NOTICES.md).
