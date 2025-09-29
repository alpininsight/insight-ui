# Step Bar Component (Version 0.1.0)

The step bar component visualises multi-step processes, such as onboarding flows or checkout pipelines.

## Usage

```django
{% load insight_tags %}
{% step_bar items=step_items %}
```

### Data Structure

```python
step_items = [
    {"title": "Account", "completed": True},
    {"title": "Billing", "completed": False},
    {"title": "Review", "completed": False},
]
```

Render additional metadata (e.g., links) by extending the template or augmenting each dictionary.

## Customisation
- Override `components/steps_bar.html` to change icons, progress indicators, or layout.
- Combine with `progressbar` for more granular completion signals.

## Related Components
- [Progress bar](progressbar.en.md)
- [Toggle view](toggle_view.en.md)
