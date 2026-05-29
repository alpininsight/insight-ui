"""Tests for design-theme CSS token contracts."""

from pathlib import Path

from django.test import SimpleTestCase
from insight_ui.config import CONFIG_DEFAULTS

THEME_ROOT = Path(__file__).resolve().parents[2] / "insight_ui/static/insight_ui/css/themes"
INPUT_CSS = Path(__file__).resolve().parents[2] / "insight_ui/utils/input.css"
BOOTSWATCH_THEMES = set(CONFIG_DEFAULTS["design_themes"]["stylesheets"]) - {"default", "alpin", "foundry"}
SEMANTIC_ROLES = ("primary", "secondary", "success", "info", "warning", "danger")


class DesignThemeCssTest(SimpleTestCase):
    """Verify Bootswatch-derived theme files carry text and foreground tokens."""

    def test_input_css_exposes_brand_alignment_tokens(self) -> None:
        """Brand-relevant design concepts must be public Insight UI tokens."""
        input_css = INPUT_CSS.read_text()

        for token in (
            "--font-display:",
            "--font-mono:",
            "--color-insight-pending:",
            "--color-insight-surface-page:",
            "--color-insight-surface-base:",
            "--color-insight-surface-soft:",
            "--color-insight-surface-canvas:",
            "--color-insight-surface-panel:",
            "--color-insight-surface-raised:",
            "--color-insight-surface-sunken:",
            "--color-insight-disabled:",
            "--color-insight-focus-ring:",
            "--insight-radius-sm:",
            "--insight-radius-lg:",
            "--insight-radius-pill:",
            "--insight-tracking-display:",
            "--insight-tracking-caption:",
        ):
            assert token in input_css

        for semantic_class in (
            ".insight-surface-page",
            ".insight-surface-base",
            ".insight-surface-soft",
            ".insight-surface-canvas",
            ".insight-surface-panel",
            ".insight-surface-raised",
            ".insight-surface-sunken",
            ".insight-radius-control",
            ".insight-radius-surface",
            ".insight-radius-pill",
            ".insight-focus-ring",
        ):
            assert semantic_class in input_css

    def test_dark_mode_overrides_public_tokens_without_dark_suffix_contract(self) -> None:
        """Dark mode should override the same semantic tokens instead of exposing duplicate token names."""
        input_css = INPUT_CSS.read_text()
        dark_block = input_css.split('[data-theme="dark"] {', maxsplit=1)[1].split("}", maxsplit=1)[0]

        for token in (
            "--color-insight-text-primary:",
            "--color-insight-surface-page:",
            "--color-insight-surface-base:",
            "--color-insight-border-surface:",
            "--color-insight-focus-ring-offset:",
        ):
            assert token in dark_block

        assert "-dark:" not in input_css
        assert "dark:" not in input_css

    def test_bootswatch_themes_define_text_and_button_foreground_tokens(self) -> None:
        """Every Bootswatch theme must include text and button font color tokens."""
        for theme_name in BOOTSWATCH_THEMES:
            theme_css = (THEME_ROOT / f"{theme_name}.css").read_text()

            assert "--color-insight-text-primary:" in theme_css
            assert "--color-insight-text-secondary:" in theme_css
            assert "--color-insight-text-link:" in theme_css
            assert '[data-theme="dark"]' in theme_css

            for role in SEMANTIC_ROLES:
                assert f"--color-insight-{role}-foreground:" in theme_css
                assert f"--color-insight-{role}-foreground-hover:" in theme_css
                assert f"--color-insight-{role}-foreground-active:" in theme_css

            assert "-dark:" not in theme_css

    def test_bootswatch_values_are_not_replaced_by_project_defaults(self) -> None:
        """Representative Bootswatch values should remain sourced from Bootswatch CSS."""
        brite_css = (THEME_ROOT / "brite.css").read_text()
        cerulean_css = (THEME_ROOT / "cerulean.css").read_text()

        assert "--color-insight-secondary: #fff;" in brite_css
        assert "--color-insight-button-border: #000;" in brite_css
        assert "--insight-shadow-button: 3px 3px 0 0 var(--color-insight-button-border);" in brite_css
        assert "--insight-shadow-surface: 3px 3px 0 0 var(--color-insight-border-surface);" in brite_css
        assert "--color-insight-secondary-foreground: #000;" in brite_css
        assert "--color-insight-text-primary: #495057;" in cerulean_css
        assert "--color-insight-text-secondary: rgba(73, 80, 87, 0.75);" in cerulean_css
        assert "--color-insight-primary-foreground: #fff;" in cerulean_css
        assert "--color-insight-secondary-foreground: #000;" in cerulean_css
