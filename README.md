<div align="center">

<br>

<img src="https://raw.githubusercontent.com/alpininsight/insight-ui/main/.github/assets/hero-title.svg" alt="Django-Insight-UI" width="600">

<br>

**The Modern Django Component Framework with built-in Accessibility**

65+ UI components designed with WCAG 2.2 AA as an accessibility target<br>
HTMX-powered · Tailwind-based · RTL & i18n ready

<br>

[Live Demo](https://django-insight-ui.com/) · [Get Started](https://django-insight-ui.com/docs/installation) · [Components](https://django-insight-ui.com/docs/configs)

<br>

[![PyPI](https://img.shields.io/pypi/v/insight-ui.svg)](https://pypi.org/project/insight-ui/)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue?logo=python&logoColor=white)](https://github.com/alpininsight/insight-ui/blob/main/pyproject.toml)
[![Django](https://img.shields.io/badge/django-5.2%20to%206.x-092E20?logo=django&logoColor=white)](https://github.com/alpininsight/insight-ui/blob/main/pyproject.toml)
[![License: AGPL-3.0](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)](https://github.com/alpininsight/insight-ui/blob/main/LICENSE)

</div>

<br>

Insight UI is a reusable Django component library that provides production-ready
UI building blocks. Components are implemented as Django template tags with typed
configuration dataclasses, styled with Tailwind CSS, and enhanced with HTMX for
interactivity — no JavaScript framework required.

## Features

- **Accessibility-focused** — Keyboard, focus and ARIA behavior in navigation, forms, tables and modals
- **HTMX integration** — Partial updates without full page reloads
- **Tailwind design system** — Customizable semantic tokens for fast brand alignment
- **RTL & i18n ready** — Right-to-left layouts and localization included
- **Light & dark themes** — Automatic theme switching with CSS custom properties

WCAG 2.2 AA is a design target, not a verified package-wide conformance claim.
Conformance must be assessed for complete pages and processes in the consuming
application. See [Accessibility](https://github.com/alpininsight/insight-ui/blob/main/docs/accessibility.md) for scope and limitations.

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

See [Getting Started](https://github.com/alpininsight/insight-ui/blob/main/docs/getting-started.md) for complete setup including static assets.

## Documentation

The following guides describe the public package and contributor workflow on GitHub.

| Guide | Description |
|-------|-------------|
| [Getting Started](https://github.com/alpininsight/insight-ui/blob/main/docs/getting-started.md) | Installation and configuration |
| [Components](https://github.com/alpininsight/insight-ui/blob/main/docs/components.md) | Template tag API and patterns |
| [Design System](https://github.com/alpininsight/insight-ui/blob/main/docs/design-system.md) | Tokens, theming, and customization |
| [Static Assets](https://github.com/alpininsight/insight-ui/blob/main/docs/static-assets.md) | Staticfiles and CDN configuration |
| [Accessibility](https://github.com/alpininsight/insight-ui/blob/main/docs/accessibility.md) | WCAG scope, testing, and limitations |
| [Internationalization](https://github.com/alpininsight/insight-ui/blob/main/docs/i18n.md) | i18n and RTL support |

Full component reference and live examples at [django-insight-ui.com](https://django-insight-ui.com/).

## Contributing

```bash
git clone https://github.com/alpininsight/insight-ui.git
cd insight-ui
uv sync --all-groups
npm ci
npm run build:static-all
uv run pytest
```

The `devtools` app provides a local playground for component development:

```bash
uv run python manage.py runserver 127.0.0.1:8000
```

Edit `devtools/views.py` for Configs and `devtools/templates/devtools/playground.html`
for their template tags, then open http://127.0.0.1:8000/.

To scaffold a new component:

```bash
uv run python manage.py create_component --name "My Widget" --category input --no-js --dry-run
```

See [CONTRIBUTING.md](https://github.com/alpininsight/insight-ui/blob/main/CONTRIBUTING.md) for the full workflow.

## Package Scope

This repository contains the `insight_ui` Python package. The documentation website,
component catalog, and examples are maintained in a separate repository.
The local `devtools` playground and contributor guides stay in the Git checkout,
not the wheel or sdist. Contributors need no private repository or credentials.

## License

[GNU Affero General Public License v3.0](https://github.com/alpininsight/insight-ui/blob/main/LICENSE).
For commercial licensing see [COMMERCIAL_LICENSE.md](https://github.com/alpininsight/insight-ui/blob/main/COMMERCIAL_LICENSE.md).

Licensing metadata follows [REUSE](https://reuse.software). Third-party notices
are in [NOTICE](https://github.com/alpininsight/insight-ui/blob/main/NOTICE) and [insight_ui/THIRD_PARTY_NOTICES.md](https://github.com/alpininsight/insight-ui/blob/main/insight_ui/THIRD_PARTY_NOTICES.md).
