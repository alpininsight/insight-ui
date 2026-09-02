"""Tests for the range_slider component."""

# ruff: noqa: E501

import insight_ui.templatetags.insight_tags
import pytest
from bs4 import BeautifulSoup
from insight_ui.configs.input import SliderConfig

from tests.unit.components.test_template_tags import TemplateTagsTestCase


class TestRangeSlider(TemplateTagsTestCase):
    """Test suite for the range_slider component."""

    def test_slider_config(self) -> None:
        """Test the {% slider %} tag with config dataclass."""
        config = SliderConfig(
            "range-slider-skip",
            "range_slider_skip",
            "Legend Mode: Skip",
            value=6,
            minimum=1,
            maximum=12,
            items=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            legend_mode="skip",
        )

        result = insight_ui.templatetags.insight_tags.slider(config=config)
        assert result["slider_config"] == config

    def test_slider(self) -> None:
        """Test the {% slider %} tag."""
        template_string = """
        {% load insight_tags %}
        {% slider tag_id="cpu-cores" name="cpu_core_count" value=4 minimum=2 maximum=8 step_size=2 disabled=False label="Choose amount of CPU-Cores:" %}
        """
        rendered = self.render_template(template_string)
        soup = BeautifulSoup(rendered, "html.parser")

        wrapper = soup.find("div")

        label = wrapper.find("label")
        assert "Choose amount of CPU-Cores:" in label.get_text()
        assert label["for"] == "cpu-cores"

        input_element = wrapper.find("input")
        assert input_element["id"] == "cpu-cores"
        assert input_element["name"] == "cpu_core_count"
        assert input_element["value"] == "4"
        assert input_element["min"] == "2"
        assert input_element["max"] == "8"
        assert input_element["step"] == "2"
        assert not input_element.has_attr("disabled")

    def test_slider_config_rejects_value_min_greater_than_value_max(self) -> None:
        """SliderConfig raises ValueError when value_min exceeds value_max in dual mode."""
        with pytest.raises(ValueError, match="value_min"):
            SliderConfig(name="price", dual=True, minimum=0, maximum=1000, value_min=800, value_max=200)

    def test_slider_config_accepts_valid_dual_range(self) -> None:
        """SliderConfig allows a valid value_min/value_max pair in dual mode."""
        config = SliderConfig(name="price", dual=True, minimum=0, maximum=1000, value_min=200, value_max=800)
        assert (config.value_min, config.value_max) == (200, 800)
