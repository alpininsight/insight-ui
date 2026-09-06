# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the textarea component."""

from bs4 import BeautifulSoup
from insight_ui.configs import TextareaConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase

# TODO: Implement tests for Textarea component  # noqa: TD002, TD003


class TestTextarea(TemplateTagsTestCase):
    """Test suite for the textarea component."""

    def test_textarea_renders_help_text_and_error_semantics(self) -> None:
        """help_text and error are linked via aria-describedby, aria-invalid and aria-errormessage."""
        config = TextareaConfig(
            tag_id="message",
            name="message",
            label="Message",
            required=True,
            help_text="Max 500 characters",
            error="Message is too long",
        )
        rendered = self.render_template("{% load insight_tags %}{% textarea config %}", {"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        field = soup.find("textarea")
        assert field.has_attr("required")
        assert field["aria-required"] == "true"
        assert field["aria-invalid"] == "true"
        assert field["aria-describedby"] == "message-help message-error"
        assert field["aria-errormessage"] == "message-error"
        assert soup.find("p", id="message-help").get_text(strip=True) == "Max 500 characters"
        error = soup.find("p", id="message-error")
        assert not error.has_attr("role")  # field errors are linked text, not live regions
        assert error.get_text(strip=True) == "Message is too long"

    def test_textarea_emits_nothing_when_messages_are_empty(self) -> None:
        """Plain optional textarea carries no error semantics and no message paragraphs."""
        rendered = self.render_template('{% load insight_tags %}{% textarea name="message" label="Message" %}')
        soup = BeautifulSoup(rendered, "html.parser")

        field = soup.find("textarea")
        for attr in ("aria-required", "aria-invalid", "aria-describedby", "aria-errormessage"):
            assert not field.has_attr(attr)
        assert soup.find("p") is None

    def test_textarea_label_and_control_share_the_tag_id(self) -> None:
        """WCAG 1.3.1 / 4.1.2: label[for] equals textarea[id] even when tag_id differs from name."""
        config = TextareaConfig(tag_id="msg-id", name="msg", label="Message")
        rendered = self.render_template("{% load insight_tags %}{% textarea config %}", {"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        assert soup.find("label")["for"] == "msg-id"
        assert soup.find("textarea")["id"] == "msg-id"
