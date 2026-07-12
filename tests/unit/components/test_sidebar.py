"""Tests for the sidebar component."""

from bs4 import BeautifulSoup
from insight_ui.configs.navigation import SidebarConfig, SidebarDataConfig

from tests.unit.components.test_template_tags import TemplateTagsTestCase


class TestSidebar(TemplateTagsTestCase):
    """Test suite for the sidebar component."""

    def test_sidebar_basic(self) -> None:
        """Test für grundlegende sidebar Funktionalität."""
        sidebar_data = {"title": "Navigation", "categories": []}
        template_string = """
        {% load insight_tags %}
        {% sidebar sidebar_data=sidebar_data %}
        """
        rendered = self.render_template(template_string, context={"sidebar_data": sidebar_data})
        assert "Navigation" in rendered

    def test_sidebar_mobile_hidden(self) -> None:
        """Test für optionale mobile Ausblendung statischer Sidebars."""
        sidebar_data = {"title": "Navigation", "categories": []}
        template_string = """
        {% load insight_tags %}
        {% sidebar sidebar_data=sidebar_data mobile_hidden=True %}
        """
        rendered = self.render_template(template_string, context={"sidebar_data": sidebar_data})
        assert "hidden xl:block sticky" in rendered

    def test_sidebar_close_button_uses_semantic_icon_button_class(self) -> None:
        """The drawer close button uses the semantic sidebar icon button class."""
        sidebar_config = SidebarConfig(SidebarDataConfig(title="Menu"), side="right", static=False, auto_close=False)

        rendered = self.render_template(
            "{% load insight_tags %}{% sidebar config=sidebar_config %}", context={"sidebar_config": sidebar_config}
        )
        soup = BeautifulSoup(rendered, "html.parser")

        close_button = soup.select_one('button[data-insight-dismiss="sidebar"]#right-sidebar-close')

        assert close_button is not None
        assert close_button.get("class") == ["insight-sidebar-icon-button"]
        assert "hover:bg-gray-100" not in rendered
        assert "dark:hover:bg-gray-700" not in rendered
