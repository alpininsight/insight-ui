# Template Tags (Version 0.1.0)

Insight UI exposes a collection of inclusion tags that render ready-made components. The most common ones live in `insight_ui/templatetags/insight_tags.py`.

| Tag | Purpose | Template |
| --- | --- | --- |
| `navbar` | Navigation bar with branding, links and user menu | `components/navbar.html` |
| `footer` | Page footer with link columns | `components/footer.html` |
| `alert` | Message banner supporting `info`, `success`, `warning`, `error` | `components/alert.html` |
| `infinite_scroll` | HTMX-powered infinite scroll container | `components/infinite_scroll.html` |
| `sidebar` | Secondary navigation with grouped categories | `components/sidebar.html` |

Each inclusion tag returns a dictionary whose keys map directly to the template variables.

## Creating Your Own Tags
1. Add a function to `insight_ui/templatetags/insight_tags.py` and decorate it with `@register.inclusion_tag`.
2. Place the corresponding template under `templates/insight_ui/components/`.
3. Optionally add demo data in `insight_ui/demo_context.py` so the documentation site can showcase the component.

Check the component documentation for concrete examples.
