"""Tests for the radio_block component."""

import pytest
from bs4 import BeautifulSoup
from insight_ui.configs import RadioBlockConfig, RadioItemConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestRadioBlock(TemplateTagsTestCase):
    """Test suite for the radio_block component."""

    def test_radio_block(self) -> None:
        """Test the {% radio_block %} tag with HTMX attributes."""
        # Create a test config with HTMX attributes (not using demo context)
        config = RadioBlockConfig(
            "size",
            "Select size:",
            items=[
                RadioItemConfig("small", "small-size", "s"),
                RadioItemConfig("medium", "medium-size", "m"),
                RadioItemConfig("large", "large-size", "l", disabled=True),
            ],
            as_row=True,
            request_url="/api/size/",
            hx_target_id="size-target",
            method="onSizeChange",
        )

        template_string = """
        {% load insight_tags %}
        {% radio_block config %}
        """

        rendered = self.render_template(template_string, {"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        wrapper = soup.find("fieldset")

        # Check label (legend element for accessibility)
        legend = wrapper.find("legend")
        assert legend.text.strip() == "Select size:"

        form = wrapper.find("form", id="size")
        assert form is not None

        # Check count of radios
        inputs = form.find_all("input", type="radio")
        labels = form.find_all("label")
        assert len(inputs) == 3  # noqa: PLR2004

        # First radio
        assert inputs[0]["id"] == "size-small-size"
        assert inputs[0]["name"] == "size"
        assert inputs[0]["value"] == "small"
        assert inputs[0].has_attr("checked")
        assert not inputs[0].has_attr("disabled")
        assert inputs[0].has_attr("hx-get")
        assert inputs[0].has_attr("hx-target")
        assert inputs[0].has_attr("hx-swap")
        assert inputs[0].has_attr("data-radio-callback")
        assert labels[0]["for"] == "size-small-size"
        assert labels[0].get_text().strip() == "s"

        # Second radio
        assert inputs[1]["id"] == "size-medium-size"
        assert inputs[1]["name"] == "size"
        assert inputs[1]["value"] == "medium"
        assert not inputs[1].has_attr("checked")
        assert not inputs[1].has_attr("disabled")
        assert labels[1]["for"] == "size-medium-size"
        assert labels[1].get_text().strip() == "m"

        # Third radio
        assert inputs[2]["id"] == "size-large-size"
        assert inputs[2]["name"] == "size"
        assert inputs[2]["value"] == "large"
        assert not inputs[2].has_attr("checked")
        assert inputs[2].has_attr("disabled")
        assert labels[2]["for"] == "size-large-size"
        assert labels[2].get_text().strip() == "l"

    def test_radio_block_config_rejects_current_value_not_matching_items(self) -> None:
        """RadioBlockConfig raises ValueError when current_value matches no item."""
        with pytest.raises(ValueError, match="current_value"):
            RadioBlockConfig(
                name="view",
                items=[RadioItemConfig(value="card")],
                current_value="table",
            )
