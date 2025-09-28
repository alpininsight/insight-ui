# Differentiator Component (Version 0.1.0)

The differentiator component compares two versions of content side by side, similar to a diff view. It is useful for highlighting changes or differences between items.

## Usage

```django
{% load insight_tags %}
{% differentiator left=left_text right=right_text %}
```

### Parameters
- **left**: text or HTML displayed on the left.
- **right**: text or HTML displayed on the right.
- Optional keyword arguments are passed through to the template via `options`.

## Customisation

Adjust `components/differentiator.html` to change the layout, add icons, or modify styling. The component relies on Tailwind utilities for spacing and typography.

## Related Components
- [Code block](code_block.en.md)
- [Alert](alert.en.md)
