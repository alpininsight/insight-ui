# Base Template (Version 0.1.0)

The base template acts as the skeleton for every page that uses Insight UI. It wires up the header, footer, skip links, HTMX configuration, and theme toggling. Extend it as follows:

```django
{% extends "insight_ui/base.html" %}
```

## Blocks Provided

- `title` – page title (wrapped with `{% trans %}` in examples).
- `navbar` – navigation bar section, defaults to the Insight UI navbar.
- `content` – main content area.
- `footer` – footer section.

You can override these blocks to inject custom components.

## Context Requirements

To populate the default navbar and footer, pass the corresponding context dictionaries:

```python
from insight_ui.demo_context import get_navbar_context, get_footer_context

def view(request):
    context = {}
    context |= get_navbar_context()
    context |= get_footer_context()
    return render(request, "my_template.html", context)
```

Feel free to swap in your own data sources.

## Customisation

- Override specific components by copying the template files into `templates/insight_ui/...` inside your project.
- Extend Tailwind tokens in `insight_ui/utils/input.css` to align branding.

## Related Links

- [Navbar component](components/navbar.en.md)
- [Footer component](components/footer.en.md)
- [Naming conventions](guides/naming_conventions.en.md)
