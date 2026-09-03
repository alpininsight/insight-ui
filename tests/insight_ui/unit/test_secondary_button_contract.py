"""Regression tests for the semantic secondary button colour contract."""

from pathlib import Path


def test_secondary_buttons_use_theme_foreground_and_border_tokens() -> None:
    """A product theme can safely use a light secondary surface.

    The component layer must use semantic aliases instead of requiring every
    consumer to override ``.btn-secondary`` or ``.btn-outline-secondary``.
    """
    stylesheet = (Path(__file__).parents[3] / "insight_ui" / "utils" / "input.css").read_text(encoding="utf-8")

    for token in (
        "--color-insight-secondary-foreground",
        "--color-insight-secondary-border",
        "--color-insight-secondary-border-hover",
        "--color-insight-secondary-border-active",
        "--color-insight-secondary-text",
    ):
        assert token in stylesheet

    secondary = stylesheet.split(".btn-secondary {", 1)[1].split(".btn-success", 1)[0]
    outline = stylesheet.split(".btn-outline-secondary {", 1)[1].split(".btn-outline-success", 1)[0]

    assert "color: var(--color-insight-secondary-foreground)" in secondary
    assert "border-color: var(--color-insight-secondary-border)" in secondary
    assert "color: var(--color-insight-secondary-text)" in outline
    assert "border-color: var(--color-insight-secondary-border)" in outline
