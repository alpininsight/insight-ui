# Alert Component (Version 0.1.0)

The alert component displays dismissible status messages in four variants: `info`, `success`, `warning`, and `error`.

## Usage

```django
{% load insight_tags %}
{% alert message="All data saved" type="success" dismissible=True %}
```

### Parameters
- **message** (`str`): text displayed inside the banner.
- **type** (`str`): one of `info`, `success`, `warning`, `error` (defaults to `info`).
- **dismissible** (`bool`): show a close button when `True` (defaults to `True`).

## Styling

The component relies on theme tokens defined in `insight_ui/utils/input.css`. Each variant has its own colour pairing to ensure readable contrast in light and dark mode.

## Accessibility

- Uses `role="alert"` so screen readers announce messages immediately.
- The dismiss button is keyboard-accessible and exposes an `aria-label`.

## Related Templates
- `insight_ui/templates/insight_ui/components/alert.html`
- Inclusion tag: `alert` in `insight_ui/templatetags/insight_tags.py`
- Demo context: see `get_alert_context` inside `insight_ui/demo_context.py`

## Related Components
- [Navbar](navbar.md) – alerts often pair with global navigation
- [Infinite Scroll](infinite_scroll.md) – to display load status
