# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Regression tests for reusable Insight UI design tokens."""

import re
from pathlib import Path

import pytest

INPUT_CSS = Path("insight_ui/utils/input.css")
SRGB_LINEAR_THRESHOLD = 0.04045
WCAG_AA_CONTRAST_RATIO = 4.5


def _hex_token(css: str, token: str) -> str:
    """Return the first hexadecimal value assigned to a design token."""
    match = re.search(rf"^\s*{re.escape(token)}:\s*(#[0-9A-Fa-f]{{6}});", css, flags=re.MULTILINE)
    assert match, f"Missing hexadecimal value for {token}"
    return match.group(1)


def _relative_luminance(color: str) -> float:
    """Calculate WCAG relative luminance for a six-digit hexadecimal color."""
    channels = tuple(int(color[index : index + 2], 16) / 255 for index in (1, 3, 5))

    def linearize(channel: float) -> float:
        return channel / 12.92 if channel <= SRGB_LINEAR_THRESHOLD else ((channel + 0.055) / 1.055) ** 2.4

    red, green, blue = (linearize(channel) for channel in channels)
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def _contrast_ratio(foreground: str, background: str) -> float:
    """Calculate the WCAG contrast ratio between two hexadecimal colors."""
    lighter, darker = sorted((_relative_luminance(foreground), _relative_luminance(background)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def test_shadow_role_tokens_are_available() -> None:
    """Ensure packaged theme input exposes the shared shadow role tokens."""
    css = INPUT_CSS.read_text()

    for token in (
        "--shadow-insight-subtle",
        "--shadow-insight-surface",
        "--shadow-insight-raised",
        "--shadow-insight-overlay",
        "--shadow-insight-focus",
    ):
        assert token in css


def test_radius_role_tokens_are_available() -> None:
    """Ensure semantic radius tokens remain available in the source stylesheet."""
    css = INPUT_CSS.read_text()

    for token in (
        "--radius-insight-xs",
        "--radius-insight-s",
        "--radius-insight-m",
        "--radius-insight-l",
        "--radius-insight-xl",
        "--radius-insight-full",
        "--radius-insight-control",
        "--radius-insight-surface",
        "--radius-insight-raised",
        "--radius-insight-overlay",
    ):
        assert token in css


def test_insight_tokens_are_not_defined_twice() -> None:
    """Keep source theme tokens deterministic and easy to override."""
    css = INPUT_CSS.read_text()
    tokens = re.findall(r"^\s*(--insight-[\w-]+)\s*:", css, flags=re.MULTILINE)

    duplicates = sorted({token for token in tokens if tokens.count(token) > 1})

    assert duplicates == []


@pytest.mark.parametrize("role", ["primary", "secondary", "success", "warning", "danger", "info"])
@pytest.mark.parametrize(
    ("foreground", "background"),
    [
        ("on-fill", "action"),
        ("on-fill", "action-dark"),
        ("text", "soft"),
        ("text-dark", "soft-dark"),
    ],
    ids=lambda suffix: suffix,
)
def test_semantic_color_pairs_meet_wcag_aa(role: str, foreground: str, background: str) -> None:
    """Keep filled controls and text on soft surfaces readable in both themes."""
    css = INPUT_CSS.read_text()
    foreground_token = f"--color-insight-{role}-{foreground}"
    background_token = f"--color-insight-{role}-{background}"
    foreground_color = _hex_token(css, foreground_token)
    background_color = _hex_token(css, background_token)

    ratio = _contrast_ratio(foreground_color, background_color)

    assert ratio >= WCAG_AA_CONTRAST_RATIO, (
        f"{foreground_token} ({foreground_color}) on {background_token} ({background_color}) "
        f"has contrast {ratio:.2f}, needs {WCAG_AA_CONTRAST_RATIO}"
    )
