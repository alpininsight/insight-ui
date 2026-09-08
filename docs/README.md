<!--
SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
SPDX-License-Identifier: AGPL-3.0-only
-->

# Package And Contributor Guides

Start with [CONTRIBUTING.md](../CONTRIBUTING.md) to build and preview a new
component. These guides describe the reusable package and local development,
not a second documentation application or a deployment system.

| Guide | Purpose |
| --- | --- |
| [Getting started](getting-started.md) | Integrate the package, settings and base template into your own Django app. |
| [Components](components.md) | Configs, template tags, composition and declarative examples. |
| [Conventions](conventions.md) | Naming, HTML, JavaScript lifecycle and source ownership. |
| [Design system](design-system.md) | Existing semantic tokens and safe changes to the styling contract. |
| [Static assets](static-assets.md) | Local files, Tailwind compilation, minification and generic CDN settings. |
| [Internationalization](i18n.md) | Package translations, gettext and RTL checks. |
| [Accessibility](accessibility.md) | Component requirements and behavior-test responsibilities. |
| [Testing](testing.md) | Local quality, regression, asset and distribution checks. |
| [New component checklist](new-component-checklist.md) | Review criteria for the public contributor PR. |

## Ownership

The implementation and these public development rules live in `insight-ui`.
Dataclass field metadata, source code and example manifests remain the API
source of truth; Markdown does not duplicate every parameter table or component
demo. [The reference website](https://insight-ui.com/) is maintained separately
and can refer to these guides instead of maintaining another copy of the rules.

The website's catalog, search, editorial examples and application-level audit
evidence are not required to contribute. Internal infrastructure, deployment
instructions and commercial deliverables do not belong in these guides.

These are Git repository guides. The current distribution contract excludes
`docs/` from both wheel and sdist; it does not exclude public Markdown from Git.
Source-only preview tools remain separate from the runtime wheel.
