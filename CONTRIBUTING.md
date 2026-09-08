<!--
SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
SPDX-License-Identifier: AGPL-3.0-only
-->

# Contributing To Insight UI

Build reusable Django components here: their typed configuration, templates,
JavaScript when needed, source assets, and behavior tests. You do not need the
separate documentation application or access to private services to contribute.

The scaffold and preview commands are available on `develop`. Start from an
updated source checkout; an older installed wheel is not the contributor host.

## Package Reference

The [package guides](docs/README.md) are available in this repository without
access to the separate documentation application. Read the relevant guide when
changing a component rather than treating the generated skeleton as finished:

| Task | Guide |
| --- | --- |
| Use the package in a Django application | [Getting started](docs/getting-started.md) |
| Change Configs, tags or composition | [Components](docs/components.md) and [conventions](docs/conventions.md) |
| Change colors, surfaces, radii or shadows | [Design system](docs/design-system.md) |
| Build CSS/JS or serve package assets | [Static assets](docs/static-assets.md) |
| Add translated strings or RTL behavior | [Internationalization](docs/i18n.md) |
| Check keyboard, focus and ARIA behavior | [Accessibility](docs/accessibility.md) |
| Validate and submit a component | [Testing](docs/testing.md) and [component checklist](docs/new-component-checklist.md) |

## The Workflow

![Six steps: start a feature worktree from develop; dry-run and generate an atom, molecule, or organism; complete Config, tag, template, tests, and manifest; format, build assets, and preview on localhost; run behavior and distribution checks; open a pull request to develop. Documentation maintainers subsequently reuse the manifest.](.github/images/contributor-workflow.svg)

1. Create a feature branch and worktree from the latest `develop`.
2. Choose a category and atomic level; inspect a dry-run before generating files.
3. Implement the component and its examples using existing Insight UI patterns.
4. Format the source, build local assets, and preview one component.
5. Test behavior and the package boundary, not only the screenshot.
6. Open a pull request to `develop`; maintainers handle the separate reference site.

## 1. Prepare A Source Worktree

