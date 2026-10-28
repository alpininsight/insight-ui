<!--
SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
SPDX-License-Identifier: AGPL-3.0-only
-->

# Components And Composition

This is the package architecture for contributors, not a duplicate component
catalog. Start with [getting started](getting-started.md) for host setup or
[CONTRIBUTING.md](../CONTRIBUTING.md) for generation and local preview.

## Source Of Truth

| Part | Source | Responsibility |
| --- | --- | --- |
| Config | [configs/](../insight_ui/configs/) | Dataclass fields, defaults, implemented validation, `field(metadata={"doc": ...})` and examples. |
| Public Config exports | [configs/__init__.py](../insight_ui/configs/__init__.py) | Importable package API; do not create a parallel schema. |
| Template tags | [insight_tags.py](../insight_ui/templatetags/insight_tags.py) | Django API and normalization of supported arguments. |
| HTML | [component templates](../insight_ui/templates/insight_ui/components/) | Semantics, composition, ARIA and behavior hooks. |
| Design roles | [input.css](../insight_ui/utils/input.css) | Shared colors, surfaces, typography, radii and shadows. |
| Optional behavior | [JavaScript modules](../insight_ui/static/insight_ui/js/) | Events, state, initialization and cleanup. |
| Regression tests | [Python tests](../tests/insight_ui/) and [Vitest tests](../tests/js/) | Public behavior, escaping, edge cases and lifecycle. |

Use the Config's real fields and tag signature. Not every tag accepts arbitrary
keyword arguments or a dictionary. `{% navbar %}` without a config renders the
brand from `INSIGHT_UI["brand"]` and no links. A `NavbarConfig` is passed
through `build_config()`, which rejects a dictionary. Type annotations alone do
not validate every value; check the Config constructor and rendering tests.

## Configs And Supported Overrides

The button supports both inline arguments and Config objects:

```python
from insight_ui.configs import ButtonConfig

save_button = ButtonConfig(label="Save", color="primary", button_type="submit")
```

```django
{% load insight_tags %}
{% button label="Save" color="primary" button_type="submit" %}
{% button config=save_button %}
{% button config=save_button label="Save changes" %}
```

Pass `save_button` in the host view's template context. `color` and `variant`
(solid, outline, subtle, link, plain) select the look; `button_type` selects the HTML button type.

With an existing Config, `build_config()` returns a copy with supplied overrides.
Generated tags forward only supplied `**kwargs`; they do not declare `UNSET`
defaults. When adding explicit optional arguments, follow `button()`'s `UNSET`
pattern so omission does not overwrite a Config value. `False` is an override;
`None` is also an override, valid only where the field allows it. Keep field
types, metadata, examples and rendering tests aligned.

The button also supports documented `data_*`, `aria_*` and `hx_*` arguments:

```django
{% load insight_tags %}
{% button label="Open menu" data_insight_dropdown="actions" aria_controls="actions" aria_expanded="false" %}
```

Underscores become hyphens and values become strings. Supplying `data_*`,
`aria_*` or `hx_*` replaces that Config attribute list, rather than appending to
it. This example supplies only a trigger; the host must supply the target element
and required JavaScript. An attribute alone does not implement an interaction.
Do not assume these extra arguments exist on every other template tag.

### Native link downloads

Set `download=True` on a link button to download its target, or pass a string
such as `download="report.svg"` to suggest a filename. Downloads require
`request_url` and cannot be combined with HTMX request settings.

## HTMX Requests

Components that send requests take an optional `htmx: HtmxConfig` for the options
shared by all components: target, swap method, method, push URL, indicator,
confirm, vals and the global loading bar. Templates render it only through
`{% htmx_attributes %}`; a test rejects direct field access.

What a component's mechanism needs is fixed by the component and passed to
`htmx_attributes` as an override: its own URL (`request_url`), `trigger`,
`target`, `swap`, `method`, `indicator`, `push_url` and `global_indicator` for
background requests. For example, the chat always posts and appends to its own
response container; `live_content` polls with its interval and stays out of the
global loading bar unless the Config asks for it.
`HtmxConfig.show_global_loading_indicator=None` keeps that component default.

## Find A Component's Arguments

This guide is not a catalog. The full per-component reference with live examples
is at [django-insight-ui.com](https://django-insight-ui.com/docs/configs). In an
installed package the same information comes from the source of truth above:

- the tag signature in [insight_tags.py](../insight_ui/templatetags/insight_tags.py),
- the Config's docstring `Attributes`, each field's `metadata["doc"]`, its default
  and the `__example__` constructor.

```python
from dataclasses import MISSING, fields

from insight_ui.configs import FormConfig

for config_field in fields(FormConfig):
    default = "required" if config_field.default is MISSING else repr(config_field.default)
    print(config_field.name, default, config_field.metadata.get("doc", ""))
print(FormConfig.__example__)
```

Common options can also be passed directly to the tag. For example,
`{% form title="Contact" fields=fields submit_label="Send" method="get" %}`
works without building a `FormConfig` in Python.

## Atomic Composition

| Level | Responsibility |
| --- | --- |
| Atom | One small reusable primitive with a clear contract. |
| Molecule | A focused combination of existing components. |
| Organism | A larger reusable section composed from existing components. |

Atomic level and category are independent metadata, not new Config inheritance
trees. Molecules/organisms should call existing child tags with child Configs;
do not copy their HTML, event handling or token definitions. Authentication,
database queries and product-specific catalog state belong in the host.

## Scaffolding And Preview

The `create_component` management command scaffolds new components with minimal
boilerplate. Run `uv run python manage.py create_component --name "My Widget"`
to generate a template, config dataclass, and tag registration. Keep host
catalogs and editorial content outside the package. See the
[new component checklist](new-component-checklist.md).

[All package guides](README.md)
