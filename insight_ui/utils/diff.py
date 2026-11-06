# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Word and line diffs for the text_diff and code_diff components."""

import re
import textwrap
from difflib import SequenceMatcher
from itertools import accumulate

# Words, runs of whitespace and single punctuation marks, so a changed comma does not mark the whole word.
_TOKENS = re.compile(r"\s+|\w+|[^\w\s]")

# Below this share of equal tokens a line pair counts as rewritten; marking its changes would mark almost
# everything, so the line background alone says enough.
_MIN_SIMILARITY = 0.5

# Marks separated by at most this many characters (a space, a quote) read as one change.
_MAX_GAP = 2

type Span = tuple[int, int]


def word_changes(old: str, new: str) -> tuple[float, list[tuple[str, Span, Span]]]:
    """Compare two texts word by word.

    Args:
        old: The original text.
        new: The changed text.

    Returns:
        The similarity (0 to 1) and the opcodes ("equal", "delete", "insert", "replace") with the
        character spans they cover in the old and in the new text.

    """
    old_tokens = _TOKENS.findall(old)
    new_tokens = _TOKENS.findall(new)
    old_offsets = [0, *accumulate(map(len, old_tokens))]
    new_offsets = [0, *accumulate(map(len, new_tokens))]
    matcher = SequenceMatcher(None, old_tokens, new_tokens, autojunk=False)
    changes: list[tuple[str, Span, Span]] = [
        (tag, (old_offsets[i1], old_offsets[i2]), (new_offsets[j1], new_offsets[j2]))
        for tag, i1, i2, j1, j2 in matcher.get_opcodes()
    ]
    return matcher.ratio(), changes


def text_parts(old: str, new: str) -> list[dict[str, str]]:
    """Split two texts into unchanged, removed and added parts, in reading order.

    Args:
        old: The original text.
        new: The changed text.

    Returns:
        Parts with a "kind" ("equal", "delete" or "insert") and their "text".

    """
    parts = []
    for tag, (old_start, old_end), (new_start, new_end) in word_changes(old, new)[1]:
        if tag == "equal":
            parts.append({"kind": "equal", "text": old[old_start:old_end]})
            continue
        if old_end > old_start:
            parts.append({"kind": "delete", "text": old[old_start:old_end]})
        if new_end > new_start:
            parts.append({"kind": "insert", "text": new[new_start:new_end]})
    return parts


def _merge_close(spans: list[Span]) -> list[Span]:
    """Join spans that are only a few characters apart, so a change is not split into fragments."""
    merged: list[Span] = []
    for start, end in spans:
        if merged and start - merged[-1][1] <= _MAX_GAP:
            merged[-1] = (merged[-1][0], end)
        else:
            merged.append((start, end))
    return merged


def _changed_spans(old_line: str, new_line: str) -> tuple[list[Span], list[Span]]:
    """Return the changed parts of two similar lines; nothing if the line was rewritten."""
    similarity, changes = word_changes(old_line, new_line)
    if similarity < _MIN_SIMILARITY:
        return [], []
    old_spans = [old for tag, old, _ in changes if tag != "equal" and old[1] > old[0]]
    new_spans = [new for tag, _, new in changes if tag != "equal" and new[1] > new[0]]
    return _merge_close(old_spans), _merge_close(new_spans)


def code_lines(code: str) -> list[str]:
    """Return the lines of a snippet without common indentation and surrounding blank lines.

    Args:
        code: The snippet, e.g. an indented triple-quoted string.

    Returns:
        The lines of the snippet.

    """
    return textwrap.dedent(code).strip("\n").splitlines()


def unified_diff(old: str, new: str) -> tuple[str, list[Span]]:
    """Build a unified diff of two snippets and the changed parts inside changed lines.

    Every line is kept and starts with a marker: " " unchanged, "-" removed, "+" added. A removed and an
    added line at the same position of a changed block are compared word by word.

    Args:
        old: The original code.
        new: The changed code.

    Returns:
        The diff text and the [start, end) character spans of the changed parts within it.

    """
    old_lines = code_lines(old)
    new_lines = code_lines(new)
    lines: list[str] = []
    paired: list[tuple[int, int, str, str]] = []
    for tag, i1, i2, j1, j2 in SequenceMatcher(None, old_lines, new_lines, autojunk=False).get_opcodes():
        if tag == "equal":
            lines.extend(f" {line}" for line in old_lines[i1:i2])
            continue
        removed, added = old_lines[i1:i2], new_lines[j1:j2]
        first_removed = len(lines)
        first_added = first_removed + len(removed)
        paired.extend(
            (first_removed + offset, first_added + offset, old_line, new_line)
            for offset, (old_line, new_line) in enumerate(zip(removed, added, strict=False))
        )
        lines.extend(f"-{line}" for line in removed)
        lines.extend(f"+{line}" for line in added)

    # Character offset of each line's content: its start in the joined text plus the marker column.
    content_starts = [start + 1 for start in accumulate((len(line) + 1 for line in lines), initial=0)]
    spans: list[Span] = []
    for removed_index, added_index, old_line, new_line in paired:
        old_spans, new_spans = _changed_spans(old_line, new_line)
        spans.extend((content_starts[removed_index] + s, content_starts[removed_index] + e) for s, e in old_spans)
        spans.extend((content_starts[added_index] + s, content_starts[added_index] + e) for s, e in new_spans)
    return "\n".join(lines), sorted(spans)
