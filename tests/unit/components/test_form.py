"""Tests for the form component."""

from tests.unit.components.test_template_tags import TemplateTagsTestCase


class TestForm(TemplateTagsTestCase):
    """Test suite for the form component."""

    def test_form_basic(self) -> None:
        """Test für grundlegende form Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% form title="Test Form" request_url="/api/form_submit/" %}
        """
        rendered = self.render_template(template_string)
        assert "Test Form" in rendered
