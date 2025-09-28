# Search Bar Component (Version 0.1.0)

The search bar component renders a keyword input optimised for HTMX lookups.

## Usage

```django
{% load insight_tags %}
{% search_bar request_view="search_view" simple=True search_query=initial_query %}
```

### Parameters
- **request_view** (`str`): Django URL pattern used for the search request (required).
- **simple** (`bool`): toggles a simplified layout.
- **search_query** (`str`, optional): prefill the input value.

## HTMX Integration
- The template sets `hx-get` and `hx-target` so results can be rendered inline.
- Customize the target element via the `options` dictionary if needed.

## Accessibility
- Includes a proper label and supports keyboard submission.

## Related Components
- [Navbar](navbar.en.md) – includes an embedded search bar variant.
- [Generic filter](generic_filter.en.md)
