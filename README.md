# Insight UI
<!-- Badges -->

![CI](https://github.com/alpininsight/insight-ui/actions/workflows/release.yml/badge.svg?branch=main)
![Conventional Commits](https://github.com/alpininsight/insight-ui/actions/workflows/feature-pr-title.yml/badge.svg?branch=develop)
![Staging (develop)](https://github.com/alpininsight/insight-ui/actions/workflows/release-develop.yml/badge.svg?branch=develop)
![Release](https://github.com/alpininsight/insight-ui/actions/workflows/release.yml/badge.svg?branch=main)
![Publish](https://github.com/alpininsight/insight-ui/actions/workflows/main-publish-pypi.yml/badge.svg?branch=main)

[![Ruff](https://img.shields.io/badge/ruff-checked-5D3FD3?logo=python&logoColor=white)](https://github.com/astral-sh/ruff)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue?logo=python&logoColor=white)](pyproject.toml)
[![Django](https://img.shields.io/badge/django-5.2-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PyPI - Version](https://img.shields.io/pypi/v/insight-ui.svg)](https://pypi.org/project/insight-ui/)
[![License: AGPL-3.0](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)](LICENSE)

Insight UI is a modern, extensible UI framework for Django. It ships with reusable, WCAG 2.1 AA-compliant components, live HTMX integrations, and a Tailwind-based design system so teams can bootstrap projects quickly. The published version is derived from Git tags via hatch-vcs and kept in sync by release-please.

## Highlights
- **Accessible components**: ready-made navigation, forms, tables, alerts, carousels, and more.
- **Internationalization**: RTL layouts, language switchers, and localization helpers.
- **Performance minded**: HTMX-powered partial updates reduce full page reloads.
- **Theming**: customizable Tailwind tokens and component layers for fast brand alignment.

## Installation
```bash
uv add insight-ui

# or install from Git
uv add "git+https://github.com/alpininsight/insight-ui@main"
```

Add the app to your Django project:
```python
INSTALLED_APPS = [
    # ...
    "insight_ui",
    # ...
]
```

Run the application and visit the Installation page in your browser for configuration details and Tailwind workflows.

## Local Development
```bash
uv sync --all-groups
cp .env.example .env
uv run python manage.py setup_dev
uv run python manage.py runserver 0:10800
```

The WebSocket demo lives in `utils/main.py`:
```bash
uv run ./utils/main.py
```

## Testing
```bash
uv run pytest
```

CI runs tests against Python 3.12, 3.13, and 3.14. Note that Python 3.14 is still in development, so some third-party packages may not fully support it yet. The CI matrix uses `fail-fast: false` to ensure all versions report results independently.

## Documentation

The application is self-documenting — run it locally and open it in your browser to read details about each component on its corresponding page, including live examples.

Additional developer references in `docs/`:
- [Contributing Guide](docs/contributing.md)
- [Naming Conventions](docs/naming_conventions.md)
- [Accessibility](docs/accessibility.md)
- [Internationalization](docs/i18n.md)

## Contributing
We welcome improvements! Please read the [Contributor Guide](docs/contributing.md) alongside the [Naming Conventions](docs/naming_conventions.md) before opening a pull request.

Code ownership and review for this repository are managed via `.github/CODEOWNERS`. By default, changes are owned by the `@alpininsight` organization, with CI/CD workflows under `.github/workflows/` explicitly covered.

## License
Insight UI is released under the GNU Affero General Public License v3.0.
