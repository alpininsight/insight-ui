# Pagination Component (Version 0.1.0)

The pagination component renders numbered page navigation with previous/next controls.

## Usage

```django
{% load insight_tags %}
{% pagination page=pagination_page page_links=page_links request_view="pagination_view" %}
```

- `pagination_page`: Django `Page` instance.
- `page_links`: list produced by `get_page()` in `insight_ui/utils/pagination.py`.
- `request_view`: URL name used for HTMX requests.

## Customisation
- Override `components/pagination.html` to change the layout or icons.
- Combine with `generic_filter` or `infinite_scroll` when switching UX patterns.

## Related Guides
- [Infinite Scroll](infinite_scroll.en.md)
- [Generic filter](generic_filter.en.md)
