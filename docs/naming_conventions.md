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

## Data-Attributs (HTML)

### Component identification
Each JavaScript component is identified by a `data-*` attribute in the HTML:

| Component | Main-Attribute | Example |
|------------|----------------|----------|
| `accordion` | `data-accordion` | `<div data-accordion="faq-group">` |
| `dropdown` | `data-dropdown-toggle` | `<button data-dropdown-toggle="menu-id">` |
| `modal` | `data-insight-toggle="modal"` | `<button data-insight-toggle="modal">` |
| `tabs` | `data-tabs` | `<div data-tabs>` |
| ... |

### Component options
Optional settings use the schema `data-{component}-{option}`:

```html
<!-- Accordion with exclusive mode -->
<div data-accordion="faq" data-accordion-exclusive="true">

<!-- 3D carousel with camera alignment -->
<div data-3D-carousel="gallery" data-carousel-face-camera="true" data-carousel-velocity="500">
```

### Action attributes
The following patterns are used for user interactions:

| Action | Attribute | Usage |
|--------|----------|------------|
| Close/Dismiss | `data-insight-dismiss="{type}"` | `data-insight-dismiss="alert"`, `data-insight-dismiss="modal"` |
| Toggle | `data-insight-toggle="{type}"` | `data-insight-toggle="modal"` |
| Target-Reference | `data-insight-target="{id}"` | `data-insight-target="modal-1"` |
| Callback | `data-radio-callback="{fn}"` | `data-radio-callback="onSelect"` |
| ... |

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
