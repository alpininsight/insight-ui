# Brand Settings

Insight UI supports a central brand default in `settings.py`.

The goal is to avoid repeating the same title, logo and footer text in every app while still keeping navigation and layout composition explicit.

## Settings Example

```python
INSIGHT_UI = {
    "brand": {
        "title": "Insight UI",
        "home_url": "/",
        "logo": {
            "url": "insight_ui/svg/ai-logo.svg",
            "url_dark": "insight_ui/svg/ai-logo.svg",
            "alt": "Insight UI Logo",
            "height": "2rem",
        },
        "mark": None,
        "footer_text": "A modern, accessible, and responsive UI library for Django projects.",
    }
}
```

## Rule

Use `settings.py` for stable brand defaults:

- app title
- home URL
- logo asset
- optional brand mark
- footer description text

Use component configs for concrete app composition:

- navbar links
- dropdowns
- search
- login/user menu
- footer links
- contact links
- copyright and version information

Explicit component configuration always wins. Passing a custom `NavbarConfig(...)` or `FooterConfig(...)` still renders exactly that configuration.

## Why This Exists

Normal apps usually need one shared brand source for navbar, footer and login/status screens. Without this, `insight-ui-*` apps repeat logo paths, titles and footer text in several places.

The central brand default solves that duplication without making Insight UI automatically render a full navbar or footer from settings. That would be too rigid because navigation, links and user menus are application-specific.
