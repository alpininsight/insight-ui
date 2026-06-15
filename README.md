# Insight UI

[![Ruff](https://img.shields.io/badge/ruff-checked-5D3FD3?logo=python&logoColor=white)](https://github.com/astral-sh/ruff)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue?logo=python&logoColor=white)](pyproject.toml)
[![Django](https://img.shields.io/badge/django-5.2%20to%206.x-092E20?logo=django&logoColor=white)](pyproject.toml)
[![PyPI - Version](https://img.shields.io/pypi/v/insight-ui.svg)](https://pypi.org/project/insight-ui/)
[![License: AGPL-3.0](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)](LICENSE)

Insight UI is a modern, extensible UI framework for Django. It ships with reusable, WCAG 2.1 AA-compliant components, live HTMX integrations, and a Tailwind-based design system so teams can bootstrap projects quickly. Tailwind CSS is the default styling implementation; the public design contract is semantic. The published version is derived from Git tags via hatch-vcs and kept in sync by release-please.

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

## Container Runtime
The repository now ships a Django container workflow at `.github/workflows/container-build.yml`. It builds a production-oriented image, bakes static assets into the image during `docker build`, smoke-tests `migrate` and optional runtime `collectstatic`, and publishes branch images to GHCR on pushes to `develop` and `main`.

Build and run locally:
```bash
docker build -t insight-ui:local .
docker run --rm -p 8000:8000 insight-ui:local
```

Runtime flags:
- `RUN_MIGRATIONS=1` runs `python manage.py migrate --noinput` before the web process starts. This is enabled by default for single-container Docker runs.
- `RUN_COLLECTSTATIC=1` re-runs `python manage.py collectstatic --noinput` at container start when you need to refresh a mounted static volume. Static assets are already collected during the image build, so the default remains `0`.
- `ARTIFACT_VERSION` and `GIT_COMMIT_SHA` are injected at build time and surfaced at runtime via `/api/info`.
- `DEPLOYMENT_ENVIRONMENT`, `DEPLOYMENT_LANE`, `DEPLOYMENT_SLOT`, `PLATFORM_NAMESPACE`, and `PUBLIC_BASE_URL` let the same image describe its current blue/green role without code changes.

For Kubernetes, use the same image and disable startup migrations on scaled web deployments (`RUN_MIGRATIONS=0`). Run `python manage.py migrate --noinput` as a one-off Job or init step instead, then start the web pods from the published image.

Runtime endpoints:
- `/healthz` for cheap liveness probes
- `/readyz` for cheap readiness checks against local prerequisites
- `/api/info` for canonical runtime identity and build metadata

For blue/green promotion, the repo publishes one slot-neutral image. The
platform moves the tested digest between `develop` and `main` aliases by
changing the slot wiring, not by rebuilding a second `main` image.

The deployment-specific prep for `insight-ui.demo.alpininsight.ai` is documented in [Deployment Contract](docs/deployment.md).

The WebSocket demo lives in `utils/main.py`:
```bash
uv run ./utils/main.py
```

## Static Assets and CDN
Insight UI ships readable JavaScript and CSS sources together with generated
`.min.js` and `.min.css` distribution files. The generated files are committed
next to their sources and verified in CI.

CDN delivery uses the shared `.github-private` static-assets workflow. Release
assets should be consumed from immutable version paths such as
`https://cdn.alpininsight.ai/insight-ui/vX.Y.Z/`. Branch aliases
`develop/` and `main/` are reserved for preview and demo comparisons, while
`latest/` is only a convenience smoke-test alias.

The full CDN contract, required secrets, runtime settings, and cache rules are
documented in [CDN Static Assets](docs/cdn-static-assets.md).

## Testing
```bash
# Python code
uv run pytest

# JavaScript code (no local node.js required due docker container)
docker run --rm -it -v ${PWD}:/app -w /app  node:25-alpine sh -c "npm install && npx vitest run"
```

CI runs tests against Python 3.12, 3.13, and 3.14. Note that Python 3.14 is still in development, so some third-party packages may not fully support it yet. The CI matrix uses `fail-fast: false` to ensure all versions report results independently.

## Documentation

The application is self-documenting. Run it locally and open it in your browser to read component documentation, examples, parameters, and accessibility notes on the corresponding pages.

The `docs/` directory is reserved for repository-level developer and governance references:
- [Contributing Guide](docs/contributing.md)
- [New Component Self-Documentation Checklist](docs/new-component-self-documentation-checklist.md)
- [Documentation Architecture](docs/docs-architecture.md)
- [Naming Conventions](docs/naming_conventions.md)
- [Design System Contract](docs/design-system-contract.md)
- [CDN Static Assets](docs/cdn-static-assets.md)
- [Accessibility](docs/accessibility.md)
- [Internationalization](docs/i18n.md)

## Contributing
We welcome improvements! Please read the [Contributor Guide](docs/contributing.md) alongside the [Naming Conventions](docs/naming_conventions.md) before opening a pull request.

Code ownership and review for this repository are managed via `.github/CODEOWNERS`. By default, changes are owned by the `@alpininsight` organization, with CI/CD workflows under `.github/workflows/` explicitly covered.

## License
Insight UI is released under the GNU Affero General Public License v3.0.
