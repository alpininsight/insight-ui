# Carousel Component (Version 0.1.0)

The carousel component cycles through cards or images with keyboard support, pagination dots, and optional autoplay.

## Usage

```django
{% load insight_tags %}
{% carousel carousel_items=carousel_items show_index=True slides_count=range_total_slides items_per_slide=2 %}
```

### Parameters
- **carousel_items** (`list`): data rendered inside each slide.
- **show_index** (`bool`): display the current slide index.
- **show_dots** (`bool`): render pagination dots below the content.
- **autoplay** (`bool`): automatically advance slides.
- **slides_count** (`range`/`iterable`): number of slides.
- **items_per_slide** (`int`): number of items shown per slide.

## Templates
- `components/carousel.html` – base layout.
- `components/carousels/card_carousel.html` – renders cards inside slides.
- `components/carousels/image_carousel.html` – image-focused variant.

## Demo Data

See `get_card_carousel_context()` and `get_image_carousel_context()` in `insight_ui/demo_context.py` for sample payloads using Tailwind cards and Picsum images.

## Accessibility

- Includes keyboard navigation and focus trapping for controls.
- Uses aria attributes to describe slide positions.

## Related Components
- [Card](card.md)
- [Image carousel demo](../guides/customization.md)
