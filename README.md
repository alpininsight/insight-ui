# Insight UI

A reusable Django + HTMX component library with semantic design tokens,
keyboard-accessible components, localization, and light/dark themes.

[Documentation and examples](https://insight-ui.com/) ·
[Component reference](https://insight-ui.com/docs/configs) ·
[Issues](https://github.com/alpininsight/insight-ui/issues)

## Package Scope

This repository contains the `insight_ui` Python package, its generic component
tests, and the source assets used to build its CDN distribution. It does not
contain or deploy a documentation website.

The documentation application, component catalog, examples, documentation tests,
and Enterprise deliverables are maintained separately in `insight-ui-docs`.
API docstrings and configuration metadata remain in the library because they
describe its public API. Accessibility is tested, but this is not a blanket
WCAG certification of the library or an application built with it.

## Installation

Python 3.12+ and Django 5.2 or 6.x are supported. Initial public PyPI publication
is being prepared; availability is subject to the repository owner's release
decision. Once a release is available:

```bash
uv add insight-ui
```

Add `insight_ui` to your existing Django project's `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # Your Django applications...
    "insight_ui",
]
```

Use the template tags in your own templates:

```django
{% load insight_tags %}
{% button label="Get started" type="primary" %}
```

See the [installation guide](https://insight-ui.com/docs/installation) for host
settings, base templates, staticfiles, and optional CDN configuration. Installing
the package does not install a documentation app, server, or Enterprise service.

## Contributing And Tests

Work on a feature branch based on `develop`, then open a pull request. Keep
reusable changes here; coordinate reference examples and application tests in
the documentation repository instead of copying its application back here.

```bash
uv sync --all-groups
uv run pytest
npm ci
npm test
npm run build:static-all
npm run verify:static-build
uv build
uv run python scripts/check_distribution.py
```

Package tests use `tests.settings`, a minimal Django host, not the documentation
server. `input.css` remains the design-token source; the static build compiles
package-only sources and creates minified CSS/JS for CDN delivery. Generated
minified files are ignored. The wheel and sdist contain the readable assets.

## License

[GNU Affero General Public License v3.0](LICENSE).
For alternative licensing inquiries see [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md).
