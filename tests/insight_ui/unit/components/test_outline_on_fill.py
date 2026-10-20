# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Outline interactions must read the filled-ink role, not assume white text."""

import re
from pathlib import Path

import pytest

FAMILIES = ("primary", "secondary", "success", "warning", "danger", "info")
ROOT = Path(__file__).resolve().parents[4]


@pytest.mark.parametrize("family", FAMILIES)
def test_outline_uses_existing_on_fill_role_for_hover_and_active(family: str) -> None:
    """Active ink is explicit, including keyboard activation without hover."""
    source = (ROOT / "insight_ui/utils/input.css").read_text()
    rule = re.search(rf"\.btn-outline-{family}\s*\{{([^}}]+)\}}", source)
    assert rule is not None
    body = rule.group(1)
    assert f"hover:text-insight-{family}-on-fill" in body
    assert f"active:text-insight-{family}-on-fill" in body
    assert "text-white" not in body
    assert f"text-insight-{family}-text" in body


@pytest.mark.parametrize("family", FAMILIES)
def test_packaged_css_contains_the_interaction_ink(family: str) -> None:
    """The shipped stylesheet, not just source @apply, must contain both states."""
    css = (ROOT / "insight_ui/static/insight_ui/css/tailwind.css").read_text()
    rule = re.search(rf"\.btn-outline-{family}\s*\{{(.*?)\n  \}}", css, re.DOTALL)
    assert rule is not None
    assert f"color: var(--color-insight-{family}-on-fill)" in rule.group(1)
    assert "&:active" in rule.group(1)
    assert "&:hover" in rule.group(1)
