# Radio Button Component (Version 0.1.0)

The radio button partial provides consistent styling for grouped radio inputs.

## Usage

```django
{% load insight_tags %}
{% include "insight_ui/components/input_elements/radio_button.html" with field=radio_field %}
```

`radio_field` can be a Django form field or a custom dictionary matching the structure used in `demo_context.py`.

## Features
- Accessible markup with labels and focus styles
- Works with HTMX and traditional form submissions
- Theme colours pulled from Tailwind tokens

## Customisation
- Override `components/input_elements/radio_button.html` to modify layout or add hints.

## Related Inputs
- [Checkbox](checkbox.en.md)
- [Toggle button](toggle_button.en.md)
