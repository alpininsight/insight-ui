# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the packaged web app manifest."""

from __future__ import annotations

import json
import struct
from pathlib import Path

import insight_ui

FAVICON_DIR = Path(insight_ui.__file__).parent / "static" / "insight_ui" / "favicon"
PNG_IHDR_LENGTH = 13
PNG_RGB_COLOR_TYPE = 2


def test_packaged_webmanifest_references_existing_relative_icons() -> None:
    """Manifest icon paths should survive arbitrary Django static URL prefixes."""
    manifest = json.loads((FAVICON_DIR / "site.webmanifest").read_text(encoding="utf-8"))

    assert manifest["start_url"] == "/"
    assert manifest["scope"] == "/"
    assert manifest["display"] == "standalone"

    for icon in manifest["icons"]:
        source = icon["src"]
        assert not source.startswith("/")
        assert (FAVICON_DIR / source).is_file()


def test_packaged_webmanifest_has_dedicated_maskable_icons() -> None:
    """Android launchers should receive mask-safe 192px and 512px assets."""
    manifest = json.loads((FAVICON_DIR / "site.webmanifest").read_text(encoding="utf-8"))

    maskable_icons = {icon["sizes"]: icon for icon in manifest["icons"] if icon.get("purpose") == "maskable"}

    assert set(maskable_icons) == {"192x192", "512x512"}
    assert all(icon["type"] == "image/png" for icon in maskable_icons.values())

    for dimensions, icon in maskable_icons.items():
        icon_path = FAVICON_DIR / icon["src"]
        with icon_path.open("rb") as png:
            signature = png.read(8)
            chunk_length = struct.unpack(">I", png.read(4))[0]
            chunk_type = png.read(4)
            width, height, _bit_depth, color_type = struct.unpack(">IIBB", png.read(10))

        expected_size = int(dimensions.split("x", maxsplit=1)[0])
        assert signature == b"\x89PNG\r\n\x1a\n"
        assert chunk_length == PNG_IHDR_LENGTH
        assert chunk_type == b"IHDR"
        assert (width, height) == (expected_size, expected_size)
        assert color_type == PNG_RGB_COLOR_TYPE  # Maskable icons need an opaque background.
