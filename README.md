# Django-Insight-UI

Django-Insight-UI (short `insight-ui`) is a reusable Django and HTMX component
library with semantic design tokens, keyboard-accessible components,
localization, and light and dark themes.

[Documentation and examples](https://insight-ui.com/) ·
[Component reference](https://insight-ui.com/docs/configs) ·
[Issues](https://github.com/alpininsight/insight-ui/issues)

## Package Scope

This repository contains the `insight_ui` Python package, its generic component
tests, public contributor guides, and the source assets used to build its CDN distribution. It does not
contain or deploy a documentation website.

The documentation application, component catalog, examples, documentation tests,
and Enterprise deliverables are maintained separately in `insight-ui-docs`.
API docstrings and configuration metadata remain in the library because they
describe its public API. Keyboard, focus and ARIA behavior tests also remain
here. WCAG 2.2 AA is a design target, not a verified package-wide conformance
claim. Consumers must evaluate their complete rendered pages and processes;
package tests do not certify an application. See the
[accessibility guide](docs/accessibility.md) for contributor checks and limits.

That evaluation is work, and teams facing a tender questionnaire or an audit
rarely want to start from scratch. We keep the groundwork prepared as a product:
an accessibility test catalogue, per-component evidence from the automated runs,
and the regulatory documentation such reviews ask for. It is offered with the
Enterprise licence and services described on [insight-ui.com](https://insight-ui.com/).
None of it is needed to use this package.

## Installation

Python 3.12+ and Django 5.2, 6.0 and 6.1 are supported. Stable releases are
available on [PyPI](https://pypi.org/project/insight-ui/):

```bash
uv add insight-ui
```

This is a production-supported MVP with a defined feature scope, not a promise
that every planned feature is complete. Keep the application's dependency lock
under version control and test upgrades before deploying them.

Add `insight_ui` to your existing Django project's `INSTALLED_APPS` and ensure
Django staticfiles is enabled. Keep your other applications and settings:

```python
INSTALLED_APPS = [
    # Your Django applications...
    "django.contrib.staticfiles",
    "insight_ui",
]
STATIC_URL = "/static/"
```

Complete the [host setup](docs/getting-started.md#configure-the-host), including
the base-template context processor and static assets. Then use the real
component tags in your own template:

```django
{% extends "insight_ui/base.html" %}
{% load insight_tags %}

{% block title %}My application{% endblock %}
{% block content %}
    {% button label="Get started" type="primary" %}
    {% card title="Welcome" subtitle="Your first card" content="Card content goes here." %}
    {% alert type="success" message="Component rendered successfully." dismissible=False %}
{% endblock %}
```

The base template loads CSS/JS; individual component tags do not. `card` takes
`content` or a `CardConfig`, not an `endcard` closing tag. `alert` uses `message`,
not a `title` argument. Labels supplied by the host should be translated there;
see [internationalization](docs/i18n.md).

See [Getting started](docs/getting-started.md) for a complete first page and
[Static assets](docs/static-assets.md) for optional CDN configuration. Installing
the package does not install a documentation app, server, or Enterprise service.

## Contributing And Tests

Public package guides are kept here: [getting started](docs/getting-started.md),
[components](docs/components.md), [design tokens](docs/design-system.md),
[static assets](docs/static-assets.md), [translations](docs/i18n.md), and
[accessibility](docs/accessibility.md). See the [guide index](docs/README.md)
for conventions, tests and the component checklist. These Markdown guides are
not a documentation application and do not require access to private services.

Start with the [contributor guide](CONTRIBUTING.md) for an illustrated workflow:
scaffold a component, preview it locally, test it, and submit a pull request.

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

### Scaffold And Preview One Component

Contributors do not need the separate documentation application. From this
repository's source checkout, install the development dependencies and build
the local assets:

```bash
uv sync --all-groups
npm ci
npm run build:static-all
```

Use the existing Django management-command interface through the small
source-only `devtools` host. Inspect the proposed changes first with `--dry-run`,
then run the same command without that flag:

```bash
uv run python -m devtools create_component --name "Example Panel" \
  --category form --level molecule --compose input_field,button --dry-run
uv run python -m devtools create_component --name "Example Panel" \
  --category form --level molecule --compose input_field,button
uv run ruff check --fix
uv run ruff format
npm run build:static-all
uv run python -m devtools preview example_panel --port 8010
```

Open **http://127.0.0.1:8010/**. Only the selected component is rendered, using
the `default` example from `insight_ui/component_manifests/example_panel.json`.
Choose another declared example with `?example=example_name`. Editing example
values requires a page reload; rebuild the CSS when you introduce new utility
classes. `create_component --help` lists the generator options; `--js` requests a
JavaScript scaffold. The output is a starting point, not finished behavior.

| Level | Starting point | Composition rule |
| --- | --- | --- |
| `atom` | One small reusable primitive | Use the existing semantic design tokens. |
| `molecule` | A focused combination of primitives | Reuse their Config dataclasses and template tags. |
| `organism` | A larger reusable interface section | Compose existing components; keep application logic outside the library. |

The atomic level describes composition; the category describes purpose. They
do not introduce parallel `AtomConfig` or `MoleculeConfig` inheritance trees.
Include your component code, Config metadata, declarative example manifest and
behavior tests in the contributor PR. The documentation application can consume
that same contract separately; do not copy its catalog, editorial pages or
audit reports back into this package.

The preview binds **only to `127.0.0.1`**, with local readable CSS, fonts and
JavaScript. It ignores CDN settings from the environment. It has no login,
catalog, component-writing web endpoint, database setup requirement, or public
deployment mode. HTTP-triggered HTMX features, WebSocket backends and external
chart/map libraries are intentionally not supplied: test those integrations in
your own application host. Keyboard and ARIA behavior tests remain package tests;
this preview is not a WCAG-conformance claim.

`devtools` ships in the source archive so source contributors can use it, but
**never in the runtime wheel**. `scripts/check_distribution.py` verifies both
boundaries. Nothing here adds the full self-documentation application to an
installed `insight-ui` package.

## License

[GNU Affero General Public License v3.0](LICENSE).
For alternative licensing inquiries see [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md).

Licensing metadata follows the [REUSE specification](https://reuse.software): every
file carries an SPDX header or is covered by `REUSE.toml`, licence texts live in
`LICENSES/`, and bundled third-party components (Atkinson Hyperlegible Next under
OFL-1.1, Heroicons and Tailwind CSS under MIT) are listed in `NOTICE` and in
`insight_ui/THIRD_PARTY_NOTICES.md`, which ships inside the package.
