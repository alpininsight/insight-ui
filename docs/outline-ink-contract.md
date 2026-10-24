<!--
SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
SPDX-License-Identifier: AGPL-3.0-only
-->

# Outline Interaction Ink

The stacked button API uses `color=<family>, variant="outline"` for six semantic
families. An outline starts
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

This branch integrates the unchanged refactor
[#733](https://github.com/alpininsight/insight-ui/pull/733) through the native
download branch [#743](https://github.com/alpininsight/insight-ui/pull/743).
Merge in the order **#733 -> #743 -> #744**, rechecking the exact heads after
each integration. No integration into `develop` or `main` is performed here.
The refactor's canonical `--btn-on-fill` implementation is retained, without
restoring the obsolete `.btn-outline-<family>` rules. The source, packaged-CSS
and 96 browser observations now exercise the actual new API. The required CI
job keeps both the native-download and outline-interaction browser programs.
Do not claim a stable consumer API from these open PRs.

Stable v1.15.1 predates both the `on-fill` rename and this correction.
Consumers must choose a tested stable package and matching token contract;
this source PR neither upgrades a consumer nor changes live traffic.
