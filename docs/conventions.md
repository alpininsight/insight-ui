<!--
SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
SPDX-License-Identifier: AGPL-3.0-only
-->

# Contributor Conventions

Use the current neighboring implementation and generator as the reference.
This guide describes public development rules, not internal team operations.

## Names And Ownership

These are conventions for new scaffolds, not a claim that every older component
has the same layout. Use `--name "Example Panel"` for these names and `--js` to
include the browser module and its tests:

| Concern | Convention | Example |
| --- | --- | --- |
| Python fields, functions, tags and component slug | `snake_case` | `example_panel` |
| Config class | `PascalCase` + `Config` | `ExamplePanelConfig` |
| Component template | Existing components directory; slug filename | `example_panel.html` |
| Browser module | `insight-ui-` prefix and kebab-case | `insight-ui-example-panel.js` |
| Tests | Python `test_*.py`; Vitest `*.test.js` | `test_example_panel.py`, `example-panel.test.js` |
| Config metadata | Typed fields and `metadata["doc"]` | Describe required fields, behavior and defaults. |
| Mutable Config defaults | A dataclass `default_factory` | Never share a list between instances. |

Config modules are organized by category. Use [configs/](../insight_ui/configs/)
and its public exports, not one new configuration system per atomic level.
See [component anatomy](components.md) for the source map.

## HTML And Data Hooks

- Prefer native controls and semantic elements over clickable generic elements.
- Preserve Django's escaping. Do not make untrusted content safe to simplify a demo.
- IDs and `aria-controls` / `aria-labelledby` references must remain unique when
  a component is repeated. Boolean HTML attributes are present or absent, not
  strings such as `disabled="false"`.
- Use existing semantic classes and [design roles](design-system.md). Data
  attributes identify behavior or pass parameters, not purely decorative styles.
- Follow the relevant module's exact `data-insight-*` spelling. Existing hooks
  are public compatibility surfaces; do not rename them as incidental cleanup.

For example, [Dropdown](../insight_ui/static/insight_ui/js/insight-ui-dropdown.js)
reads a target element ID from `data-insight-dropdown`. Options are component
specific; do not invent a global option naming scheme that existing modules
do not understand.

## JavaScript Lifecycle

Use the ES module and initialization patterns in
[insight-ui-init.js](../insight_ui/static/insight_ui/js/insight-ui-init.js).
The optional `--js` output from [scaffolding_js.py](../insight_ui/scaffolding_js.py)
registers the class in `window.InsightUI` and the shared initializer. It is a
lifecycle skeleton, not finished behavior.

- The scaffold's `initAll(root = document)` scans descendants of the supplied
  root. The shared initializer currently calls `initAll()` document-wide on
  `DOMContentLoaded` and `htmx:afterSwap`, not with a swap-scoped root.
- Avoid duplicate listeners or duplicate instances on the same element.
- Retain bound listener references or register listeners with the scaffold's
  `this.controller.signal` so `destroy()` can release them.
- Attach the instance as `element.__insightInstance`: the cleanup hook in
  [insight-ui-utils.js](../insight_ui/static/insight_ui/js/insight-ui-utils.js)
  calls its `destroy()` on `htmx:beforeCleanupElement`. Removal outside that hook
  needs explicit cleanup, including timers, observers and global listeners.
- Preserve keyboard behavior and focus, not just click handling.
- Add Vitest regression tests for initialization, reinitialization and cleanup.

Do not introduce a new global constructor namespace or a second initializer
for a single component. Use [existing JS tests](../tests/js/) as working examples.

## Text, Licensing And Review

Follow [i18n](i18n.md) for user-facing strings, interpolation and RTL. Technical
identifiers are not translated. Preserve the repository's SPDX/REUSE conventions;
do not add internal brand assets or third-party assets without provenance.

New public fields, hooks and tokens require compatible defaults and tests.
Document breaking changes explicitly. Temporary screenshots, browser profiles,
credentials, local paths and debugging output are not package source.

[All package guides](README.md) | [Contribution workflow](../CONTRIBUTING.md)
