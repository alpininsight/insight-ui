# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Ensure the archive gate detects accidental application packaging."""

import io
import tarfile
import zipfile
from email.message import EmailMessage
from pathlib import Path

import pytest
from scripts.check_distribution import REQUIRED, SOURCE_ONLY, check_archive, check_metadata


@pytest.mark.parametrize(
    "path",
    [
        "documentation/views.py",
        "core/settings.py",
        "enterprise/offer.md",
        "docs/getting-started.md",
        "devtools/views.py",
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


@pytest.mark.parametrize("kind", ["wheel", "sdist"])
def test_archive_check_accepts_public_package_payload(
    tmp_path: Path, kind: str, distribution_metadata: EmailMessage
) -> None:
    """The gate accepts the required generic library files."""
    if kind == "wheel":
        path = tmp_path / "example.whl"
        with zipfile.ZipFile(path, "w") as archive:
            for name in REQUIRED:
                archive.writestr(name, "fixture")
            archive.writestr("insight_ui-1.0.0.dist-info/METADATA", distribution_metadata.as_bytes())
    else:
        path = tmp_path / "example.tar.gz"
        contents = dict.fromkeys(REQUIRED | SOURCE_ONLY, b"fixture")
        contents["PKG-INFO"] = distribution_metadata.as_bytes()
        with tarfile.open(path, "w:gz") as archive:
            for name, data in contents.items():
                member = tarfile.TarInfo(f"insight_ui-1.0.0/{name}")
                member.size = len(data)
                archive.addfile(member, io.BytesIO(data))
    check_archive(path)


@pytest.mark.parametrize("field", ["Name", "Requires-Python", "Classifier", "Project-URL", "Description-Content-Type"])
def test_built_metadata_must_match_source(field: str, distribution_metadata: EmailMessage) -> None:
    """Stale maturity, Python support and project links must fail before upload."""
    metadata = distribution_metadata
    del metadata[field]
    if field == "Classifier":
        metadata[field] = "Development Status :: 3 - Alpha"
    with pytest.raises(SystemExit, match=field):
        check_metadata(metadata.as_bytes())


@pytest.mark.parametrize("description", ["", "[Get started](docs/getting-started.md)"])
def test_built_description_must_match_readme(description: str, distribution_metadata: EmailMessage) -> None:
    """Both archive formats must carry the reviewed README, not stale PyPI links."""
    distribution_metadata.set_content(description)
    with pytest.raises(SystemExit, match="Description differs"):
        check_metadata(distribution_metadata.as_bytes())


@pytest.mark.parametrize("missing", ["package.json", "package-lock.json"])
def test_sdist_requires_reproducible_javascript_dependencies(
    tmp_path: Path, missing: str, distribution_metadata: EmailMessage
) -> None:
    """The bundled JS suite must retain the inputs needed for npm ci."""
    path = tmp_path / "example.tar.gz"
    contents = dict.fromkeys((REQUIRED | SOURCE_ONLY) - {missing}, b"fixture")
    contents["PKG-INFO"] = distribution_metadata.as_bytes()
    with tarfile.open(path, "w:gz") as archive:
        for name, data in contents.items():
            member = tarfile.TarInfo(f"insight_ui-1.0.0/{name}")
            member.size = len(data)
            archive.addfile(member, io.BytesIO(data))
    with pytest.raises(SystemExit, match="missing=") as error:
        check_archive(path)
    assert missing in str(error.value)


def test_distribution_requires_metadata(tmp_path: Path) -> None:
    """A payload-only archive cannot pass without its public metadata."""
    path = tmp_path / "example.whl"
    with zipfile.ZipFile(path, "w") as archive:
        for name in REQUIRED:
            archive.writestr(name, "fixture")
    with pytest.raises(SystemExit, match="exactly one distribution metadata"):
        check_archive(path)


def test_duplicate_metadata_is_rejected(tmp_path: Path, distribution_metadata: EmailMessage) -> None:
    """A ZIP duplicate must not disappear when archive paths are deduplicated."""
    path = tmp_path / "example.whl"
    with zipfile.ZipFile(path, "w") as archive:
        for name in REQUIRED:
            archive.writestr(name, "fixture")
        name = "insight_ui-1.0.0.dist-info/METADATA"
        archive.writestr(name, distribution_metadata.as_bytes())
        with pytest.warns(UserWarning, match="Duplicate name"):
            archive.writestr(name, distribution_metadata.as_bytes())
    with pytest.raises(SystemExit, match="exactly one distribution metadata"):
        check_archive(path)
