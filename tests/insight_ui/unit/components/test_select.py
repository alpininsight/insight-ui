# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the select component."""

import pytest
from bs4 import BeautifulSoup
from insight_ui.configs import SelectConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase

# TODO: Implement tests for Select component  # noqa: TD002, TD003


class TestSelect(TemplateTagsTestCase):
    """Test suite for the select component."""

    def test_select_config_rejects_selected_option_not_in_options(self) -> None:
        """SelectConfig raises ValueError when selected_option is not one of options."""
        with pytest.raises(ValueError, match="selected_option"):
            SelectConfig(name="country", options={"de": "Germany"}, selected_option="fr")

    def test_select_config_accepts_selected_option_in_options(self) -> None:
        """SelectConfig allows selected_option that is present in options."""
        config = SelectConfig(name="country", options={"de": "Germany"}, selected_option="de")
        assert config.selected_option == "de"

    def test_select_config_accepts_empty_selected_option(self) -> None:
        """SelectConfig allows the default empty selected_option (no selection)."""
        config = SelectConfig(name="country", options={"de": "Germany"})
        assert config.selected_option == ""

    def test_select_config_warns_on_disabled_without_reason(self) -> None:
        """SelectConfig inherits the disabled/disabled_reason warning from BaseFormFieldConfig."""
        with pytest.warns(UserWarning, match="disabled without a disabled_reason"):
            SelectConfig(name="country", disabled=True)

    def test_select_uses_name_as_fallback_id_for_its_visible_label(self) -> None:
        """A select without an explicit tag ID still has an accessible label."""
        config = SelectConfig(name="country", label="Country", options={"de": "Germany"})

        rendered = self.render_template("{% load insight_tags %}{% select config %}", {"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        select = soup.find("select")
        label = soup.find("label")
        assert select["id"] == "country"
        assert label["for"] == "country"
