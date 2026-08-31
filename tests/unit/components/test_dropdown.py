"""Tests for the dropdown component."""

import pytest
from insight_ui.configs import DropdownItemConfig

from tests.unit.components.test_template_tags import TemplateTagsTestCase

# TODO: Implement tests for Dropdown component  # noqa: TD002, TD003


class TestDropdown(TemplateTagsTestCase):
    """Test suite for the dropdown component."""

    def test_dropdown_item_config_requires_request_url(self) -> None:
        """DropdownItemConfig requires request_url (avoids dead '#' links)."""
        with pytest.raises(TypeError):
            DropdownItemConfig(text="Profile")  # type: ignore[call-arg]
