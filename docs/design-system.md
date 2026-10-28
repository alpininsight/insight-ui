<!--
SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
SPDX-License-Identifier: AGPL-3.0-only
-->

# Public Design System Contract

[input.css](../insight_ui/utils/input.css) is the source for shared design tokens
and component styles. Generated
[tailwind.css](../insight_ui/static/insight_ui/css/tailwind.css) is output, not the
place to fix a design value. Tailwind implements the current styling system;
Insight UI's roles describe the design purpose.

## Existing Roles

Use the current names. The v1.15.1 family tokens `foreground` and `text` were
renamed, and the old `text` name changed meaning. Follow the two-pass replace
in [Migrating to 2.0](migration-2.0.md) before editing a host stylesheet:

| Purpose | Token source | Preferred class / use |
| --- | --- | --- |
| Page background | `--color-insight-bg-base` | `bg-insight-base` |
| Card/panel background | `--color-insight-bg-surface` | `bg-insight-surface` |
| Emphasized surface | `--color-insight-bg-raised` | `bg-insight-raised` |
| Overlay background | `--color-insight-bg-overlay` | `bg-insight-overlay` |
| Surface border | `--color-insight-border-surface` | `border-insight-surface` |
| Main content text | `--color-insight-text-body` | `text-insight-body` |
| Heading text | `--color-insight-text-headline` | `text-insight-headline` |
| Secondary content | `--color-insight-text-muted` | `text-insight-muted` |
| Semantic text/icon color | `--color-insight-primary-text` | `text-insight-primary-text` |
| Filled action background | `--color-insight-primary-action` | Prefer the existing primary button. |
| Text on the filled action | `--color-insight-primary-on-action` | Used together with its action background. |
| Link text | `--color-insight-text-link` | `text-insight-link` (with hover color and underline) |
| Reusable spacing | `--spacing-insight-m` | `p-insight-m`, `gap-insight-m` |
| Control radius | `--radius-insight-control` | `rounded-insight-control` |
| Surface radius | `--radius-insight-surface` | `rounded-insight-surface` |
| Surface shadow | `--shadow-insight-surface` | `shadow-insight-surface` |
| Overlay shadow | `--shadow-insight-overlay` | `shadow-insight-overlay` |

The background, border and text shorthands are defined with `@utility` in
`input.css`, so they work with variants (`hover:bg-insight-raised`,
`even:bg-insight-base`, `after:bg-insight-surface`) like any Tailwind utility.
Define new shorthands the same way: a plain class in `@layer utilities` gets no
variants, and the variant class silently does nothing
([test](../tests/insight_ui/unit/test_utility_variants.py)). The plain classes
are always in the package stylesheet; a variant is only generated where a
package template or your own Tailwind build uses it. Opacity modifiers such as
`/50` need the token utility, e.g. `odd:bg-insight-bg-raised/50` in the
[table template](../insight_ui/templates/insight_ui/components/table.html).

The [token checker](../scripts/check_design_tokens.py) flags selected raw color,
radius, shadow and verbose utility patterns. Some replacement suggestions are
older names; verify them against `input.css`, not as a separate token contract.
This table is a starting point, not an inventory of every value.

## Color Families

`primary`, `secondary`, `success`, `warning`, `danger` and `info` share the same
tokens. Pick the token by what you color, not by the theme:

| You color | Token | Light / dark theme |
| --- | --- | --- |
| A border, bar or indicator | `--color-insight-primary` | The same in both themes |
| Text, an icon, a link or an outline border | `--color-insight-primary-text` | Switches to `-text-dark` |
| The fill of a button or checked control | `--color-insight-primary-action`, `-action-hover`, `-action-active` | Switches to `-action-dark` and its states |
| Text and icons on that fill | `--color-insight-primary-on-action` | Switches to `-on-action-dark` |
| A subtle background (subtle button, badge, alert) | `--color-insight-primary-soft` | Switches to `-soft-dark` |

The family color itself (`text-insight-primary`) is an accent. It does not
change with the theme, so as text it lacks contrast in one of them; use
`text-insight-primary-text` for text and icons. Tokens ending in `-dark` hold the
dark theme values; templates use the names without `-dark`, which switch on
`[data-theme="dark"]`.

