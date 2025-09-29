# Card Component (Version 0.1.0)

Cards present grouped information such as titles, subtitles, media, and action buttons.

## Usage

```django
{% load insight_tags %}
{% card title="Project" subtitle="Active" content="Short summary" %}
```

### Parameters
- **title** (`str`): main headline.
- **subtitle** (`str`, optional): secondary text.
- **content** (`str`): body copy.
- **image** (`dict`, optional): `{ "url": "...", "alt": "..." }`.
- **actions** (`list`, optional): list of button dictionaries (text, url, type).

## Variants

Additional layouts exist in `components/cards/`:
- `card.html` – vertical layout with optional image.
- `horizontale_card.html` – horizontal layout.
- `flip_card.html` – card with front/back content.

## Customisation

Override the specific card template or create a new component extending `insight_ui/components/cards/_base.html` (if present). Tailwind utility classes control spacing and theme tokens.

## Related Components
- [Bullet point list](bullet_point_list.md)
- [Carousel](carousel.md)
