# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Real compiled-CSS acceptance of outline ink in both themes and input modes."""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

import django
from django.template import Context, Template
from playwright.sync_api import sync_playwright

if TYPE_CHECKING:
    from playwright.sync_api import Page

FAMILIES = ("primary", "secondary", "success", "warning", "danger", "info")
ROOT = Path(__file__).resolve().parents[2]
MIN_CONTRAST = 4.5

READ_STYLE = """element => {
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = 1;
  const ctx = canvas.getContext('2d', {willReadFrequently: true});
  function rgb(color) {
    ctx.clearRect(0, 0, 1, 1); ctx.fillStyle = color; ctx.fillRect(0, 0, 1, 1);
    return [...ctx.getImageData(0, 0, 1, 1).data];
  }
  function lum(values) {
    const c = values.slice(0, 3).map(v => {
      const n = v / 255;
      return n <= .04045 ? n / 12.92 : ((n + .055) / 1.055) ** 2.4;
    });
    return c[0] * .2126 + c[1] * .7152 + c[2] * .0722;
  }
  const style = getComputedStyle(element), fg = rgb(style.color);
  let bg = rgb(style.backgroundColor);
  if (bg[3] === 0) bg = rgb(getComputedStyle(document.body).backgroundColor);
  const values = [lum(fg), lum(bg)].sort((a, b) => a - b);
  return {fg, bg, ratio: (values[1] + .05) / (values[0] + .05),
          active: element.matches(':active'), hover: element.matches(':hover')};
}"""


def check_state(page: Page, family: str, state: str, *, theme: str, override: bool) -> None:
    """Exercise one real input state and assert its computed contrast."""
    button = page.locator(f"#{family}")
    page.mouse.move(0, 0)
    if state in {"hover", "active-pointer"}:
        button.hover()
    if state == "active-pointer":
        page.mouse.down()
    elif state == "active-keyboard":
        button.focus()
        page.keyboard.down("Space")
    # Let the real transition finish; no replacement/mocked styles.
    page.wait_for_timeout(220)
    values = button.evaluate(READ_STYLE)
    assert values["ratio"] >= MIN_CONTRAST, (theme, override, family, state, values)
    if state.startswith("active"):
        assert values["active"], (state, values)
    if state == "active-keyboard":
        assert not values["hover"], values
    if override and state != "normal":
        assert values["fg"][:3] == [17, 24, 39], values
    if state == "active-pointer":
        page.mouse.up()
    elif state == "active-keyboard":
        page.keyboard.up("Space")


def main() -> None:
    """Check normal/hover/pointer and keyboard active with actual packaged CSS."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
    django.setup()
    from insight_ui.configs import ButtonConfig  # noqa: PLC0415

    buttons = [ButtonConfig(label=family, color=family, variant="outline", tag_id=family) for family in FAMILIES]
    markup = Template("{% load insight_tags %}{% for item in buttons %}{% button config=item %}{% endfor %}").render(
        Context({"buttons": buttons})
    )
    css = (ROOT / "insight_ui/static/insight_ui/css/tailwind.css").read_text()
    synthetic = "".join(
        f"--color-insight-{family}-{role}{suffix}: {value};"
        for family in FAMILIES
        for role, value in (("action-hover", "#e2e8f0"), ("action-active", "#cbd5e1"), ("on-fill", "#111827"))
        for suffix in ("", "-dark")
    )
    count = 0
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        for theme in ("light", "dark"):
            for override in (False, True):
                extra = f":root,[data-theme=dark]{{{synthetic}}}" if override else ""
                page.set_content(
                    f'<!doctype html><html data-theme="{theme}"><head><style>{css}</style><style>{extra}'
                    "body{padding:32px;background:var(--color-insight-bg-base)}</style></head>"
                    f"<body>{markup}</body></html>"
                )
                for family in FAMILIES:
                    for state in ("normal", "hover", "active-pointer", "active-keyboard"):
                        check_state(page, family, state, theme=theme, override=override)
                        count += 1
        browser.close()
    print(f"Outline ink: {count} compiled-CSS state/theme/override checks passed.")  # noqa: T201


if __name__ == "__main__":
    main()
