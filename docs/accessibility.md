<!--
SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
SPDX-License-Identifier: AGPL-3.0-only
-->

# Accessibility

WCAG 2.2 AA is a design target, not a certification or a verified package-wide
conformance claim. This guide defines contributor expectations and known limits.
Conformance concerns full pages and complete processes, including all applicable
A/AA criteria and the other [W3C conformance requirements](https://www.w3.org/TR/WCAG22/#conformance-reqs).
A component, passing unit suite or clean scanner result cannot establish that.

## Component Contract

- Prefer native buttons, links and form controls with meaningful visible labels.
  Use headings and landmarks appropriate to the composed page, not its styling.
- Give icon-only actions an accessible name. Hide purely decorative icons from
  assistive technology; provide useful alternatives for informative images.
- Add ARIA only where needed. Referenced IDs must exist and be unique; keep
  expanded, selected, checked and value states synchronized with the interaction.
- Support Tab/Shift+Tab and native activation. Define arrow/Home/End behavior for
  composite widgets according to their pattern, not one universal key mapping.
- Keep keyboard focus visible and in a logical order, including after HTMX
  replacements. Remove event handlers and focus traps when components close or
  are destroyed; repeated initialization must not duplicate behavior.

For modal interactions, move focus inside on opening, contain Tab/Shift+Tab,
provide a visible close control and Escape dismissal, then restore focus to the
invoker or a logical successor. Background content must actually be unavailable
to interaction; `aria-modal="true"` alone does not implement this. Choose initial
focus for the content, not always the first button. See the
[W3C modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/).
A persistent navigation sidebar is not automatically a modal dialog.

## Current Implementation Boundaries

Check source and rendered output rather than relying on descriptive comments:

- The [modal template](../insight_ui/templates/insight_ui/components/modal.html)
  declares a dialog with `aria-modal` and a title reference. Supply a unique
  `tag_id` and meaningful title; these attributes do not prove background isolation.
- The [modal](../insight_ui/static/insight_ui/js/insight-ui-modal.js) and
  [sidebar](../insight_ui/static/insight_ui/js/insight-ui-sidebar.js) implement
  Escape handling and attempt focus restoration. Sidebar close cleanup waits for
  `transitionend`; verify focus return when transitions are absent or interrupted.
- The shared [focus helper](../insight_ui/static/insight_ui/js/insight-ui-utils.js)
  captures candidates once and does not filter hidden or disabled controls.
  Test empty content, changing content and removed triggers explicitly.

For `input_field`, provide a visible `label` and non-empty unique `tag_id`.
The [input template](../insight_ui/templates/insight_ui/components/input.html)
uses that ID for label association; `name` is not an automatic ID fallback.
At this revision, [base fields](../insight_ui/configs/base.py) and
[InputFieldConfig](../insight_ui/configs/input.py) have no `help_text` or `error`
parameters. The template does not emit linked help/error paragraphs,
`aria-invalid` or `aria-errormessage`. The
[form template](../insight_ui/templates/insight_ui/components/form.html)'s
`#form-error` is a plain container, not an implemented alert region.

Do not document automatic error announcements or pass unsupported Config fields.
When adding reusable error support, link instructions/errors to the control,
explain the correction in text, and test focus and announcement behavior without
announcing every invalid field at once. Follow the
[W3C form notification guidance](https://www.w3.org/WAI/tutorials/forms/notifications/).
Generic fixes and their regression tests belong here; app-specific validation
and page composition remain with the consumer.

## Themes And Contrast

Use semantic roles from [input.css](../insight_ui/utils/input.css), such as
`text-insight-headline`, `text-insight-body`, `*-action` for filled controls and
`*-foreground` on matching `*-soft` surfaces. Do not substitute a brand/accent
color for readable text just because it shares the same hue.

Recheck both default light/dark themes and every new theme or override against
the actual rendered backgrounds, including hover, active, selected, focus and
error states. Gradients, transparency and consumer styles change effective pairs.
Never communicate an error or selection through color alone.

- Text normally needs 4.5:1 contrast, or 3:1 for large text as defined by W3C
  (18 pt regular or 14 pt bold). Apply the criterion's stated exceptions, not
  blanket theme exemptions: [SC 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).
- Necessary visual cues for controls/states and meaningful graphics need 3:1
  against adjacent colors, subject to the criterion's exceptions:
  [SC 1.4.11](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html).

[Token tests](../tests/insight_ui/unit/test_design_tokens.py) check selected
action/text and foreground/soft pairs in source CSS for both themes. They do
not measure every rendered state or prove a new theme accessible.

## Verification And Ownership

After [contributor setup](../CONTRIBUTING.md), run focused package checks:

```bash
uv run pytest tests/insight_ui/unit/components/test_input_field.py tests/insight_ui/unit/test_design_tokens.py
npm test -- tests/js/utils.test.js tests/js/modal.test.js tests/js/sidebar.test.js
```

[Vitest is configured for jsdom](../vitest.config.js), not a real browser.
[Utility tests](../tests/js/utils.test.js) exercise initial focus, Tab wrapping
and cleanup in that environment. The [modal](../tests/js/modal.test.js) and
[sidebar](../tests/js/sidebar.test.js) trap-focus checks spy on helper calls;
they do not demonstrate a complete browser focus trap. Current
[input-field tests](../tests/insight_ui/unit/components/test_input_field.py)
cover Config bounds, not accessible error rendering. Add regressions for fixes.

Keep reusable keyboard, ARIA, focus and lifecycle tests in this package's
[Python](../tests/insight_ui/unit/) and [JavaScript](../tests/js/) suites.
The separate Docs application owns its rendered catalog and its browser checks
(for example Playwright/axe) plus manual keyboard and screen-reader evidence;
it should reference package test results, not copy the unit suite.
Consumers likewise test their complete pages, content and authentication flows.

Use the local component preview for isolated smoke checks, not application
authentication or language-selection proof; see [i18n limits](i18n.md).
Manually check keyboard-only operation, screen-reader names/states, narrow and
zoomed layouts, forced colors and reduced motion in the actual host and theme.
Record the package revision, commands/results, tested states, browser and
assistive technology versions, artifacts and remaining gaps in the PR.
[W3C evaluation guidance](https://www.w3.org/WAI/test-evaluate/tools/selecting/)
explains why automation must be supplemented by human evaluation.

[Back to docs](README.md) | [Contributing](../CONTRIBUTING.md)
