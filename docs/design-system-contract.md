# Design system contract

This document defines where Insight UI design-system decisions live and how reusable
theme contracts should evolve across the core package and sibling packages such as
`insight-ui-webgl`.

The goal is to keep the core package stable and reusable without turning it into a
collection of component-specific styling exceptions.

## Business perspective

The contract is not only a technical cleanup. It is a product and maintenance
boundary:

- Host applications can change brand, state, and domain visuals without forking
  components.
- Sibling packages can integrate with Insight UI without copying its templates or
  hardcoding unrelated colors.
- Reviewers can decide whether a new visual value is part of the public design
  API or only an implementation detail.
- Breaking visual changes become visible because public tokens and component
  contracts are named and documented.
- Customers get consistent behavior across 2D screens, 3D views, and future
  immersive interfaces.

The core package should therefore define the smallest stable language that many
consumers can share. Extensions should own fast-moving domain details until a
pattern is mature enough to promote into the core contract.

## Reading order

This document is intentionally ordered from the current system to future domains:

1. Where we are today: the current 2D contract and the files that already define
   the reusable design language.
2. 3D extension contract: which existing 2D concepts should carry into WebGL,
   graph, or model-viewer components.
3. Immersive-domain naming: how XR and AR concepts should be named without
   forcing runtime behavior into the core package.

3D and immersive packages should not invent a separate visual language first.
They should begin with the current 2D contract, reuse it where the concept is the
same, and add only the domain concepts that cannot be expressed with existing
tokens, templates, or behavior hooks.

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
| Reusable surfaces | component classes in `@layer components` | Containers, examples, inline tags, and forms share the same visual treatment. |

The preferred flow for a consumer project is:

1. Copy or provide a project-owned `input.css`.
2. Set the corporate identity in the `@theme` block.
3. Use Insight UI template tags and component classes as usual.
4. Override component templates only when structure, behavior, or component anatomy
   must change.

This keeps brand alignment centralized. A project can change its visual identity
without editing every button, form, heading, or documentation example.

## Where we are today: 2D

The normal 2D design system is the starting point before any 3D or immersive
extension is discussed. Insight UI already defines brand colors, status colors,
text hierarchy, reusable surfaces, base layout, documentation chrome, component
templates, JavaScript hooks, and accessibility contracts. The missing piece was
not a complete implementation, but an explicit source-of-truth document that
explains where those decisions belong.

### Current documentation map

| Topic | Documented? | Source |
|---|---:|---|
| `input.css` as Tailwind/theme source file | Yes | `insight_ui/templates/insight_ui/docs/customization.html:78` |
| `@theme` contains theme variables and colors | Yes | `insight_ui/templates/insight_ui/docs/customization.html:232` |
| `@layer base` defines HTML base styles | Yes | `insight_ui/templates/insight_ui/docs/customization.html:291` |
| `@layer components` defines reusable classes | Yes | `insight_ui/templates/insight_ui/docs/customization.html:301` |
| Brand, status, and text colors | Yes, in code | `insight_ui/utils/input.css:15` |
| Text helpers `.text-primary`, `.text-secondary`, `.text-link` | Yes, in code | `insight_ui/utils/input.css:85` |
| Button system | Yes, in code and partially in docs | `insight_ui/utils/input.css:96` |
| Standard surfaces `.component-container`, `.example-container`, `.info-container`, `.inline-tag` | Yes, in code | `insight_ui/utils/input.css:171` |
| Base layout: header, navbar, sidebars, content, footer | Yes, separately | `insight_ui/templates/insight_ui/base.html:62` |
| Demo container and self-documentation chrome | Yes, separately | `insight_ui/templates/insight_ui/docs/demo_container.html:3` |
| Clear taxonomy: `input.css` vs. templates vs. JavaScript | Now documented here | `docs/design-system-contract.md` |
| 2D to 3D theme contract mapping | Now documented here | `docs/design-system-contract.md` |

