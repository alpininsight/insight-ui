# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the chat component."""

from bs4 import BeautifulSoup
from insight_ui.configs import ChatConfig, HtmxConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestChat(TemplateTagsTestCase):
    """Test suite for the chat component."""

    def render_chat(self, config: ChatConfig) -> BeautifulSoup:
        """Render the chat for the given config."""
        rendered = self.render_template("{% load insight_tags %}{% chat config %}", {"config": config})
        return BeautifulSoup(rendered, "html.parser")

    def test_posts_messages_and_appends_the_response(self) -> None:
        """The form posts to request_url and appends the answer to its own response container."""
        soup = self.render_chat(ChatConfig(request_url="/chat/"))
        form = soup.form

        assert form["hx-post"] == "/chat/"
        assert form["hx-target"] == "#chat-response"
        assert form["hx-swap"] == "beforeend"
        assert soup.find(id="chat-response")["aria-live"] == "polite"
        assert soup.find("input", attrs={"name": "msg"})["id"] == "chat-message"
        assert soup.find("label")["for"] == "chat-message"

    def test_two_chats_do_not_share_ids(self) -> None:
        """tag_id prefixes every ID, so a second chat targets its own container."""
        soup = self.render_chat(ChatConfig(request_url="/support/", tag_id="support"))

        assert soup.form["hx-target"] == "#support-response"
        assert soup.find(id="support-response") is not None
        assert soup.find(id="support-message") is not None

    def test_shared_request_options_do_not_change_the_mechanism(self) -> None:
        """Method, target and swap stay fixed; the HtmxConfig adds the shared options."""
        htmx = HtmxConfig(
            request_url="/ignored/", method="get", target="#elsewhere", swap_method="innerHTML", vals={"room": 1}
        )
        form = self.render_chat(ChatConfig(request_url="/chat/", htmx=htmx)).form

        assert form["hx-post"] == "/chat/"
        assert not form.has_attr("hx-get")
        assert form["hx-target"] == "#chat-response"
        assert form["hx-swap"] == "beforeend"
        assert form["hx-vals"] == '{"room":1}'
