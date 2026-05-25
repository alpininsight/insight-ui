"""Tests for design-theme CSS token contracts."""

from pathlib import Path

from django.test import SimpleTestCase
from insight_ui.config import CONFIG_DEFAULTS

THEME_ROOT = Path(__file__).resolve().parents[2] / "insight_ui/static/insight_ui/css/themes"
BOOTSWATCH_THEMES = set(CONFIG_DEFAULTS["design_themes"]["stylesheets"]) - {"default", "alpin", "foundry"}
SEMANTIC_ROLES = ("primary", "secondary", "success", "info", "warning", "danger")


class DesignThemeCssTest(SimpleTestCase):
    """Verify Bootswatch-derived theme files carry text and foreground tokens."""

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

    def test_bootswatch_values_are_not_replaced_by_project_defaults(self) -> None:
        """Representative Bootswatch values should remain sourced from Bootswatch CSS."""
        brite_css = (THEME_ROOT / "brite.css").read_text()
        cerulean_css = (THEME_ROOT / "cerulean.css").read_text()

        assert "--color-insight-secondary: #fff;" in brite_css
        assert "--color-insight-secondary-foreground: #000;" in brite_css
        assert "--color-insight-text-primary: #495057;" in cerulean_css
        assert "--color-insight-text-secondary: rgba(73, 80, 87, 0.75);" in cerulean_css
        assert "--color-insight-primary-foreground: #fff;" in cerulean_css
        assert "--color-insight-secondary-foreground: #000;" in cerulean_css
