"""Tests for the chat component."""

from bs4 import BeautifulSoup

from tests.unit.components.test_template_tags import TemplateTagsTestCase


class TestChat(TemplateTagsTestCase):
    """Test suite for the chat component."""

    def test_chat_response_uses_semantic_message_classes(self) -> None:
        """Chat response bubbles use semantic classes instead of hard-coded colors."""
        rendered = self.render_template(
            '{% include "insight_ui/components/chat_response.html" with msg=msg %}', context={"msg": "Hello"}
        )
        soup = BeautifulSoup(rendered, "html.parser")

        own_message = soup.select_one(".insight-chat-message-own")
        response_message = soup.select_one(".insight-chat-message-response")

        assert own_message is not None
        assert response_message is not None
        assert "insight-chat-message" in own_message.get("class", [])
        assert "insight-chat-message" in response_message.get("class", [])
        assert "bg-gray-50" not in own_message.get("class", [])
        assert "dark:bg-gray-700" not in own_message.get("class", [])
        assert "bg-gray-200" not in response_message.get("class", [])
        assert "dark:bg-gray-600" not in response_message.get("class", [])
