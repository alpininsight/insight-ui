# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Compile and include app catalogs in every distribution, without system gettext."""

from io import BytesIO
from pathlib import Path
from typing import Any

from babel.messages.mofile import write_mo
from babel.messages.pofile import read_po
from hatchling.builders.hooks.plugin.interface import BuildHookInterface


def compile_catalogs(root: Path) -> list[str]:
    """Validate committed PO sources and deterministically compile their MO artifacts."""
    locale = root / "insight_ui" / "locale"
    sources = sorted(locale.glob("*/LC_MESSAGES/*.po"))
    required = {locale / "de/LC_MESSAGES/django.po", locale / "de/LC_MESSAGES/djangojs.po"}
    if not required.issubset(sources):
        message = "The package must include both German gettext source catalogs."
        raise ValueError(message)
    artifacts = []
    for source in sources:
        with source.open("rb") as stream:
            catalog = read_po(stream, locale=source.parent.parent.name, domain=source.stem, abort_invalid=True)
        untranslated = [
            entry.id
            for entry in catalog
            if entry.id
            and (
                "fuzzy" in entry.flags
                or not entry.string
                or (isinstance(entry.string, tuple) and not all(entry.string))
            )
        ]
        if str(catalog.locale) != source.parent.parent.name or catalog.fuzzy or untranslated or list(catalog.check()):
            message = f"Catalog must be complete, non-fuzzy and preserve placeholders: {source.relative_to(root)}"
            raise ValueError(message)
        output = BytesIO()
        write_mo(output, catalog, use_fuzzy=False)
        destination = source.with_suffix(".mo")
        destination.write_bytes(output.getvalue())
        artifacts.append(destination.relative_to(root).as_posix())
    return artifacts


class CustomBuildHook(BuildHookInterface):
    """Include ignored MO outputs in wheels and source distributions."""

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        """Compile PO sources before Hatch selects files for either distribution."""
        del version
        build_data.setdefault("artifacts", []).extend(compile_catalogs(Path(self.root)))
