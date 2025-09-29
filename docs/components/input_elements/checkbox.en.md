# Checkbox Component (Version 0.1.0)

The checkbox component standardises the look of boolean inputs, including label placement and focus styling.

## Usage

```django
{% include "insight_ui/components/input_elements/checkbox.html" with field=checkbox_field %}
```

`checkbox_field` can be a Django form field or a dictionary with the following keys:

```python
checkbox_field = {
    "id": "accept_terms",
    "label": "I agree to the terms",
    "checked": False,
    "help_text": "You must accept before continuing.",
}
```

## Features
- Works seamlessly with Django forms (rendered via `{{ form.accept_terms }}`)
- Supports optional helper text and error messages
- Styled focus ring and hover states driven by Tailwind tokens

## Accessibility
- Labels are associated via `for` / `id` attributes.
- Keep helper text concise and ensure error messages are announced alongside the control.

## Related Inputs
- [Radio button](radio_button.en.md)
- [Toggle button](toggle_button.en.md)
