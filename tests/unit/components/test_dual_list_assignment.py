"""Tests for the dual list assignment component."""

from insight_ui.configs import DualListAssignmentConfig, DualListAssignmentItemConfig

from tests.unit.components.test_template_tags import TemplateTagsTestCase


class TestDualListAssignment(TemplateTagsTestCase):
    """Test suite for the dual list assignment component."""

    def test_renders_available_and_assigned_options_with_hidden_inputs(self) -> None:
        """Render assigned values as hidden inputs for ordinary Django form posts."""
        rendered = self.render_template(
            """
            {% load insight_tags %}
            {% dual_list_assignment config=config %}
            """,
            {
                "config": DualListAssignmentConfig(
                    name="role_slugs",
                    label="Organization roles",
                    options=[
                        DualListAssignmentItemConfig("organization-member", "Organization Member"),
                        DualListAssignmentItemConfig("organization-admin", "Organization Admin"),
                    ],
                    selected_values=["organization-member"],
                )
            },
        )

        assert "data-insight-dual-list-assignment" in rendered
        assert 'name="role_slugs" value="organization-member"' in rendered
        assert 'value="organization-admin"' in rendered
        assert "Organization Admin" in rendered

    def test_accepts_dictionary_options_from_template_tag(self) -> None:
        """Accept simple value-to-label dictionaries without caller-side config objects."""
        rendered = self.render_template(
            """
            {% load insight_tags %}
            {% dual_list_assignment name="role_slugs" options=options selected_values=selected_values %}
            """,
            {
                "options": {
                    "organization-member": "Organization Member",
                    "organization-developer": "Organization Developer",
                },
                "selected_values": ["organization-developer"],
            },
        )

        assert 'name="role_slugs" value="organization-developer"' in rendered
        assert "Organization Member" in rendered
        assert "Organization Developer" in rendered
