# Styling (Version 0.1.0)

Insight UI relies on Tailwind CSS as its design system. This guide summarises the key extension points so you can align the look and feel with your product.

## Theme Tokens

- Edit `insight_ui/utils/input.css` to override colours, typography, spacing, or animations.
- The `@theme` block defines CSS variables such as `--color-insight-primary` and `--font-sans`. Update them to adjust the global palette or font family.
- Use `@layer base` for defaults applied to native HTML elements (e.g. headings, buttons).

## Component Layers

Inside `@layer components` you can define reusable Tailwind shortcuts. Example:

```css
@layer components {
  .btn {
    @apply inline-flex items-center gap-2 rounded-sm border-2 px-5 py-1.5;
  }
  .btn-primary {
    @apply btn bg-insight-primary text-white hover:bg-insight-primary-hover;
  }
}
```

Use these classes in templates (`<button class="btn btn-primary">…</button>`).

## Dark Mode

Insight UI toggles light/dark mode via `data-theme`. Tailwind handles this through the custom variant defined in `input.css`:

```css
@custom-variant dark (&:where([data-theme=dark], [data-theme=dark] *));
```

Ensure any new colour tokens have suitable contrast for the dark variant.

## Overriding Templates

To change component markup, copy the original template into your project under `templates/insight_ui/...` and adjust it there. Example:

```
myapp/
  templates/
    insight_ui/
      components/
        navbar.html  # overrides the packaged navbar
```

## Asset Considerations

- Custom fonts can be declared with `@font-face` inside `input.css`.
- If Tailwind fails to include a class, make sure the template directory is listed in the `@source` directive.

## Related Guides

- [Customization](customization.en.md)
- [Naming Conventions](naming_conventions.en.md)
