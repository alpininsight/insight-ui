"""Tests for the list component (layout tag)."""

import pytest

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestList(TemplateTagsTestCase):
    """Test suite for the list component."""

    def test_list_basic(self) -> None:
        """Test basic list with default settings."""
        template_string = """
        {% load layout_tags %}
        {% list %}
            {% listitem %}First{% endlistitem %}
            {% listitem %}Second{% endlistitem %}
        {% endlist %}
        """
        rendered = self.render_template(template_string)
        assert "<ul" in rendered
        assert "<li>" in rendered
        assert "First" in rendered
        assert "Second" in rendered
        assert "flex-col" in rendered

    def test_list_horizontal(self) -> None:
        """Test horizontal list layout."""
        template_string = """
        {% load layout_tags %}
        {% list horizontal %}
            {% listitem %}A{% endlistitem %}
            {% listitem %}B{% endlistitem %}
        {% endlist %}
        """
        rendered = self.render_template(template_string)
        assert "flex-row" in rendered
        assert "flex-wrap" in rendered

    def test_list_ordered(self) -> None:
        """Test ordered list renders as <ol>."""
        template_string = """
        {% load layout_tags %}
        {% list ordered=True %}
            {% listitem %}Step 1{% endlistitem %}
            {% listitem %}Step 2{% endlistitem %}
        {% endlist %}
        """
        rendered = self.render_template(template_string)
        assert "<ol" in rendered
        assert "</ol>" in rendered

    def test_list_with_markers(self) -> None:
        """Test list with visible markers."""
        template_string = """
        {% load layout_tags %}
        {% list marker="disc" marker_position="outside" %}
            {% listitem %}Item{% endlistitem %}
        {% endlist %}
        """
        rendered = self.render_template(template_string)
        assert "list-disc" in rendered
        assert "list-outside" in rendered

    def test_list_decimal_markers(self) -> None:
        """Test ordered list with decimal markers."""
        template_string = """
        {% load layout_tags %}
        {% list ordered=True marker="decimal" %}
            {% listitem %}One{% endlistitem %}
            {% listitem %}Two{% endlistitem %}
        {% endlist %}
        """
        rendered = self.render_template(template_string)
        assert "list-decimal" in rendered

    def test_list_aria_label(self) -> None:
        """Test list with aria-label for accessibility."""
        template_string = """
        {% load layout_tags %}
        {% list aria_label="Navigation options" %}
            {% listitem %}Home{% endlistitem %}
        {% endlist %}
        """
        rendered = self.render_template(template_string)
        assert 'aria-label="Navigation options"' in rendered

    def test_list_custom_gap(self) -> None:
        """Test list with custom gap."""
        template_string = """
        {% load layout_tags %}
        {% list gap="xl" %}
            {% listitem %}A{% endlistitem %}
        {% endlist %}
        """
        rendered = self.render_template(template_string)
        assert "gap-insight-xl" in rendered

    def test_listitem_with_class(self) -> None:
        """Test listitem with custom class."""
        template_string = """
        {% load layout_tags %}
        {% list %}
            {% listitem class="font-bold text-red-500" %}Highlighted{% endlistitem %}
        {% endlist %}
        """
        rendered = self.render_template(template_string)
        assert 'class="font-bold text-red-500"' in rendered

    def test_list_invalid_param(self) -> None:
        """Test list raises error for unknown parameter."""
        template_string = """
        {% load layout_tags %}
        {% list unknown_param="value" %}
            {% listitem %}Item{% endlistitem %}
        {% endlist %}
        """
        with pytest.raises(ValueError, match="Unknown parameter"):
            self.render_template(template_string)

    def test_list_invalid_marker(self) -> None:
        """Test list raises error for invalid marker."""
        template_string = """
        {% load layout_tags %}
        {% list marker="star" %}
            {% listitem %}Item{% endlistitem %}
        {% endlist %}
        """
        with pytest.raises(ValueError, match="marker"):
            self.render_template(template_string)

    def test_list_marker_inside(self) -> None:
        """Test list with inside marker position."""
        template_string = """
        {% load layout_tags %}
        {% list marker="disc" marker_position="inside" %}
            {% listitem %}Item{% endlistitem %}
        {% endlist %}
        """
        rendered = self.render_template(template_string)
        assert "list-inside" in rendered
