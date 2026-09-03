"""Tests for the public wheel package contract."""

import tomllib
from pathlib import Path


def test_documentation_app_is_included_in_wheel() -> None:
    """Ship the extracted documentation APIs consumed by extension packages."""
    project = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    packages = project["tool"]["hatch"]["build"]["targets"]["wheel"]["packages"]
    assert "documentation" in packages
