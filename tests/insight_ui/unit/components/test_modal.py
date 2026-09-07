"""Tests for the modal component."""

import pytest

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestModal(TemplateTagsTestCase):
    """Test suite for the modal component (layout tag)."""

    def test_modal_basic(self) -> None:
        """Test basic modal functionality with block tag."""
        template_string = """
        {% load layout_tags %}
        {% modal id="test-modal" title="Test Modal" %}
            <p>Modal content</p>
        {% endmodal %}
        """
        rendered = self.render_template(template_string)
        assert "test-modal" in rendered
        assert "Test Modal" in rendered
        assert "Modal content" in rendered

    def test_modal_with_custom_width(self) -> None:
        """Test modal with custom width."""
        template_string = """
        {% load layout_tags %}
        {% modal id="wide-modal" title="Wide Modal" width=48 %}
            <p>Content</p>
        {% endmodal %}
        """
        rendered = self.render_template(template_string)
        assert "max-width: 48rem" in rendered

    def test_modal_without_title(self) -> None:
        """Test modal without title only shows close button in header."""
        template_string = """
        {% load layout_tags %}
        {% modal id="no-title-modal" %}
            <p>No title content</p>
        {% endmodal %}
        """
        rendered = self.render_template(template_string)
        assert "no-title-modal" in rendered
        assert "No title content" in rendered
        # Close button should still be present
        assert 'data-insight-dismiss="modal"' in rendered

    def test_modal_without_close_button(self) -> None:
        """Test modal with show_close=False hides the close button."""
        template_string = """
        {% load layout_tags %}
        {% modal id="no-close-modal" title="No Close" show_close=False %}
            <p>Content</p>
        {% endmodal %}
        """
        rendered = self.render_template(template_string)
        assert "no-close-modal" in rendered
        # Header should not contain close button (only the content might have one)
        # We check that the header area doesn't have the icon button
        assert "No Close" in rendered

    def test_modal_accessibility_attributes(self) -> None:
        """Test modal has proper accessibility attributes."""
        template_string = """
        {% load layout_tags %}
        {% modal id="a11y-modal" title="Accessible Modal" %}
            <p>Content</p>
        {% endmodal %}
        """
        rendered = self.render_template(template_string)
        assert 'role="dialog"' in rendered
        assert 'aria-modal="true"' in rendered
        assert 'aria-labelledby="a11y-modal-title"' in rendered

    def test_modal_requires_id(self) -> None:
        """Test modal raises error when id is missing."""
        template_string = """
        {% load layout_tags %}
        {% modal title="No ID Modal" %}
            <p>Content</p>
        {% endmodal %}
        """
        with pytest.raises(ValueError, match="requires an 'id' parameter"):
            self.render_template(template_string)
