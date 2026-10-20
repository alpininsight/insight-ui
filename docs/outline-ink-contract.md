<!--
SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
SPDX-License-Identifier: AGPL-3.0-only
-->

# Outline Interaction Ink

The current `develop` API has six semantic outline families. An outline starts
with the family's `--color-insight-<family>-text` role on an unfilled surface.
When hover or active fills the control, the text must read
`--color-insight-<family>-on-fill`, not a hardcoded white utility.
This is the same existing role used by the solid variant; no palette or
corporate values are added here.

Active ink is explicit: keyboard Space can activate a button without pointer
hover. Testing only a mouse-held button would miss that path. Neutral controls
remain a separate [#686](https://github.com/alpininsight/insight-ui/issues/686)
contract and are not declared repaired by this bounded semantic-family fix.

## Verification

```bash
npm run build:tailwind
uv run pytest tests/insight_ui/unit/components/test_outline_on_fill.py
uv run --with playwright==1.64.0 python -m playwright install chromium
uv run --with playwright==1.64.0 python -m tests.browser.outline_ink_smoke
```

The real browser reads the packaged stylesheet and public tag output. It checks
six families, Light/Dark, normal/hover/pointer-active/keyboard-active, both the
default palette and a neutral synthetic dark-on-fill override: 96 observations.
No style replacement disables or fakes the interaction rules. The existing
required stylesheet CI job also runs the browser program.

## Integration and release

Open refactor [#733](https://github.com/alpininsight/insight-ui/pull/733) already
uses `--btn-on-fill` for its new outline API. This PR does not mutate that
owner's branch. If the refactor integrates first, rebase and adapt these
regressions to its actual classes/configuration, retaining its implementation
instead of restoring obsolete class names. Do not merge competing branches
blindly or claim a stable consumer API from an open PR.

Stable v1.15.1 predates both the `on-fill` rename and this correction.
Consumers must choose a tested stable package and matching token contract;
this source PR neither upgrades a consumer nor changes live traffic.
