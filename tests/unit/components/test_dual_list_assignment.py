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

    def test_uses_side_by_side_desktop_layout(self) -> None:
        """Keep the control close to Django Admin's horizontal M2M selector."""
        rendered = self.render_template(
            """
            {% load insight_tags %}
            {% dual_list_assignment name="role_slugs" options=options selected_values=selected_values %}
            """,
            {
                "options": {
                    "organization-member": "Organization Member",
                    "organization-admin": "Organization Admin",
                },
                "selected_values": ["organization-admin"],
            },
        )

        assert "flex flex-col gap-3 lg:flex-row" in rendered
        assert "flex shrink-0 flex-col justify-center gap-2" in rendered
        list_count = 2
        assert rendered.count("min-w-0 flex-1 space-y-2") == list_count
