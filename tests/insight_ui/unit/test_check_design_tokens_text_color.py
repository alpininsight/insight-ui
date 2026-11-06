# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the design token check that keeps color family accents out of text colors."""

from pathlib import Path

import pytest
from scripts.check_design_tokens import build_family_text_config, find_violations


def reported(tmp_path: Path, classes: str) -> list[tuple[str, str | None]]:
    """Return the reported classes and their suggestions for a template with the given classes."""
    template = tmp_path / "component.html"
    template.write_text(f'<div class="{classes}"></div>\n', encoding="utf-8")
    return [(v.class_name, v.suggestion) for v in find_violations(template, [build_family_text_config()])]


@pytest.mark.parametrize(
    ("classes", "expected"),
    [
        pytest.param("text-insight-primary", ("text-insight-primary", "text-insight-primary-text"), id="text"),
        pytest.param(
            "hover:text-insight-danger", ("hover:text-insight-danger", "hover:text-insight-danger-text"), id="variant"
        ),
    ],
)
def test_family_accent_as_text_is_reported(tmp_path: Path, classes: str, expected: tuple[str, str]) -> None:
    """The accent does not switch with the theme; text and icons use the -text token."""
    assert reported(tmp_path, classes) == [expected]


@pytest.mark.parametrize(
    "classes",
    [
        pytest.param("text-insight-primary-text", id="text-token"),
        pytest.param("border-insight-primary bg-insight-success", id="accent-as-border-and-fill"),
        pytest.param("text-insight-primary-on-action", id="on-action"),
        pytest.param("text-insight-headline text-insight-muted", id="text-roles"),
    ],
)
def test_readable_text_tokens_and_accents_on_borders_pass(tmp_path: Path, classes: str) -> None:
    """Only the accent as text color is reported."""
    assert reported(tmp_path, classes) == []
