# Naming Conventions (Version 0.1.0)

This guide documents the naming rules that keep Insight UI consistent across Python, templates, and assets. Please follow them when adding new components or demos.

## Python Modules & Functions
- Modules and packages use `snake_case` (`insight_ui/templatetags/insight_tags.py`).
- Public functions and variables also use `snake_case`; classes are written in `PascalCase`.
- Keep template tags descriptive: `navbar`, `infinite_scroll`, `toggle_view`.
- Tests belong in `test_*.py` files inside the component’s app (`insight_ui/tests/test_template_tags.py`).

## Templates
- Component templates live in `templates/insight_ui/components/` and use `snake_case` names, e.g. `image_carousel.html` or `navbar.html`.
- Variants are stored in subfolders: `components/cards/card.html`, `components/carousels/image_carousel.html`.
- Every template that renders a component must accept a context dictionary named after the component (`carousel_items`, `sidebar_data`).

## Static Assets
- CSS/JS file names follow `kebab-case`: `static/insight_ui/js/sidebar.js`, `static/insight_ui/css/tailwind.css`.
- Images and SVGs use `kebab-case` as well (`static/insight_ui/svg/logo.svg`).
- Bundle component-specific assets inside a folder that mirrors the template (`static/insight_ui/js/carousel/…`).

## Demo Data & Context Helpers
- Demo context helpers reside in `insight_ui/demo_context.py`. Use the prefix `get_…_context` (for example `get_image_carousel_context`).
- Utility functions that map data to demo payloads live in `insight_ui/demo_utils.py`.

## Translation Keys & Text
- Wrap user-facing strings with `gettext` (`_()`) in Python or `{% trans %}` in templates.
- Use dotted keys when you need explicit translation identifiers: `_(
"insight_ui.components.carousel.caption")`.

## File Prefix Summary
- `get_…_context` – demo context helpers.
- `*_detailpage.html` – documentation partials for the MkDocs site.
- `test_*.py` – component tests.
- `*_storyboard` / `storybook_view` params – used for linking to documentation views.

Following these conventions keeps new contributions predictable and makes it easy to spot regressions during reviews.
