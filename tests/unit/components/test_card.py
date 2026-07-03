"""Tests for the card component."""

from bs4 import BeautifulSoup
from insight_ui.configs import ButtonConfig

from tests.unit.components.test_template_tags import TemplateTagsTestCase


class TestCard(TemplateTagsTestCase):
    """Test suite for the card component."""

    def test_card_basic(self) -> None:
        """Test für grundlegende card Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% card title="Test Card" content="Test Card Content" %}
        """
        rendered = self.render_template(template_string)
        assert "Test Card" in rendered

    def test_card_content_allows_html(self) -> None:
        """Card content can render developer-provided HTML fragments."""
        rendered = self.render_template(
            '{% load insight_tags %}{% card title="Formatted" content="<strong>Important</strong><br>Line 2" %}'
        )
        assert "<strong>Important</strong>" in rendered
        assert "<br>Line 2" in rendered

    def test_card_actions_stay_inside_long_html_content_layout(self) -> None:
        """Long formatted card content must not push actions outside the card."""
        card = {
            "title": "Formatted card content",
            "content": (
                "<p>This card uses <strong>bold text</strong>, <em>line breaks</em>, "
                "and a short list:</p><ul><li>Safe developer supplied markup</li>"
                "<li>Structured text in cards</li><li>Additional content that should scroll</li></ul>"
            ),
            "actions": [ButtonConfig(label="Learn more", request_url="/docs/", type="primary")],
        }
        template_string = """
        {% load insight_tags %}
        {% card title=card.title content=card.content actions=card.actions %}
        """

        rendered = self.render_template(template_string, context={"card": card})
        soup = BeautifulSoup(rendered, "html.parser")

        outer_card = soup.find("div", class_="max-w-96")
        assert outer_card is not None
        assert "flex" in outer_card.get("class", [])
        assert "flex-col" in outer_card.get("class", [])
        assert "min-h-56" in outer_card.get("class", [])
        assert "h-56" not in outer_card.get("class", [])

        body = outer_card.find("div", class_="flex")
        assert body is not None
        assert "min-h-0" in body.get("class", [])
        assert "flex-1" in body.get("class", [])
        assert "min-h-56" not in body.get("class", [])

        content = outer_card.find("div", class_="overflow-auto")
        assert content is not None
        assert "min-h-0" in content.get("class", [])
        assert "grow" in content.get("class", [])
        assert content.find("strong", string="bold text") is not None

        actions = outer_card.find("div", class_="mt-auto")
        assert actions is not None
        assert "flex-wrap" in actions.get("class", [])
        # Button with request_url renders as <a> tag
        action_link = actions.find("a", class_="btn")
        assert action_link is not None
        assert action_link.get_text(strip=True) == "Learn more"
