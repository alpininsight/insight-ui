# Toggle Button Component (Version 0.1.0)

The toggle button component represents binary states (on/off) with accessible styling.

## Usage

```django
{% include "insight_ui/components/input_elements/toggle_button.html" with field=toggle_field %}
```

`toggle_field` should provide `id`, `label`, and `checked` information (either via a Django form field or a dictionary).

## Features
- Keyboard-friendly toggle behaviour
- High-contrast focus and active states
- Supports helper text via optional context keys

## Customisation
- Override `components/input_elements/toggle_button.html` to adjust icons or animations.
- Combine with ARIA descriptions for more context.

## Related Inputs
- [Checkbox](checkbox.en.md)
- [Range slider](range_slider.en.md)
