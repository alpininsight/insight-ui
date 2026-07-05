"""Regression tests for reusable Insight UI design tokens."""

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
