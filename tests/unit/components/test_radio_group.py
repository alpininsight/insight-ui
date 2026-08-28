"""Tests for the radio_group component."""

from bs4 import BeautifulSoup
from documentation.component_details.demo_context import get_radio_group_context

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

        wrapper = soup.find("fieldset")

        # Check label (legend element for accessibility)
        legend = wrapper.find("legend")
        assert legend.text.strip() == "Select AI Model:"

        # Check count of radios
        inputs = wrapper.find_all("input", type="radio")
        assert len(inputs) == 3  # noqa: PLR2004

        # Check labels are rendered
        labels = wrapper.find_all("label")
        assert len(labels) == 3  # noqa: PLR2004

        # First radio (checked)
        assert inputs[0]["id"] == "model1"
        assert inputs[0]["name"] == "model"
        assert inputs[0]["value"] == "BERT"
        assert inputs[0].has_attr("checked")
        assert not inputs[0].has_attr("disabled")
        assert "BERT" in labels[0].get_text()

        # Second radio
        assert inputs[1]["id"] == "model2"
        assert inputs[1]["name"] == "model"
        assert inputs[1]["value"] == "PaLM 2"
        assert not inputs[1].has_attr("checked")
        assert not inputs[1].has_attr("disabled")
        assert "PaLM 2" in labels[1].get_text()

        # Third radio (disabled)
        assert inputs[2]["id"] == "model3"
        assert inputs[2]["name"] == "model"
        assert inputs[2]["value"] == "LLaMA 2"
        assert not inputs[2].has_attr("checked")
        assert inputs[2].has_attr("disabled")
        assert "LLaMA 2" in labels[2].get_text()
