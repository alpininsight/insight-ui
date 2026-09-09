# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Licence hygiene: SPDX headers, REUSE metadata and third-party notices.

Customers run software-composition scans against the package; every source file
must carry an SPDX header and the bundled third-party components must ship their
licence texts (REUSE specification 3.3, OpenChain ISO/IEC 5230).
"""

from __future__ import annotations

import hashlib
import re
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
# Licence texts are kept verbatim; the hashes pin them against edits. Project-specific
# terms (the dual-licensing offer) belong in NOTICE and COMMERCIAL_LICENSE.md, never
# inside a licence text - the GNU text forbids changing the licence document itself.
# LICENSE:        https://www.gnu.org/licenses/agpl-3.0.txt
# LICENSES/*.txt: https://github.com/spdx/license-list-data (text/<identifier>.txt)
CANONICAL_LICENCE_SHA256 = {
    "LICENSE": "0d96a4ff68ad6d4b6f1f30f713b18d5184912ba8dd389f86aa7710db079abcb0",
    "LICENSES/AGPL-3.0-only.txt": "d8a6cc31abc16b6748c7a21f21611f5a1ec33f67d22ca23d7da1c19b95496bee",
    "LICENSES/CC0-1.0.txt": "a2010f343487d3f7618affe54f789f5487602331c0a8d03f49e9a7c547cf0499",
    "LICENSES/MIT.txt": "b05785f9f18e6716bab63424b11454513b9943a222595b70411009202fc592b5",
    "LICENSES/OFL-1.1.txt": "8eea8287e5876b539670cadb82e99f9a7afddec6f6730811be1daf25d2e9bcfd",
}
AGPL_CLOSING_LINE = "<https://www.gnu.org/licenses/>."
COMMERCIAL_CONTACT = "contact@alpininsight.ai"
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


@pytest.mark.parametrize(("name", "digest"), sorted(CANONICAL_LICENCE_SHA256.items()))
def test_licence_text_matches_its_canonical_source(name: str, digest: str) -> None:
    """Licence texts are byte-identical to the published originals.

    Software-composition scanners compare licence files against the canonical texts;
    a modified file is reported as an unknown or custom licence.
    """
    actual = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    assert actual == digest, f"{name} deviates from its canonical text (sha256 {actual})"


def test_license_carries_no_appended_terms() -> None:
    """LICENSE ends with the AGPL text, so no project terms are appended to it."""
    lines = [line.strip() for line in (ROOT / "LICENSE").read_text(encoding="utf-8").splitlines()]
    assert [line for line in lines if line][-1] == AGPL_CLOSING_LINE


def test_dual_licensing_offer_is_documented_outside_the_licence_text() -> None:
    """The commercial track stays discoverable in NOTICE and COMMERCIAL_LICENSE.md."""
    assert "COMMERCIAL_LICENSE.md" in (ROOT / "NOTICE").read_text(encoding="utf-8")
    assert "Commercial License" in (ROOT / "COMMERCIAL_LICENSE.md").read_text(encoding="utf-8")


def test_commercial_licence_states_one_contact_address() -> None:
    """The stub names a single address for commercial enquiries, spelled identically.

    A wrong or misspelled address silently costs enquiries, and the address has
    diverged from the rest of the repository before.
    """
    text = (ROOT / "COMMERCIAL_LICENSE.md").read_text(encoding="utf-8")
    assert COMMERCIAL_CONTACT in text
    found = set(re.findall(r"[A-Za-z][A-Za-z._-]*@alpininsight\.[a-z]+", text))
    assert found == {COMMERCIAL_CONTACT}, f"conflicting contact addresses: {sorted(found)}"
