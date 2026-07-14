"""Tests for the brand_mark component."""

from bs4 import BeautifulSoup
from insight_ui.configs.utils import BrandMarkConfig

from tests.unit.components.test_template_tags import TemplateTagsTestCase


class TestBrandMark(TemplateTagsTestCase):
    """Test suite for the brand_mark component."""

    def test_brand_mark_logo_position_start_is_default(self) -> None:
        """Default position keeps the group left-aligned (no justify-between)."""
        rendered = self.render_template("{% load insight_tags %}{% brand_mark %}")
        root = BeautifulSoup(rendered, "html.parser").find("div")
        assert "justify-between" not in root.get("class", [])

    def test_brand_mark_logo_position_end_pushes_logo_to_edge(self) -> None:
        """Position 'end' left-aligns the wordmark and pushes the logo out."""
        rendered = self.render_template('{% load insight_tags %}{% brand_mark logo_position="end" %}')
        root = BeautifulSoup(rendered, "html.parser").find("div")
        assert "justify-between" in root.get("class", [])

    def test_brand_mark_custom_text(self) -> None:
        """primary_text / secondary_text override the wordmark runs."""
        rendered = self.render_template(
            '{% load insight_tags %}{% brand_mark primary_text="Foo Bar" secondary_text="Cloud" %}'
        )
        assert "Foo Bar" in rendered
        assert "Cloud" in rendered

    def test_brand_mark_config(self) -> None:
        """A config dict configures the mark (mirrors the logo tag style)."""
        rendered = self.render_template(
            "{% load insight_tags %}{% brand_mark config=cfg %}", context={"cfg": BrandMarkConfig(logo_position="end")}
        )
        root = BeautifulSoup(rendered, "html.parser").find("div")
        assert "justify-between" in root.get("class", [])
        assert "order-2" in rendered
