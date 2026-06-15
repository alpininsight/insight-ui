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
