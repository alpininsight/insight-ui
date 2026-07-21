# Brand Settings

Insight UI supports a central brand default in `settings.py`.

The goal is to avoid repeating the same brand mark, logo and footer text in every app while still keeping navigation and layout composition explicit.

## Settings Example

```python
from insight_ui.configs import BrandMarkConfig, LogoConfig

INSIGHT_UI = {
    "brand": {
        "home_url": "/",
        "mark": BrandMarkConfig(
            primary_text="Insight",
            secondary_text="UI",
            logo=LogoConfig(
                url="insight_ui/svg/ai-logo.svg",
                url_dark="insight_ui/svg/ai-logo.svg",
                alt="Insight UI Logo",
                height="2rem",
            ),
        ),
        "footer_text": "A modern, accessible, and responsive UI library for Django projects.",
    }
}
```

The navbar and footer defaults read the logo through `brand.mark.logo`.
Do not configure deprecated top-level brand keys such as `brand.logo` or
`brand.title` for navbar branding; those values are not used by the current
brand default builders.

## Rule

Use `settings.py` for stable brand defaults:

- home URL
- brand mark text
- logo asset through `brand.mark.logo`
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

Normal apps usually need one shared brand source for navbar, footer and login/status screens. Without this, `insight-ui-*` apps repeat brand mark text, logo paths and footer text in several places.

The central brand default solves that duplication without making Insight UI automatically render a full navbar or footer from settings. That would be too rigid because navigation, links and user menus are application-specific.
