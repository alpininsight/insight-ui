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
- [ ] The Config is typed, exported and documented through field metadata.
- [ ] Defaults, validation and optional values agree with the real tag signature.
- [ ] Molecules/organisms reuse child Configs and tags, not copies of their HTML/JS.
- [ ] HTML is semantic, untrusted values stay escaped and repeated IDs are safe.
- [ ] CSS uses the [existing semantic roles](design-system.md); no duplicate
  component-specific gray palette or obsolete token names were introduced.
- [ ] A useful default example and edge cases are represented in the manifest.

## Behavior And Verification

- [ ] User-facing strings are translatable; check [i18n](i18n.md), long text and RTL.
- [ ] [Keyboard, focus and ARIA](accessibility.md) work for relevant states.
- [ ] Optional JS handles repeated initialization, HTMX replacement and cleanup.
- [ ] Python and, when appropriate, Vitest tests verify actual public behavior.
- [ ] Assets were rebuilt and the component inspected in light/dark and narrow views.
- [ ] Required [quality and distribution checks](testing.md) passed on the PR head.
- [ ] The PR explains the use case, compatible defaults, tests and remaining limits.
- [ ] Licensing/provenance is recorded for any new assets; no private brand files,
  credentials, browser profiles or temporary debugging captures were included.

## Maintainer Handoff

Maintainers can use the reviewed Config metadata and manifest to update the
separate reference application. Catalog registration, translations of editorial
pages, search indexing and application-level evidence belong to that downstream
change. Do not require contributors to modify private files to finish this PR.

When a change alters the package contract, update the relevant public guide here.
Keep full parameter tables generated from Config metadata rather than maintaining
another hand-written schema in Markdown. Review the merged result as well as
the feature branch before declaring an integration complete.

[All package guides](README.md)
