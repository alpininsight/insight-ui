# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Keep package onboarding separate from the documentation application."""

from pathlib import Path


def test_readme_describes_package_installation_and_external_documentation() -> None:
    """The public entry point installs the library, not its documentation host."""
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "https://insight-ui.com/" in readme
    assert "uv add insight-ui" in readme
    assert '"insight_ui"' in readme
    assert "insight-ui-docs" in readme
    assert "does not\ncontain or deploy a documentation website" in readme
    assert "manage.py setup_dev" not in readme
    assert "tailwind runserver" not in readme
    assert "](docs/getting-started.md)" in readme
    assert "](docs/static-assets.md)" in readme
    assert "](docs/README.md)" in readme
    assert "AA-compliant" not in readme
    assert "https://pypi.org/project/insight-ui/" in readme
    assert "Initial public PyPI publication" not in readme
    assert "Once a release is available" not in readme
