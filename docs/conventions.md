# Conventions

This guide documents the naming conventions that keep Insight UI consistent across Python, templates, and assets.

## Python

- Follow standard Python naming conventions (PEP 8)
- Components and template tags use concise names: `navbar`, `sidebar`, `accordion`
- Test files are in `tests/` and start with `test_`, e.g., `test_template_tags.py`

## Templates

- Component templates are in `templates/insight_ui/components/` using `snake_case`:
  - `image_carousel.html`
  - `navbar.html`
- Variants go in subdirectories:
  - `components/cards/card.html`
  - `components/cards/app_card.html`
- Context dictionaries match component names: `carousel_items`, `sidebar_data`

## Static Assets

- CSS/JS files use `kebab-case`: `insight-ui-sidebar.js`
- Images and SVGs also use `kebab-case`: `favicon-16x16.png`

## CSS Classes

Tailwind CSS is the default styling implementation, but public component markup should prefer stable Insight UI class names.

Use the `insight-*` prefix for stable classes:

| Pattern | Use For | Example |
|---------|---------|---------|
| `insight-surface-*` | Reusable surfaces and containers | `insight-surface-card` |
| `insight-layout-*` | Shared layout regions | `insight-layout-content` |
| `insight-component-*` | Component-specific structure | `insight-component-sidebar` |
| `insight-state-*` | Semantic state styling | `insight-state-disabled` |
| `insight-doc-*` | Documentation surfaces | `insight-doc-demo` |

### When to Create a Semantic Class

| Tailwind Pattern | Create Semantic Class When |
|-----------------|---------------------------|
| `bg-*`, `border`, `rounded`, `shadow` together | Reusable container (cards, panels, modals) |
| `flex`, `grid`, `gap-*` as repeated pattern | Shared layout primitive |
| `hover:*`, `active:*`, `focus:*`, `disabled:*` | Semantic public behavior (selected, disabled, open) |
| Documentation chrome | Self-documentation structures |

Do not add a semantic class for every Tailwind utility. Add one only when it names a reusable design concept.

## Data Attributes

### Component Identification

Each JavaScript component is identified by `data-insight-{component_name}`:

```html
<div data-insight-accordion="accordion-container-id">
<button data-insight-dropdown="menu-container-id">
<button data-insight-modal="modal-container-id">
```

### Component Options

Additional options use `data-{option}` without repeating the component name:

```html
<!-- Accordion with exclusive mode -->
<div data-insight-accordion="faq" data-exclusive="true">

<!-- 3D carousel with options -->
<div data-insight-3D-carousel="gallery" data-face-camera="true" data-velocity="500">
```

### Action Attributes

| Action | Attribute | Example |
|--------|-----------|---------|
| Close/Dismiss | `data-insight-dismiss="{type}"` | `data-insight-dismiss="modal"` |
| Callback | `data-radio-callback="{fn}"` | `data-radio-callback="onSelect"` |

### Boolean Attributes

Write HTML boolean attributes without a value:

```html
<!-- Correct -->
<input type="checkbox" checked disabled>

<!-- Wrong -->
<input type="checkbox" checked="true" disabled="true">
```

## Demo Data and Context Helpers

- Demo context functions follow `get_{component}_context` pattern
- Helper functions for data preparation are in `insight_ui/demo_utils.py`

## Translations

- User-relevant texts use `gettext` (`_()`) in Python or `{% trans %}` in templates
- Explicit keys use dot notation: `_("insight_ui.components.carousel.caption")`
