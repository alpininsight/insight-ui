# Form Component (Version 0.1.0)

The form component showcases common form layouts and input patterns used throughout Insight UI.

## Usage

```django
{% load insight_tags %}
{% include "insight_ui/components/form.html" with fields=form_fields %}
```

`form_fields` is typically sourced from `get_form_context()` in `insight_ui/demo_context.py`.

## Features

- Demonstrates text inputs, selects, checkboxes, radio buttons, and validation states.
- Works with both Django forms and custom context dictionaries.
- Styled via the Tailwind theme defined in `insight_ui/utils/input.css`.

## Customisation

Copy `components/form.html` into your project under `templates/insight_ui/components/` and adjust the markup to fit your requirements. You can break the form into smaller partials or wire it to Django form objects directly.

## Related Components
- [Input elements overview](inputs.en.md)
- [Modal](modal.en.md)
- [Generic filter](generic_filter.en.md)
