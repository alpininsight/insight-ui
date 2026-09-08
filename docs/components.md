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
| Contributor examples | [component_manifest.py](../insight_ui/component_manifest.py) | Schema/loader for generated `insight_ui/component_manifests/<slug>.json` files. |
| Generator | [scaffolding.py](../insight_ui/scaffolding.py) | Source-checkout generation, exports, tags, composition and tests. |
| Regression tests | [Python tests](../tests/insight_ui/) and [Vitest tests](../tests/js/) | Public behavior, escaping, edge cases and lifecycle. |

Use the Config's real fields and tag signature. Not every tag accepts arbitrary
keyword arguments or a dictionary. For example, `navbar` requires a `config`
argument and does not use the shared Config builder. Type annotations alone do
not validate every value; check the Config constructor and rendering tests.

## Configs And Supported Overrides

The button supports both inline arguments and Config objects:

```python
from insight_ui.configs import ButtonConfig

save_button = ButtonConfig(label="Save", type="primary", button_type="submit")
```

```django
{% load insight_tags %}
{% button label="Save" type="primary" button_type="submit" %}
{% button config=save_button %}
{% button config=save_button label="Save changes" %}
```

Pass `save_button` in the host view's template context. `type` selects the visual
variant; `button_type` selects the HTML button type.

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

## Manifest And Preview

The generator creates declarative examples and source references alongside the
component. Each example must have a unique name, and a `default` example is
required. Validate examples with `build_example_config()` from
`component_manifest.py`, which constructs Configs through the shared builder,
including nested Config mappings. Examples are JSON data, not Python to evaluate.

The local preview and downstream hosts can consume the same manifest and Config
metadata. Keep host catalogs and editorial content outside the package. See the
[new component checklist](new-component-checklist.md).

[All package guides](README.md)
