# Popover Component (Version 0.1.0)

The popover component displays contextual information anchored to a trigger element.

## Usage

```django
{% load insight_tags %}
{% include "insight_ui/components/popover.html" with popover_id="details" trigger_text="Details" content=popover_html %}
```

### Parameters
- `popover_id`: unique DOM ID for the popover container.
- `trigger_text`: button label that toggles the popover.
- `content`: HTML content inside the popover.
- Optional kwargs like `position` can be supplied via `options`.

## Accessibility
- Uses ARIA attributes to label the popover and tie it to the trigger.
- Focus remains on the trigger while the popover is open; ensure keyboard shortcuts close it.

## Customisation
- Override `components/popover.html` to adjust transition effects or layout.
- Tailwind classes control spacing and colours.

## Related Components
- [Tooltip](tooltip.en.md)
- [Modal](modal.en.md)
