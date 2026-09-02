"""Tests for the corner_ribbon component."""

from tests.unit.components.test_template_tags import TemplateTagsTestCase

# TODO: Implement tests for CornerRibbon component  # noqa: TD002, TD003


class TestCornerRibbon(TemplateTagsTestCase):
    """Test suite for the corner_ribbon component."""

    def test_renders_a_non_interactive_status_ribbon_by_default(self) -> None:
        """Keep the existing passive status ribbon behaviour by default."""
        rendered = self.render_template("{% load insight_tags %}{% corner_ribbon text='Beta' %}")

        assert 'role="status"' in rendered
        assert "pointer-events-none" in rendered
        assert "<a" not in rendered

    def test_renders_an_accessible_link_when_request_url_is_set(self) -> None:
        """Render a regular accessible link for an actionable ribbon."""
        rendered = self.render_template(
            "{% load insight_tags %}"
            "{% corner_ribbon text='Beta test' color='primary' foreground_color='secondary' "
            "request_url='mailto:contact@example.com' aria_label='Request a beta test by email' %}"
        )

        assert 'href="mailto:contact@example.com"' in rendered
        assert 'aria-label="Request a beta test by email"' in rendered
        assert "text-insight-secondary" in rendered
        assert "pointer-events-none" not in rendered
