# Range Slider Component (Version 0.1.0)

The range slider component styles HTML `<input type="range">` controls with Insight UI tokens.

## Usage

```django
{% include "insight_ui/components/input_elements/range_slider.html" with field=range_field %}
```

Set `range_field` to a Django form field or dictionary containing `id`, `label`, `min`, `max`, and `value`.

## Features
- Displays current value beside the slider
- Supports customised min/max steps
- Theme-aware styling for light/dark mode

## Customisation
Override `components/input_elements/range_slider.html` to add tick marks or tooltips.

## Related Inputs
- [Slider toggle](toggle_button.en.md)
- [Radio button](radio_button.en.md)
