# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Outline interactions must read the filled-ink role, not assume white text."""

import re
from pathlib import Path

import pytest

FAMILIES = ("primary", "secondary", "success", "warning", "danger", "info")
ROOT = Path(__file__).resolve().parents[4]


@pytest.mark.parametrize("family", FAMILIES)
def test_outline_uses_existing_on_action_role_for_hover_and_active(family: str) -> None:
    """Active ink is explicit, including keyboard activation without hover."""
    source = (ROOT / "insight_ui/utils/input.css").read_text()
    rule = re.search(rf"\.btn-{family}\s*,\s*\.control-{family}\s*\{{([^}}]+)\}}", source)
    assert rule is not None
    body = rule.group(1)
    assert f"--tone-on-action: var(--color-insight-{family}-on-action)" in body
    assert f"--tone-ink: var(--color-insight-{family}-text)" in body
    for state in ("hover", "active"):
        interaction = re.search(rf"(?m)^\s*\.btn-outline:where\([^{{]*:{state}\s*\{{([^}}]+)\}}", source)
        assert interaction is not None
        assert "color: var(--tone-on-action)" in interaction.group(1)
        assert "text-white" not in interaction.group(1)
    assert ".btn-outline-" not in source


@pytest.mark.parametrize("family", FAMILIES)
def test_packaged_css_contains_the_interaction_ink(family: str) -> None:
    """The shipped stylesheet, not just source @apply, must contain both states."""
    css = (ROOT / "insight_ui/static/insight_ui/css/tailwind.css").read_text()
    rule = re.search(rf"\.btn-{family}\s*,\s*\.control-{family}\s*\{{([^}}]+)\}}", css)
    assert rule is not None
    assert f"--tone-on-action: var(--color-insight-{family}-on-action)" in rule.group(1)
    for state in ("hover", "active"):
        interaction = re.search(rf"(?m)^\s*\.btn-outline:where\([^{{]*:{state}\s*\{{([^}}]+)\}}", css)
        assert interaction is not None
        assert "color: var(--tone-on-action)" in interaction.group(1)
