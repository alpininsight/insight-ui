# Live Content Component (Version 0.1.0)

The live content component periodically refreshes a fragment using HTMX polling. It’s ideal for dashboards or status views that need frequent updates without full page reloads.

## Usage

```django
{% load insight_tags %}
{% live_content url="/api/live-data/" interval=5000 initial_content=initial_html %}
```

### Parameters
- **url**: endpoint that returns the updated HTML fragment (required).
- **interval**: polling interval in milliseconds; set to `0` to disable automatic polling.
- **initial_content**: HTML rendered before the first update (optional).
- **trigger**: custom HTMX trigger (defaults to `load, every {interval}s`).
- `**kwargs`: passed through to the template via `options`.

## Customisation
- Update `components/live_content.html` to change the wrapper or add loading indicators.
- Combine with ARIA live regions for screen-reader announcements.

## Related Components
- [Infinite Scroll](infinite_scroll.en.md)
- [Alert banner](alert.en.md)
