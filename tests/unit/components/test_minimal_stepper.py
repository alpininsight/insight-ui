"""Tests for the minimal_stepper component."""

from tests.unit.components.test_template_tags import TemplateTagsTestCase

# TODO: Implement tests for MinimalStepBar component  # noqa: TD002, TD003


class TestMinimalStepper(TemplateTagsTestCase):
    """Test suite for the minimal_stepper component."""

    def test_minimal_stepper_uses_status_foreground_tokens(self) -> None:
        """Status segments must use theme foreground tokens instead of fixed white text."""
        template_string = """
        {% load insight_tags %}
        {% minimal_stepper items=items %}
        """
        rendered = self.render_template(template_string, context={"items": ["success", "failed", "active", ""]})

        assert "text-insight-success-foreground" in rendered
        assert "text-insight-danger-foreground" in rendered
        assert "text-insight-primary-foreground" in rendered
        assert "text-insight-pending-foreground" in rendered
        assert "text-white" not in rendered
