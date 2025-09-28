# Tooltip Component (Version 0.1.0)

The tooltip component shows additional information when users hover or focus on a trigger element.

## Usage

```django
{% include "insight_ui/components/tooltip.html" with tooltip_id="help" text="Need assistance?" %}
```

- `tooltip_id`: unique identifier for the tooltip.
- `text`: content displayed inside the tooltip.

## Accessibility
- Tooltips should also appear on focus to support keyboard navigation.
- Keep messages concise and supplement them with inline help when necessary.

## Customisation
- Override `components/tooltip.html` to change arrow styles or add icons.
- Tailwind classes can be adjusted to modify colours and spacing.

## Related Components
- [Popover](popover.en.md)
- [Alert banner](alert.en.md)
