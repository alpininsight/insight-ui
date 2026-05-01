# Documentation architecture

This document explains how Insight UI documentation is structured and where
maintainers should place different kinds of information. Treat these rules as
policy: documentation templates render the docs, but they are not the deepest
source of truth for component behavior, design tokens, or API contracts.

## Source-of-truth policy

| Surface | Responsibility | Rule |
|---|---|---|
| `README.md` | Package overview, install, quick start, and links | Keep it short and user-facing. Link to deeper docs instead of duplicating policy. |
| `docs/design-system-contract.md` | Stable public design contract | Define reusable design concepts, tokens, semantic classes, and contract boundaries. |
| `docs/naming_conventions.md` | Naming rules and hook conventions | Define stable naming for Python, templates, CSS, assets, and `data-insight-*` hooks. |
| `docs/contributing.md` | Contributor workflow and decision rules | Explain how contributors change components, docs, tests, and public contracts. |
| `insight_ui/component_details/*` | Per-component self-documentation data | Own component descriptions, usage examples, parameters, accessibility notes, related topics, and demo context. |
| `insight_ui/templatetags/insight_tags.py` | Django API source of truth | Own template tag signatures, parameter defaults, context normalization, and Django-facing component APIs. |
| `insight_ui/utils/input.css` | Token and reusable class source of truth | Own public tokens, base styles, and semantic reusable classes. Generated CSS is output, not the contract. |
| `insight_ui/static/insight_ui/js/*` | Behavior hook source of truth | Own JavaScript state, lifecycle, event handling, and `data-insight-*` behavior contracts. |
| `insight_ui/templates/insight_ui/docs/*` | Rendered documentation presentation | Compose and present documentation. Do not move canonical behavior, API, or design rules here. |

