"""Tests for the public wheel package contract."""

import tomllib
from pathlib import Path


def test_insight_ui_is_included_in_wheel() -> None:
    """Ensure the insight_ui package is included in the wheel for PyPI distribution."""
    project = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    packages = project["tool"]["hatch"]["build"]["targets"]["wheel"]["packages"]
    assert "insight_ui" in packages