`-action` is separate from the accent for brand colors that work in only one
theme. A dark brand blue is a fine accent, and a fine button in the light theme,
but barely visible as a button on the dark background. Keep the accent and give
the dark theme a lighter button and text color in your theme:

```css
@theme {
    --color-insight-primary: #003153;             /* brand color, borders and bars */
    --color-insight-primary-action-dark: #2F6FAB; /* lighter buttons in the dark theme */
    --color-insight-primary-action-hover-dark: #3A78B4;
    --color-insight-primary-action-active-dark: #2A6399;
    --color-insight-primary-text-dark: #9CC8EB;   /* readable text and icons in the dark theme */
}
```

The dark button colors stay dark enough for the white `-on-action` text (4.5:1)
and light enough to stand out from the dark page (3:1). For a light button in
the dark theme, set `--color-insight-primary-on-action-dark` to a dark text
color instead. The same applies to a light brand color, e.g. yellow, which needs
dark `-on-action` text on its buttons. [The token tests](../tests/insight_ui/unit/test_design_tokens.py)
check that text, links and text on fills reach WCAG AA in both themes.

## Host Assets And Contributor Builds

Hosts can use the packaged stylesheet without a contributor build;
`INSIGHT_UI["use_tailwind_cli"]` defaults to `False` in
[config.py](../insight_ui/config.py). Do not copy `tests.tailwind_settings` or
`devtools` into a host. Host-only styles belong in its own stylesheet/build.

For package changes, `build:static-all` in [package.json](../package.json) builds
Tailwind with [tests/tailwind_settings.py](../tests/tailwind_settings.py), then
generates minified assets. `input.css` explicitly scans package templates,
Configs, JavaScript and template tags, not host templates, Markdown or manifest
JSON. Exporting a token does not include every possible utility or variant.

## Color Is A Role, Not A Palette Copy

Choose an existing shared role before adding a component-specific token. A table,
menu and card should not each define their own unrelated gray palette for the
same surface purpose. Geometry utilities may remain technical where they are
layout details; reusable visual decisions should have a stable semantic role.

Distinguish an accent from readable foreground text and a filled action. The
`primary`, `secondary`, `success`, `warning`, `danger` and `info` families provide
different values for these purposes. Reusing an arbitrary accent as a button
background does not guarantee readable text in both themes.

For a reusable panel, prefer composing existing components or a shared surface:

```html
<section class="insight-surface p-insight-m">
    <h2 class="text-insight-headline">Panel title</h2>
    <p class="text-insight-body">Panel content</p>
</section>
```

## Light And Dark

Set `data-theme="light"` or `data-theme="dark"` on `<html>`. Dark mappings in
`input.css` explicitly select the corresponding `*-dark` values; not every token
has a dark counterpart or mapping. Use the existing
[ThemeToggle](../insight_ui/static/insight_ui/js/insight-ui-theme-toggle.js) for
interactive switching. Legacy `dark:` utilities also remain. When changing a
role, inspect its mapping and affected consumers.

Use the local preview's theme toggle to inspect text, borders, surfaces, hover,
focus and disabled states. Verify contrast for the actual color pair. A token
name, successful build or light-theme screenshot is not accessibility evidence.

## Adding Or Changing A Token

1. Search `input.css` and existing component consumers for an equivalent role.
2. Reuse that role, or explain why a new shared purpose is necessary.
3. Define the role centrally; prefer references to existing roles over duplicate
   literals when the purposes are related.
4. Update affected templates/JS and include complete dynamic class variants in
   scanned sources or `@source inline(...)`. Check the generated CSS; do not rely
   on classes seen only in host templates, manifests or Markdown examples.
5. Run the [asset build and token checks](testing.md), then test both themes and
   relevant interaction states.

Motion, blur and density should also use semantic names when exposed as public
behavior, but **a proposed name is not an implemented token**. Only document a
specific token as available when it exists in the current source and has tested
consumers. Do not reintroduce legacy names to make an old guide appear correct.

Fonts and generic icons are reusable package assets; product brand configuration
belongs to the host. Follow existing icon APIs and licensing, not private logo
copies. The extension rule is composition first: domain-only concepts stay in the
extension; broadly reusable, stable concepts may become package roles.

[All package guides](README.md) | [Contribution workflow](../CONTRIBUTING.md)
