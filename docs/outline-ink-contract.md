<!--
SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
SPDX-License-Identifier: AGPL-3.0-only
-->

# Outline Interaction Ink

The button API uses `color=<family>, variant="outline"` for six semantic
families. An outline starts with the family's
`--color-insight-<family>-text` role on an unfilled surface. When hover or active
fills the control, its text reads `--color-insight-<family>-on-action`, the same
role used by the solid variant.

Active ink is explicit: keyboard Space can activate a button without pointer
hover. The real browser checks that path as well as pointer activation. Neutral
controls retain their separate [#686](https://github.com/alpininsight/insight-ui/issues/686)
contract; these checks cover the six semantic families.

## Verification

```bash
npm run build:tailwind
uv run pytest tests/insight_ui/unit/components/test_outline_on_action.py
uv run --with playwright==1.64.0 python -m playwright install chromium
uv run --with playwright==1.64.0 python -m tests.browser.outline_ink_smoke
uv run --with playwright==1.64.0 python -m tests.browser.button_download_smoke
```

The real browser reads the packaged stylesheet and public tag output. It checks
six families, Light/Dark, normal/hover/pointer-active/keyboard-active, both the
default palette and a synthetic dark-ink override: 96 observations. The download
program checks three native keyboard downloads with page JavaScript disabled.

The required browser CI job uses the official Playwright Python image, pinned
to version 1.64.0 and a registry-verified SHA-256 digest. The matching Python
package uses the browser binaries already included in that image; CI does not
download a browser at runtime. Both browser programs gate the PR through the
existing quality gate.

## Component contract

The outline and native-download checks use the same public button Config and
template tag as applications. Interaction colors use `--tone-on-action` and
`--color-insight-<family>-on-action`. Native downloads use `download` and `htmx`;
an empty suggested filename is normalized to the browser's default filename.

Applications should pair their theme tokens with the installed package version.
Changing package source or passing the browser checks does not update an
application's installed package or activate a release.
