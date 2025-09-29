# Infinite Scroll Component (Version 0.1.0)

The infinite scroll component loads additional list entries on demand instead of forcing people to step through numbered pages. When the visitor reaches a configured threshold near the bottom, HTMX fetches the next chunk from the backend and appends it to the list.

## Usage

```django
{% load insight_tags %}
{% infinite_scroll items=scroll_items view_name="more_items" %}
```

Integrate the inclusion tag inside any list or card view. Combine it with HTMX endpoints that return partial markup.

## Parameters

- **items** (`list`): already loaded entries that should be rendered initially.
- **view_name** (`str`): Django URL pattern name used to fetch additional data (legacy alias `request_view` is still accepted).
- **page** (`int`, optional): current page index that will be sent to the backend (defaults to `1`).
- **has_next** (`bool`, optional): set to `False` when no further results exist to hide the loader/button.
- **auto_fetch** (`bool`, optional): switch to `False` to render a “Load more” button instead of automatic fetching.
- **threshold** (`int`, optional): pixel offset before the bottom at which the next request is triggered (defaults to `100`).

Any additional keyword arguments are passed to the template via the `options` dictionary.

## Related Components

- [Pagination](pagination.md) – traditional numbered navigation.
- [Live Content](live_content.md) – periodic updates via HTMX polling.

## Implementation Notes

- Template: `insight_ui/templates/insight_ui/components/infinite_scroll.html`
- Template tag: `infinite_scroll` in `insight_ui/templatetags/insight_tags.py`
- Demo context: see `get_infinite_scroll_context()` in `insight_ui/demo_context.py`
