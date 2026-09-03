"""Tests for the public wheel package contract."""

import tomllib
from pathlib import Path


def test_wheel_contains_only_the_reusable_package() -> None:
    """Do not ship the application-owned documentation code with Insight UI."""
    project = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    packages = project["tool"]["hatch"]["build"]["targets"]["wheel"]["packages"]
    assert packages == ["insight_ui"]
