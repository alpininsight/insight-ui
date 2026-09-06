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

    def test_select_renders_help_text_and_error_semantics(self) -> None:
        """help_text and error are linked via aria-describedby, aria-invalid and aria-errormessage."""
        config = SelectConfig(
            name="country",
            label="Country",
            options={"de": "Germany"},
            required=True,
            help_text="Pick your residence",
            error="Country is required",
        )
        rendered = self.render_template("{% load insight_tags %}{% select config %}", {"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        select = soup.find("select")
        assert select.has_attr("required")
        assert select["aria-required"] == "true"
        assert select["aria-invalid"] == "true"
        assert select["aria-describedby"] == "country-help country-error"
        assert select["aria-errormessage"] == "country-error"
        assert soup.find("p", id="country-help").get_text(strip=True) == "Pick your residence"
        error = soup.find("p", id="country-error")
        assert not error.has_attr("role")  # field errors are linked text, not live regions
        assert error.get_text(strip=True) == "Country is required"

    def test_select_emits_nothing_when_messages_are_empty(self) -> None:
        """Plain optional select carries no error semantics and no message paragraphs."""
        config = SelectConfig(name="country", label="Country", options={"de": "Germany"})
        rendered = self.render_template("{% load insight_tags %}{% select config %}", {"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        select = soup.find("select")
        for attr in ("aria-required", "aria-invalid", "aria-describedby", "aria-errormessage"):
            assert not select.has_attr(attr)
        assert soup.find("p") is None
