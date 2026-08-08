"""Tests for the checkbox_group component."""

from bs4 import BeautifulSoup
from insight_ui.configs.input import CheckboxGroupConfig, CheckboxItemConfig

from tests.unit.components.test_template_tags import TemplateTagsTestCase


class TestCheckboxGroup(TemplateTagsTestCase):
    """Test suite for the checkbox_group component."""

    def test_checkbox_group(self) -> None:
        """Test the {% checkbox_group %} tag."""
        checkbox_context = CheckboxGroupConfig(
            "language",
            "Choose languages: (max. 3)",
            [
                CheckboxItemConfig("english", "English", "english"),
                CheckboxItemConfig("german", "German", "german", checked=True),
                CheckboxItemConfig("french", "French", "french"),
                CheckboxItemConfig("spanish", "Spanish", "spanish"),
                CheckboxItemConfig("italian", "Italian (currently not available)", "italian", True),
            ],
            True,
            1,
            3,
        )

        template_string = """
        {% load insight_tags %}
        {% checkbox_group checkbox_config %}
        """

        rendered = self.render_template(template_string, {"checkbox_config": checkbox_context})
        soup = BeautifulSoup(rendered, "html.parser")

        wrapper = soup.find("fieldset", {"data-insight-checkbox-group": True})
        assert wrapper["data-minimum-checked"] == "1"

        # Check label (legend element for accessibility)
        legend = wrapper.find("legend")
        assert legend.text == "Choose languages: (max. 3)"

        # Check count of checkboxes
        inputs = wrapper.find_all("input", type="checkbox")
        assert len(inputs) == 5  # noqa: PLR2004

        # Check labels are rendered
        labels = wrapper.find_all("label")
        assert len(labels) == 5  # noqa: PLR2004

        # First checkbox
        assert inputs[0]["id"] == "english"
        assert inputs[0]["name"] == "language"
        assert inputs[0]["value"] == "english"
        assert not inputs[0].has_attr("checked")
        assert not inputs[0].has_attr("disabled")
        assert "English" in labels[0].get_text()

        # Second checkbox (checked)
        assert inputs[1]["id"] == "german"
        assert inputs[1]["name"] == "language"
        assert inputs[1]["value"] == "german"
        assert inputs[1].has_attr("checked")
        assert not inputs[1].has_attr("disabled")
        assert "German" in labels[1].get_text()

        # Fifth checkbox (disabled)
        assert inputs[4]["id"] == "italian"
        assert inputs[4]["name"] == "language"
        assert inputs[4]["value"] == "italian"
        assert not inputs[4].has_attr("checked")
        assert inputs[4].has_attr("disabled")
        assert "Italian" in labels[4].get_text()