![Insight UI documentation source-of-truth map](https://kroki.showcase.alpininsight.ai/graphviz/svg/eNp9U02P2jAQvfdXWPS25StAAqhKJQJxeyiX1d6gWpl4SNx17Mg23WWr_vdOCCQBqnJA8_3evHG4SA0rMvKV_P5ASGVvDFMvXJjwKeqSXZpoqU3YcRi1BTOgXKdLCsbDzrA_QVNpDhaK0vV99Mvusx_4nR-fcW5ZQjY2YwWEO_3WJdYdJYQdow-KA-_uhZTAsbc0zngf6Ywu6BKDl8AyWvmxV1Zp5RTLccDCCCbPESveIfRmXZIzkwpV4ntBF_9GFQngKZK4DAsm08kswlZmjH499Q77c1wM1KvgLgu9_gTbsK_QUiRHspFsBzLsPEKhrXDaHC8ZrhO7VY_xYrWO-zknn06RwQPaNyutonhB49ZK42g2okHFL8EdDEtcjbRkSiuRMElEXkjIUXnmhFZ1JaIKZUWauWfHUtsvjogtVHFw_cRatG3ZkAx-IplbcWM6Xk5bTKg_j4dRxcSC3OMKDRGdF1oh_CnTK1OcOdagH8QgudQ8c3BMyHvIeElX1G9BesNoPvMqSAe4InNg_wFa57bKQs4UrkS-Pa2_l0Ijjd6ZRe-BZFq_2GqggVRYZ5q7rfAmJ-XgzdXZrWp4n3OVio1TjSsMvvGL_lcjW-zw2-BggF9XayWPd-rHo3jUkiKmE_xVUDkT2CoUmEaMdSvGFEf-vwS8ooeS6INJoKf3PWcOLiMcEmER197KP4ynlLYwg3EQ0JP8zSPvfWnDX73K_6dqFdrvB-MXoa9vfJOob4XxtnR3wt9y-PMXOoWTqQ)

<details>
<summary>Diagram source</summary>

```dot
digraph G {
  graph [rankdir=TB, bgcolor="transparent", pad="0.4", nodesep="0.55", ranksep="0.65"];
  node [shape=box, style="rounded,filled", fillcolor="#F8FAFC", color="#CBD5E1", fontname="Arial", fontsize=18, margin="0.16,0.12"];
  edge [color="#64748B", arrowsize=0.9, penwidth=1.4];

  policy [label="Repository policy docs\nREADME.md + docs/*.md", fillcolor="#DBEAFE", color="#3B82F6"];
  contract [label="Canonical implementation contracts\ninsight_tags.py + input.css + static/js/*", fillcolor="#FEF3C7", color="#F59E0B"];
  selfdoc [label="Component self-doc data\ninsight_ui/component_details/*", fillcolor="#ECFDF5", color="#10B981"];
  templates [label="Component templates\nsemantic HTML + data-insight-* hooks"];
  registry [label="Docs context registry\ncomponent_context.py + context.py"];
  presentation [label="Docs templates\nrendered presentation only", fillcolor="#FEE2E2", color="#EF4444"];
  maintainers [label="Maintainers and reviewers\nsource-of-truth decisions", fillcolor="#E0E7FF", color="#6366F1"];

  policy -> maintainers;
  contract -> maintainers;
  contract -> templates;
  selfdoc -> registry;
  templates -> registry;
  registry -> presentation;
  presentation -> maintainers;
}
```

</details>

## Documentation pipeline

The self-documenting application is built from three layers:

1. Component context data in `insight_ui/component_details/`.
2. Django views and context helpers that assemble page context.
3. Documentation templates that render the assembled context into full pages or
   HTMX partials.

`component_context.py` is the registry for per-component documentation. Context
builders use `@register_component(Component.X)` and contribute dictionaries for
description, usage, parameters, accessibility, and related topics.

`component_detail_page_view()` receives a component name, resolves the
registered context with `get_component_context(Component(component_name))`, adds
demo metadata, and renders either `component_detailpage.html` or the HTMX
partial `component_detailpage_partial.html`.

`storybook_view()` receives a component category, uses `get_storybook_context()`
from `context.py`, and renders either `storybook.html` or
`storybook_partial.html`. The shared component list presentation lives in
`storybook_content.html`.

![Insight UI component documentation pipeline](https://kroki.showcase.alpininsight.ai/graphviz/svg/eNqVU0tv2zAMvu9XCNllDyeN83ASDB5QJ9aGAbusPQxohkCJGEetLBmSsjQr-t9H-RWvPc2HmKTJ7-NHMlxkhhUH8oU8vSGksu8MUw9cmPg2Ccg222mpTdxzGLUFM6BcLyAF43FvOJigqTQHC4V3p1P0fXXtR9Per0-I61PInT2wAuKtfgyIdWcJcc_oo-LAg72QEjjWeqPme0vn9JouMdgElslqmoY-SyunWI4A10YwWUes-ANxOA9IzkwmlOcPowB_RlUTwDNsogGLJrPJPMFSZow-lbXDwQKFgToJ7g5xOJhgGdZhkw4LJduCjHsrvbNVaK2uODpXO50XWuFY7NVTaz-_ELNK0muadsSMk_mIRlVnvwWcLgT3TGW6jK1Vi7fh4JiQm4JlsPHfqkoDmbDOnNvqH01Aav1wLNYqA7e5oOxwTvDo3i2byPsKp0K3LcwNyH0f1ZFc86MEu8Y12Z0RhRNaBeRosQ1_BIblFkcYhmfcO0jmXm0xXdIVnXaEh8NkMQ8b2lxfhHunbvBf5bkuJZOPZUEjYlCcKxQ_kw6KV0Ic5IVvBzvfH6WscrQhX2-___R9u_puuveWpqN01Ok0pRN8Ko6tPxIwnTnjRAxw4k-gRH-pe5jOKO2gReMoorVuoYRrob7dEFAHpnaQo9y1EsqK7OD6R9H3eYN7S9jeIbc9scK-apqOl7MODZ0u0mFS0dTLa5narV_WWjMTzhzrN8wfyAGv5z-o2n9J_3N1zPhuTxPt5rzQLBeB73qg7fmXWXgAdUo7JfQbGd2q57_EZYs7)

<details>
<summary>Diagram source</summary>

```dot
digraph G {
  graph [rankdir=TB, bgcolor="transparent", pad="0.4", nodesep="0.55", ranksep="0.65"];
  node [shape=box, style="rounded,filled", fillcolor="#F8FAFC", color="#CBD5E1", fontname="Arial", fontsize=18, margin="0.16,0.12"];
  edge [color="#64748B", arrowsize=0.9, penwidth=1.4];

  route [label="Docs route\n/docs/components/{component}", fillcolor="#DBEAFE", color="#3B82F6"];
  view [label="Django view\ncomponent_detail_page_view"];
  registry [label="Registry lookup\nget_component_context(Component)"];
  details [label="Self-doc modules\ndescription, usage, params, a11y, related", fillcolor="#ECFDF5", color="#10B981"];
  demo [label="Demo context\ncomponent_demo_view + demo_context.py"];
  page [label="Detail templates\nfull page or HTMX partial", fillcolor="#FEE2E2", color="#EF4444"];
  browser [label="Rendered docs page", fillcolor="#E0E7FF", color="#6366F1"];
  init [label="JS enhancement\ninsight-ui-init.js after swaps", fillcolor="#FEF3C7", color="#F59E0B"];
  modules [label="Component modules\nenhance data-insight-* hooks", fillcolor="#FEF3C7", color="#F59E0B"];

  route -> view -> registry -> details -> page -> browser;
  view -> demo -> page;
  init -> modules -> browser;
}
```

</details>

## Runtime layers

Insight UI components should stay aligned across these runtime layers:

| Layer | Canonical location | Responsibility |
|---|---|---|
| Django template tag API | `insight_ui/templatetags/insight_tags.py` | Public Django-facing signature, defaults, and normalized context. |
| Component HTML | `insight_ui/templates/insight_ui/components/` | Semantic structure, ARIA, data hooks, and default Tailwind implementation. |
| Design tokens and classes | `insight_ui/utils/input.css` | Theme tokens, base styles, and reusable semantic classes. |
| JavaScript behavior | `insight_ui/static/insight_ui/js/` | Initialization, lifecycle, state, events, and hook behavior. |
| Self-doc data | `insight_ui/component_details/` | User-facing component explanation, examples, parameter docs, and accessibility notes. |
| Rendered docs presentation | `insight_ui/templates/insight_ui/docs/` | Layout and display of docs pages, demos, storybook pages, and HTMX partials. |

`insight-ui-init.js` imports component modules, exposes them through
`window.InsightUI`, initializes all components on `DOMContentLoaded`, and
re-initializes after HTMX swaps. Component modules must therefore be safe to run
more than once on the same DOM by using their singleton/lifecycle pattern.

## Where a concern belongs

Use this routing rule when reviewing or implementing documentation changes:

![Insight UI documentation change routing](https://kroki.showcase.alpininsight.ai/graphviz/svg/eNpdUk1PGzEQvfMrrO0NsgEKoZHQVspnpUq9UG6kQhN7smvFO3ZtL5Ci_veOdzdpws3z5s1782GlSw-uEt_E-5kQ3fvJA22V9sXjdCDWpbTG-iKLjAYHHilmA-FAFdnV8JafZBUGdCm8GXGcqvt4NMp-3bNuooinUIHDYm3fBiLEncEi87YhhWqw0cag4tr06P0-LcfLyXLG4B6YTeejxXViWYoENQtMvAbTI0H_weL6qjVEVbLhvvDu9svteMo08N6-tryr4ZiJzJQVUOIaWKMpslkXevzdYIgfOppPF5Pl4qijm-n48_KumzHaLdJB57GNrBcBa6CopZAGQliRJtfEoQxBXAjemy4pD7sQsc4lz-BBxmGtVnTBHrWzxNtmCbPJlZVCb8SLDnptsLeE8r8h1s5AxBZMshAbj8mPgyo-MxyGbseufEPeXUT_nBzxLTKcDJsAJR5hTI28g9B5VdZuD2YKIuS9cn7e5lb0_aeorWoMtoVdN0mXL6WpTMIvPI22FHhC5uzH6vSd509EERLh4DO3MpxmLBludi8fLrk-XJ6viKyQQJa0BCOMLXnhFfp-T84aLXcH1Qd0Nuho_a7PrKiTaTdvNG3FxttaPCwm8x8L8VrxJZuAPt-A5Emyk4-Tf-0uf38KQXkKpBWdIsdjfci0Td2f_f0HZ5s2yQ)

<details>
<summary>Diagram source</summary>

```dot
digraph G {
  graph [rankdir=TB, bgcolor="transparent", pad="0.4", nodesep="0.35", ranksep="0.55"];
  node [shape=box, style="rounded,filled", fillcolor="#F8FAFC", color="#CBD5E1", fontname="Arial", fontsize=10];
  edge [color="#64748B", arrowsize=0.8];

  change [label="Change request", fillcolor="#DBEAFE", color="#3B82F6"];
  token [label="Token or semantic class\ninput.css + design-system-contract.md\n+ component self-doc if visible"];
  tag [label="Template tag signature\ninsight_tags.py + parameter_context.py\n+ usage_context.py + tests"];
  hook [label="data-insight-* hook\nJS module + template\n+ naming_conventions.md + self-doc"];
  presentation [label="Docs presentation only\ntemplates/docs/*\nno canonical logic here"];
  policy [label="Repository policy\ndocs/*.md\nlink from README when user-facing"];

  change -> token;
  change -> tag;
  change -> hook;
  change -> presentation;
  change -> policy;
}
```

</details>

| Change type | Required documentation update |
|---|---|
| Token or semantic class | Update `insight_ui/utils/input.css` and `docs/design-system-contract.md`; update component self-doc if users see or configure it. |
| Template tag signature or parameter behavior | Update `insight_ui/templatetags/insight_tags.py`, `component_details/parameter_context.py`, `component_details/usage_context.py`, and tests. |
| `data-insight-*` hook | Update the owning JS module, component template, `docs/naming_conventions.md`, and component self-doc. |
| Component docs text, usage, parameters, or accessibility | Update `insight_ui/component_details/*`; do not encode this primarily in docs templates. |
| Storybook or detail-page layout | Update `insight_ui/templates/insight_ui/docs/*`; keep canonical API, token, and behavior rules in their owning files. |
| Repository-level contributor policy | Update `docs/*.md`; add a README link only when the doc is useful as a public entry point. |

## Kroki diagram maintenance

Documentation diagrams are rendered through
`https://kroki.showcase.alpininsight.ai/` as SVG image links so they are visible
in GitHub Markdown. The diagram source is kept next to each image in a
collapsible `dot` block. If the source changes, regenerate the Kroki URL from
the updated Graphviz source using Kroki's deflate plus URL-safe base64 encoding.
