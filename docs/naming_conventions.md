# Naming conventions

This guide documents the naming conventions that keep Insight UI consistent across Python, templates, and assets. Please adhere to these guidelines when extending components or demos.

## Python modules & functions
- Python methods, classes, etc. are named according to standard Python convention.
- Components/template tags should have concise and appropriate names e.g. `navbar`, `sidebar`, `accordion`.
- Files for testing are located in the `tests/` directory. They start with `test` and a name appropriate to the tests they contain, e.g. `test_*.py`.

## Templates
- Component templates are located under `templates/insight_ui/components/` and use `snake_case`, e.g. `image_carousel.html` or `navbar.html`.
- Variants are stored in subdirectories: `components/cards/card.html`, `components/cards/app_card.html`, etc..
- Each component template expects a context dictionary whose name corresponds to the component (`carousel_items`, `sidebar_data`).

## Static assets
- CSS/JS files use `kebab-case`: `insight-ui-sidebar.js`.
- Images and SVGs also follow `kebab case`: `favicon-16X16.png`.

## CSS classes and design semantics

Tailwind CSS is the default styling implementation, but the public design
contract should stay semantic. New reusable component markup should prefer stable
Insight UI class names when the concept is part of the component contract.
Tailwind utility classes may still be used inside the default implementation and
for local, non-contract layout details.

Use the `insight-*` prefix for stable classes that describe Insight UI concepts:

| Pattern | Use for | Example |
|---|---|---|
| `insight-surface-*` | Reusable surfaces and containers | `insight-surface-card` |
| `insight-layout-*` | Shared layout regions or layout primitives | `insight-layout-content` |
| `insight-component-*` | Component-specific stable structure | `insight-component-sidebar` |
| `insight-state-*` | Semantic state styling | `insight-state-disabled` |
| `insight-doc-*` | Self-documentation surfaces and examples | `insight-doc-demo` |
| `insight-border-*` | Themeable semantic border colors | `insight-border-surface` |
| `insight-shadow-*` | Themeable semantic elevation and offsets | `insight-shadow-surface` |

Use this mapping when deciding whether repeated Tailwind utility usage should
become a semantic Insight UI class:

| Tailwind-oriented concept | Prefer semantic class when shared | Notes |
|---|---|---|
| `bg-*`, `dark:bg-*`, `border`, `rounded`, `shadow` used together for a reusable container | `insight-surface-*`, `insight-border-*`, `insight-shadow-*` | Use for cards, panels, modal bodies, docs examples, and other named surfaces. |
| `flex`, `grid`, `gap-*`, `space-*`, `px-*`, `py-*` used as a repeated structural pattern | `insight-layout-*` | Use for shared layout primitives. Keep one-off alignment utilities local. |
| Component root classes mixed with repeated spacing, border, and state utilities | `insight-component-*` | Use when the class describes stable component anatomy, not just visual decoration. |
| `hover:*`, `active:*`, `focus:*`, `disabled:*`, `aria-*`, or state-specific variants | `insight-state-*` | Use when the state is a semantic public behavior such as selected, disabled, open, or invalid. |
| Documentation/demo chrome such as examples, code areas, or demo wrappers | `insight-doc-*` | Use for self-documentation structures that should stay consistent across demos. |
| Brand, status, or text colors such as `text-insight-*`, `bg-insight-*`, `border-insight-*` | Token plus semantic class | Keep the token in `input.css`; add a class only when the usage pattern is repeated. |

Do not add a semantic class for every Tailwind utility. Add one only when it
names a reusable design or component concept that should survive a future styling
implementation change.

## Data-Attributs (HTML)

### Component identification
Each JavaScript component is identified by a `data-insight-{component_name}` attribute in the HTML. The value of this attribute is the `id` of the target HTML element, if necessary.

| Component | Main-Attribute | Example |
|------------|----------------|----------|
| `accordion` | `data-insight-accordion` | `<div data-insight-accordion="accordion-container-id">` |
| `dropdown` | `data-insight-dropdown` | `<button data-insight-dropdown="menu-container-id">` |
| `modal` | `data-insight-modal="modal"` | `<button data-insight-modal="modal-container-id">` |
| `tabs` | `data-insight-tabs` | `<div data-insight-tabs="tabs-container-id">` |
| ... |

