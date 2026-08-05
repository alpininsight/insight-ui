<div align="center">

<br>

<img src=".github/assets/hero-title.svg" alt="Insight UI" width="400">

<br>

**Modern Django Component Framework**

65+ accessible, WCAG 2.1 AA-compliant UI components<br>
HTMX-powered · Tailwind-based · Self-documenting

<br>

[Live Demo](https://insight-ui.com) · [Get Started](docs/getting-started.md) · [Components](docs/components.md)

<br>

[![PyPI](https://img.shields.io/pypi/v/insight-ui.svg)](https://pypi.org/project/insight-ui/)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue?logo=python&logoColor=white)](pyproject.toml)
[![Django](https://img.shields.io/badge/django-5.2%20to%206.x-092E20?logo=django&logoColor=white)](pyproject.toml)
[![License: AGPL-3.0](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)](LICENSE)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-5D3FD3?logo=ruff&logoColor=white)](https://github.com/astral-sh/ruff)

<br>

<img src=".github/assets/hero-divider.svg" alt="" width="600">

</div>

<br>

## Features

- **Accessible by default** — Navigation, forms, tables, modals, and more, all WCAG 2.1 AA-compliant
- **HTMX integration** — Partial updates without full page reloads
- **Tailwind design system** — Customizable tokens for fast brand alignment
- **RTL & i18n ready** — Right-to-left layouts and localization helpers included
- **Self-documenting** — Run locally to browse interactive component docs

## Quick Start

Install the package:

```bash
uv add insight-ui
```

Add to your Django settings:

```python
INSTALLED_APPS = [
    # ...
    "insight_ui",
]
```

Use components in your templates:

```django
{% load insight_tags %}

{% button label="Get Started" type="primary" size="m" %}

{% card title="Welcome" subtitle="Your first card" %}
    <p>Card content goes here.</p>
{% endcard %}

{% alert type="success" title="Done!" message="Component rendered successfully." %}
```

Visit the [Getting Started Guide](docs/getting-started.md) for Tailwind configuration and advanced setup.

## Installation Options

```bash
# From PyPI (recommended)
uv add insight-ui

# From Git (latest development)
uv add "git+https://github.com/alpininsight/insight-ui@develop"
```

## Local Development

```bash
git clone https://github.com/alpininsight/insight-ui.git
cd insight-ui
uv sync --all-groups
cp .env.example .env
uv run python manage.py setup_dev
uv run python manage.py tailwind runserver  # Starts dev server with Tailwind compiler
```

Open [http://localhost:8000](http://localhost:8000) to browse the component documentation.

## Testing

```bash
# Python tests
uv run pytest

# JavaScript tests
npm install && npx vitest run

# JavaScript tests alternative (no local Node.js required, but Docker)
docker run --rm -v ${PWD}:/app -w /app node:25-alpine sh -c "npm install && npx vitest run"
```

## Documentation

The application is self-documenting — run it locally to explore components with live examples.

Developer references in `docs/`:

| Guide | Description |
|-------|-------------|
| [Getting Started](docs/getting-started.md) | Installation and configuration |
| [Using Components](docs/components.md) | Template tag API and patterns |
| [Design System](docs/design-system.md) | Tokens, theming, and extension |
| [Accessibility](docs/accessibility.md) | WCAG compliance guidelines |
| [Internationalization](docs/i18n.md) | i18n and RTL support |
| [Testing](docs/testing.md) | Test structure and commands |
| [Contributing](docs/contributing.md) | Workflow and guidelines |

## Contributing

We welcome contributions! Please read the [Contributing Guide](docs/contributing.md) and [Conventions](docs/conventions.md) before opening a pull request.

## Support

- [GitHub Issues](https://github.com/alpininsight/insight-ui/issues) — Bug reports and feature requests
- [GitHub Discussions](https://github.com/alpininsight/insight-ui/discussions) — Questions and ideas

## License

Insight UI is released under the [GNU Affero General Public License v3.0](LICENSE).

For commercial licensing options, see [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md).
