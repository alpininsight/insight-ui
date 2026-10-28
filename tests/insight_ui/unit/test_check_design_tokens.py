# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the design token checker used as pre-commit hook."""

from pathlib import Path

import pytest
from scripts.check_design_tokens import (
    build_color_config,
    build_radius_config,
    build_shadow_config,
    build_verbose_config,
    find_violations,
)

CONFIGS = [build_color_config(), build_radius_config(), build_shadow_config(), build_verbose_config()]


def violations(tmp_path: Path, classes: str) -> list[str]:
    """Return the classes the checker reports for a template with the given class attribute."""
    template = tmp_path / "component.html"
    template.write_text(f'<div class="{classes}"></div>\n', encoding="utf-8")
    return [violation.class_name for violation in find_violations(template, CONFIGS)]


@pytest.mark.parametrize(
    "classes",
    [
        pytest.param("bg-insight-bg-base-dark", id="dark-token-has-no-shorthand"),
        pytest.param("text-insight-text-link-hover", id="longer-token"),
        pytest.param("bg-insight-bg-raised/50", id="opacity-needs-the-token"),
        pytest.param("rounded-insight-surface shadow-insight-raised", id="semantic-tokens"),
    ],
)
def test_whole_classes_only(tmp_path: Path, classes: str) -> None:
    """A verbose token inside a longer class is not reported; its suggestion would not exist."""
    assert violations(tmp_path, classes) == []


@pytest.mark.parametrize(
    ("classes", "reported"),
    [
        pytest.param("bg-insight-bg-base", "bg-insight-bg-base", id="verbose"),
        pytest.param("hover:bg-insight-bg-raised", "hover:bg-insight-bg-raised", id="verbose-with-variant"),
        pytest.param("p-4 bg-gray-300", "bg-gray-300", id="raw-color"),
        pytest.param("rounded-lg", "rounded-lg", id="raw-radius"),
        pytest.param("shadow-md", "shadow-md", id="raw-shadow"),
    ],
)
def test_reports_raw_and_verbose_classes(tmp_path: Path, classes: str, reported: str) -> None:
    """Raw Tailwind values and verbose tokens with a shorthand are reported."""
    assert violations(tmp_path, classes) == [reported]
