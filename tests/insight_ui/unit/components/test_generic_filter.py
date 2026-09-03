"""Tests for the generic_filter component."""

import pytest
from insight_ui.configs import FilterConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase

# TODO: Implement tests for GenericFilter component  # noqa: TD002, TD003


class TestGenericFilter(TemplateTagsTestCase):
    """Test suite for the generic_filter component."""

    def test_filter_config_rejects_selected_option_not_in_options(self) -> None:
        """FilterConfig raises ValueError when selected_option is not present in a non-empty options dict."""
        with pytest.raises(ValueError, match="selected_option"):
            FilterConfig(name="status", options={"active": "Active"}, selected_option="inactive")

    def test_filter_config_accepts_default_selected_option_with_unset_options(self) -> None:
        """FilterConfig does not raise for the default empty selected_option when options is empty."""
        config = FilterConfig(name="status")
        assert config.selected_option == ""
