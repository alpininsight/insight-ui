# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Ensure the archive gate detects accidental application packaging."""

import zipfile
from pathlib import Path

import pytest
from scripts.check_distribution import REQUIRED, check_archive


@pytest.mark.parametrize(
    "path",
    [
        "documentation/views.py",
        "core/settings.py",
        "enterprise/offer.md",
        "insight_ui/static/insight_ui/js/insight-ui-demo-container.js",
    ],
)
def test_archive_check_rejects_non_package_payload(tmp_path: Path, path: str) -> None:
    """A valid-looking wheel must fail when docs or Enterprise code is added."""
    wheel = tmp_path / "example.whl"
    with zipfile.ZipFile(wheel, "w") as archive:
        for name in [*REQUIRED, path]:
            archive.writestr(name, "fixture")
    with pytest.raises(SystemExit, match="unexpected="):
        check_archive(wheel)


def test_archive_check_accepts_public_package_payload(tmp_path: Path) -> None:
    """The gate accepts the required generic library files."""
    wheel = tmp_path / "example.whl"
    with zipfile.ZipFile(wheel, "w") as archive:
        for name in REQUIRED:
            archive.writestr(name, "fixture")
    check_archive(wheel)
