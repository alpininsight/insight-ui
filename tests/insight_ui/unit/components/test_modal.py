"""Tests for the modal component."""

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestModal(TemplateTagsTestCase):
    """Test suite for the modal component."""

    def test_modal_basic(self) -> None:
        """Test für grundlegende modal Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% modal tag_id="test-modal" title="Test Modal" %}
        """
        rendered = self.render_template(template_string)
        assert "test-modal" in rendered
        assert "Test Modal" in rendered
