<!--
SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
SPDX-License-Identifier: AGPL-3.0-only
-->

# Public Component Config Contract

This is the shared contributor contract for `insight-ui` and its reusable
`insight-ui-*` extensions. Package-specific checklists map it to their own
modules and tests; documentation applications consume it rather than defining
a second component API. See [components and composition](components.md) for
the Core rendering contract.

## Ownership And Imports

| Concern | Owner |
| --- | --- |
| Public Config dataclasses and exports | The reusable package's `<python_package>.configs` and its `__all__`. |
| Documented type aliases | `<python_package>.configs.types.TYPE_REGISTRY`, alongside the real aliases. |
| Rendering, validation and supported overrides | The package's actual Configs, template tags, templates and behavior tests. |
| Catalog selection, editorial examples, search and documentation routes | The consuming Docs application or package-local showcase adapter. |
| Settings, database, server and deployment | The consuming Django host, not the component Config API. |

For example, Core exports through `insight_ui.configs`; User exports through
`profiles.configs`. Public Configs must not live under `component_details`,
`showcase` or a documentation application's modules. Those consumers may move
without moving or breaking the package's public import path. Do not copy Config
definitions into the catalog, or require a private catalog edit to contribute
to the public package.

## Match The Implemented Rendering Contract

New Configs are typed, keyword-only dataclasses. Export them through the
package's `configs.__all__`, and document public fields in translatable
`metadata["doc"]`. Follow the package's docstring and executable-example
requirements in the [new component checklist](new-component-checklist.md).
Register documented type aliases with their allowed values and descriptions;
test those values against the aliases instead of maintaining another enum in
Markdown or the documentation host.

A Config must describe the component that actually renders: supported fields,
required values, defaults, validation and override behavior must agree. Do not
inherit fields merely to share documentation when the tag cannot consume them.
Request context and the `config` transport argument are not component fields.

There are two signature shapes to distinguish:

- A direct-argument tag exposes its real defaults and required arguments.
  Check the Config against those arguments, including field order where the
  package's API depends on it.
- A Config-aware tag can use Core's `build_config()` and the shared `UNSET`
  sentinel. Its effective defaults come from the Config, not from a literal
  equality between `UNSET` and a field default. Test omission, Config input and
  explicit keyword overrides, including `False` and permitted `None` values.

The presence of a Config class does **not** prove that its tag accepts
`config=`. Document that calling form only after the corresponding package
implements and tests it. An export relocation does not itself implement a new
tag signature, a narrower wheel or a Docs integration.

## Required Verification

1. Import the public exports and check that they are the intended Config
   dataclasses, with keyword-only fields and documented public parameters.
2. Compare Configs with the real tag contract. For direct-argument tags, cover
   required fields and defaults; for Config-aware tags, cover effective defaults,
   Config-plus-keyword precedence and invalid input. Keep rejection tests for
   unsupported arguments. Reflection helps detect drift but does not prove
   rendering behavior.
3. Render meaningful examples through the real tags and templates. Verify
   relevant escaping, validation, accessibility and JavaScript lifecycle too.
4. Check the scaffolder's real category choices, Config export, tag wiring and
   metadata. Generated placeholders are not finished components; use portable
   paths in dry-run output.
5. Run the package's [distribution checks](testing.md) against the built wheel
   in an isolated consumer, without accidentally importing the source checkout
   or the demo host. Use only the declared consumer dependencies and required
   Django apps. Package public imports and supported rendering must not rely on
   undeclared host-only modules. Verify the declared wheel contents and metadata,
   rather than assuming a source reorganization changed them.

## Documentation Handoff

Parameter and type tables come from the selected installed package's public
exports, field metadata and type registry. The Docs application owns the
adapter, editorial content, source views and integration tests. A new docset
still needs its own registration and acceptance checks; an export alone does
not make it discoverable in every Docs deployment.

Bind the handoff to a package version and source revision. Test the consuming
reference pages, actual demos, source lookup and search against that artifact.
Do not carry CI, review or artifact receipts from an older head across a rebase
or a base-branch import without revalidation. Keep source, package publication,
Docs deployment and live acceptance as separate claims.

Operational runbooks should link here for the component contract and own only
their installation and runtime gates. Do not duplicate full parameter tables or
turn a documentation-only change into permission to publish or deploy.

[All package guides](README.md)
