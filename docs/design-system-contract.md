# Design system contract

This document defines the stable public design language of Insight UI and the
rules for extending it across the core package, sibling packages, and host
projects.

The goal is to keep `insight-ui` reusable and stable without turning the core
package into a collection of domain-specific styling exceptions.

Tailwind CSS is the default and reference styling implementation, but the public
design contract is semantic. Reusable design decisions should be expressed as
Insight UI semantics first: tokens, component classes, template structure,
behavior hooks, and accessibility contracts. A future Bootstrap or custom CSS
implementation would need to implement the same contract rather than redefine
the design language.

## What this document is

A design-system contract is an agreement about which visual and behavioral
concepts are public and stable, where they belong in the codebase, and how new
packages should reuse them.

Use this document when you need to answer questions such as:

- Should this visual value be a public token or a local implementation detail?
- Does this belong in `input.css`, a component template, JavaScript, or an
  extension package?
- Is this a shared Insight UI concept or only a domain-specific detail?
- Can a host application override this globally without copying templates?
- Would this concept still make sense if the styling implementation changed?

This document is not a full component catalog and it does not replace the
customization guide. It defines the stable rules behind those documents.

## User-facing starting point

For users, the design system starts with their corporate identity, not with
template overrides. A host application should map its brand values to Insight
UI's semantic tokens in `input.css` first:

| Corporate identity value | Insight UI token area | Result |
|---|---|---|
| Brand color | `--color-insight-primary` and interaction variants | Primary buttons, links, focus accents, and important actions follow the brand. |
| Supporting brand color | `--color-insight-secondary` and variants | Secondary buttons and supporting accents stay aligned. |
| Feedback palette | `success`, `warning`, `danger`, `info` tokens | Alerts, state indicators, and validation colors stay consistent. |
| Text palette | `text-primary`, `text-secondary`, `text-link` tokens | Content hierarchy works across components and dark mode. |
| Typography | `--font-sans` and base heading styles | Pages and components share the same type direction. |
| Reusable surfaces | Component classes in `@layer components` | Containers, examples, inline tags, and forms share the same visual treatment. |

The preferred flow for a consumer project is:

1. Copy or provide a project-owned `input.css`.
2. Set the corporate identity in the `@theme` block.
3. Use Insight UI template tags and component classes as usual.
4. Override component templates only when structure, behavior, or component
   anatomy must change.

This keeps brand alignment centralized. A project can change its visual identity
without editing every button, form, heading, or documentation example.

## Source of truth

| Concern | Source of truth | Rule |
|---|---|---|
| Theme tokens | `insight_ui/utils/input.css` in `@theme` | Add stable brand, semantic, text, surface, and state tokens here. |
| Base element styles | `insight_ui/utils/input.css` in `@layer base` | Use for generic HTML behavior such as headings, horizontal rules, and cursor behavior. |
| Reusable utility/component classes | `insight_ui/utils/input.css` in `@layer components` | Use for reusable classes such as `.btn`, `.input`, `.component-container`, or `.inline-tag`. |
| Component structure | `insight_ui/templates/insight_ui/components/` | Put semantic HTML, ARIA attributes, layout composition, and component anatomy here. |
| Page shell structure | `insight_ui/templates/insight_ui/base.html` | Owns header, navbar block, drawer block, sidebars, heading, content, and footer placement. |
| Self-documentation demos | `insight_ui/templates/insight_ui/docs/` and `insight_ui/component_details/` | Owns component examples, detail-page text, parameter docs, related components, and demo context. |
| Frontend behavior | `insight_ui/static/insight_ui/js/` | Owns initialization, state, keyboard handling, resize handling, and behavior attached to `data-*` attributes. |
| Template tag API | `insight_ui/templatetags/insight_tags.py` | Owns reusable Django-facing component APIs and context normalization. |
| Extension-specific components and tokens | Sibling package or host project | Owns domain-specific components and fast-moving tokens until they become stable enough for core. |

Do not use generated CSS as the design-system source. The built stylesheet under
`insight_ui/static/insight_ui/css/` is output, not the design contract.

## Documentation surfaces and source-of-truth boundaries

Insight UI's docs are split between repository-level Markdown, component
self-documentation, and rendered application pages. Keep these boundaries clear:

- Markdown docs in `docs/` define policy, public contracts, naming rules, and
  maintainer workflow.
- `insight_ui/component_details/*` defines per-component user-facing docs such
  as descriptions, usage, parameters, accessibility notes, related topics, and
  demo context.
- `insight_ui/templatetags/insight_tags.py` defines the Django-facing component
  API and must stay aligned with the parameter self-doc.
- `insight_ui/utils/input.css` defines public tokens and reusable semantic
  classes. Generated CSS is never the contract.
- `insight_ui/static/insight_ui/js/*` defines behavior contracts for
  `data-insight-*` hooks.
- `insight_ui/templates/insight_ui/docs/*` renders documentation pages and HTMX
  partials. These templates may compose and display docs, but they should not
  become the canonical explanation of API, token, or behavior contracts.

The maintainer-facing map for these boundaries lives in
[Documentation Architecture](docs-architecture.md).

## Stable public contract today

These concepts already exist in Insight UI and form the baseline that extensions
and host applications should inherit before introducing domain-specific variants.

