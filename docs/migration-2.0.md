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
- [ ] Replace `#loading-indicator` and stop relying on an `hx-indicator` inherited from `<body>`.
- [ ] Check first paint when the visitor has not saved a theme, including a dark operating system.
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
- [ ] Replace `FormFieldConfig` with the concrete field config. Pass `name=` as a keyword.
- [ ] Give every button a non-empty label, and give ids, names and URLs that the configs now require.
- [ ] Use lowercase hyphenated `DataAttrConfig` names.
- [ ] Remove `trigger=` from `HtmxConfig`.
- [ ] Rename `htmx_config=` to `htmx=` on buttons, forms, the search bar and `generic_filter`.
- [ ] Rename `badge_config=` (hero), `table_config=` and `view_radio_config=` (toggle view), `usermenu=` (navbar) and `empty_msg=` (table).
- [ ] Re-check `swap_method` on navbar, footer, sidebar, search, generic filter, form and bullet lists.
- [ ] Re-check `push_url=False` on dropdown items, the navbar user menu and the search bar.
- [ ] Move `show_global_loading_indicator=` from `live_content` into its `HtmxConfig`, and give a second `chat` on a page its own `tag_id`.
- [ ] Leave button `type`, pagination helpers and `explanation` as they are until the open pull requests in [Pending before 2.0.0](#pending-before-200) merge.

## Color tokens are a silent break

[#693](https://github.com/alpininsight/insight-ui/pull/693) renamed the six families
`primary`, `secondary`, `success`, `warning`, `danger` and `info`.
The old names still match a real token, and the meaning has changed.

| v1.15.1 | Meaning then | 2.0 name |
| --- | --- | --- |
| `--color-insight-<family>-text` | White text on a filled button | `--color-insight-<family>-on-fill` |
| `--color-insight-<family>-foreground` | Colored text and icons | `--color-insight-<family>-text` |
| `--color-insight-<family>-foreground-dark` | Same color in the dark theme | `--color-insight-<family>-text-dark` |

Utility classes follow the variable name. `text-insight-danger-foreground`
becomes `text-insight-danger-text`. The same substring is in `bg-`, `border-`
and other utilities generated from that token.

A host rule that still says `text-insight-primary-text` compiles. In v1.15.1
that class was white text on a filled button. It is now the colored text tone
(`#0856C0` in the light theme).

Do the replacement in this order. Pass 2 writes the new `-text` names. Running
it first makes a later `-text` → `-on-fill` pass rewrite those names as well.

```bash
# 1. Old on-fill token. The (?!-) skip keeps a later -text-dark result intact.
perl -pi -e 's/insight-(primary|secondary|success|warning|danger|info)-text(?!-)/insight-$1-on-fill/g' FILES

# 2. Old colored-text token, including the -dark variant.
perl -pi -e 's/insight-(primary|secondary|success|warning|danger|info)-foreground/insight-$1-text/g' FILES
```

Limit both passes to those six families. A global `-text` → `-on-fill` replace
also rewrites `--color-insight-text-body`, `--color-insight-text-headline`,
`--color-insight-text-muted` and `--color-insight-text-link`. Those names did
not change. There is no `-on-fill-dark` token. The old on-fill value was
`#FFFFFF` in both themes.

Before:

```html
<button class="bg-insight-danger-action text-insight-danger-text">Delete</button>
<p class="text-insight-danger-foreground">Something failed.</p>
```

After:

```html
<button class="bg-insight-danger-action text-insight-danger-on-fill">Delete</button>
<p class="text-insight-danger-text">Something failed.</p>
```

Search:

```text
insight-(primary|secondary|success|warning|danger|info)-(text|foreground)
```

Review matches of `-text` before editing. A match that is already the colored
text tone on a migrated tree must stay `-text`.

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

Button `type` and badge `type` are still the color token. This rename does
not touch them.

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

`explanation` was added to `InputFieldConfig`, `TextareaConfig` and the
`input_field` and `textarea` tags. `SelectConfig.explanation` was already
there. [#746](https://github.com/alpininsight/insight-ui/pull/746) would
rename `explanation` to `help_text` and is not merged. Keep the current field
if you already pass it, and wait before renaming a host to `help_text`.

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

`ButtonConfig(disabled=True)` still sets `type` to `"disabled"`.
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

## Checked, and not a 2.0 break

These showed up in earlier notes. The current tree does not do them.

- [#696](https://github.com/alpininsight/insight-ui/pull/696) removed `None`
  from list-argument annotations. It did not add a runtime rejection. Omit
  the argument, or pass `[]`. `ensure_list()` still turns `None` into `[]`
  for the descriptions that use it.
- `login.html` is unchanged since v1.15.1, including its `flex flex-1`
  content child. `content_fill` is still only read by `base.html`. The login
  template does not take that variable.
- Pagination still renders `hx-target="#list-container"` and
  `hx-indicator="#insight-global-loading-indicator"`.
  `PaginationConfig.surrounding_pages` still exists and defaults to `[]`.
  `insight_ui.utils.pagination.get_page` still exists.
  Disabled previous/next buttons pass `disabled_reason=""`, so they do not
  warn.
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

Other additions you can adopt without a rename: `heading_level`,
`BadgeListConfig`, `MessageDialogConfig`, `data_attrs` on form fields,
`required` on checkbox and toggle, removable badges,
`LegalNoticeConfig.holder_url` / `holder_logo`, and the `method`, `target`,
`swap` and `global_indicator` overrides of `{% htmx_attributes %}` for host
markup that fixes those values itself.

## Pending before 2.0.0

These pull requests are open. They are not merged, and they are not part of
the tree this guide describes. Do not migrate a host to them yet.

| Pull request | State | What it would change if it merged |
| --- | --- | --- |
| [#733](https://github.com/alpininsight/insight-ui/pull/733) | Open | Button and badge `type` / `outline` / `subtle` would become `color` and `variant` (`solid`, `outline`, `subtle`, `link`, `plain`). |
| [#743](https://github.com/alpininsight/insight-ui/pull/743) | Open, stacked on #733 | A `download` attribute on link buttons. It cannot merge without #733. |
| [#744](https://github.com/alpininsight/insight-ui/pull/744) | Open, stacked on #733 and #743 | Outline hover and active ink would use the shared on-fill token. Host `.btn-outline-<family>` rules would stop applying. |
| [#738](https://github.com/alpininsight/insight-ui/pull/738) | Open | Pagination would render plain links unless you pass an `HtmxConfig`. `surrounding_pages` and `insight_ui.utils.pagination.get_page` would be removed in favor of Django's `Paginator.get_page` and `get_elided_page_range`. |
| [#746](https://github.com/alpininsight/insight-ui/pull/746) | Open | `explanation` would be removed from input, textarea, select, `FilterConfig` and `PaginationIppConfig`. The replacement name in that pull request is `help_text`. `disabled_reason` on form fields would become visible text linked with `aria-describedby`. |

[#739](https://github.com/alpininsight/insight-ui/pull/739) and
[#740](https://github.com/alpininsight/insight-ui/pull/740) are a 1.15
maintenance path. They are not part of this 2.0 line.
