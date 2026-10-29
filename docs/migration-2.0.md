<!--
SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
SPDX-License-Identifier: AGPL-3.0-only
-->

# Migrating to Insight UI 2.0

This guide covers consumer changes on `develop` since the `v1.15.1` tag.
There is no `2.0.0` tag yet. The runtime Python and Django requirements are
unchanged. The dev pin `django-stubs` moved from 6.1.1 to 6.1.2. No template,
static file or Python module was removed.

Apply the checklist, then read the section for each hit. Every break below
has a before/after snippet, the pull request that introduced it, and a search
pattern for a host project.

[Getting started](getting-started.md) | [Design system](design-system.md) | [Guide index](README.md)

## Checklist

- [ ] Rename the six color-family tokens in two passes. Do this before any other class edit.
- [ ] Replace the family `-hover` / `-active` tokens with `-action-hover` / `-action-active`, and use `-text` for colored text.
- [ ] Replace `#loading-indicator` and stop relying on an `hx-indicator` inherited from `<body>`.
- [ ] Check first paint when the visitor has not saved a theme, including a dark operating system.
- [ ] Remove host wrappers that add their own page padding or max-width, and review `{% page padding %}`, which is vertical only now.
- [ ] Drop host offsets for the fixed navbar (`pt-16`, `top-16`); set `--insight-navbar-height` for a taller navbar.
- [ ] Wait for tooltips in browser tests, or set `INSIGHT_UI["tooltip_show_delay"]` to `0`.
- [ ] Point form error targets at `#<tag_id>-error` when the form has a `tag_id`.
- [ ] Update selectors and DOM tests for footer headings, icon wrappers, tooltip wrappers and the required asterisk.
- [ ] Expect `aria-disabled="true"` on a disabled link button, with no `href` and no `hx-*`.
- [ ] Keep `{% surface %}` hrefs relative or `http` / `https` / `mailto`, and pass layout-tag attributes unescaped.
- [ ] Let layout-tag filters and `_()` translations resolve on each render. A filter on a quoted value is kept.
- [ ] Give `{% tabs %}` a stable `id`. Expect one active tab, `type="button"`, an SVG for `icon`, and `hx-trigger="load, click"` on the active HTMX tab.
- [ ] In a right-to-left container, ArrowLeft moves to the next tab.
- [ ] Pass config dataclasses into template tags. Dictionaries are rejected.
- [ ] Rename alert `type`, infobox `info_type` and status screen `status` to `severity`.
- [ ] Map stepper booleans and the old step strings onto `pending` / `current` / `completed` / `failed`.
- [ ] Replace `completed=` / `current=` on bullet point items with `status=`, and pass `request_url` as a URL, not a URL name.
- [ ] Replace `FormFieldConfig` with the concrete field config. Pass `name=` as a keyword.
- [ ] Give every button a non-empty label, and give ids, names and URLs that the configs now require.
- [ ] Use lowercase hyphenated `DataAttrConfig` names.
- [ ] Remove `trigger=` from `HtmxConfig`.
- [ ] Rename `htmx_config=` to `htmx=` on buttons, forms, the search bar and `generic_filter`.
- [ ] Rename `badge_config=` (hero), `table_config=` and `view_radio_config=` (toggle view), `usermenu=` (navbar) and `empty_msg=` (table).
- [ ] Re-check `swap_method` on navbar, footer, sidebar, search, generic filter, form and bullet lists.
- [ ] Re-check `push_url=False` on dropdown items, the navbar user menu and the search bar.
- [ ] Rebuild query builder views on `parse_filters` and `build_query`, and rename `model_fields` to `fields`.
- [ ] Move `show_global_loading_indicator=` from `live_content` into its `HtmxConfig`, and give a second `chat` on a page its own `tag_id`.
- [ ] Replace `hx_target_id=` / `hx_swap_method=` on `radio_block` with `htmx=HtmxConfig(target="#…", swap_method="outerHTML")`.
- [ ] Replace `explanation=` with `help_text=`, and expect `disabled_reason` as visible text below form fields.
- [ ] Replace button and badge `type=` / `outline=` / `subtle=` with `color=` and `variant=`, and the old `btn-*` color classes with `btn` plus modifiers.
- [ ] Replace `get_page` with Django's `Paginator`, drop `surrounding_pages`, rename `ipp_config=` to `items_per_page=`, and pass an `HtmxConfig` where pagination should swap via HTMX.

## Color tokens are a silent break