### Source of truth

| Concern | Source of truth | Rule |
|---|---|---|
| Theme tokens | `insight_ui/utils/input.css` in `@theme` | Add stable brand, semantic, text, surface, and official domain tokens here. |
| Base element styles | `insight_ui/utils/input.css` in `@layer base` | Use for generic HTML behavior such as headings, horizontal rules, and cursor behavior. |
| Reusable utility/component classes | `insight_ui/utils/input.css` in `@layer components` | Use for reusable classes such as `.btn`, `.input`, `.component-container`, or `.inline-tag`. |
| Component structure | `insight_ui/templates/insight_ui/components/` | Put semantic HTML, ARIA attributes, layout composition, and component anatomy here. |
| Page shell structure | `insight_ui/templates/insight_ui/base.html` | Owns header, navbar block, drawer block, sidebars, heading, content, and footer placement. |
| Self-documentation demos | `insight_ui/templates/insight_ui/docs/` and `insight_ui/component_details/` | Owns component examples, detail-page text, parameter docs, related components, and demo context. |
| Frontend behavior | `insight_ui/static/insight_ui/js/` | Owns initialization, state, keyboard handling, resize handling, and behavior attached to `data-*` attributes. |
| Template tag API | `insight_ui/templatetags/insight_tags.py` | Owns reusable Django-facing component APIs and context normalization. |
| Extension-specific components | Sibling package, for example `insight-ui-webgl` | Owns domain-specific components, Three.js/WebGL code, and component-specific tokens. |

Do not use generated CSS as the design-system source. The built stylesheet under
`insight_ui/static/insight_ui/css/` is output, not the design contract.

### Existing 2D design concepts

These concepts already exist in Insight UI and form the baseline for future domains
such as 3D, WebGL, graph visualization, or model viewers.

| 2D concept | Current representation | Design meaning |
|---|---|---|
| Brand colors | `--color-insight-primary`, `--color-insight-secondary` | Main product actions and secondary accents. |
| Interaction variants | `*-hover`, `*-active` color tokens | Pointer and pressed states for interactive elements. |
| Status colors | `success`, `warning`, `danger`, `info` tokens | Semantic user feedback and system state. |
| Text hierarchy | `text-primary`, `text-secondary`, `text-link` | Primary content, secondary content, and navigable text. |
| Dark mode | `@custom-variant dark` and dark text tokens | Theme-aware rendering via `data-theme=dark`. |
| Surfaces | `.component-container`, `.example-container`, cards, panels, modal body | Visual containers that separate content from the page background. |
| Page background | `body` classes in `base.html` | Global application background and text baseline. |
| Borders | `border-gray-*`, accent borders, component borders | Separation, grouping, and hierarchy. |
| Elevation | `shadow`, `shadow-md`, `shadow-lg`, modal shadows | Visual stacking and object prominence. |
| Radius | `rounded-sm`, `rounded`, `rounded-lg` | Component shape and perceived density. |
| Spacing and sizing | Tailwind utilities in templates | Component rhythm, density, and responsive layout. |
| Focus state | `focus:ring-*`, `focus-visible:*`, outline utilities | Keyboard discoverability and accessibility. |
| Disabled state | `.btn-disabled`, disabled form controls | Unavailable actions or muted objects. |
| Layout hierarchy | navbar, sidebars, heading, content, footer, drawer blocks | Page shell and navigation structure. |
| Overlay hierarchy | modal backdrop, sidebar backdrop, z-index utilities | Layering for temporary UI and blocking interactions. |
| Documentation surfaces | code block, inline tag, demo container | Self-documentation chrome and examples. |
| Responsive behavior | Tailwind breakpoints and component template branches | Viewport-specific layout changes. |
| Directionality | RTL-aware classes and CSS rules | Bidirectional layout support. |
| Data hooks | `data-insight-*` and component-specific `data-*` attributes | Stable JavaScript initialization and behavior contracts. |
| Accessibility hooks | ARIA attributes, semantic HTML, focus handling | WCAG-aligned component behavior. |

