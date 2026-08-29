# Design System

This document defines the stable public design language of Insight UI and the rules for extending it across the core package, sibling packages, and host projects.

## What This Document Covers

A design-system contract is an agreement about which visual and behavioral concepts are public and stable, where they belong in the codebase, and how new packages should reuse them.

Use this document when you need to answer:

- Should this visual value be a public token or a local implementation detail?
- Does this belong in `input.css`, a component template, JavaScript, or an extension package?
- Is this a shared Insight UI concept or only a domain-specific detail?
- Can a host application override this globally without copying templates?

## Source of Truth

| Concern | Location | Rule |
|---------|----------|------|
| Theme tokens | `insight_ui/utils/input.css` `@theme` | Stable brand, semantic, text, surface, and state tokens |
| Base element styles | `insight_ui/utils/input.css` `@layer base` | Generic HTML behavior (headings, rules, cursors) |
| Reusable component classes | `insight_ui/utils/input.css` `@layer components` | Classes like `.btn`, `.input`, `.component-container` |
| Component structure | `insight_ui/templates/insight_ui/components/` | Semantic HTML, ARIA, layout, data hooks |
| Page shell structure | `insight_ui/templates/insight_ui/base.html` | Header, navbar, sidebars, content, footer |
| Template tag API | `insight_ui/templatetags/insight_tags.py` | Django-facing component APIs and context normalization |
| JavaScript behavior | `insight_ui/static/insight_ui/js/` | Initialization, state, keyboard, `data-*` behavior |
| Self-documentation | `documentation/component_details/` | Descriptions, usage, parameters, accessibility, demos |
| Naming conventions | `docs/conventions.md` | Stable naming for Python, templates, CSS, hooks |
| Design contract | This document | Public tokens, semantic classes, extension rules |

**Important:** Never use generated CSS (`static/insight_ui/css/`) as the design-system source. The built stylesheet is output, not the contract.

## Stable Public Contract

These concepts form the baseline that extensions and host applications should inherit:

| Concept | Representation | Design Meaning |
|---------|----------------|----------------|
| Brand colors | `--color-insight-primary`, `--color-insight-secondary` | Main actions and secondary accents |
| Interaction variants | `*-hover`, `*-active` tokens | Pointer and pressed states |
| Status colors | `success`, `warning`, `danger`, `info` | Semantic user feedback |
| Text hierarchy | `text-primary`, `text-secondary`, `text-link` | Content hierarchy |
| Dark mode | `@custom-variant dark` | Theme-aware via `data-theme=dark` |
| Surfaces | `.component-container`, cards, panels | Visual containers |
| Layout hierarchy | Navbar, sidebars, heading, content, footer | Page shell structure |
| Overlay hierarchy | Modal backdrop, sidebar backdrop, z-index | Temporary UI layering |
| Data hooks | `data-insight-*` attributes | JavaScript behavior contracts |
| Accessibility | ARIA attributes, semantic HTML, focus | WCAG-aligned behavior |

## Implementation Rules

Use these placement rules when deciding where a design-system concept belongs:

| Change Type | Location |
|-------------|----------|
| Stable theme tokens | `insight_ui/utils/input.css` |
| Shared semantic component classes | `@layer components` |
| Semantic HTML, ARIA, data hooks | Component templates |
| JavaScript behavior | `insight_ui/static/insight_ui/js/` |
| Django-facing API normalization | Template tags |
| Component explanations and examples | `documentation/component_details/*` |

Data attributes should stay behavior-oriented. They are part of the JavaScript contract and should not be introduced as purely decorative markers.

## Semantic Non-Color Roles

Color, radius, shadow, and surface tokens already use semantic roles. Motion, blur, and density should follow the same pattern:

| Area | Semantic Role | Technical Implementation |
|------|---------------|-------------------------|
| Motion duration | `--insight-motion-duration-fast` | `--duration-fast` |
| Motion easing | `--insight-motion-ease-standard` | `--ease-out`, cubic-bezier |
| Backdrop blur | `--insight-backdrop-blur` | `--blur-sm`, `backdrop-filter` |
| Density | `--insight-density-control-x` | Tailwind spacing scale |

This keeps the public contract independent from Tailwind's token names.

## Extension Contract

Extensions should inherit the core design language first and add only domain concepts that cannot be expressed with existing core tokens.

### What Extensions Inherit

- Brand and status colors
- Text hierarchy
- Reusable surfaces
- Focus, hover, disabled, and selected states
- Layout and overlay hierarchy
- Accessibility expectations
- JavaScript hook conventions

### What Stays in an Extension

Keep a token, class, or behavior in the extension when:

- It is used by one domain or component family only
- It depends on renderer, runtime, or extension internals
- It is likely to change while the extension matures
- It is not meaningful for general Insight UI consumers
- It can safely use a local fallback

### What Belongs in Core

Promote an extension concept into core when:

- It is useful across multiple components or packages
- It describes a stable design concept, not an implementation detail
- Host applications should be able to override it globally
- The name and meaning are expected to remain stable

### Extension Token Naming

Core token pattern:
```css
--color-insight-primary
--color-insight-danger
```

Extension token pattern:
```css
--color-insight-<domain>-<semantic-purpose>
```

Examples:
```css
--color-insight-flow-edge-selected
--color-insight-webgl-grid-line
```

## Decision Checklist

Before adding a new design value:

1. Is this a stable design concept or a local implementation detail?
2. Should downstream apps override it globally?
3. Will more than one component or extension use it?
4. Does it need a documented public API name?
5. Does it belong to styling only, or does it require JavaScript behavior?

Use the answers to place the change in the appropriate location.

## Documentation Pipeline

The self-documenting application is built from three layers:

1. **Component context data** in `documentation/component_details/`
2. **Django views** that assemble page context
3. **Documentation templates** that render into pages or HTMX partials

`component_context.py` is the registry for per-component documentation. Context builders use `@register_component(Component.X)` and contribute dictionaries for description, usage, parameters, accessibility, and related topics.

### Runtime Layers

| Layer | Location | Responsibility |
|-------|----------|----------------|
| Template tag API | `insight_tags.py` | Public signature, defaults, context |
| Component HTML | `templates/.../components/` | Semantic structure, ARIA, data hooks |
| Design tokens | `input.css` | Theme tokens, base styles, classes |
| JavaScript | `static/.../js/` | Initialization, lifecycle, events |
| Self-doc data | `documentation/component_details/` | User-facing docs |
| Rendered docs | `documentation/templates/documentation/docs/` | Layout and display |

## Maintenance Expectations

- Adding a core token is a public API addition
- Renaming or removing a core token is a breaking change
- Changing a token default may be visually significant (mention in release notes)
- New components must update self-documenting demo and parameter documentation
- Extensions should document which core tokens they consume and which local tokens they own
