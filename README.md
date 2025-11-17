# Insight UI
<!-- Badges -->

![CI](https://github.com/alpininsight/insight-ui/actions/workflows/release.yml/badge.svg?branch=main)
![Conventional Commits](https://github.com/alpininsight/insight-ui/actions/workflows/feature-pr-title.yml/badge.svg?branch=develop)
![Staging (develop)](https://github.com/alpininsight/insight-ui/actions/workflows/release-develop.yml/badge.svg?branch=develop)
![Release](https://github.com/alpininsight/insight-ui/actions/workflows/release.yml/badge.svg?branch=main)
![Publish](https://github.com/alpininsight/insight-ui/actions/workflows/main-publish-pypi.yml/badge.svg?branch=main)

[![Ruff](https://img.shields.io/badge/ruff-checked-5D3FD3?logo=python&logoColor=white)](https://github.com/astral-sh/ruff)
[![Python](https://img.shields.io/badge/python-3.13%2B-blue?logo=python&logoColor=white)](pyproject.toml)
[![Django](https://img.shields.io/badge/django-5.2-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PyPI - Version](https://img.shields.io/pypi/v/insight-ui.svg)](https://pypi.org/project/insight-ui/)
[![License: AGPL-3.0](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)](LICENSE)

Insight UI is a modern, extensible UI framework for Django. It ships with reusable, WCAG 2.1 AA-compliant components, live HTMX integrations, and a Tailwind-based design system so teams can bootstrap projects quickly. The published version is derived from Git tags via hatch-vcs and kept in sync by release-please.

## Highlights
- **Accessible components**: ready-made navigation, forms, tables, alerts, carousels, and more.
- **Internationalisation**: RTL layouts, language switchers, and localisation helpers.
- **Performance minded**: HTMX-powered partial updates reduce full page reloads.
- **Theming**: customisable Tailwind tokens and component layers for fast brand alignment.

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

See the [Installation guide](docs/en/installation.md) for configuration details and Tailwind workflows.

## Local Development
```bash
uv sync --all-groups
uv run python manage.py migrate
uv run python manage.py runserver
```

The WebSocket demo lives in `utils/main.py`:
```bash
uv run ./utils/main.py
```

## Documentation
- English: `docs/en/` (served via MkDocs)
- Deutsch: `docs/de/`

Run the site locally:
```bash
uv run mkdocs serve
```

## Contributing
We welcome improvements! Please read the [Contributor Guide](docs/en/contributing.md) alongside the [naming conventions](docs/en/guides/naming_conventions.md) before opening a pull request. Remember to mirror changes in both language trees.

## License
Insight UI is released under the GNU Affero General Public License v3.0.
