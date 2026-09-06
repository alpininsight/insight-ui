# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the input_field component."""

import pytest
from bs4 import BeautifulSoup
from insight_ui.configs import InputFieldConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase

# TODO: Implement tests for InputField component  # noqa: TD002, TD003


class TestInputField(TemplateTagsTestCase):
    """Test suite for the input_field component."""

    def test_input_field_config_rejects_minimum_greater_than_maximum(self) -> None:
        """InputFieldConfig raises ValueError when minimum exceeds maximum."""
        with pytest.raises(ValueError, match="minimum"):
            InputFieldConfig(name="amount", input_type="number", minimum=10, maximum=5)

    def test_input_field_config_rejects_min_length_greater_than_max_length(self) -> None:
        """InputFieldConfig raises ValueError when min_length exceeds max_length."""
        with pytest.raises(ValueError, match="min_length"):
            InputFieldConfig(name="username", min_length=10, max_length=5)

    def test_input_field_config_accepts_valid_bounds(self) -> None:
        """InputFieldConfig allows consistent minimum/maximum and min_length/max_length."""
        config = InputFieldConfig(
            name="amount", input_type="number", minimum=0, maximum=100, min_length=1, max_length=3
        )
        assert (config.minimum, config.maximum) == (0, 100)

    def test_input_field_renders_help_text_and_error_semantics(self) -> None:
        """help_text and error are linked via aria-describedby, aria-invalid and aria-errormessage."""
        config = InputFieldConfig(
            tag_id="email",
            name="email",
            label="E-Mail",
            required=True,
            help_text="Use your work address",
            error="Invalid address",
        )
        rendered = self.render_template("{% load insight_tags %}{% input_field config %}", {"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        field = soup.find("input")
        assert field.has_attr("required")
        assert field["aria-required"] == "true"
        assert field["aria-invalid"] == "true"
        assert field["aria-describedby"] == "email-help email-error"
        assert field["aria-errormessage"] == "email-error"

        help_text = soup.find("p", id="email-help")
        assert help_text.get_text(strip=True) == "Use your work address"
        error = soup.find("p", id="email-error")
        assert not error.has_attr("role")  # field errors are linked text, not live regions
        assert error.get_text(strip=True) == "Invalid address"
        assert "text-insight-danger-foreground" in error["class"]

    def test_input_field_uses_name_as_fallback_id_prefix(self) -> None:
        """Without tag_id the message ids are derived from name."""
        template_string = """
        {% load insight_tags %}
        {% input_field name="email" label="E-Mail" help_text="Hint" %}
        """
        soup = BeautifulSoup(self.render_template(template_string), "html.parser")

        assert soup.find("input")["aria-describedby"] == "email-help"
        assert soup.find("p", id="email-help") is not None

    def test_input_field_without_id_or_name_emits_no_dangling_references(self) -> None:
        """No aria-describedby / aria-errormessage when neither tag_id nor name exist."""
        template_string = """
        {% load insight_tags %}
        {% input_field label="Anonymous" help_text="Hint" error="Oops" %}
        """
        soup = BeautifulSoup(self.render_template(template_string), "html.parser")

        field = soup.find("input")
        assert not field.has_attr("aria-describedby")
        assert not field.has_attr("aria-errormessage")
        assert field["aria-invalid"] == "true"
        paragraphs = soup.find_all("p")
        assert len(paragraphs) == 2  # noqa: PLR2004
        assert all(not p.has_attr("id") for p in paragraphs)

    def test_input_field_emits_nothing_when_messages_are_empty(self) -> None:
        """Plain optional fields carry no error semantics and no message paragraphs."""
        template_string = """
        {% load insight_tags %}
        {% input_field tag_id="username" name="username" label="Username" %}
        """
        soup = BeautifulSoup(self.render_template(template_string), "html.parser")

        field = soup.find("input")
        for attr in ("aria-required", "aria-invalid", "aria-describedby", "aria-errormessage"):
            assert not field.has_attr(attr)
        assert soup.find("p") is None
        assert soup.find(attrs={"role": "alert"}) is None

    def test_input_field_label_targets_the_control_when_only_name_is_set(self) -> None:
        """WCAG 1.3.1 / 4.1.2: the label is associated via the name fallback id."""
        config = InputFieldConfig(name="email", label="E-Mail")
        rendered = self.render_template("{% load insight_tags %}{% input_field config %}", {"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        assert soup.find("label")["for"] == "email"
        assert soup.find("input")["id"] == "email"

    def test_input_field_without_id_or_name_has_no_for_attribute(self) -> None:
        """No dangling label reference when neither tag_id nor name exist."""
        config = InputFieldConfig(label="Search")
        rendered = self.render_template("{% load insight_tags %}{% input_field config %}", {"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        assert not soup.find("label").has_attr("for")
        assert not soup.find("input").has_attr("id")
