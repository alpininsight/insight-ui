"""Tests for design-theme CSS token contracts."""

from pathlib import Path

from django.test import SimpleTestCase
from insight_ui.config import CONFIG_DEFAULTS

THEME_ROOT = Path(__file__).resolve().parents[2] / "insight_ui/static/insight_ui/css/themes"
INPUT_CSS = Path(__file__).resolve().parents[2] / "insight_ui/utils/input.css"
TAILWIND_CSS = Path(__file__).resolve().parents[2] / "insight_ui/static/insight_ui/css/tailwind.css"
TAILWIND_MIN_CSS = Path(__file__).resolve().parents[2] / "insight_ui/static/insight_ui/css/tailwind.min.css"
STYLE_FAMILY_THEMES = {"skeuomorphic", "flat", "material", "neumorphic", "glass", "bento", "drawn"}
PROJECT_THEMES = {"default", "alpin", "foundry"} | STYLE_FAMILY_THEMES
BOOTSWATCH_THEMES = set(CONFIG_DEFAULTS["design_themes"]["stylesheets"]) - PROJECT_THEMES
SEMANTIC_ROLES = ("primary", "secondary", "success", "info", "warning", "danger")
DARK_BOOTSWATCH_THEMES = ("cyborg", "darkly", "quartz", "slate", "solar", "superhero", "vapor")
WHITE_SECONDARY_THEMES = ("lux", "materia", "simplex", "zephyr")


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
            "--insight-border-width-control:",
            "--insight-border-width-surface:",
            "--insight-border-style-control:",
            "--insight-surface-texture:",
            "--insight-background-pattern:",
            "--insight-gradient-surface:",
            "--insight-gradient-button:",
            "--insight-radius-sm:",
            "--insight-radius-lg:",
            "--insight-radius-pill:",
            "--insight-shadow-inset:",
            "--insight-shadow-raised:",
            "--insight-shadow-offset:",
            "--insight-backdrop-blur:",
            "--insight-motion-duration-normal:",
            "--insight-motion-easing-standard:",
            "--insight-density-control-x:",
            "--insight-density-surface-y:",
            "--insight-font-display:",
            "--insight-icon-family:",
            "--insight-sketch-line-offset:",
            "--insight-tracking-display:",
            "--insight-tracking-caption:",
        ):
            assert token in input_css

        assert '[data-theme="dark"] {' in input_css
        assert "--color-insight-text-primary: var(--color-insight-text-primary-dark);" in input_css
        assert "--color-insight-surface-panel: var(--color-insight-surface-panel-dark);" in input_css
        assert "--color-insight-border-control: var(--color-insight-border-control-dark);" in input_css

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
            ".insight-border-control-width",
            ".insight-border-surface-width",
            ".insight-surface-textured",
            ".insight-gradient-surface",
            ".insight-shadow-inset",
            ".insight-glass",
            ".insight-motion-standard",
            ".insight-density-control",
            ".insight-font-display",
            ".insight-sketch-border",
        ):
            assert semantic_class in input_css

    def test_design_theme_switcher_has_curated_display_order(self) -> None:
        """The default selector should expose style families, not every color variant."""
        design_themes = CONFIG_DEFAULTS["design_themes"]
        display_order = design_themes["display_order"]

        assert display_order == (
            "default",
            "skeuomorphic",
            "flat",
            "material",
            "neumorphic",
            "glass",
            "brite",
            "bento",
            "drawn",
        )
        assert set(display_order) <= set(design_themes["stylesheets"])
        assert set(display_order) <= set(design_themes["labels"])

    def test_generated_tailwind_css_includes_semantic_surface_and_radius_classes(self) -> None:
        """Packaged CSS must include semantic classes used by component templates."""
        for css_file in (TAILWIND_CSS, TAILWIND_MIN_CSS):
            css = css_file.read_text()

            for selector in (
                ".insight-surface-page",
                ".insight-surface-base",
                ".insight-surface-soft",
                ".insight-radius-control",
                ".insight-radius-surface",
                ".insight-radius-pill",
                ".insight-gradient-surface",
                ".insight-shadow-inset",
                ".insight-glass",
                ".insight-density-control",
                ".insight-font-display",
                ".insight-sketch-border",
            ):
                assert selector in css

    def test_drawn_theme_defines_semantic_style_tokens(self) -> None:
        """The drawn style should be CSS-only and driven by the public token contract."""
        drawn_css = (THEME_ROOT / "drawn.css").read_text()

        for token in (
            "--insight-design-theme-name: drawn;",
            "--insight-border-width-control:",
            "--insight-surface-texture:",
            "--insight-background-pattern:",
            "--insight-gradient-surface:",
            "--insight-shadow-button:",
            "--insight-radius-md:",
            "--insight-sketch-line-offset:",
            "--insight-sketch-shadow:",
        ):
            assert token in drawn_css

    def test_style_family_themes_define_light_and_dark_semantic_tokens(self) -> None:
        """Style families should override semantic tokens instead of component CSS."""
        for theme_name in STYLE_FAMILY_THEMES:
            theme_css = (THEME_ROOT / f"{theme_name}.css").read_text()

            assert f"--insight-design-theme-name: {theme_name};" in theme_css
            assert "--color-insight-text-primary:" in theme_css
            assert "--color-insight-surface-page:" in theme_css
            assert "--color-insight-surface-panel:" in theme_css
            assert "--color-insight-border-control:" in theme_css
            assert '[data-theme="dark"]' in theme_css
            assert "--color-insight-text-primary-dark: var(--color-insight-text-primary);" in theme_css
            assert "--color-insight-surface-panel-dark: var(--color-insight-surface-panel);" in theme_css
            assert "--color-insight-border-control-dark: var(--color-insight-border-control);" in theme_css

    def test_input_css_uses_semantic_tokens_for_core_utilities(self) -> None:
        """Core utilities should inherit dark values through central token overrides."""
        input_css = INPUT_CSS.read_text()

        for selector in (
            ".btn-subtil",
            ".btn-disabled",
            ".component-container",
            ".example-container",
            ".info-container",
            ".inline-tag",
            ".input",
            ".slider-wrapper",
        ):
            assert selector in input_css

        assert ".btn-subtil:where([data-theme=dark], [data-theme=dark] *)" not in input_css
        assert ".component-container:where([data-theme=dark], [data-theme=dark] *)" not in input_css
        assert ".input:where([data-theme=dark], [data-theme=dark] *)" not in input_css
        assert ".dark .slider-wrapper" not in input_css
        assert "background-color: var(--color-insight-surface-soft);" in input_css
        assert "border-color: var(--color-insight-border-surface);" in input_css

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
        zephyr_css = (THEME_ROOT / "zephyr.css").read_text()

        assert "--color-insight-secondary: #fff;" in brite_css
        assert "--color-insight-button-border: #000;" in brite_css
        assert "--insight-shadow-button: 3px 3px 0 0 var(--color-insight-button-border);" in brite_css
        assert "--insight-shadow-surface: 3px 3px 0 0 var(--color-insight-border-surface);" in brite_css
        assert "--color-insight-secondary-foreground: #000;" in brite_css
        assert "--color-insight-text-primary: #495057;" in cerulean_css
        assert "--color-insight-text-secondary: rgba(73, 80, 87, 0.75);" in cerulean_css
        assert "--color-insight-primary-foreground: #fff;" in cerulean_css
        assert "--color-insight-secondary-foreground: #000;" in cerulean_css
        assert "--color-insight-secondary-border: #dee2e6;" in zephyr_css

    def test_dark_bootswatch_themes_define_dark_surface_and_border_tokens(self) -> None:
        """Dark design themes need dark aliases for semantic surface classes."""
        for theme_name in DARK_BOOTSWATCH_THEMES:
            theme_css = (THEME_ROOT / f"{theme_name}.css").read_text()

            for token in (
                "--color-insight-surface-page-dark:",
                "--color-insight-surface-base-dark:",
                "--color-insight-surface-soft-dark:",
                "--color-insight-surface-muted-dark:",
                "--color-insight-surface-canvas-dark:",
                "--color-insight-surface-panel-dark:",
                "--color-insight-surface-raised-dark:",
                "--color-insight-surface-sunken-dark:",
                "--color-insight-border-surface-dark:",
                "--color-insight-border-control-dark:",
                "--color-insight-border-muted-dark:",
            ):
                assert token in theme_css

    def test_white_secondary_bootswatch_themes_define_visible_secondary_borders(self) -> None:
        """White secondary buttons need visible border tokens on white surfaces."""
        for theme_name in WHITE_SECONDARY_THEMES:
            theme_css = (THEME_ROOT / f"{theme_name}.css").read_text()

            assert "--color-insight-secondary: #fff;" in theme_css
            assert "--color-insight-secondary-border: #dee2e6;" in theme_css
            assert "--color-insight-secondary-border-hover: #ced4da;" in theme_css
            assert "--color-insight-secondary-border-active: #adb5bd;" in theme_css
