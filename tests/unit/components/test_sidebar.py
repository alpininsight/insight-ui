"""Tests for the sidebar component."""

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
