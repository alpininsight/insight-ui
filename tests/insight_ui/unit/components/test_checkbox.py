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
        assert "text-primary" in label_spans[0]["class"]

        assert checkboxes[1]["id"] == "newsletter-box"
        assert checkboxes[1]["name"] == "newsletter"
        assert checkboxes[1]["value"] == "subscribed"
        assert checkboxes[1].has_attr("checked")
        assert checkboxes[1].has_attr("disabled")
        assert label_spans[1].get_text() == "Subscribe for Newsletter"
        assert "text-secondary" in label_spans[1]["class"]
