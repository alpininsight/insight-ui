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
describe its public API. Components are built to WCAG 2.1 AA and are WCAG 2.2 ready, with a
self-assessment and known limitations documented per component on the
documentation site. WCAG conformance is defined for complete web pages, so
this is not a certification of the library or of an application built with
it; conformance evidence is produced through the Enterprise Service.

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
installed Insight UI package.

## License

[GNU Affero General Public License v3.0](LICENSE).
For alternative licensing inquiries see [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md).

Licensing metadata follows the [REUSE specification](https://reuse.software): every
file carries an SPDX header or is covered by `REUSE.toml`, licence texts live in
`LICENSES/`, and bundled third-party components (Atkinson Hyperlegible Next under
OFL-1.1, Heroicons and Tailwind CSS under MIT) are listed in `NOTICE` and in
`insight_ui/THIRD_PARTY_NOTICES.md`, which ships inside the package.
