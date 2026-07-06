"""Tests for the radio_group component."""

from bs4 import BeautifulSoup
from insight_ui.component_details.demo_context import get_radio_group_context

from tests.unit.components.test_template_tags import TemplateTagsTestCase


class TestRadioGroup(TemplateTagsTestCase):
    """Test suite for the radio_group component."""

    def test_radio_group(self) -> None:
        """Test the {% radio_group %} tag."""
        context = get_radio_group_context()

        template_string = """
        {% load insight_tags %}
        {% radio_group config=model_radio_config %}
        """

        rendered = self.render_template(template_string, context)
        soup = BeautifulSoup(rendered, "html.parser")

        wrapper = soup.find("div")

        # Check label
        label_span = wrapper.find("span")
        assert label_span.text.strip() == "Select AI Model:"

        # Check layout
        container = wrapper.find("div", class_="flex")
        assert "space-y-1" in container["class"]

        # Check count of radios
        inputs = container.find_all("input", type="radio")
        label_spans = container.find_all("span")
        assert len(inputs) == 3  # noqa: PLR2004

        # First radio
        assert inputs[0]["id"] == "model1"
        assert inputs[0]["name"] == "model"
        assert inputs[0]["value"] == "BERT"
        assert inputs[0].has_attr("checked")
        assert not inputs[0].has_attr("disabled")
        assert label_spans[0].get_text() == "BERT"

        # Second radio
        assert inputs[1]["id"] == "model2"
        assert inputs[1]["name"] == "model"
        assert inputs[1]["value"] == "PaLM 2"
        assert not inputs[1].has_attr("checked")
        assert not inputs[1].has_attr("disabled")
        assert label_spans[1].get_text() == "PaLM 2"

        # Third radio
        assert inputs[2]["id"] == "model3"
        assert inputs[2]["name"] == "model"
        assert inputs[2]["value"] == "LLaMA 2"
        assert not inputs[2].has_attr("checked")
        assert inputs[2].has_attr("disabled")
        assert label_spans[2].get_text() == "LLaMA 2 (currently not available)"
