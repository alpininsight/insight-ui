# Design token impact map

This document shows which visible UI areas are affected by the public design
tokens in `insight_ui/utils/input.css`.

The screenshots are intentionally stored as before/after pairs. They show the
state before the token migration in this pull request and the state after the
components were moved to semantic Insight UI tokens and classes.

## How to regenerate

Start the local demo server first:

```bash
uv run python manage.py runserver 127.0.0.1:8010
```

Then capture the two phases:

```bash
INSIGHT_UI_SCREENSHOT_PHASE=before node scripts/capture-design-token-screenshots.mjs
INSIGHT_UI_SCREENSHOT_PHASE=after node scripts/capture-design-token-screenshots.mjs
```

The script writes screenshots to `docs/assets/design-token-impact-map/`.

## Token areas

| Token area | Main tokens/classes | Typical affected UI |
|---|---|---|
| Brand colors | `--color-insight-primary`, `--color-insight-secondary`, foreground and interaction variants | buttons, links, focus accents, active states |
| Status colors | `success`, `warning`, `danger`, `info`, `pending` token families | alerts, infoboxes, step indicators, validation |
| Text hierarchy | `text-primary`, `text-secondary`, `text-link`, `text-disabled` | page copy, navigation, muted states |
| Surfaces | `--color-insight-surface-*`, `insight-surface-*` | page background, cards, forms, dropdowns, modals |
| Tonal elevation aliases | `canvas`, `panel`, `raised`, `sunken` | Brand-compatible names for the same surface ladder |
| Borders | `--color-insight-border-*`, `insight-border-*` | cards, tables, sidebars, form controls |
| Shadows | `--insight-shadow-*`, `insight-shadow-*` | buttons, controls, cards, overlays |
| Radius | `--insight-radius-*`, `insight-radius-*` | controls, cards, pills, overlays |
| Typography | `--font-sans`, `--font-display`, `--font-mono`, tracking tokens | headings, labels, code/documentation surfaces |

## Overview

| Before | After |
|---|---|
| ![Default overview before](assets/design-token-impact-map/before/default/overview.png) | ![Default overview after](assets/design-token-impact-map/after/default/overview.png) |

Affected areas: page surface, navbar surface, sidebar surface, dropdown surface,
border hierarchy, text hierarchy, and component list surfaces.

## Buttons

| Before | After |
|---|---|
| ![Default buttons before](assets/design-token-impact-map/before/default/buttons.png) | ![Default buttons after](assets/design-token-impact-map/after/default/buttons.png) |

Affected areas: button foreground tokens, button border fallback tokens, button
shadow tokens, disabled tokens, radius-control, and focus/interaction states.

## Forms

| Before | After |
|---|---|
| ![Default forms before](assets/design-token-impact-map/before/default/forms.png) | ![Default forms after](assets/design-token-impact-map/after/default/forms.png) |

Affected areas: control surface, control border, control shadow, control radius,
validation/status colors, and disabled/muted text states.

## Cards And Surfaces

| Before | After |
|---|---|
| ![Default cards before](assets/design-token-impact-map/before/default/cards.png) | ![Default cards after](assets/design-token-impact-map/after/default/cards.png) |

Affected areas: surface-base, surface-soft, surface border, surface shadow, and
surface radius.

## Navigation

| Before | After |
|---|---|
| ![Default navigation before](assets/design-token-impact-map/before/default/navigation.png) | ![Default navigation after](assets/design-token-impact-map/after/default/navigation.png) |

Affected areas: navbar, sidebar, selected item surface, inactive item borders,
hover surface, and overlay shadow.

## Feedback

| Before | After |
|---|---|
| ![Default feedback before](assets/design-token-impact-map/before/default/feedback.png) | ![Default feedback after](assets/design-token-impact-map/after/default/feedback.png) |

Affected areas: status color families, status foreground, feedback surface tint,
and feedback radius/shadow.

## Data Display

| Before | After |
|---|---|
| ![Default table before](assets/design-token-impact-map/before/default/table.png) | ![Default table after](assets/design-token-impact-map/after/default/table.png) |

Affected areas: table surface, alternating row surfaces, border hierarchy, and
muted empty-state text.

## Range Slider

| Before | After |
|---|---|
| ![Default range slider before](assets/design-token-impact-map/before/default/range-slider.png) | ![Default range slider after](assets/design-token-impact-map/after/default/range-slider.png) |

Affected areas: primary track color, inactive track surface, control radius,
thumb border, and focus ring.

## Brite Theme Smoke

| Before | After |
|---|---|
| ![Brite buttons before](assets/design-token-impact-map/before/brite/buttons.png) | ![Brite buttons after](assets/design-token-impact-map/after/brite/buttons.png) |

The Brite theme is the harshest smoke test because it uses white secondary
buttons with black borders and hard neobrutalist shadows. If surface, border, or
shadow tokens regress, this page usually shows it first.

## Remaining Follow-Up Areas

Some components still intentionally keep local implementation details. These are
not yet public design-system tokens:

- carousel positioning and image-caption overlays,
- pseudo-element slider thumb internals where browser support requires verbose
  utility selectors,
- one-off geometric decoration drop shadows,
- icon glyph selection.

Those values should only become public tokens when they repeat across multiple
components or need host-project override support.
