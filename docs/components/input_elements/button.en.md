# Button Component (Version 0.1.0)

Insight UI provides Tailwind-based button styles that keep call-to-action elements consistent across the project. Buttons are defined via component utilities rather than inline classes, which means you can use short class names like `btn`, `btn-primary`, `btn-secondary`, etc.

## Usage

```django
<button class="btn btn-primary" type="submit">
    {% trans "Save changes" %}
</button>
```

Additional variations:

- `btn-secondary` – neutral background
- `btn-outlined` – transparent background with border
- `btn-small` / `btn-large` – size modifiers
- `btn-icon` – space optimised button for icon-only actions

These classes are defined in `insight_ui/utils/input.css` inside the `@layer components` block. Adjust the tokens in that file to change colours or spacing.

## Accessibility Tips

- Always use descriptive button text or add `aria-label` when the button only contains an icon.
- Ensure the button remains reachable via keyboard (all default styles preserve focus outlines).
- Prefer `<button>` elements over clickable `<div>`s to get correct semantics automatically.

## Related Components

- [Alert banner](../alert.en.md)
- [Modal](../modal.en.md)
