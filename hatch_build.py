# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Hatch build hook: compile the package gettext catalogs into the wheel.

Compiled ``.mo`` files are build outputs (ignored by Git), but Django only loads
compiled catalogs. The hook compiles every ``insight_ui/locale/*/LC_MESSAGES/*.po``
with Babel into a temporary directory and force-includes the results, so wheels
built from a checkout or from the sdist ship both ``django`` and ``djangojs``.
"""

import shutil
import tempfile
from pathlib import Path
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

LOCALE_GLOB = "insight_ui/locale/*/LC_MESSAGES/*.po"


def compile_catalog(source: Path, target: Path) -> None:
    """Compile one PO file, failing on syntax or placeholder errors."""
    from babel.messages.mofile import write_mo  # noqa: PLC0415
    from babel.messages.pofile import read_po  # noqa: PLC0415

    with source.open("rb") as handle:
        catalog = read_po(handle, abort_invalid=True)
    errors = [f"{message.id!r}: {error}" for message, problems in catalog.check() for error in problems]
    if errors:
        message = f"{source}: invalid translations: {'; '.join(errors)}"
        raise ValueError(message)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("wb") as handle:
        write_mo(handle, catalog)


class GettextCatalogHook(BuildHookInterface):
    """Add compiled gettext catalogs to regular (non-editable) wheels."""

    PLUGIN_NAME = "custom"

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        """Compile catalogs before the wheel is assembled."""
        if self.target_name != "wheel" or version == "editable":
            return
        root = Path(self.root)
        sources = sorted(root.glob(LOCALE_GLOB))
        if not sources:
            message = f"No gettext catalogs found under {root / 'insight_ui/locale'}"
            raise FileNotFoundError(message)
        self._output = Path(tempfile.mkdtemp(prefix="insight-ui-mo-"))
        for source in sources:
            relative = source.relative_to(root).with_suffix(".mo")
            target = self._output / relative
            compile_catalog(source, target)
            build_data["force_include"][str(target)] = relative.as_posix()

    def finalize(self, version: str, build_data: dict[str, Any], artifact_path: str) -> None:  # noqa: ARG002
        """Remove the temporary compiled catalogs after the wheel is written."""
        output = getattr(self, "_output", None)
        if output is not None:
            shutil.rmtree(output, ignore_errors=True)
