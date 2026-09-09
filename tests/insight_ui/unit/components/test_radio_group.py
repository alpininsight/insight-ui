# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the radio_group component."""

import pytest
from bs4 import BeautifulSoup
from insight_ui.configs import RadioGroupConfig, RadioItemConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestRadioGroup(TemplateTagsTestCase):
    """Test suite for the radio_group component."""

    def test_radio_group(self) -> None:
        """Test the {% radio_group %} tag."""
        context = {
            "model_radio_config": RadioGroupConfig(
                "model",
                "Select AI Model:",
                [
                    RadioItemConfig("BERT", "model1", "BERT"),
                    RadioItemConfig("PaLM 2", "model2", "PaLM 2"),
                    RadioItemConfig("LLaMA 2", "model3", "LLaMA 2", disabled=True, disabled_reason="Unavailable"),
                ],
            )
        }

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

    def test_radio_group_config_rejects_current_value_not_matching_items(self) -> None:
        """RadioGroupConfig raises ValueError when current_value matches no item."""
        with pytest.raises(ValueError, match="current_value"):
            RadioGroupConfig(
                name="model",
                items=[RadioItemConfig(value="gpt-4")],
                current_value="claude",
            )

    def test_radio_group_config_defaults_current_value_to_first_item(self) -> None:
        """RadioGroupConfig fills current_value from the first item when unset."""
        config = RadioGroupConfig(name="model", items=[RadioItemConfig(value="gpt-4")])
        assert config.current_value == "gpt-4"

    def test_radio_item_config_tag_id_is_optional(self) -> None:
        """RadioItemConfig can be constructed without tag_id."""
        item = RadioItemConfig(value="gpt-4")
        assert item.tag_id == ""