### Component options
Additional attributes do not repeat he component name. Optional settings use the schema `data-{option}`:

```html
<!-- Accordion with exclusive mode -->
<div data-insight-accordion="faq" data-exclusive="true">

<!-- 3D carousel with camera alignment -->
<div data-insight-3D-carousel="gallery" data-face-camera="true" data-velocity="500">
```

### Action attributes
The following patterns are used for user interactions across components:

| Action | Attribute | Usage |
|--------|----------|------------|
| Close/Dismiss | `data-insight-dismiss="{type}"` | `data-insight-dismiss="alert"`, `data-insight-dismiss="modal"` |
| Callback | `data-radio-callback="{fn}"` | `data-radio-callback="onSelect"` |
| ... |

### JavaScript consumers of data-insight hooks

Every documented `data-insight-*` hook must have one owning JavaScript module or
one explicit delegated handler. If a hook changes, update the owning module, the
template that emits the hook, the component self-documentation, and this table.

| Hook | Owner | Notes |
|---|---|---|
| `data-insight-accordion` | `insight-ui-accordion.js` | Initializes accordion groups and reads `data-exclusive`. |
| `data-insight-carousel` | `insight-ui-carousel.js` | Initializes carousel controls and track behavior. |
| `data-insight-checkbox-group` | `insight-ui-checkbox.js` | Handles grouped checkbox behavior. |
| `data-insight-code-block` | `insight-ui-code-block.js` | Enhances code blocks and reads optional `data-filename`. |
| `data-insight-collapsible` | `insight-ui-collapsible.js` | Connects a trigger with a collapsible target. |
| `data-insight-demo-container`, `data-insight-demo-iframe` | `insight-ui-demo-container.js` | Controls docs demo iframe viewport sizing. |
| `data-insight-dropdown` | `insight-ui-dropdown.js` | Connects dropdown triggers with menu targets. |
| `data-insight-modal` | `insight-ui-modal.js` | Connects modal triggers with modal targets. |
| `data-insight-multiselect` | `insight-ui-multiselect.js` | Initializes multiselect combobox behavior. |
| `data-insight-popover`, `data-insight-tooltip` | `insight-ui-floater.js` | Creates floating popover and tooltip behavior. |
| `data-insight-sidebar` | `insight-ui-sidebar.js` | Initializes sidebar wrappers and side-specific controls. |
| `data-insight-tabs` | `insight-ui-tabs.js` | Initializes tab list, tab panel, and optional HTMX behavior. |
| `data-insight-theme-toggle` | `insight-ui-theme-toggle.js` | Handles theme switching. |
| `data-insight-3D-carousel` | `insight-ui-3D-carousel.js` | Initializes 3D carousel behavior and reads 3D options such as `data-face-camera` and `data-velocity`. |
| `data-insight-websocket`, `data-insight-websocket-status` | `insight-ui-websocket.js` | Bridges HTMX WebSocket events to status text and custom DOM events. |
| `data-insight-dismiss` | `insight-ui-modal.js`, `insight-ui-sidebar.js`, `insight-ui-utils.js` | Dismissal is scoped by value, for example `modal`, `sidebar`, `alert`, or `form-errors`. |

### Boolean attributes
HTML Boolean attributes should be written without a value:

```html
<!-- Correct -->
<input type="checkbox" checked disabled>

<!-- Wrong -->
<input type="checkbox" checked="true" disabled="true">
```

## Demo data & context helpers
- Demo context functions always have the same structure `get_{component}_context` (e.g., `get_accordion_context`).
- Helper functions for data preparation are located in `insight_ui/demo_utils.py`.

## Translations & Texts
- User-relevant texts are encapsulated in Python with `gettext` (`_()`) or in templates with `{% trans %}`.
- Explicit keys use the dot style: `_(“insight_ui.components.carousel.caption”)`.

Compliance with these conventions ensures that contributions can be checked and maintained more easily.
