"""Regression tests for reusable Insight UI design tokens."""

import re
from pathlib import Path

INPUT_CSS = Path("insight_ui/utils/input.css")


def test_shadow_role_tokens_are_available() -> None:
    """Ensure packaged theme input exposes the shared shadow role tokens."""
    css = INPUT_CSS.read_text()

    for token in (
        "--insight-shadow-none",
        "--insight-shadow-subtle",
        "--insight-shadow-surface",
        "--insight-shadow-raised",
        "--insight-shadow-overlay",
        "--insight-shadow-focus",
    ):
        assert token in css


def test_shadow_role_classes_are_available() -> None:
    """Ensure packaged theme input exposes reusable shadow utility classes."""
    css = INPUT_CSS.read_text()

    for class_name in (
        ".insight-shadow-none",
        ".insight-shadow-subtle",
        ".insight-shadow-surface",
        ".insight-shadow-raised",
        ".insight-shadow-overlay",
        ".insight-hover-shadow-raised:hover",
        ".insight-hover-shadow-overlay:hover",
    ):
        assert class_name in css


def test_insight_tokens_are_not_defined_twice() -> None:
    """Keep source theme tokens deterministic and easy to override."""
    css = INPUT_CSS.read_text()
    tokens = re.findall(r"^\s*(--insight-[\w-]+)\s*:", css, flags=re.MULTILINE)

    duplicates = sorted({token for token in tokens if tokens.count(token) > 1})

    assert duplicates == []


def test_range_control_uses_semantic_tokens() -> None:
    """Range slider styling should use Insight UI roles, not local technical tokens."""
    css = INPUT_CSS.read_text()

    for token in (
        "--insight-control-range-progress",
        "--insight-control-range-track",
        "--insight-control-range-track-dark",
        "--insight-control-range-fill",
        "--insight-control-range-radius",
        "--insight-control-range-thumb-bg",
        "--insight-control-range-thumb-border",
        "--insight-control-range-thumb-radius",
    ):
        assert token in css

    for legacy_token in (
        "--range-progress",
        "--slider-track-active",
        "--slider-track-inactive",
    ):
        assert legacy_token not in css
