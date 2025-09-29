# Progress Bar Component (Version 0.1.0)

The progress bar component visualises completion percentages using theme colours.

## Usage

```django
{% load insight_tags %}
{% progressbar value=65 label="Deployment progress" %}
```

### Parameters
- **value** (`int` or `float`): progress percentage (0–100).
- **label** (`str`, optional): text displayed alongside the bar.
- Additional kwargs are exposed via `options` (e.g., `variant="success"`).

## Accessibility
- Renders with `role="progressbar"` and sets `aria-valuenow`, `aria-valuemin`, `aria-valuemax`.
- Provide descriptive labels especially when multiple bars appear on one page.

## Customisation
- Override `components/progressbar.html` to change animations or add icons.

## Related Components
- [Step bar](step_bar.en.md)
- [Toggle view](toggle_view.en.md)
