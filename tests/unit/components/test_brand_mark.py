"""Tests for the brand_mark component."""

from insight_ui.configs.utils import BrandMarkConfig

from tests.unit.components.test_template_tags import TemplateTagsTestCase


class TestBrandMark(TemplateTagsTestCase):
    """Test suite for the brand_mark component."""

    def test_brand_mark_renders_default_text(self) -> None:
        """Default brand mark renders without errors."""
        rendered = self.render_template("{% load insight_tags %}{% brand_mark %}")
        assert rendered.strip() != ""

    def test_brand_mark_custom_text(self) -> None:
        """primary_text / secondary_text override the wordmark runs."""
        rendered = self.render_template(
            '{% load insight_tags %}{% brand_mark primary_text="Foo Bar" secondary_text="Cloud" %}'
        )
        assert "Foo Bar" in rendered
        assert "Cloud" in rendered

    def test_brand_mark_config(self) -> None:
        """A config dict configures the mark."""
        rendered = self.render_template(
            "{% load insight_tags %}{% brand_mark config=cfg %}",
            context={"cfg": BrandMarkConfig(primary_text="Custom", secondary_text="Brand")},
        )
        assert "Custom" in rendered
        assert "Brand" in rendered
