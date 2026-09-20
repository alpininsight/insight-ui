<!--
SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
SPDX-License-Identifier: AGPL-3.0-only
-->

# New Component Checklist

This checklist is for the **public package PR**. An external contributor does
not need access to the separate catalog, its editorial tools or audit reports.
Follow [CONTRIBUTING.md](../CONTRIBUTING.md) for the generator and local preview.

## Component Contract

- [ ] Existing components cannot already express the use case through composition.
- [ ] The name, category and atomic level describe the component, not a customer.
- [ ] The Config is a typed dataclass exported through `insight_ui.configs`.
- [ ] Defaults, validation and optional values agree with the real tag signature.
- [ ] Molecules/organisms reuse child Configs and tags, not copies of their HTML/JS.
- [ ] HTML is semantic, untrusted values stay escaped and repeated IDs are safe.
- [ ] CSS uses the [existing semantic roles](design-system.md); no duplicate
  component-specific gray palette or obsolete token names were introduced.

## Documentation-Ready Public Inputs

- [ ] Every field has a type, a description in the Config docstring's `Attributes`
  section and matching English text in translatable `metadata["doc"]`.
- [ ] The Config's `__example__` contains up-to-date Python constructor source text
  using real fields and non-secret example values; it is not a Config instance.
- [ ] A test instantiates that example and renders it through the registered tag
  and real template, checking meaningful content rather than only a successful response.
- [ ] The example, defaults, supported overrides and nested Configs agree with the
  implementation; the scaffold's placeholder has been replaced.
- [ ] The PR points to the Config, example, tag/template and behavior tests, without
  requiring a second schema, mandatory JSON manifest or private catalog changes.

## Behavior And Verification

- [ ] User-facing strings are translatable; check [i18n](i18n.md), long text and RTL.
- [ ] [Keyboard, focus and ARIA](accessibility.md) work for relevant states.
- [ ] Optional JS handles repeated initialization, HTMX replacement and cleanup.
- [ ] Python and, when appropriate, Vitest tests verify actual public behavior.
- [ ] Config docstring/metadata integrity and the relevant scaffold tests pass;
  they supplement, not replace, tests of the completed component and its examples.
- [ ] Assets were rebuilt and the component inspected in light/dark and narrow views.
- [ ] Required [quality and distribution checks](testing.md) passed on the PR head.
- [ ] The PR explains the use case, compatible defaults, tests and remaining limits.
- [ ] Licensing/provenance is recorded for any new assets; no private brand files,
  credentials, browser profiles or temporary debugging captures were included.

## Maintainer Handoff

The public handoff is the reviewed package implementation, metadata, examples
and tests. Maintainers separately consume the exact reviewed package artifact,
identified by version and source revision, in the reference application. They
verify catalog registration, parameters, real demos, source views and search
against that artifact, not just an older package pin that happens to pass tests.

Editorial translations and application-level audit evidence also belong to that
downstream change. Public package tests are not proof of a completed reference
site or full WCAG conformance. Contributors need neither private credentials nor
private documentation edits to finish their PR.

When a change alters the package contract, update the relevant public guide here.
Keep full parameter tables generated from Config metadata rather than maintaining
another hand-written schema in Markdown. Review the merged result as well as
the feature branch before declaring an integration complete.

[All package guides](README.md)
