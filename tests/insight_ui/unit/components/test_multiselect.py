# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the multiselect component."""

import pytest
from bs4 import BeautifulSoup
from insight_ui.configs import MultiselectConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase

# TODO: Implement tests for Multiselect component  # noqa: TD002, TD003


class TestMultiselect(TemplateTagsTestCase):
    """Test suite for the multiselect component."""

    def test_multiselect_config_rejects_selected_options_not_in_options(self) -> None:
        """MultiselectConfig raises ValueError for entries not present in options."""
        with pytest.raises(ValueError, match="selected_options"):
            MultiselectConfig(name="tags", options=["Python", "Django"], selected_options=["Rust"])

    def test_multiselect_config_rejects_selected_options_exceeding_maximum(self) -> None:
        """MultiselectConfig raises ValueError when selected_options exceeds maximum."""
        with pytest.raises(ValueError, match="maximum"):
            MultiselectConfig(
                name="tags", maximum=1, options=["Python", "Django"], selected_options=["Python", "Django"]
            )

    def test_multiselect_config_accepts_valid_selected_options(self) -> None:
        """MultiselectConfig allows selected_options within options and maximum."""
        config = MultiselectConfig(name="tags", maximum=2, options=["Python", "Django"], selected_options=["Python"])
        assert config.selected_options == ["Python"]

    def test_multiselect_config_warns_on_disabled_without_reason(self) -> None:
        """MultiselectConfig inherits the disabled/disabled_reason warning from BaseFormFieldConfig."""
        with pytest.warns(UserWarning, match="disabled without a disabled_reason"):
            MultiselectConfig(name="tags", disabled=True)

    def test_multiselect_applies_combobox_attributes_to_the_text_input(self) -> None:
        """The editable input, rather than a wrapper, owns combobox semantics."""
        config = MultiselectConfig(name="tags", label="Tags", options=["Python"])

        rendered = self.render_template("{% load insight_tags %}{% multiselect config %}", {"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        search = soup.find("input", {"type": "text"})
        listbox = soup.find("div", {"role": "listbox"})
        assert search["role"] == "combobox"
        assert search["aria-controls"] == "tags-listbox"
        assert listbox["aria-multiselectable"] == "true"
