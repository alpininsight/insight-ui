"""Tests for the flip_card component."""

from tests.unit.components.test_template_tags import TemplateTagsTestCase


class TestFlipCard(TemplateTagsTestCase):
    """Test suite for the flip_card component."""

    def test_flip_card_back_content_and_style(self) -> None:
        """Flip card can render formatted content on a styled back side."""
        card = {
            "title": "Formatted Flip",
            "content": "Front <strong>content</strong>.",
            "image": {"url": "/static/product.png", "alt": "Product preview"},
            "back_content": "<p>Lorem ipsum</p>",
        }
        template_string = """
        {% load insight_tags %}
        {% flip_card title=card.title content=card.content image=card.image back_content=card.back_content %}
        """

        rendered = self.render_template(template_string, context={"card": card})
        assert "Front <strong>content</strong>." in rendered
        assert "<p>Lorem ipsum</p>" in rendered