Use Git, [uv](https://docs.astral.sh/uv/getting-started/installation/), and Node.js
with npm. Use the Python version in `.python-version` for local development;
the supported package versions are listed in the [README](README.md).

From a clone of this repository:

```bash
git fetch origin develop
git worktree add -b feat/example-panel ../insight-ui-example-panel origin/develop
cd ../insight-ui-example-panel
uv sync --all-groups
npm ci
```

The commands assume `origin` points to the upstream repository. If working from
a fork, fetch the upstream remote and use its `develop` ref as the starting
point instead. Push your feature branch to your fork, not to upstream `develop`.

Run contributor commands from this worktree's root. The `devtools` preview host
is source-only: it is included in the source distribution, not the installed
wheel. Installing the library into an unrelated app is not a substitute for
this checkout. No documentation app or database setup is needed for the preview.

## 2. Choose The Component Shape

Check the [component reference](https://insight-ui.com/docs/configs) and existing
source before adding a new component. Prefer composing existing components over
copying their markup or behavior.

| Level | Starting point | Generator requirement |
| --- | --- | --- |
| `atom` | One small primitive with its own configuration and template. | No `--compose`. |
| `molecule` | A focused combination, such as a field and an action. | `--compose` names existing component tags with Config dataclasses. |
| `organism` | A larger functional section assembled from components. | The same explicit composition contract; you implement the layout and behavior. |

The level describes composition. The category describes purpose and selects
the existing configuration module; neither creates a new Config class hierarchy.
Categories are `layout`, `navigation`, `input`, `popup`, `util`, `list`, `filter`,
`card`, and `form`.

These are alternative dry-runs for the three levels:

```bash
uv run python -m devtools create_component \
  --name "Example Status" --category util --level atom --dry-run

uv run python -m devtools create_component \
  --name "Example Panel" --category form --level molecule \
  --compose input_field,button --dry-run

uv run python -m devtools create_component \
  --name "Example Toolbar" --category form --level organism \
  --compose input_field,button --dry-run
```

`--dry-run` validates the request and lists paths without writing files. The
generator rejects existing names, incompatible composition, and unsafe import
or JavaScript name collisions. Resolve the reported cause rather than bypassing
validation or overwriting another component.

The rest of this guide uses **Example Panel**. Generate it once by removing
`--dry-run`:

```bash
uv run python -m devtools create_component \
  --name "Example Panel" --category form --level molecule \
  --compose input_field,button
```

If your component needs JavaScript, add `--js` to both its dry-run and its initial
generation command. It creates lifecycle wiring and a test stub, not finished
interaction logic. Do not run the generator a second time over an existing name.

## 3. Complete The Scaffold

For the example above, generation creates or updates these source files:

| File | Your responsibility |
| --- | --- |
| `insight_ui/configs/forms.py` | Define `ExamplePanelConfig` fields, defaults, and field documentation. Other categories use their corresponding module. |
| `insight_ui/configs/__init__.py` | Export the Config using the existing package API. |
| `insight_ui/templatetags/insight_tags.py` | Register the real `example_panel` inclusion tag. |
| `insight_ui/templates/insight_ui/components/example_panel.html` | Implement accessible markup; compose children through their existing tags. |
| `tests/insight_ui/unit/components/test_example_panel.py` | Extend the generated render checks with meaningful behavior, escaping, and edge cases. |
| `insight_ui/component_manifests/example_panel.json` | Keep component metadata and named example inputs consistent with the Config. |

With `--js`, the generator also creates
`insight_ui/static/insight_ui/js/insight-ui-example-panel.js` and
`tests/js/example-panel.test.js`, and registers the module in the existing
`insight-ui-init.js`. Follow the package's initialization and cleanup patterns,
including repeated HTMX initialization where applicable.

Use semantic design roles from `insight_ui/utils/input.css` before adding new
tokens. Keep colors, borders, radii, and shadows consistent with existing
components. Do not add private brand assets or a separate component-specific
palette to this public package.

### Example Inputs Are Not A Second Implementation

The manifest names the public Config class, template, composition, and examples.
Its `examples` entries contain a `name` and a `config` object. Keep a `default`
example and give additional examples unique names. The preview constructs the
real Config dataclass and renders the real template tag from these inputs.

Edit the generated manifest to make the example useful. For example, the
`default` entry's **`config` object** for Example Panel can be:

```json
{
  "label": "Find an item",
  "tag_id": "example-panel",
  "input_field": {"name": "query", "label": "Query"},
  "button": {"label": "Search"}
}
```

This is not a complete manifest. The same object can be supplied in a JSON file
with `--example-config <path>` during the initial dry-run and generation. Keep
values declarative; the manifest does not execute arbitrary Python or replace
the field documentation in the Config dataclass.

## 4. Build And Preview Locally

Normalize generated imports and formatting, then compile and minify the assets:

```bash
uv run ruff check --fix
uv run ruff format
npm run build:static-all
uv run python -m devtools preview example_panel --port 8010
```

Open **[http://127.0.0.1:8010/](http://127.0.0.1:8010/)**. Stop the server with
`Ctrl+C`. If the port is occupied, choose another port with `--port`.

The server binds only to `127.0.0.1` and previews the selected component, not a
catalog. `/?example=default` selects the default input; another declared example
can be selected with `?example=<name>`. Unknown examples return 404. Use the
preview's light/dark switch and narrow the viewport to check both appearance
and layout.

The preview uses local package CSS, fonts, and JavaScript, with CDN delivery
disabled. Its initial page does not need external assets or private credentials.
It is not an application backend: submission endpoints, WebSocket services, or
remote chart/map data need an appropriate integration test host.

`build:static-all` compiles Tailwind from `input.css` and package sources, then
creates minified CSS/JS. **`build:static` alone only minifies existing assets.**
Rebuild after changing templates, classes, tokens, or JavaScript. Commit any
tracked readable asset changes, but do not force-add ignored `.min.css` or
`.min.js` files. Building locally does not publish to a CDN.

## 5. Check Behavior And Distribution

Start with the generated component test:

```bash
uv run pytest tests/insight_ui/unit/components/test_example_panel.py
```

If you generated JavaScript, run its focused test too:

```bash
npm test -- tests/js/example-panel.test.js
```

Then run the package checks before opening the PR:

```bash
uv run ruff check --no-fix
uv run ruff format --check
uv run python -m django check --settings=tests.settings
uv run pytest
npm test
npm run verify:static-build
uv build
uv run python scripts/check_distribution.py
git diff --check
```

The tests use the package's minimal Django host, not the documentation app.
Keep Keyboard, ARIA, focus, and lifecycle behavior tests in the library when
they protect the component contract. Those tests and a local preview are not
a complete WCAG conformance audit of an application.

Check long text, missing optional values, escaping of untrusted text, repeated
instances, light/dark mode, and narrow screens. For interactive components, test
keyboard operation, accessible names, and focus behavior as well as mouse use.
The generated test stubs are a starting point, not an acceptance checklist.

## 6. Open A Pull Request

Review `git diff` and `git status` before staging. Include only the intended
source, tests, manifest, and tracked generated assets. Preserve the existing
SPDX/REUSE licensing conventions; see [LICENSE](LICENSE) and [NOTICE](NOTICE).

Push your feature branch and open a PR targeting **`develop`**, with a
Conventional Commit title such as `feat(components): add example panel`.
Explain the use case, why existing components are not enough, how composition
works, and which checks you ran. Mention any missing tests or known limits.

Include a useful preview image in the PR when appearance changes. Temporary
debugging screenshots, browser profiles, caches, and credentials do not belong
in the repository. Commit an image only when documentation references it or an
actual visual-regression test uses it as a baseline.

### Maintainer Handoff

The separate reference site can consume the reviewed component manifest and
Config metadata instead of duplicating the component implementation. Maintainers
coordinate that import and any editorial examples after the package change is
accepted. Contributors do not need private documentation access: keep the
manifest and behavior tests here; the full catalog, documentation application,
and application-level audit evidence stay outside the public package.