### Recommended target shape

Use this target shape when deciding where a design-system concept should live.

| Concept | Preferred home | Notes |
|---|---|---|
| Brand colors | `input.css` | Core public contract. |
| Status colors | `input.css` | Core public contract. |
| Text colors | `input.css` | Core public contract. |
| Typography | `input.css` | Core font and heading behavior. |
| Dark mode contract | `input.css` | Core theme variant and dark text/surface tokens. |
| Focus and interaction colors | `input.css`, then templates where structural | Stable colors belong in tokens; exact focus placement belongs in components. |
| Surfaces | Base in `input.css`, concrete surfaces in templates | Reusable container classes belong in CSS; component anatomy stays in templates. |
| Borders | Base in `input.css`, concrete borders in templates | Generic border semantics can become tokens; component-specific borders stay local. |
| Shadows and elevation | Prefer tokens/classes in `input.css` when standardized | Current usage is mostly Tailwind utilities in templates. Promote only repeated patterns. |
| Radius | Prefer tokens/classes in `input.css` when standardized | Current usage is mostly Tailwind utilities in templates. Promote only repeated patterns. |
| Spacing and sizing | Mostly templates and Tailwind utilities | Promote only repeated layout rhythm that should be public API. |
| Layout hierarchy | `base.html` | Page shell, optional blocks, and structural regions. |
| Modals and overlays | Component templates plus JavaScript | Templates own markup; JavaScript owns behavior and state. |
| Documentation and code surfaces | `input.css` plus docs templates | Shared classes in CSS, demo chrome in docs templates. |
| Responsive behavior | Templates plus Tailwind classes | Component-specific breakpoints stay in templates unless they become a public setting. |
| RTL and i18n behavior | Templates plus specific CSS rules | Keep text and direction decisions close to component markup. |
| JS hooks and data attributes | Templates plus JavaScript files | Markup declares stable hooks; JavaScript owns behavior. |
| Accessibility contracts | Templates, component-detail docs, tests | ARIA/focus semantics should be documented and tested with the component. |

## 3D extension contract

3D features should reuse the same design language where the concept is shared.
The core package should define only stable domain-level 3D tokens. Specific graph,
model-viewer, shader, material, or Three.js implementation details belong in the
extension package.

| Existing 2D concept | 3D/domain equivalent | Belongs in core? |
|---|---|---:|
| Page background | Scene or canvas background | Yes, if shared across 3D components. |
| Component surface | 3D panel, plane, label backing, inspector surface | Yes, as generic 3D surface tokens. |
| Border | Grid line, helper line, outline | Yes, for generic grid/reference lines. |
| Elevation | Depth shadow, ambient separation, object prominence | Usually extension-specific unless abstracted as a shared surface rule. |
| Primary color | Selection, active object, primary highlight | Yes. |
| Secondary color | Secondary highlight, helper object | Yes. |
| Text primary | 3D label primary text | Yes. |
| Text secondary | Muted label/helper text | Yes. |
| Text link | Clickable annotation or linked label | Yes. |
| Success | Valid, healthy, completed object | Yes. |
| Warning | Near-threshold or caution object | Yes. |
| Danger | Error, critical object, threshold breach | Yes. |
| Info | Informational marker | Yes. |
| Focus | Keyboard target ring or accessible object outline | Yes, if represented in shared 3D controls. |
| Hover | Pointer hover outline or glow | Yes, as a semantic interaction token. |
| Disabled | Muted or unavailable object/material | Yes. |
| Modal overlay | Viewport overlay or scrim | Yes, if used across 3D viewports. |
| Graph node selected | Selected graph node material/emissive color | No, extension-specific. |
| GLTF wireframe | Model-viewer wireframe color | No, extension-specific. |
| Camera frustum | Debug/helper camera visualization | No, extension-specific. |
| Shader-specific material | Custom shader implementation detail | No, extension-specific. |

