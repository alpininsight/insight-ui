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

Use the current names, not earlier token names from old examples:

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
| Semantic text/icon color | `--color-insight-primary-foreground` | `text-insight-primary-foreground` |
| Filled action background | `--color-insight-primary-action` | Prefer the existing primary button. |
| Text on the filled action | `--color-insight-primary-text` | Used together with its action background. |
| Reusable spacing | `--spacing-insight-m` | `p-insight-m`, `gap-insight-m` |
| Control radius | `--radius-insight-control` | `rounded-insight-control` |
| Surface radius | `--radius-insight-surface` | `rounded-insight-surface` |
| Surface shadow | `--shadow-insight-surface` | `shadow-insight-surface` |
| Overlay shadow | `--shadow-insight-overlay` | `shadow-insight-overlay` |

The background, border and text shorthands are explicit `@layer utilities`
classes, not interchangeable with generated Tailwind utilities. Prefer them for
plain classes, but do not assume state or opacity variants exist. For example,
the [table template](../insight_ui/templates/insight_ui/components/table.html)
uses `odd:bg-insight-bg-raised/50`, which is present in the generated CSS.

The [token checker](../scripts/check_design_tokens.py) flags selected raw color,
radius, shadow and verbose utility patterns. Some replacement suggestions are
older names; verify them against `input.css`, not as a separate token contract.
This table is a starting point, not an inventory of every value.

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
