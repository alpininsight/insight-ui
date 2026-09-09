# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the toggle component."""

# ruff: noqa: E501

import insight_ui.templatetags.insight_tags
from bs4 import BeautifulSoup
from insight_ui.configs.input import ToggleConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestToggle(TemplateTagsTestCase):
    """Test suite for the toggle component."""

    def test_toggle_config(self) -> None:
        """Test the {% toggle %} tag with config dataclass."""
        config = ToggleConfig("toggle-switch", "toggle-switch", "Click me!", switch=True)
        result = insight_ui.templatetags.insight_tags.toggle(config=config)

        assert result["toggle_config"] == config

    def test_toggle(self) -> None:
        """Test the {% toggle %} tag."""
        template_string = """
        {% load insight_tags %}
        {% toggle tag_id="theme-toggle" name="toggle_theme" value="toggle_theme" checked=False disabled=False label="Dark" method="changeTheme" switch=True %}
        """
        rendered = self.render_template(template_string)
        soup = BeautifulSoup(rendered, "html.parser")

        switch = soup.find("label")

        label = switch.find("span")
        assert "Dark" in label.get_text()

        input_element = switch.find("input")
        assert input_element["id"] == "theme-toggle"
        assert input_element["name"] == "toggle_theme"
        assert input_element["value"] == "toggle_theme"
        assert input_element["onclick"] == "changeTheme()"
        assert not input_element.has_attr("checked")
        assert not input_element.has_attr("disabled")

    def test_toggle_switch(self) -> None:
        """Test the {% toggle %} tag."""
        template_string = """
        {% load insight_tags %}
        {% toggle tag_id="theme-toggle" name="toggle_theme" value="toggle_theme" checked=False disabled=False label="Dark" method="changeTheme" %}
        """
        rendered = self.render_template(template_string)
        soup = BeautifulSoup(rendered, "html.parser")

        wrapper = soup.find("div")

        label = wrapper.find("label")
        assert "Dark" in label.get_text()
        assert label["for"] == "theme-toggle"

        input_element = wrapper.find("input")
        assert input_element["id"] == "theme-toggle"
        assert input_element["name"] == "toggle_theme"
        assert input_element["value"] == "toggle_theme"
        assert input_element["onclick"] == "changeTheme()"
        assert not input_element.has_attr("checked")
        assert not input_element.has_attr("disabled")
