"""Regression tests for reusable Insight UI design tokens."""

import re
from pathlib import Path

INPUT_CSS = Path("insight_ui/utils/input.css")


def test_shadow_role_tokens_are_available() -> None:
    """Ensure packaged theme input exposes the shared shadow role tokens."""
    css = INPUT_CSS.read_text()

    for token in (
        "--shadow-insight-subtle",
        "--shadow-insight-surface",
        "--shadow-insight-raised",
        "--shadow-insight-overlay",
        "--shadow-insight-focus",
    ):
        assert token in css


def test_radius_role_tokens_are_available() -> None:
    """Ensure semantic radius tokens remain available in the source stylesheet."""
    css = INPUT_CSS.read_text()

    for token in (
        "--radius-insight-xs",
        "--radius-insight-s",
        "--radius-insight-m",
        "--radius-insight-l",
        "--radius-insight-xl",
        "--radius-insight-full",
        "--radius-insight-control",
        "--radius-insight-surface",
        "--radius-insight-raised",
        "--radius-insight-overlay",
    ):
        assert token in css


def test_insight_tokens_are_not_defined_twice() -> None:
    """Keep source theme tokens deterministic and easy to override."""
    css = INPUT_CSS.read_text()
    tokens = re.findall(r"^\s*(--insight-[\w-]+)\s*:", css, flags=re.MULTILINE)

    duplicates = sorted({token for token in tokens if tokens.count(token) > 1})

    assert duplicates == []