### Minimal 3D core contract

If Insight UI adopts an official 3D theme contract, keep the initial core set small:

```css
@theme {
    --color-insight-3d-bg: #1a1a2e;
    --color-insight-3d-surface: #111827;
    --color-insight-3d-surface-muted: #1f2937;
    --color-insight-3d-border: #374151;

    --color-insight-3d-text-primary: #ffffff;
    --color-insight-3d-text-secondary: #d1d5db;
    --color-insight-3d-text-link: var(--color-insight-text-link);

    --color-insight-3d-selection: var(--color-insight-primary);
    --color-insight-3d-hover: var(--color-insight-primary-hover);
    --color-insight-3d-active: var(--color-insight-primary-active);
    --color-insight-3d-focus: var(--color-insight-primary-hover);
    --color-insight-3d-disabled: #6b7280;

    --color-insight-3d-success: var(--color-insight-success);
    --color-insight-3d-warning: var(--color-insight-warning);
    --color-insight-3d-danger: var(--color-insight-danger);
    --color-insight-3d-info: var(--color-insight-info);

    --color-insight-3d-axis-x: #ff6b6b;
    --color-insight-3d-axis-y: #6bcf7f;
    --color-insight-3d-axis-z: #4fa3ff;
    --color-insight-3d-grid-line: #22223a;
    --color-insight-3d-grid-center: #444466;

    --color-insight-3d-annotation: #ffcc00;
    --color-insight-3d-threshold: var(--color-insight-danger);
}
```

Extensions should consume these with CSS variable fallbacks:

```css
color: var(--color-insight-3d-axis-x, #ff6b6b);
```

JavaScript renderers should resolve them from the root element:

```javascript
const axisX = getComputedStyle(document.documentElement)
    .getPropertyValue("--color-insight-3d-axis-x")
    .trim() || "#ff6b6b";
```

### Token naming conventions

Use semantic names. A token name should describe the role of the value, not the
current color.

Core token patterns:

```css
--color-insight-primary
--color-insight-danger
--color-insight-text-primary
```

Official domain token pattern:

```css
--color-insight-<domain>-<semantic-purpose>
```

For official 3D tokens, prefer `3d` as the domain because it describes the design
domain rather than the rendering technology:

```css
--color-insight-3d-bg
--color-insight-3d-surface
--color-insight-3d-border
--color-insight-3d-text-primary
--color-insight-3d-selection
--color-insight-3d-hover
--color-insight-3d-axis-x
--color-insight-3d-grid-line
--color-insight-3d-threshold
```

Extension-specific token pattern:

```css
--color-insight-<domain>-<component>-<semantic-purpose>
```

Examples:

```css
--color-insight-3d-graph-node
--color-insight-3d-graph-edge-highlight
--color-insight-3d-model-wireframe
--color-insight-3d-model-bounds
```

Avoid names tied to implementation internals unless the token intentionally belongs
to an extension:

```css
/* Avoid in insight-ui core */
--color-insight-3d-gltf-wireframe
--color-insight-3d-shader-fresnel
--color-insight-3d-camera-frustum
```

### Promotion rules for extension tokens

Start specific tokens in the extension package. Promote a token to Insight UI core
only when it has become a stable, reusable ecosystem concept.

A token belongs in `insight-ui` when most of these are true:

- It is useful across multiple components or sibling packages.
- It describes a design concept, not a renderer implementation detail.
- Host applications should be able to override it globally.
- The name and meaning are expected to remain stable.
- It maps cleanly to existing 2D design concepts.
- It can be documented as public API.

A token belongs in an extension package when most of these are true:

- It is used by one component family only.
- It depends on Three.js, WebGL, WebGPU, GLTF, camera helpers, shaders, or graph layout internals.
- It is likely to change while the component matures.
- It is not meaningful for non-3D or non-domain consumers.
- It can safely use a fallback when the host app does not define it.

## Immersive-domain naming

Use `xr` for immersive-domain naming unless the concept is strictly AR-only.
`xr` keeps the contract open for augmented reality, mixed reality, WebXR, camera
overlays, and future immersive surfaces without tying the core package to one
runtime.

Core should not define AR engine behavior, sensor logic, camera permissions,
hit-testing algorithms, WebXR session lifecycle, plane detection logic, or device
capability handling. Those belong in an extension package such as
`insight-ui-xr` or `insight-ui-ar`.

Core may define XR tokens only after they are stable, reusable, and useful across
several immersive components.

| XR/AR concept | Core token candidate? | Notes |
|---|---:|---|
| Overlay text | Yes | Maps to text hierarchy. |
| Overlay surface | Yes | Maps to component surfaces and panels. |
| Reticle / placement cursor | Yes, if used broadly | Maps to selection/focus. |
| Valid placement state | Yes | Should usually alias `success`. |
| Invalid placement state | Yes | Should usually alias `danger`. |
| Tracking warning state | Yes | Should usually alias `warning`. |
| Spatial anchor marker | Maybe | Promote only if multiple components share it. |
| Plane detection preview | Maybe | Promote only after the visual language stabilizes. |
| Measurement guide | Maybe | Promote only if reused across measurement and placement tools. |
| Safety boundary | Maybe | Likely extension-owned until several components share it. |
| Occlusion debug material | No | Renderer/debug implementation detail. |
| Camera permission UI | No | Component/runtime flow, not a theme token. |
| WebXR session state | No | JavaScript behavior. |
| Device capability fallback | No | Extension behavior and user messaging. |

Potential future XR token names:

```css
--color-insight-xr-overlay-surface
--color-insight-xr-overlay-text-primary
--color-insight-xr-overlay-text-secondary
--color-insight-xr-reticle
--color-insight-xr-reticle-valid
--color-insight-xr-reticle-invalid
--color-insight-xr-tracking-limited
--color-insight-xr-anchor
--color-insight-xr-plane
--color-insight-xr-measurement
--color-insight-xr-boundary
```

Recommended aliases:

```css
--color-insight-xr-reticle-valid: var(--color-insight-success);
--color-insight-xr-reticle-invalid: var(--color-insight-danger);
--color-insight-xr-tracking-limited: var(--color-insight-warning);
```

XR and AR components also need non-color contracts:

- Permission and unsupported-device messaging.
- Reduced-motion behavior.
- Minimum target sizes for touch and gaze interactions.
- Contrast against unpredictable camera backgrounds.
- Tracking-lost and tracking-limited states.
- Safe fallbacks for non-XR browsers.
- Clear ownership of units, for example meters vs. application units.
- Separation between camera feed, overlay UI, and rendered objects.

These are component and runtime contracts, not just CSS tokens.

## Decision checklist

Before adding a new design value, answer these questions:

1. Is this a stable design concept or a component implementation detail?
2. Should downstream apps override it globally?
3. Does it map to an existing 2D concept?
4. Will more than one component or extension use it?
5. Does it need a documented public API name?
6. Does it require JavaScript behavior, or is it purely a token/style concern?

Use the answers to place the change:

- Stable theme contract: `insight_ui/utils/input.css`
- Semantic component structure: component template
- Behavior and state: JavaScript module
- Django API normalization: template tag
- Extension-specific domain behavior: sibling package

## Maintenance expectations

- Adding a core token is a public API addition and should be documented.
- Renaming or removing a core token is a breaking change.
- Changing a token default may be visually significant and should be mentioned in release notes.
- New visual components should update their self-documenting demo and parameter documentation.
- Extension packages should document which core tokens they consume and which local tokens they own.
