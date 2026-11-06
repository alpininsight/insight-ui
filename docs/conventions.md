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
generate the browser module skeleton. Add its behavior tests yourself:

| Concern | Convention | Example |
| --- | --- | --- |
| Python fields, functions, tags and component slug | `snake_case` | `example_panel` |
| Config class | `PascalCase` + `Config` | `ExamplePanelConfig` |
| Component template | Existing components directory; slug filename | `example_panel.html` |
| Browser module | `insight-ui-` prefix and kebab-case | `insight-ui-example-panel.js` |
| Tests | Python `test_*.py`; Vitest `*.test.js` | `test_example_panel.py`, `example-panel.test.js` |
| Config metadata | Typed fields and `metadata["doc"]` | Describe required fields, behavior and defaults. |
| Mutable Config defaults | A dataclass `default_factory` | Never share a list between instances. |

### Config Fields And Tag Arguments

- A field that holds another Config is named by its role, without a `_config`
  suffix: `htmx`, `icon`, `badge`, `table`, `items_per_page`, `user_menu`.
  Several fields of the same kind get role prefixes: `primary_action`,
  `secondary_action`.
- Field and tag names are the snake case of the class name. Class names follow
  English spelling: `navbar`, `sidebar`, `dropdown` and `checkbox` are one word,
  `search_bar` and `user_menu` are two.
- `request_url` is where a component navigates or sends its request. `url` (and
  `url_dark`) is the resource itself, such as an image or logo. A Config with
  several URLs uses `<role>_url`: `sign_up_url`, `cancel_url`.
- Text fields end in `_text`: `help_text`, `error_text`, `empty_text`. A
  component whose main content is a message uses `message`.
- A component that sends requests takes an optional `htmx: HtmxConfig` for the
  shared options. What its own mechanism needs (trigger, target, swap, method)
  goes to `{% htmx_attributes %}` as an override; see
  [HTMX requests](components.md#htmx-requests).
- Layout tags use an HTML dialect on purpose: `id`, `class`, `href`. Components use
  `tag_id`, `extra_classes` and `request_url`. Keep each side consistent.
- Field descriptions in `metadata["doc"]` are one line. Allowed values and
  defaults come from the type and the field itself, so do not repeat them.

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
The optional `--js` flag of `create_component` generates a JavaScript module
skeleton only. Register it manually in the shared initializer: add the import,
the class in `window.InsightUI`, and its `initAll()` call alongside the existing
components. Tests are not generated; add lifecycle and interaction coverage.
The skeleton is not finished behavior.

- The scaffold's `initAll()` scans the document for its `data-insight-*` selector.
  The shared initializer calls `initAll()` document-wide on `DOMContentLoaded`
  and `htmx:afterSwap`, not with a swap-scoped root.
- Avoid duplicate listeners or duplicate instances on the same element.
- Retain each listener's `{ element, type, handler }` in the scaffold's
  `boundHandlers` array so `destroy()` can remove it. The skeleton does not create
  an `AbortController`; add explicit cleanup for any additional resources.
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

When you rename or remove something public, update every usage in the same
change. Mark breaking commits with `!` and add a section to
[Migrating to 2.0](migration-2.0.md) (or the guide of the next major version):
before/after, the pull request and a search pattern for host projects,
plus a checklist entry. Temporary screenshots, browser profiles,
credentials, local paths and debugging output are not package source.

[All package guides](README.md) | [Contribution workflow](../CONTRIBUTING.md)
