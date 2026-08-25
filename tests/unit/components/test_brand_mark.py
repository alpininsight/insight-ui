"""Tests for the brand_mark component."""

from insight_ui.configs.utils import BrandMarkConfig

from tests.unit.components.test_template_tags import TemplateTagsTestCase


class TestBrandMark(TemplateTagsTestCase):
    """Test suite for the brand_mark component."""

    def test_brand_mark_renders_default_text(self) -> None:
        """Default brand mark renders without errors."""
        rendered = self.render_template("{% load insight_tags %}{% brand_mark %}")
        assert rendered.strip() != ""
        assert "The two halves of the wordmark" not in rendered

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

    def test_brand_mark_secondary_text_uses_the_accent_token(self) -> None:
        """The wordmark's second half is the accent, not the primary.

        insight-brand DESIGN.md makes Signal Orange the single accent and keeps
        it constant across the Light and Dark palettes, while text colours flip
        between them. The template carried ``text-insight-primary`` here, so the
        word rendered in Berliner Blau in both themes -- off-brand, and on the
        dark canvas it was dark navy on near-black at roughly 1.3:1.

        Pinned separately from the render smoke tests above because both classes
        are valid CSS and both render without error: nothing else in the suite
        can tell the difference.
        """
        rendered = self.render_template("{% load insight_tags %}{% brand_mark %}")
        assert "text-insight-secondary" in rendered
        assert "font-bold text-insight-primary" not in rendered