| Concept | Current representation | Design meaning |
|---|---|---|
| Brand colors | `--color-insight-primary`, `--color-insight-secondary` | Main product actions and secondary accents. |
| Interaction variants | `*-hover`, `*-active` color tokens | Pointer and pressed states for interactive elements. |
| Status colors | `success`, `warning`, `danger`, `info` tokens | Semantic user feedback and system state. |
| Text hierarchy | `text-primary`, `text-secondary`, `text-link` | Primary content, secondary content, and navigable text. |
| Dark mode | `@custom-variant dark` and dark text tokens | Theme-aware rendering via `data-theme=dark`. |
| Border hierarchy | `--color-insight-border-surface`, `--color-insight-border-control`, `insight-border-*` | Themeable boundaries for cards, docs surfaces, forms, inputs, and controls. |
| Shadow hierarchy | `--insight-shadow-*`, `insight-shadow-*` | Themeable elevation and neobrutalist offsets mapped from the project design language, with Tailwind values as defaults. |
| Surfaces | `.component-container`, `.example-container`, cards, panels, modal body | Visual containers that separate content from the page background. |
| Layout hierarchy | Navbar, sidebars, heading, content, footer, drawer blocks | Page shell and navigation structure. |
| Overlay hierarchy | Modal backdrop, sidebar backdrop, z-index utilities | Layering for temporary UI and blocking interactions. |
| Documentation surfaces | Code block, inline tag, demo container | Self-documentation chrome and examples. |
| Responsive behavior | Tailwind breakpoints and component template branches | Viewport-specific layout changes. |
| Data hooks | `data-insight-*` and component-specific `data-*` attributes | Stable JavaScript initialization and behavior contracts. |
| Accessibility hooks | ARIA attributes, semantic HTML, focus handling | WCAG-aligned component behavior. |

## Implementation rules

Use the following placement rules when deciding where a design-system concept
should live:

- Stable theme tokens belong in `insight_ui/utils/input.css`.
- Shared semantic component classes belong in `@layer components`.
- Reusable borders and shadows should use `--color-insight-border-*` and
  `--insight-shadow-*` tokens instead of direct `border-gray-*` or `shadow-*`
  utilities when the visual rule is part of the component contract.
- Semantic HTML, ARIA, component anatomy, and data hooks belong in templates.
- JavaScript behavior belongs in `insight_ui/static/insight_ui/js/`.
- Django-facing API normalization belongs in template tags.
- Examples, parameter documentation, and component explanations belong in the
  self-documenting docs.

Data attributes should stay behavior-oriented. They are part of the JavaScript
contract and should not be introduced as purely decorative markers.

## Extension contract

`insight-ui` should define the generic rules that every extension follows, not a
bilateral agreement with one specific sibling package.

An extension may be a sibling package such as `insight-ui-webgl`, but the same
rules apply to any future package: it should inherit the core design language
first and add only the domain concepts that cannot be expressed with the
existing core tokens, templates, and behavior hooks.

Concrete token mapping tables for a specific domain belong in that extension's
own repository. The core contract only needs to define:

- which concepts belong in core,
- which concepts stay in the extension,
- how extension tokens should be named,
- when extension concepts are mature enough to promote into core.

### What extensions inherit from core

Extensions should reuse the existing Insight UI contract wherever the concept is
shared:

- brand and status colors,
- text hierarchy,
- reusable surfaces,
- focus, hover, disabled, and selected states,
- layout and overlay hierarchy,
- accessibility expectations,
- JavaScript hook conventions.

### What stays in an extension

Keep a token, class, or behavior in the extension package when most of these
are true:

- it is used by one domain or component family only,
- it depends on renderer, runtime, or extension internals,
- it is likely to change while the extension matures,
- it is not meaningful for general Insight UI consumers,
- it can safely use a local fallback when the host app does not define it.

### What belongs in core

Promote an extension concept into `insight-ui` only when most of these are true:

- it is useful across multiple components or sibling packages,
- it describes a stable design concept, not an implementation detail,
- host applications should be able to override it globally,
- the name and meaning are expected to remain stable,
- it can be documented as public API without extension-specific context.

### Naming rules for extension tokens

Prefer semantic names. A token name should describe the role of the value, not
the current implementation detail.

Core token examples:

```css
--color-insight-primary
--color-insight-danger
--color-insight-text-primary
```

Extension token pattern:

```css
--color-insight-<domain>-<semantic-purpose>
```

Examples:

```css
--color-insight-flow-edge-selected
--color-insight-graph-node-highlight
--color-insight-webgl-grid-line
--color-insight-xr-overlay-surface
```

Avoid pushing implementation internals into the core contract. Tokens tied to a
specific renderer, engine, or temporary component detail should remain local to
the extension package.

## Decision checklist

Before adding a new design value, answer these questions:

1. Is this a stable design concept or a local implementation detail?
2. Should downstream apps override it globally?
3. Will more than one component or extension use it?
4. Does it need a documented public API name?
5. Does it belong to styling only, or does it require JavaScript behavior?

Use the answers to place the change:

- stable theme contract: `insight_ui/utils/input.css`
- semantic component structure: component template
- behavior and state: JavaScript module
- Django API normalization: template tag
- extension-specific domain behavior: sibling package or host project

## Maintenance expectations

- Adding a core token is a public API addition and should be documented.
- Renaming or removing a core token is a breaking change.
- Changing a token default may be visually significant and should be mentioned in release notes.
- New visual components should update their self-documenting demo and parameter documentation.
- Extensions should document which core tokens they consume and which local tokens they own.
