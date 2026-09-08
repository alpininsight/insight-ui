# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the checkbox component."""

# ruff: noqa: E501

import insight_ui.templatetags.insight_tags
from bs4 import BeautifulSoup
from insight_ui.configs.input import CheckboxConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestCheckbox(TemplateTagsTestCase):
    """Test suite for the checkbox component."""

    def test_checkbox_config(self) -> None:
        """Test the {% checkbox %} tag with config dataclass."""
        config = CheckboxConfig(
            "accept-terms", "accept_terms", "I accept the terms and conditions", required=True, value="accepted"
        )

        result = insight_ui.templatetags.insight_tags.checkbox(config=config)
        assert result["checkbox_config"] == config

    def test_checkbox_single_params(self) -> None:
        """Test the {% checkbox %} tag with single params."""
        template_string = """
        {% load insight_tags %}
        {% checkbox tag_id="accept-terms" name="accept_terms" value="accepted" checked=False disabled=False label="I accept the terms and conditions" %}
        {% checkbox tag_id="newsletter-box" name="newsletter" value="subscribed" checked=True disabled=True label="Subscribe for Newsletter" %}
        """
        rendered = self.render_template(template_string)
        soup = BeautifulSoup(rendered, "html.parser")

        checkboxes = soup.find_all("input")
        label_spans = soup.find_all("span")
        assert checkboxes[0]["id"] == "accept-terms"
        assert checkboxes[0]["name"] == "accept_terms"
        assert checkboxes[0]["value"] == "accepted"
        assert not checkboxes[0].has_attr("checked")
        assert not checkboxes[0].has_attr("disabled")
        assert label_spans[0].get_text() == "I accept the terms and conditions"
        assert "text-insight-headline" in label_spans[0]["class"]

        assert checkboxes[1]["id"] == "newsletter-box"
        assert checkboxes[1]["name"] == "newsletter"
        assert checkboxes[1]["value"] == "subscribed"
        assert checkboxes[1].has_attr("checked")
        assert checkboxes[1].has_attr("disabled")
        assert label_spans[1].get_text() == "Subscribe for Newsletter"
        assert "text-insight-body" in label_spans[1]["class"]

    def test_checkbox_renders_help_text_and_error_semantics(self) -> None:
        """help_text and error are linked via aria-describedby, aria-invalid and aria-errormessage."""
        template_string = """
        {% load insight_tags %}
        {% checkbox tag_id="accept-terms" name="accept_terms" value="accepted" label="I accept" required=True help_text="Please read the terms first" error="You must accept the terms" %}
        """
        soup = BeautifulSoup(self.render_template(template_string), "html.parser")

        checkbox = soup.find("input")
        assert checkbox.has_attr("required")
        assert checkbox["aria-required"] == "true"
        assert checkbox["aria-invalid"] == "true"
        assert checkbox["aria-describedby"] == "accept-terms-help accept-terms-error"
        assert checkbox["aria-errormessage"] == "accept-terms-error"

        # Messages live outside the wrapping <label> so the label text stays clean
        label = soup.find("label")
        assert label.find("p") is None
        assert soup.find("p", id="accept-terms-help").get_text(strip=True) == "Please read the terms first"
        error = soup.find("p", id="accept-terms-error")
        assert not error.has_attr("role")  # field errors are linked text, not live regions
        assert error.get_text(strip=True) == "You must accept the terms"

    def test_checkbox_emits_nothing_when_messages_are_empty(self) -> None:
        """Plain optional checkbox carries no error semantics and no message paragraphs."""
        template_string = """
        {% load insight_tags %}
        {% checkbox tag_id="newsletter" name="newsletter" value="yes" label="Newsletter" %}
        """
        soup = BeautifulSoup(self.render_template(template_string), "html.parser")

        checkbox = soup.find("input")
        for attr in ("required", "aria-required", "aria-invalid", "aria-describedby", "aria-errormessage"):
            assert not checkbox.has_attr(attr)
        assert soup.find("p") is None
        assert soup.find("div") is None
