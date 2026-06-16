"""Tests for Insight UI runtime configuration merging."""

from django.test import SimpleTestCase, override_settings
from insight_ui.config import get_config


class ConfigMergeTest(SimpleTestCase):
    """Verify host settings extend nested defaults without dropping siblings."""

    @override_settings(
        INSIGHT_UI={"design_themes": {"stylesheets": {"custom": "custom/theme.css"}, "labels": {"custom": "Custom"}}}
    )
    def test_nested_design_theme_overrides_preserve_defaults(self) -> None:
        """Adding one host theme should not remove built-in theme assets or labels."""
        design_themes = get_config("design_themes")

        assert design_themes["stylesheets"]["custom"] == "custom/theme.css"
        assert design_themes["labels"]["custom"] == "Custom"
        assert design_themes["stylesheets"]["default"] == "insight_ui/css/themes/default.css"
        assert design_themes["stylesheets"]["cerulean"] == "insight_ui/css/themes/cerulean.css"
        assert design_themes["labels"]["default"] == "Original"
        assert design_themes["labels"]["cerulean"] == "Cerulean"
        assert design_themes["display_order"] == (
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

    @override_settings(INSIGHT_UI={"design_themes": {"default": "cerulean"}})
    def test_design_theme_default_is_added_to_display_order_when_valid(self) -> None:
        """A valid configured default must be selectable in the navbar switcher."""
        design_themes = get_config("design_themes")

        assert design_themes["default"] == "cerulean"
        assert design_themes["display_order"][0] == "cerulean"
        assert design_themes["display_order"].count("cerulean") == 1

    @override_settings(INSIGHT_UI={"design_themes": {"default": "missing-theme"}})
    def test_invalid_design_theme_default_falls_back_to_available_default(self) -> None:
        """Invalid defaults are reset before templates can render broken stylesheet URLs."""
        design_themes = get_config("design_themes")

        assert design_themes["default"] == "default"
        assert "missing-theme" not in design_themes["display_order"]
