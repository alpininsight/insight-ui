# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the public wheel package contract."""

import tomllib
from pathlib import Path


def test_insight_ui_is_included_in_wheel() -> None:
    """Ensure the insight_ui package is included in the wheel for PyPI distribution."""
    project = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    packages = project["tool"]["hatch"]["build"]["targets"]["wheel"]["packages"]
    assert packages == ["insight_ui"]


def test_source_tree_has_no_documentation_application() -> None:
    """A green package test must not hide a duplicated app in the Git source."""
    for path in ("documentation", "core", "enterprise", "docs", "manage.py", "Dockerfile"):
        assert not Path(path).exists(), path