[#693](https://github.com/alpininsight/insight-ui/pull/693) renamed the six families
`primary`, `secondary`, `success`, `warning`, `danger` and `info`.
The old names still match a real token, and the meaning has changed.

| v1.15.1 | Meaning then | 2.0 name |
| --- | --- | --- |
| `--color-insight-<family>-text` | White text on a filled button | `--color-insight-<family>-on-action` |
| `--color-insight-<family>-foreground` | Colored text and icons | `--color-insight-<family>-text` |
| `--color-insight-<family>-foreground-dark` | Same color in the dark theme | `--color-insight-<family>-text-dark` |

Utility classes follow the variable name. `text-insight-danger-foreground`
becomes `text-insight-danger-text`. The same substring is in `bg-`, `border-`
and other utilities generated from that token.

A host rule that still says `text-insight-primary-text` compiles. In v1.15.1
that class was white text on a filled button. It is now the colored text tone
(`#0856C0` in the light theme).

Do the replacement in this order. Pass 2 writes the new `-text` names. Running
it first makes a later `-text` → `-on-action` pass rewrite those names as well.

```bash
# 1. Old on-action token. The (?!-) skip keeps a later -text-dark result intact.
perl -pi -e 's/insight-(primary|secondary|success|warning|danger|info)-text(?!-)/insight-$1-on-action/g' FILES

# 2. Old colored-text token, including the -dark variant.
perl -pi -e 's/insight-(primary|secondary|success|warning|danger|info)-foreground/insight-$1-text/g' FILES
```

Limit both passes to those six families. A global `-text` → `-on-action` replace
also rewrites `--color-insight-text-body`, `--color-insight-text-headline`,
`--color-insight-text-muted` and `--color-insight-text-link`. Those names did
not change. The old value was `#FFFFFF` in both themes; 2.0 keeps it for
`-on-action` and the new `-on-action-dark`, which a theme can set for a dark
theme fill that needs other text.

Before:

```html
<button class="bg-insight-danger-action text-insight-danger-text">Delete</button>
<p class="text-insight-danger-foreground">Something failed.</p>
```

After:

```html
<button class="bg-insight-danger-action text-insight-danger-on-action">Delete</button>
<p class="text-insight-danger-text">Something failed.</p>
```

Search:

```text
insight-(primary|secondary|success|warning|danger|info)-(text|foreground)
```

Review matches of `-text` before editing. A match that is already the colored
text tone on a migrated tree must stay `-text`.

### Readable text colors and fewer state tokens

The six color families keep these tokens: the accent (`primary`), `-text`,
`-action` with `-action-hover` and `-action-active`, `-on-action` and `-soft`.
The table in [the design system guide](design-system.md#color-families) says
which one to use for what.

| v1.15.1 | 2.0 |
| --- | --- |
| `--color-insight-<family>-hover`, `-active` and their `-dark` variants | Removed. Fills use `-action-hover` / `-action-active`; text uses `-text`. |
| `--color-insight-text-link` without a dark value | `--color-insight-text-link-dark` (`#72AEFF`) |
| `--color-insight-text-link-hover` `#72AEFF` in both themes | `#1555B0` in the light theme, `--color-insight-text-link-hover-dark` `#90C5FF` |
| `{% icon color="primary" %}` renders `text-insight-primary` | Renders `text-insight-primary-text`, readable in the dark theme |

The family accent (`text-insight-danger`) does not change with the theme, and
as text it lacks contrast in one of them. The package templates now use the
`-text` token for text and icons, so colored text and icons get lighter in the
dark theme: the info box title, form and login errors, the logout entry, the
footer mail link, hover colors of collapsible and table headers, sidebar
category headings and the current table of contents entry. Tabs keep the
`-text` color after switching; before, the tab that was active on page load
kept its primary classes.

Before:

```css
@theme {
    --color-insight-primary-hover: #4F46E5;
    --color-insight-primary-active: #4338CA;
}
```

```html
<p class="text-insight-danger">Something failed.</p>
```

After, set the states of filled controls and use the text token:

```css
@theme {
    --color-insight-primary-action-hover: #4F46E5;
    --color-insight-primary-action-active: #4338CA;
}
```

```html
<p class="text-insight-danger-text">Something failed.</p>
```

Search: `-hover:` and `-active:` after a family name in theme files,
`text-insight-<family>-hover`, and `text-insight-<family>` followed by a space
or quote in templates. The [token check](../scripts/check_design_tokens.py)
reports the last one.

## Page shell

### Global loading bar

[#723](https://github.com/alpininsight/insight-ui/pull/723) and
[#718](https://github.com/alpininsight/insight-ui/pull/718).

The bar's id is `insight-global-loading-indicator`. It is `aria-hidden="true"`.
A separate `#insight-global-loading-status` live region announces a request
that is still running after one second. The old `role="progressbar"` is gone.

Before:

```html
<div hx-indicator="#loading-indicator"></div>
```

After:

```html
<div hx-indicator="#insight-global-loading-indicator"></div>
```

Search: `#loading-indicator` and `role="progressbar"` on the old bar.
`insight-global-loading-indicator` does not contain the `#loading-indicator` string.

### The body no longer sets an indicator

[#718](https://github.com/alpininsight/insight-ui/pull/718).

`<body>` used to carry `hx-indicator="#loading-indicator"`. Child requests
inherited it. The bar is now shown from `htmx:beforeSend` and hidden from
`htmx:afterRequest`. A request inside
`[data-insight-global-indicator="false"]` is ignored.

Before:

```html
<body hx-indicator="#loading-indicator">
```

After, a host element that relied on that inheritance sets its own indicator:

```html
<form hx-post="/save/" hx-indicator="#insight-global-loading-indicator"></form>
```

Background polling opts out with
`data-insight-global-indicator="false"` or
`HtmxConfig(show_global_loading_indicator=False)`.
`LiveContentConfig.show_global_loading_indicator` defaults to `False`, so live
content polling does not show the bar.

Search: `hx-indicator` on elements that have no indicator of their own, and
`show_global_loading_indicator`.

### Spacing and content width

All parts of the page now share one distance to the window edge,
`--insight-gutter` (1rem on phones, growing to 2rem from about 64rem). In
v1.15.1 each part had its own: navbar `px-4`, footer and sidebars `px-4` /
`md:px-6`, page header `px-4` / `md:px-16` with a `max-w-4xl` column, and the
content none at all.

The content is limited to a centered box of `--insight-content-max-width`
(default `80rem`). `#content` is a three-column grid: its direct children sit
in the content column, and `{% page %}` bands span the whole content area
(up to the sidebars) while their text stays in the column. Add the class
`insight-full-bleed` to your own direct children for the same effect.

| Setting or context | Effect |
| --- | --- |
| `INSIGHT_UI["content_max_width"]` | Content width for all pages, e.g. `"64rem"` |
| `content_max_width` (template context) | Content width for one page |
| `content_full_width=True` (template context) | No box and no grid; the page manages its own width |
| `INSIGHT_UI["align_navbar_footer_to_content"]` | Navbar and footer put their content into the content box instead of spanning the window |
| `content_fill=True` (template context) | Unchanged flex column for filling pages such as a login, now boxed |

`{% page padding=... %}` pads only vertically; the box provides the horizontal
gutter. The page header's text now uses the content width instead of
`max-w-4xl`.

Before:

```text
{% block content %}
    <div class="px-4 mx-auto max-w-7xl">{% page padding="m" %}...{% endpage %}</div>
{% endblock %}
```

After, drop the wrapper; the base template boxes the content:

```text
{% block content %}
    {% page padding="m" %}...{% endpage %}
{% endblock %}
```

Because direct children of `#content` are grid items, `float` has no effect on
them and their vertical margins add up instead of collapsing (`mb-4` followed
by `mt-8` is now 48px, not 32px). Elements one level deeper behave as before.
A `{% page %}` nested in another container stays in the content column.

Search: host base templates and pages for `px-`, `max-w-` and `mx-auto`
wrappers around the content, `{% page padding=`, and floated or margin-spaced
top-level elements.

### Fixed navbar is sticky

With `INSIGHT_UI["navbar_fixed"]`, v1.15.1 positioned the navbar with
`position: fixed` and reserved its height with `pt-16` on `#main`. The header
is now `position: sticky` and stays in the page flow, so `#main` no longer has
`pt-16`. On screen it behaves the same: the navbar stays at the top while the
page scrolls.

The navbar height is one variable, `--insight-navbar-height` (default `4rem`).
Sticky sidebars, the drawer button and the scroll padding for anchor targets
start below it. A host with a taller navbar sets the variable
once instead of overriding `top-16`, `pt-16` and `calc(100dvh - 4rem)`.

```css
:root {
    --insight-navbar-height: 5rem;
}
```

Search: host CSS or templates that compensate the fixed navbar with `pt-16`,
`mt-16` or `top-16`, and scripts that expect the navbar to be
`position: fixed`.

### Theme before first paint

[#707](https://github.com/alpininsight/insight-ui/pull/707).

The inline script in `base.html` runs before stylesheets. A saved
`localStorage` value of `light` or `dark` wins. With no saved choice the
script follows `prefers-color-scheme`. It also toggles the `dark` class on
`<html>`. v1.15.1 always started on `light` and did not set that class in this
script.

Before:

```javascript
const theme = localStorage.getItem("insight-ui-theme") || "light";
document.documentElement.setAttribute("data-theme", theme);
```

After:

```javascript
const saved = localStorage.getItem("insight-ui-theme");
const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
const theme = (saved === "dark" || saved === "light") ? saved : (prefersDark ? "dark" : "light");
document.documentElement.setAttribute("data-theme", theme);
document.documentElement.classList.toggle("dark", theme === "dark");
```

To force the old first paint, set `localStorage['insight-ui-theme'] = 'light'`
before the page loads. Search screenshots and login pages for a dark OS theme.
The storage key is still `insight-ui-theme`.

### Tooltip delay

[#712](https://github.com/alpininsight/insight-ui/pull/712).

`<html>` sets `data-tooltip-delay` from `INSIGHT_UI["tooltip_show_delay"]`,
default `400`. Hover waits. Keyboard focus still opens the tooltip immediately.

Before, a hover test could read the tooltip on the next frame. After, wait
400 ms, or set the delay to `0` in the test settings:

```python
INSIGHT_UI = {"tooltip_show_delay": 0}
```

Search: `data-insight-tooltip` in browser tests that hover and assert at once.

## Layout tags

[#748](https://github.com/alpininsight/insight-ui/pull/748).

`section`, `page`, `hbox`, `vbox`, `grid`, `surface`, `list` and `listitem` escape
`id`, `class`, `style`, `aria-label`, `aria-labelledby` and `href` when they
write those attributes. Pass the raw value. An already escaped string is
escaped again.

`{% surface href=... %}` allows a relative URL (no scheme, including
`//host`, `?query` and `#fragment`) and the schemes `http`, `https` and
`mailto`. Any other scheme raises `ValueError` while rendering. `javascript:`
and `data:` are rejected. `ImageConfig.url` still accepts a `data:` URL. That
allowlist is only the surface href.

Before:

```text
{% load layout_tags %}
{% surface href=report_url %}Report{% endsurface %}
```

```python
report_url = "javascript:alert(1)"
```

After, use a relative path or an `http`, `https` or `mailto` URL:

```python
report_url = "/reports/1/"
```

Search: `{% surface` together with `href=`, and layout-tag attributes that are
passed through `|escape` or `mark_safe`.

[#735](https://github.com/alpininsight/insight-ui/pull/735) resolves every
layout-tag argument when the template renders. That includes filters and
`_()` translations. A quoted literal used to be fixed while the template was
parsed, and a filter on that literal was dropped. The same compiled template
can now render in the language of each request.

`{% surface href %}` runs those filters first, then applies the scheme
allowlist above. A filtered value such as `"java"|add:"script:alert(1)"`
raises `ValueError`. [#748](https://github.com/alpininsight/insight-ui/pull/748)
added the escaping and the allowlist. It did not resolve arguments per render.

Before, this filter was dropped and the id stayed `tab-`:

```text
{% load layout_tags %}
{% section id="tab-"|add:name %}...{% endsection %}
```

After, with `name` equal to `intro`, the id is `tab-intro`.

Search: `{% section`, `{% surface`, `{% hbox`, `{% tabs` and `{% tab` with a
`|` filter on a quoted argument, and `_("` inside those tags.

`{% modal %}` accepts `config=ModalConfig(...)`. A single `id`, `title`,
`width` or `show_close` argument overrides the config.
`ModalConfig.id` must be non-empty ([#719](https://github.com/alpininsight/insight-ui/pull/719)).
The modal shell adds the blocks `modal_body` and `modal_footer`. The blocks
already on `base.html` are unchanged.

## Tabs

[#735](https://github.com/alpininsight/insight-ui/pull/735).

`id` and `label` on `{% tabs %}` name the group. `id` is the
`data-insight-tabs` value and the prefix of each panel id. `label` is the
tablist `aria-label`, and the attribute is omitted when `label` is empty.
In v1.15.1 those arguments were parsed and then ignored, so the group id
changed on every render and the tablist label was empty.

The same two arguments override a `TabsConfig`: `id` replaces `tag_id`.
`config` has to be a `TabsConfig`. A dict raises `TypeError`. An empty
`tabs` list raises `ValueError` (`needs at least one tab`) as soon as the
config is built. `{% tabs config=... %}` together with `{% tab %}` blocks
raises `ValueError`. `{% tab %}` outside `{% tabs %}` raises
`TemplateSyntaxError`.

Unknown arguments raise `ValueError` (`Unknown parameter 'colour'`).
`{% tabs %}` accepts `id`, `label` and `config`. `{% tab %}` accepts `id`,
`label`, `active`, `request_url` and `icon`.

A `{% tab %}` may sit inside `{% if %}` or `{% for %}`, and its arguments
may be variables. Exactly one tab is active, chosen again on every render:
the first with `active=True`, otherwise the first tab. Further `active=True`
flags are ignored. v1.15.1 left every marked tab selected. When none
were marked, it set `active` on the first compiled tab, and that flag
stayed set for later renders.

Every static panel is rendered, including an empty one, with
`aria-labelledby` set to the tab id and `tabindex="0"`. Each tab button is
`type="button"`. `icon` is an icon name and renders an SVG. v1.15.1 printed
the name as text inside `<span class="mr-2">`. The shipped stylesheet no
longer contains `.mr-2`.

HTMX tabs share one panel, `#<tag_id>-tab-content`, labelled by the active
tab. That tab has `hx-trigger="load, click"`. The others have no
`hx-trigger`, so they load on click. v1.15.1 set no `hx-trigger`, and the
active panel stayed empty until a click. Config mode still renders no icon.
`TabConfig` has no icon field.

Inside a right-to-left container (`dir="rtl"` on the tabs element or an
ancestor), ArrowLeft moves to the next tab and ArrowRight to the previous.
The direction is read on each key press. Home and End stay the same. The
icon mirror from [#736](https://github.com/alpininsight/insight-ui/pull/736)
does not change these keys.

Before, `id` and `label` were ignored, an icon name was printed as text, and
the active HTMX tab did not load:

```text
{% load layout_tags %}
{% tabs id="settings" label="Settings" %}
    {% tab id="general" label="General" icon="cog-6-tooth" active=True request_url="/settings/general/" %}{% endtab %}
    {% tab id="security" label="Security" active=True request_url="/settings/security/" %}{% endtab %}
{% endtabs %}
```

After, the group id is `settings`, the tablist is labelled `Settings`, the
icon is an SVG, only General is selected, and General requests its URL on
load. A second `active=True` does not select Security.

Search: `{% tabs`, `{% tab`, `TabsConfig(`, `role="tab"`, `data-insight-tabs`
and `mr-2`.

## Template tags and configs

### Dictionaries are rejected

[#688](https://github.com/alpininsight/insight-ui/pull/688).

`build_config()` raises `TypeError` unless `config` is a dataclass instance.
The private coercion helpers are gone. Nested dicts inside a list are not
turned into configs either. Build the dataclasses in the view.

Before:

```python
context = {"alert": {"message": "Saved", "type": "success"}}
```

```text
{% alert config=alert %}
```

After:

```python
from insight_ui.configs import AlertConfig

context = {"alert": AlertConfig(message="Saved", severity="success")}
```

Search: `config=` in templates whose view puts a `dict` in that variable, and
calls that used to rely on dict coercion.

### Config fields are named by their role

A field that holds another config is named after its role, without a
`_config` suffix, and in the snake case of the class name. Four fields did
not follow this:

| Config | Before | After |
| --- | --- | --- |
| `HeroConfig` | `badge_config` | `badge` |
| `ToggleViewConfig` | `table_config` | `table` |
| `ToggleViewConfig` | `view_radio_config` | `view_switch` |
| `NavbarConfig` | `usermenu` | `user_menu` |

`TableConfig.empty_msg` is now `empty_text`, like the other `*_text`
fields.

The `hero` and `toggle_view` tag arguments change the same way. The old names
raise `TypeError`.

Before:

```python
NavbarConfig(usermenu=UserMenuConfig(links=links))
```

After:

```python
NavbarConfig(user_menu=UserMenuConfig(links=links))
```

Search: `badge_config=`, `table_config=`, `view_radio_config=`, `usermenu=` and `empty_msg`.

### Severity

[#720](https://github.com/alpininsight/insight-ui/pull/720).

| v1.15.1 | 2.0 |
| --- | --- |
| `AlertConfig.type` and `{% alert type= %}` | `severity` |
| `InfoboxConfig.info_type` and `{% infobox info_type= %}` | `severity` |
| `StatusScreenConfig.status` and `{% status_screen status= %}` | `severity` |
| `AlertType`, `ALERT_TYPE_VALUES`, `validate_alert_type` | `Severity`, `SEVERITY_VALUES`, `validate_severity` |

The values are still `info`, `success`, `warning` and `error`. `"danger"`
raises `ValueError` and the message tells you to use `"error"`. Map Django
message tags onto `error`, not `danger`.

Button and badge `type` are not part of this rename; they became `color`, see
[Button and badge color and variant](#button-and-badge-color-and-variant).

Before:

```python
from insight_ui.configs import AlertConfig

AlertConfig(message="Saved", type="error")
```

```text
{% load insight_tags %}
{% alert message="Saved" type="error" %}
{% infobox message="Tip" info_type="info" %}
{% status_screen title="Done" status="success" %}
```

After:

```python
from insight_ui.configs import AlertConfig

AlertConfig(message="Saved", severity="error")
```

```text
{% load insight_tags %}
{% alert message="Saved" severity="error" %}
{% infobox message="Tip" severity="info" %}
{% status_screen title="Done" severity="success" %}
```

Search: `info_type=`, `AlertType`, `ALERT_TYPE_VALUES`, `validate_alert_type`,
`{% alert`, `{% infobox` and `{% status_screen`. On those tags, look for
`type=` and `status=`. Leave `{% button type=` and `{% badge type=` in place.

### Stepper status

[#721](https://github.com/alpininsight/insight-ui/pull/721) and
[#698](https://github.com/alpininsight/insight-ui/pull/698).

`StepperConfig.items` is still `items`. The rename to `steps` is only
`MinimalStepperConfig`.

| v1.15.1 | 2.0 |
| --- | --- |
| `StepperItemConfig(success=True)` | `status="completed"` |
| `StepperItemConfig(current=True)` | `status="current"` |
| `StepperItemConfig(failed=True)` | `status="failed"` |
| omitted booleans | `status="pending"` (the default) |
| minimal step `"active"` | `"current"` |
| minimal step `"success"` | `"completed"` |
| minimal step `""` | `"pending"` |
| minimal step `"failed"` | `"failed"` |
| `MinimalStepperConfig.items` | `steps` |
| `current_step_status` default `"active"` | `"current"` |

The failed icon on `minimal_stepper` is `x-mark`. v1.15.1 used the `danger` icon.

Before:

```python
from insight_ui.configs import MinimalStepperConfig, StepperItemConfig

StepperItemConfig(title="Address", success=True)
MinimalStepperConfig(items=["success", "active", ""])
```

```text
{% load insight_tags %}
{% minimal_stepper items=states %}
```

After:

```python
from insight_ui.configs import MinimalStepperConfig, StepperItemConfig

StepperItemConfig(title="Address", status="completed")
MinimalStepperConfig(steps=["completed", "current", "pending"])
```

```text
{% load insight_tags %}
{% minimal_stepper steps=states %}
```

Search: `success=True` and `failed=True` on `StepperItemConfig`, `items=` on
`{% minimal_stepper` and `MinimalStepperConfig`, and the strings `"active"`
and `"success"` in step lists. `{% stepper items=` stays valid.

### Button and badge color and variant

[#733](https://github.com/alpininsight/insight-ui/pull/733).

`ButtonConfig.type` mixed the color with the look (`"link"`), and `outline` /
`subtle` were two booleans that could both be set. A button now has a `color`
and a `variant`:

| Field | Values | Default |
| --- | --- | --- |
| `color` | `primary`, `secondary`, `light`, `info`, `success`, `warning`, `danger` | `primary` |
| `variant` | `solid`, `outline`, `subtle`, `link`, `plain` | `solid` |

`light` is for buttons on dark or colored surfaces. `plain` is an icon-style
button in the text color. `link` and `plain` ignore the color.

| v1.15.1 | 2.0 |
| --- | --- |
| `type="primary"` (any color) | `color="primary"` |
| `outline=True` / `subtle=True` | `variant="outline"` / `variant="subtle"` |
| `type="link"` | `variant="link"` |
| `type="neutral"` | `color="light"` on dark or colored surfaces, otherwise `variant="plain"` |
| `ButtonType`, `BUTTON_TYPE_VALUES`, `validate_button_type` | `ButtonColor` / `ButtonVariant`, `BUTTON_COLOR_VALUES` / `BUTTON_VARIANT_VALUES`, `validate_button_color` / `validate_button_variant` |

A badge has `color` (`primary`, `secondary`, `neutral`, `info`, `success`,
`warning`, `danger`) and `disabled`. `type="disabled"` becomes
`disabled=True`. `BadgeType`, `BADGE_TYPE_VALUES` and `validate_badge_type`
are replaced by `ColorType`, `COLOR_TYPE_VALUES` and `validate_color_type`.

Before:

```python
ButtonConfig(label="Cancel", type="secondary", outline=True)
BadgeConfig(label="Archived", type="disabled")
```

After:

```python
ButtonConfig(label="Cancel", color="secondary", variant="outline")
BadgeConfig(label="Archived", color="neutral", disabled=True)
```

`disabled=True` no longer replaces the color. The look comes from the
`disabled` attribute (or `aria-disabled="true"` on links), so a button that
JavaScript enables again shows its color. Combinations that used to be ignored
now raise `ValueError`: `external=True` without `request_url`, and `on_click` or
`button_type` together with `request_url`.

The CSS classes follow the same split. `.btn` alone is a solid primary button;
color and variant are modifiers:

| v1.15.1 | 2.0 |
| --- | --- |
| `btn-primary` | `btn btn-primary` |
| `btn-outline-primary` | `btn btn-outline btn-primary` |
| `btn-subtle-primary` | `btn btn-subtle btn-primary` |
| `btn-neutral`, `btn-outline-neutral` | `btn btn-light`, `btn btn-outline btn-light` |
| `btn-subtle-neutral` | `btn btn-plain` |
| `btn-disabled`, `btn-outline-disabled`, `btn-subtle-disabled` | the `disabled` attribute or `aria-disabled="true"`; `.btn-disabled` remains for labels styled as buttons |

Search: `type=` on buttons and badges, `outline=`, `subtle=`, `ButtonType`,
`BadgeType` and `btn-` classes in host templates, CSS and tests.

### Bullet point list status

`BulletPointItemConfig` uses the stepper's status values instead of the
`completed` and `current` booleans. `failed` is new and shows an x-mark in the
danger color.

Before:

```python
BulletPointItemConfig(title="Payment", completed=True)
BulletPointItemConfig(title="Review", current=True)
```

After:

```python
BulletPointItemConfig(title="Payment", status="completed")
BulletPointItemConfig(title="Review", status="current")
```

`status` defaults to `pending`; unknown values raise `ValueError`.

`request_url` is a URL, like on every other component. v1.15.1 resolved it as
a URL name with `{% url %}` for `href` but sent it unchanged as `hx-get`, so a
plain URL produced no link. Pass `reverse("name")` where you passed a name.
Items without `request_url` and the current item render as a `<div>`, not as an
`<a>` without `href`. `aria-current="step"` moves from the link to the `<li>`.

Search: `completed=` and `current=` on `BulletPointItemConfig`, and
`request_url=` values without a `/`.

### `flip_card` tag arguments

[#707](https://github.com/alpininsight/insight-ui/pull/707).

`back_title` and `back_actions` were already fields on `FlipCardConfig`.
The tag now accepts them. `back_style` was a tag argument the config never
stored. Passing it already raised `TypeError` inside `build_config`. The
argument is no longer on the tag.

`tags` on `app_card` and `flip_card` are `list[BadgeConfig]`, and the
templates already rendered them with `{% badge config=tag %}` in v1.15.1.
A list of strings did not become badges.

Search: `back_style=`.

## Forms

### `FormFieldConfig` is gone

[#692](https://github.com/alpininsight/insight-ui/pull/692).

`FormFieldConfig`, `FormFieldType`, `FORM_FIELD_TYPE_VALUES` and
`validate_form_field_type` are removed. `FormConfig.fields` takes the concrete
configs. Anything else raises `TypeError`. A subclass of one of those configs
is accepted. The public names are `FORM_FIELD_CONFIGS` and `FormField`.

| `FormFieldConfig.input_type` | Replacement |
| --- | --- |
| `text`, `password`, `email`, `number`, `tel`, `url`, `date` | `InputFieldConfig(name=..., input_type=...)` |
| `textarea` | `TextareaConfig` |
| `select` | `SelectConfig` |

`SelectConfig` has no `placeholder` field. It did not have one in v1.15.1
either. `FormFieldConfig` did. A prompt is an option whose key is
`placeholder`. That option submits an empty value. `InputFieldConfig` and
`TextareaConfig` still have `placeholder`.

`explanation` is gone from every field; see
[Help, error and disabled texts](#help-error-and-disabled-texts).

Before:

```python
from insight_ui.configs import FormFieldConfig

FormFieldConfig(input_type="password", name="password", label="Password")
FormFieldConfig(input_type="textarea", name="note", label="Note")
FormFieldConfig(input_type="select", name="country", label="Country", placeholder="Choose")
```

After:

```python
from insight_ui.configs import InputFieldConfig, SelectConfig, TextareaConfig

InputFieldConfig(name="password", input_type="password", label="Password")
TextareaConfig(name="note", label="Note")
SelectConfig(name="country", label="Country", options={"placeholder": "Choose", "de": "Germany"})
```

Search: `FormFieldConfig`, `FORM_FIELD_TYPE_VALUES`, `validate_form_field_type`,
`FormFieldType`.

### `name` is required and comes first

[#692](https://github.com/alpininsight/insight-ui/pull/692).

`name` is the first field of `BaseFormFieldConfig`, so it is the first
positional argument of every field config, including `CheckboxConfig`.
It must be a non-empty string. `None` and `""` raise `ValueError` in
`__post_init__`. A missing template variable rendered into an attribute
becomes `""` and fails the same check.

v1.15.1 field order started with `tag_id`, then `name`, and both defaulted to
`None`. The same positional call now stores the arguments the other way round.

Before:

```python
InputFieldConfig("email-id", "email")
```

After:

```python
InputFieldConfig(name="email", tag_id="email-id")
```

Search: `InputFieldConfig(`, `TextareaConfig(`, `SelectConfig(`,
`CheckboxConfig(` and the other field configs. Prefer a keyword search for
calls that pass `tag_id` positionally.

### Empty required values

[#697](https://github.com/alpininsight/insight-ui/pull/697).

These fields raise `ValueError` at construction when they are empty or `None`.
`ButtonConfig.label` is included for icon-only buttons. The label is the
accessible name.

- `ButtonConfig.label`
- `ImageConfig.url`, `ImageCarouselItemConfig.url`
- `ModalConfig.id`, `MessageDialogConfig.message`
- `CheckboxItemConfig.tag_id`
- `name` on `BaseFormFieldConfig`, `CheckboxGroupConfig`, `RadioGroupConfig`, `RadioBlockConfig`
- `DropdownConfig.tag_id`, `DropdownItemConfig.request_url`
- `UserMenuLinkConfig.request_url`
- `TabConfig.tag_id` and `TabConfig.request_url`
- `AccordionConfig.tag_id`, `ThreeDCarouselConfig.tag_id`, `ToggleViewConfig.tag_id`, `ChartConfig.tag_id`
- `request_url` on `LiveContentConfig`, `WebSocketConfig`, `ChatConfig`, `InfiniteScrollConfig`, `PaginationConfig`
- `FilterConfig.name`, `QueryBuilderFieldConfig.field`
- `BadgeListConfig.tag_id` and `BadgeListConfig.label`

Before:

```python
ButtonConfig(label="", icon_only=True)
```

After:

```python
ButtonConfig(label="Close", icon_only=True)
```

Search: `label=""` and `label=''` on buttons, and config calls whose id, name
or URL comes from a variable that can be empty.

[#722](https://github.com/alpininsight/insight-ui/pull/722).
`DataAttrConfig.name` is required and must match `[a-z0-9]+(-[a-z0-9]+)*`.
`testId` raises `ValueError`. Use `testid` or `test-id`.

Before:

```python
DataAttrConfig(name="testId")
```

After:

```python
DataAttrConfig(name="testid")
```

Search: `DataAttrConfig(`.

[#726](https://github.com/alpininsight/insight-ui/pull/726) renders the HTML
`required` attribute on `select`, `checkbox` and `toggle` when `required=True`.
The required asterisk is `aria-hidden="true"`. v1.15.1 used
`aria-label="Required"` on the input, select and textarea asterisk.

### Help, error and disabled texts

[#746](https://github.com/alpininsight/insight-ui/pull/746).

`explanation` showed a tooltip icon next to the label. Tooltips are not
reachable by keyboard or touch, so it is replaced by `help_text`, a visible hint
below the field. Every form field has `help_text` and `error_text`: input,
textarea, select, checkbox, toggle, slider and multiselect, plus checkbox group,
radio group and radio block. `FilterConfig` has `help_text`.
`PaginationIppConfig.explanation` is removed without a replacement; the label
names the selector.

Before:

```python
SelectConfig(name="country", label="Country", options=countries, explanation="Where you live.")
```

After:

```python
SelectConfig(name="country", label="Country", options=countries, help_text="Where you live.")
InputFieldConfig(name="email", label="E-Mail", error_text="Enter a valid address.")
```

The texts are plain paragraphs below the field, linked with
`aria-describedby` in the order help, disabled reason, error. An `error_text`
also sets `aria-invalid="true"` and `aria-errormessage`. The IDs are
`<tag_id>-help`, `<tag_id>-disabled` and `<tag_id>-error`, or derived from
`name` without a `tag_id`. A checkbox group only links the texts, because a
plain fieldset does not support `aria-invalid`.

`disabled_reason` on form fields and on checkbox and radio options used to be a
hover tooltip. A disabled control can neither be focused nor show a tooltip, so
the reason is now visible text below the field or option. Buttons keep the
tooltip for now.

Radio groups and radio blocks render `role="radiogroup"` on their fieldset,
named by the legend through `aria-labelledby`. Checkbox and toggle templates
wrap the control and its texts in a `<div>`. The form's error container now has
`role="alert"` and `aria-atomic="true"`, so text swapped into it is announced.

Search: `explanation=`, `data-insight-tooltip` on form fields and selectors that
expect a checkbox or toggle `<input>` as the outermost element.

## Markup selectors

[#734](https://github.com/alpininsight/insight-ui/pull/734),
[#713](https://github.com/alpininsight/insight-ui/pull/713) and
[#726](https://github.com/alpininsight/insight-ui/pull/726).

Footer section titles (`description`, Links, Contact) are `h2`. They were `h4`.

Sidebar headings stay in order and carry `data-sidebar-heading`. The title is
`h2` when it is set. The categories title is `h3` when a title is also set,
and `h2` when the title is omitted. A category heading is one level below the
categories title, or the same level as the section when that title is omitted.
v1.15.1 always used `h2`, then `h3`, then `h4`. A category heading is `h4`
only when both the title and the categories title are rendered. Style and
scripts should use `[data-sidebar-heading]`.

`heading_level` on card, app card, flip card, accordion and infinite scroll
defaults to `3`, so an existing `h3` selector still matches until a host sets
another level. Allowed values are 2–6.

The icon wrapper is `<span class="inline-flex">`. It was a `<div>`.
Tooltip wrappers on input, select and textarea are `<span>`. They were
`<div>`. The accordion chevron wrapper is `[data-accordion-chevron]`.

Before:

```css
footer h4 { }
button > div { }
```

```html
<span aria-label="Required">*</span>
```

After:

```css
footer h2 { }
button .inline-flex { }
```

```html
<span aria-hidden="true">*</span>
```

[#736](https://github.com/alpininsight/insight-ui/pull/736) adds
`rtl:-scale-x-100` to directional arrow and chevron icons unless
`mirror_rtl` is set. Right-to-left pages mirror those icons.
`IconConfig.mirror_rtl` and the tag argument `icon_mirror_rtl` override it.

Search: `footer h4`, `button > div`, `aria-label="Required"`,
`data-accordion-chevron`.

### Disabled link buttons

[#718](https://github.com/alpininsight/insight-ui/pull/718).

`ButtonConfig(disabled=True)` keeps its color; see
[Button and badge color and variant](#button-and-badge-color-and-variant).
A link (`request_url` set) renders `aria-disabled="true"` and omits `href`,
`htmx_attributes` and `hx_*`. v1.15.1 already omitted `href`, and it still
wrote `disabled` plus the HTMX attributes. A `<button>` still uses the
`disabled` attribute.

Before:

```html
<a disabled hx-get="/save/" hx-target="#main">Save</a>
```

After:

```html
<a aria-disabled="true">Save</a>
```

Search: `a[disabled]`, and tests that expect `hx-` on a disabled link.

### Form error container and indicator

[#711](https://github.com/alpininsight/insight-ui/pull/711).

The error container id is `<tag_id>-error` when `FormConfig.tag_id` is set,
and `form-error` only when it is empty. The form indicator is
`find .htmx-indicator`, so only that form's indicator is shown.
`show_loading_indicator=False` omits it. v1.15.1 used `hx-indicator=".htmx-indicator"`,
which matched every indicator on the page.

Before:

```python
response["HX-Retarget"] = "#form-error"
```

After:

```python
response["HX-Retarget"] = "#contact-error"
```

Search: `#form-error`, `HX-Retarget` and `hx-target="#form-error"`.

## HTMX

[#718](https://github.com/alpininsight/insight-ui/pull/718).

### `HtmxConfig.trigger` is gone

The trigger is fixed by the component. Passing `trigger=` raises `TypeError`.

| Component | Trigger |
| --- | --- |
| Buttons and links | HTMX default for that element (click) |
| `form` | `submit` |
| `generic_filter` | `submit, change` |
| `live_content` | `load, every <interval>s` |
| Search bar | the form default, so the button and Enter submit |

Before:

```python
HtmxConfig(request_url="/search/", target="#results", trigger="keyup changed delay:300ms")
```

After, drop `trigger` for the component default, or render your own element
and pass the trigger to the tag:

```python
HtmxConfig(request_url="/search/", target="#results")
```

```text
{% load insight_tags %}
{% htmx_attributes htmx trigger="keyup changed delay:300ms" %}
```

Search: `HtmxConfig(` and `trigger=`.

### `htmx_config` is now `htmx`

`ButtonConfig`, `FormConfig`, `SearchBarConfig` and `GenericFilterConfig`
named their `HtmxConfig` field `htmx_config`. Every other component calls it
`htmx`, so these four follow. The tag arguments of `button`, `form`,
`search_bar` and `generic_filter` change the same way. The old name raises
`TypeError`.

Before:

```python
ButtonConfig(label="Delete", htmx_config=HtmxConfig("/items/7/delete/", method="post"))
```

```text
{% button label="Load" htmx_config=htmx %}
```

After:

```python
ButtonConfig(label="Delete", htmx=HtmxConfig("/items/7/delete/", method="post"))
```

```text
{% button label="Load" htmx=htmx %}
```

Search: `htmx_config`.

### `swap_method` is applied

These templates used to read a `swap` attribute that `HtmxConfig` does not
have, so they always wrote `innerHTML`. They now write `swap_method`
(default `innerHTML`):

- navbar links (the user menu already read `swap_method`)
- footer links
- `sidebar_nav`
- search bar
- `generic_filter`
- `form`
- `bullet_point_list`

A config that set `swap_method="outerHTML"` on one of these components used
to be ignored. It is now sent. Dropdown and breadcrumbs already honored
`swap_method` in v1.15.1.

Search: `swap_method=` on navbar, footer, sidebar, search, generic filter,
form and bullet list configs.

### `hx-push-url="false"` is omitted

When `push_url` is false, `htmx_attributes` leaves the attribute off. HTMX
then inherits `hx-push-url` from an ancestor. An explicit `false` used to
block that.

This changed for dropdown items, navbar user-menu items and the search bar.
Buttons and breadcrumbs already omitted the attribute when `push_url` was
false. Navbar links, footer links, `sidebar_nav` and `generic_filter` still
force `hx-push-url="true"`.

The search bar no longer defaults `hx-indicator` to `#loading-indicator`.
Set `HtmxConfig.loading_indicator_id` when that request needs an indicator.

Before:

```html
<a hx-push-url="false" hx-get="/item/">Item</a>
```

After, with `push_url=False`, the attribute is absent. Set it on a wrapper
when a parent must not push:

```html
<div hx-push-url="false">
    <a hx-get="/item/">Item</a>
</div>
```

Search: `push_url=False` and `hx-push-url="false"` on dropdowns, the user
menu and the search bar.

A link button whose `HtmxConfig` has no `request_url` now requests the link
`href`. Setting both `ButtonConfig.request_url` and
`HtmxConfig.request_url` no longer warns. The HTMX URL is the config URL
when it is set.

### Live content, chat and tabs take an `HtmxConfig`

`live_content`, `chat` and `{% tabs %}` now render their requests through
`htmx_attributes` and accept an optional `htmx` for the shared options
(`vals`, `loading_indicator_id`, `swap_settle`, `confirm`,
`show_global_loading_indicator`, and where it fits `target`, `swap_method` and
`push_url`). What the mechanism needs stays fixed by the component:

| Component | Fixed by the component |
| --- | --- |
| `live_content` | URL, trigger `load, every <interval>s`, its own indicator |
| `chat` | URL, `hx-post`, target `#<tag_id>-response`, swap `beforeend` |
| `{% tabs %}` | tab URL, target `#<id>-tab-content`, swap `innerHTML`, trigger |

`LiveContentConfig.show_global_loading_indicator` is gone. Polling still stays
out of the global loading bar by default.

Before:

```text
{% live_content request_url="/stats/" show_global_loading_indicator=True %}
```

After:

```python
HtmxConfig(show_global_loading_indicator=True)
```

```text
{% live_content request_url="/stats/" htmx=htmx %}
```

`HtmxConfig.show_global_loading_indicator` now defaults to `None`, which keeps
the default of the component: shown for user actions, hidden for
`live_content`. `True` and `False` behave as before.

`chat` used the fixed IDs `response` and `msg`. They are now
`<tag_id>-response` and `<tag_id>-message`, with `tag_id` defaulting to
`chat`. The input name stays `msg`. Two chats on one page need different
`tag_id` values.

Tabs with `push_url=True` push the URL of a clicked tab. The active tab loads
on page view without pushing its fragment URL.

Search: `show_global_loading_indicator=` on `live_content`, `#response` and
`#msg` in host CSS, JavaScript or tests.

### `radio_block` takes an `HtmxConfig`

`RadioBlockConfig.hx_target_id` and `hx_swap_method` are gone. The options
send a request only when the block has an `htmx`, like the other components.
`request_url` stays the URL of that request.

| v1.15.1 | 2.0 |
| --- | --- |
| `hx_target_id="content"` | `htmx=HtmxConfig(target="#content")`, with the `#` |
| `hx_swap_method`, default `outerHTML` | `htmx.swap_method`, default `innerHTML` |
| `request_url` alone sent no request | Unchanged: no `htmx`, no request |

The default swap changes with the field. Set `swap_method="outerHTML"` to keep
replacing the target itself. A block with `htmx` needs a URL and `htmx.target`;
an `integrated=True` block is sent with its form, so `htmx` there raises
`ValueError` instead of being ignored.

Before:

```python
RadioBlockConfig(name="view", items=items, request_url="/products/", hx_target_id="products")
```

After:

```python
RadioBlockConfig(
    name="view",
    items=items,
    request_url="/products/",
    htmx=HtmxConfig(target="#products", swap_method="outerHTML"),
)
```

`toggle_view` sets target and swap of its view switch itself, as before: the
switch replaces the whole toggle view. Other options of the switch's
`HtmxConfig`, such as `push_url`, are kept.

Search: `hx_target_id` and `hx_swap_method`.

## Pagination

[#738](https://github.com/alpininsight/insight-ui/pull/738).

### HTMX is opt-in

v1.15.1 always sent HTMX requests into `#list-container`, included `#ipp` and
showed the global loading bar. Pagination now renders plain links. Pass an
`HtmxConfig` to swap the result instead; `include` sends further fields, for
example a filter form, with every request:

Before:

```python
PaginationConfig(request_url="/products/", current_page=page, surrounding_pages=pages)
```

After:

```python
PaginationConfig(
    request_url="/products/?q=chair",
    current_page=Paginator(products, 10).get_page(request.GET.get("page")),
    htmx=HtmxConfig(target="#list-container", push_url=True),
    include="#product-filter",
)
```

The tag builds the page URLs from `request_url` and keeps its query string, so
filters survive paging. `page_param` changes the parameter name (default
`page`). Without `htmx`, the page size selector gets an "Apply" button.

### `get_page` and `surrounding_pages` are gone

`insight_ui.utils.pagination` is removed. Use Django's
`Paginator(...).get_page(...)`. The visible page numbers now come from
`get_elided_page_range`; `on_each_side` (default 2) and `on_ends` (default 1)
replace `surrounding_pages`.

For an API that pages itself and only reports the total, page a range:

```python
page = Paginator(range(total), items_per_page).get_page(request.GET.get("page"))
```

### IDs and the page size selector

`ipp_config` is now `items_per_page`. The IDs are derived from `tag_id`
(default `pagination`): the page size form is `#<tag_id>-ipp` instead of
`#ipp`, and two paginations on one page no longer share IDs. The query
parameter of the selector is still `PaginationIppConfig.name` (default `ipp`).

Search: `get_page`, `surrounding_pages`, `ipp_config`, `#ipp` and
`#list-container`.

## Query builder

The `query_builder` component was rebuilt. Its markup, its submitted parameters and
its Python helpers changed, so treat it as a new component.

| v1.15.1 | 2.0 |
| --- | --- |
| `QueryBuilderConfig(model_fields=[...])` | `QueryBuilderConfig(fields=[...])`, plus `tag_id`, `filters`, `request_url`, `param_name`, `max_filters`, `htmx` and `show_summary` |
| `QueryBuilderFieldConfig` without `operations` | `operations` is required; a `choice` field also needs `values` |
| A host view named `get_allowed_operators`, reversed by the template | Not needed. The field definitions are rendered into the page. |
| A JSON `custom_filters` parameter, the page is reloaded by a script | A plain GET form with `filters-<n>-field`, `-operator`, `-value` and `-logic`, or HTMX with `htmx=HtmxConfig(...)` |
| `insight_ui.utils.query_builder_utils` | `insight_ui.utils.query_builder` |
| `get_filter_settings_for_field()` | Removed |
| `build_dynamic_query(filters)` returning `(Q, {}, {})` | `build_query(parse_filters(request.GET, config))` returning a `Q` |

`parse_filters` takes the config, so it reads the same `param_name` and stops at
the same `max_filters` (default 20) as the form. It keeps only filters whose
field, operator and value the field configs allow, and converts values to the
field type. `build_query` keeps the
submitted order and binds AND tighter than OR: "A AND B OR C" is
"(A AND B) OR C". v1.15.1 grouped the filters by field first.

Field, condition and value are required in the browser, so an incomplete
filter is not sent. With active filters a Reset link loads `request_url`
without them. `describe_filters(filters, fields)` returns the active
filters as a sentence with the labels, e.g. for a page title or an HTMX
response; `show_summary=True` renders it below the form.

Before:

```python
from insight_ui.utils.query_builder_utils import build_dynamic_query

filters = json.loads(request.GET.get("custom_filters", "[]"))
query, _, _ = build_dynamic_query(filters)
context["query_builder"] = QueryBuilderConfig(model_fields=FIELDS)
```

After:

```python
from insight_ui.utils.query_builder import build_query, parse_filters

config = QueryBuilderConfig(tag_id="book-filter", fields=FIELDS)
config.filters = parse_filters(request.GET, config)
books = Book.objects.filter(build_query(config.filters))
context["query_builder"] = config
```

Remove the `get_allowed_operators` view and its URL pattern.

Search: `model_fields=`, `query_builder_utils`, `get_filter_settings_for_field`,
`build_dynamic_query`, `get_allowed_operators` and `custom_filters`.

## Checked, and not a 2.0 break

These showed up in earlier notes. The current tree does not do them.

- [#696](https://github.com/alpininsight/insight-ui/pull/696) removed `None`
  from list-argument annotations. It did not add a runtime rejection. Omit
  the argument, or pass `[]`. `ensure_list()` still turns `None` into `[]`
  for the descriptions that use it.
- `login.html` is unchanged since v1.15.1, including its `flex flex-1`
  content child. `content_fill` is still only read by `base.html`. The login
  template does not take that variable.
- Disabled previous/next pagination buttons pass `disabled_reason=""`; their
  label already states the reason, so they do not warn.
- `{% navbar %}` without a config renders the brand from `INSIGHT_UI["brand"]`
  and no links. That is additive. An explicit `NavbarConfig` is rendered as
  given.
- Default HTMX script URLs in `base.html` are the same jsDelivr URLs as
  v1.15.1, now loaded by `{% insight_htmx_scripts %}` from `INSIGHT_UI["htmx"]`.
  Set `INSIGHT_UI["htmx"]["src"]` to `""` when the host loads HTMX itself.
  The keys are `src`, `integrity`, `ws_src` and `ws_integrity`.
- No file under `insight_ui/static/insight_ui/` was renamed.
  `js/insight-ui-badge-list.js` is new and imported by `insight-ui-init.js`.
  Tracked `*.min.css` and `*.min.js` files were absent in v1.15.1 and are
  absent here. [#749](https://github.com/alpininsight/insight-ui/pull/749)
  restored the CI check that keeps them untracked.
  `assets.use_minified` still resolves to the readable package files.
- Tailwind utilities are generated from the package sources. A class that
  appears only in a host template is not in `tailwind.css`. That was already
  the case. Host utilities belong in the host build.
- Context processors, `get_config()` and the public asset URL helper are
  unchanged apart from the new `INSIGHT_UI` keys above and `tooltip_show_delay`.
  With `assets.cdn_enabled`, the asset helper now keeps paths outside
  `insight_ui/` local, so a host's own `INSIGHT_UI["stylesheet"]` no longer
  points at the package CDN, where it never existed.
- `INSIGHT_UI["use_tailwind_cli"]` is gone. It never took effect: the template
  it included only loaded the `tailwind_cli` tag library, which does not reach
  `base.html`. Running `manage.py tailwind runserver` needs only
  `django_tailwind_cli` in `INSTALLED_APPS`; load its output through
  `INSIGHT_UI["stylesheet"]`. Delete the key; a leftover one is ignored.
- `shadow-insight-*` classes render the same shadows. They now read the
  `--shadow-insight-*` variables at runtime, so a theme stylesheet can change
  them; the shadow color modifier (`shadow-insight-raised/50`,
  `shadow-red-500` on the same element) no longer applies to them.

Other additions you can adopt without a rename: `INSIGHT_UI["theme_stylesheet"]`
for brand tokens without a Tailwind build (see
[theming a host](design-system.md#theming-a-host)), `download` on link buttons
(`True` or an empty string uses the default filename; a string suggests one), `heading_level`,
`BadgeListConfig`, `MessageDialogConfig`, `data_attrs` on form fields,
`required` on checkbox and toggle, removable badges,
`LegalNoticeConfig.holder_url` / `holder_logo`, the `method`, `target`,
`swap` and `global_indicator` overrides of `{% htmx_attributes %}` for host
markup that fixes those values itself, and
`{% sidebar width="fit" %}` with `min_width` / `max_width` (`narrow`,
`normal`, `wide`; the upper limit defaults to `wide`). The sidebar content
column now fills the sidebar height, so `mt-auto` moves an element to the
bottom.

## Pending before 2.0.0

These pull requests are open. They are not merged, and they are not part of
the tree this guide describes. Do not migrate a host to them yet.

| Pull request | State | What it would change if it merged |
| --- | --- | --- |
| [#744](https://github.com/alpininsight/insight-ui/pull/744) | Open, stacked on #743 | Outline hover and active ink would use the shared on-action token. Host `.btn-outline-<family>` rules would stop applying. |

[#739](https://github.com/alpininsight/insight-ui/pull/739) and
[#740](https://github.com/alpininsight/insight-ui/pull/740) are a 1.15
maintenance path. They are not part of this 2.0 line.
