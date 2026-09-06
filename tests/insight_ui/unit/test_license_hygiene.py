# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Licence hygiene: SPDX headers, REUSE metadata and third-party notices.

Customers run software-composition scans against the package; every source file
must carry an SPDX header and the bundled third-party components must ship their
licence texts (REUSE specification 3.3, OpenChain ISO/IEC 5230).
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
# REUSE-IgnoreStart
COPYRIGHT_TAG = "SPDX-FileCopyrightText:"
LICENSE_TAG = "SPDX-License-Identifier:"
# REUSE-IgnoreEnd
COPYRIGHT_LINE = f"{COPYRIGHT_TAG} 2025-2026 Alpin Insight Solutions GmbH & Co. KG"
HEADER_SUFFIXES = {".py", ".js", ".mjs"}
GENERATED = {"insight_ui/static/insight_ui/css/tailwind.css"}


def _tracked_files() -> list[Path]:
    output = subprocess.run(
        ["git", "ls-files", "-z"],  # noqa: S607 - git is required by the repository contract
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return [ROOT / name for name in output.split("\0") if name]


def _header_files() -> list[Path]:
    return [
        path
        for path in _tracked_files()
        if path.suffix in HEADER_SUFFIXES
        and path.relative_to(ROOT).as_posix() not in GENERATED
        and not path.name.endswith(".min.js")
    ]


@pytest.mark.parametrize("path", _header_files(), ids=lambda p: p.relative_to(ROOT).as_posix())
def test_source_file_carries_spdx_header(path: Path) -> None:
    """Every Python and JavaScript source file starts with the SPDX copyright and licence lines."""
    head = path.read_text(encoding="utf-8").splitlines()[:6]
    assert any(COPYRIGHT_LINE in line for line in head), f"missing copyright header: {path}"
    assert any(LICENSE_TAG in line for line in head), f"missing licence header: {path}"


def test_icons_module_declares_heroicons_licence() -> None:
    """The bundled Heroicons keep their MIT attribution."""
    head = (ROOT / "insight_ui/icons.py").read_text(encoding="utf-8").splitlines()[:6]
    assert any("Tailwind Labs, Inc." in line for line in head)
    assert any("AGPL-3.0-only AND MIT" in line for line in head)


def test_reuse_metadata_and_licence_texts_exist() -> None:
    """REUSE.toml, NOTICE and the licence texts for every identifier in use are present."""
    assert (ROOT / "REUSE.toml").is_file()
    assert (ROOT / "NOTICE").is_file()
    for identifier in ("AGPL-3.0-only", "OFL-1.1", "MIT", "CC0-1.0"):
        assert (ROOT / "LICENSES" / f"{identifier}.txt").is_file(), identifier


def test_bundled_font_ships_with_its_licence() -> None:
    """The SIL Open Font License requires the licence text to accompany the font."""
    font_dir = ROOT / "insight_ui/static/insight_ui/font"
    assert (font_dir / "AtkinsonHyperlegibleNext-VariableFont_wght.ttf").is_file()
    ofl = (font_dir / "OFL.txt").read_text(encoding="utf-8")
    assert "SIL OPEN FONT LICENSE Version 1.1" in ofl
    assert "Atkinson Hyperlegible Next Project Authors" in ofl


def test_package_ships_third_party_notices() -> None:
    """The notices for Heroicons and the font travel inside the installable package."""
    notices = (ROOT / "insight_ui/THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
    assert "Heroicons" in notices
    assert "Copyright (c) Tailwind Labs, Inc." in notices
    assert "Atkinson Hyperlegible Next" in notices
