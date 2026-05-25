"""Tests for design-theme stylesheet bootstrapping."""

from django.template import Context, Template
from django.test import SimpleTestCase, override_settings

from insight_ui.config import get_config


class DesignThemeHeadTest(SimpleTestCase):
    """Verify persisted design themes are applied before component JavaScript runs."""

    @override_settings(INSIGHT_UI={"design_themes": {"enabled": True}})
    def test_base_template_creates_design_theme_stylesheet_from_saved_theme(self) -> None:
        """The head must not hard-code the default theme stylesheet href."""
        template = Template(
            """
            {% extends "insight_ui/base.html" %}
            {% block content %}Theme test{% endblock %}
            """
        )

        rendered = template.render(Context(get_config()))

        assert 'id="insight-ui-theme-stylesheet"' not in rendered
        assert 'themeLink.id = "insight-ui-theme-stylesheet";' in rendered
        assert "themeLink.href = config.assets[selectedTheme] || config.assets[config.defaultTheme];" in rendered
        assert '"/static/insight_ui/css/themes/alpin.css"' in rendered
        assert '"/static/insight_ui/css/themes/cerulean.css"' in rendered
