"""Tests for the app_card component."""

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestAppCard(TemplateTagsTestCase):
    """Test suite for the app_card component."""

    def test_app_card_content_allows_html(self) -> None:
        """App card content can render developer-provided HTML fragments."""
        card = {
            "title": "Catalog Product",
            "content": "Supports <strong>formatted</strong> content.",
            "image": {"url": "/static/product.png", "alt": "Product preview"},
        }
        template_string = """
        {% load insight_tags %}
        {% app_card title=card.title content=card.content image=card.image %}
        """

        rendered = self.render_template(template_string, context={"card": card})
        assert "<strong>formatted</strong>" in rendered
