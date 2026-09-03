"""Tests for the input_field component."""

import pytest
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
