# Customisation (Version 0.1.0)

Insight UI is designed as a starting point that you can tailor to your product. This guide explains the main extension points.

## Configure via `settings.py`

Set global defaults in the `INSIGHT_UI` dictionary (see the overview page for the full example). Typical tweaks include the default theme variant, favicons, and SEO metadata.

## Tailwind Theme

Insight UI ships with a Tailwind input file at `insight_ui/utils/input.css`. Tailor it as follows:

1. **Sources** – ensure `@source "../templates/insight_ui/";` covers any additional template directories you introduce.
2. **Colour and typography tokens** – customise the `@theme` block and override variables such as `--color-insight-primary` or `--font-sans`.
3. **Base layer** – adjust `@layer base` rules to change the default appearance of headings, buttons, and form controls.
4. **Component shortcuts** – define reusable utility classes inside `@layer components` (e.g. `.btn`, `.btn-primary`).

If you need additional fonts, declare them with `@font-face` and reference them in the theme block.

## Overriding Templates

Every component template can be overridden by placing a file with the same path inside your project:

```
myapp/
  templates/
    insight_ui/
      components/
        navbar.html  # overrides the default navbar template
```

You can copy the original template from the package, adjust the markup, and extend it with custom blocks or Tailwind classes.

## Extending Components

- Create new Django inclusion tags in `insight_ui/templatetags/insight_tags.py`.
- Reuse the helper functions in `insight_ui/demo_utils.py` and `insight_ui/demo_context.py` to supply demo data.
- Add documentation partials in `insight_ui/templates/insight_ui/docs/partial/` so the component showroom reflects your changes.

## Dark Mode & Variants

Insight UI uses the `data-theme` attribute to switch between light and dark palettes. When you introduce new components, ensure the theme variables provide adequate contrast in both modes.

## Further Reading

- [Naming Conventions](naming_conventions.md)
- [Contributor Guide](../contributing.md)
