# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Compile and include app catalogs in every distribution, without system gettext."""

import re
from collections import Counter
from io import BytesIO
from pathlib import Path
from typing import Any

from babel.messages.catalog import Message
from babel.messages.extract import DEFAULT_KEYWORDS, extract
from babel.messages.mofile import write_mo
from babel.messages.pofile import read_po
from django.utils.translation import templatize
from hatchling.builders.hooks.plugin.interface import BuildHookInterface

NAMED_FORMAT = re.compile(r"%(?:%|\(([^)]+)\)[#0 +\-]*(?:\d+|\*)?(?:\.(?:\d+|\*))?[hlL]?[diouxXeEfFgGcrsa])")
KEYWORDS = {
    **DEFAULT_KEYWORDS,
    "gettext_lazy": None,
    "gettext_noop": None,
    "ngettext_lazy": (1, 2),
    "pgettext_lazy": ((1, "c"), 2),
    "npgettext_lazy": ((1, "c"), 2, 3),
}
type MessageKey = tuple[str | tuple[str, ...], str | None]


def extract_source_messages(root: Path) -> dict[str, set[MessageKey]]:
    """Read package sources without importing them, retaining context and plural IDs."""
    messages: dict[str, set[MessageKey]] = {"django": set(), "djangojs": set()}
    for source in sorted((root / "insight_ui").rglob("*")):
        if not source.is_file() or "locale" in source.relative_to(root / "insight_ui").parts:
            continue
        if source.suffix in {".py", ".html", ".txt"}:
            domain, method = "django", "python"
            if source.suffix == ".py":
                data = source.read_bytes()
            else:
                converted = templatize(source.read_text(encoding="utf-8"), origin=source.as_posix())
                # Django emits quoted gettext calls between dummy template text.
                # Dedent each line so Python's tokenizer accepts HTML indentation.
                data = "\n".join(line.lstrip() for line in converted.splitlines()).encode()
        elif source.suffix == ".js" and not source.name.endswith(".min.js"):
            domain, method, data = "djangojs", "javascript", source.read_bytes()
        else:
            continue
        for _line, message, _comments, context in extract(method, BytesIO(data), keywords=KEYWORDS):
            messages[domain].add((message, context))
    return messages


def _named_placeholders(value: str) -> Counter[str]:
    """Count named formats while consuming escaped percent signs as literals."""
    return Counter(match[1] for match in NAMED_FORMAT.finditer(value) if match[1] is not None)


def _preserves_placeholders(message: Message) -> bool:
    """Check each singular/plural target against the matching English source form."""
    source = message.id if isinstance(message.id, tuple) else (message.id,)
    target = message.string if isinstance(message.string, tuple) else (message.string,)
    return all(
        isinstance(value, str) and _named_placeholders(value) == _named_placeholders(source[0 if index == 0 else -1])
        for index, value in enumerate(target)
    )


def compile_catalogs(root: Path) -> list[str]:
    """Validate committed PO sources and deterministically compile their MO artifacts."""
    locale = root / "insight_ui" / "locale"
    sources = sorted(locale.glob("*/LC_MESSAGES/*.po"))
    required = {locale / "de/LC_MESSAGES/django.po", locale / "de/LC_MESSAGES/djangojs.po"}
    if not required.issubset(sources):
        message = "The package must include both German gettext source catalogs."
        raise ValueError(message)
    extracted = extract_source_messages(root)
    validated = []
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
                or not _preserves_placeholders(entry)
            )
        ]
        if str(catalog.locale) != source.parent.parent.name or catalog.fuzzy or untranslated or list(catalog.check()):
            message = f"Catalog must be complete, non-fuzzy and preserve placeholders: {source.relative_to(root)}"
            raise ValueError(message)
        present = {(entry.id, entry.context) for entry in catalog if entry.id}
        if missing := extracted.get(source.stem, set()) - present:
            message = f"Catalog omits source messages in {source.relative_to(root)}: {sorted(missing, key=repr)!r}"
            raise ValueError(message)
        validated.append((source, catalog))
    artifacts = []
    for source, catalog in validated:
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
