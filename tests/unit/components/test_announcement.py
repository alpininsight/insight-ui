"""Tests for the site-wide announcement component."""

from insight_ui.configs import AnnouncementConfig

from tests.unit.components.test_template_tags import TemplateTagsTestCase


class TestAnnouncement(TemplateTagsTestCase):
    """Test suite for the announcement component."""

    def test_announcement_renders_message_and_optional_link(self) -> None:
        """A site announcement renders its landmark and contact link."""
        rendered = self.render_template(
            "{% load insight_tags %}{% announcement config=config %}",
            {
                "config": AnnouncementConfig(
                    tag_id="beta",
                    message="Beta service",
                    link_label="Contact us",
                    link_url="mailto:test@example.com",
                )
            },
        )

        assert 'id="beta"' in rendered
        assert 'class="insight-announcement"' in rendered
        assert "Beta service" in rendered
        assert 'href="mailto:test@example.com"' in rendered
        assert "Contact us" in rendered

    def test_announcement_omits_incomplete_link(self) -> None:
        """A label without a destination does not render a non-functional link."""
        rendered = self.render_template(
            """
            {% load insight_tags %}
            {% announcement message="Beta service" link_label="Contact us" %}
            """
        )

        assert "Beta service" in rendered
        assert "Contact us" not in rendered
        assert "href=" not in rendered
