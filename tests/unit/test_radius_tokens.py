"""Regression tests for semantic radius design tokens."""

from pathlib import Path

INPUT_CSS = Path("insight_ui/utils/input.css")


def test_radius_role_tokens_are_available() -> None:
    """Ensure semantic radius tokens remain available in the source stylesheet."""
    css = INPUT_CSS.read_text()

    for token in (
        "--insight-radius-none",
        "--insight-radius-sm",
        "--insight-radius-md",
        "--insight-radius-lg",
        "--insight-radius-xl",
        "--insight-radius-pill",
        "--insight-radius-control",
        "--insight-radius-surface",
        "--insight-radius-raised",
        "--insight-radius-overlay",
    ):
        assert token in css


def test_radius_role_classes_are_available() -> None:
    """Ensure semantic radius utility classes remain available."""
    css = INPUT_CSS.read_text()

    for class_name in (
        ".insight-radius-none",
        ".insight-radius-control",
        ".insight-radius-surface",
        ".insight-radius-raised",
        ".insight-radius-overlay",
        ".insight-radius-pill",
        ".insight-radius-control-top",
        ".insight-radius-control-bottom",
        ".insight-radius-control-start",
        ".insight-radius-control-end",
        ".insight-radius-end-none",
        ".insight-radius-start-none",
        ".insight-nav-item-radius",
    ):
        assert class_name in css
