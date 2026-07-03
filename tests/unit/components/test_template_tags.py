"""Tests für Insight UI Template Tags."""

from django.contrib.auth.models import User
from django.template import Context, Template
from django.test import TestCase
from django.utils.safestring import SafeText
from django.utils.translation import activate


class TemplateTagsTestCase(TestCase):
    """Basis-Testklasse für Template Tags."""

    def setUp(self) -> None:
        """Setup für Tests."""  # noqa: D401 (It's not in imperative mood o_O)
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")  # noqa: S106
        activate("en")

    def render_template(self, template_string: str, context: dict | None = None) -> SafeText:
        """Hilfsmethode zum Rendern von Templates."""
        template = Template(template_string)
        return template.render(Context(context or {}))


class LanguageSelectorTemplateTagTest(TemplateTagsTestCase):
    """Tests für den language_selector Template Tag."""

    def test_language_selector_basic(self) -> None:
        """Test für grundlegende language_selector Funktionalität."""
        template_string = """
        {% include "insight_ui/components/toggle_language.html" %}
        """
        rendered = self.render_template(template_string)
        assert "de" in rendered
