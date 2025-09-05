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
        activate("de")

    def render_template(self, template_string: str, context: dict = {}) -> SafeText:
        """Hilfsmethode zum Rendern von Templates."""
        template = Template(template_string)
        return template.render(Context(context))


class NavbarTemplateTagTest(TemplateTagsTestCase):
    """Tests für den navbar Template Tag."""

    def test_navbar(self) -> None:
        """Test für grundlegende navbar Funktionalität."""
        nav_config = {
            "brand": {"title": "Django Insight UI NavBar"},
            "links": [
                {
                    "text": "Startseite",
                    "view_name": "storybook_view",
                    "active": True,
                    "need_auth": False,
                    "staff_only": False,
                }
            ],
            "show_searchbar": True,
            "show_usermenu": True,
            "show_language_selector": True,
            "show_theme_toggle": True,
        }

        template_string = """
        {% load insight_tags %}
        {% navbar config=nav_config %}
        """

        rendered = self.render_template(template_string, context={"nav_config": nav_config})
        assert "Django Insight UI NavBar" in rendered


class LiveContentTemplateTagTest(TemplateTagsTestCase):
    """Tests für den live_content Template Tag."""

    def test_live_content_basic(self) -> None:
        """Test für grundlegende live_content Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% live_content url="/api/live-data/" %}
        """
        rendered = self.render_template(template_string)
        assert "/api/live-data/" in rendered

    def test_live_content_with_interval(self) -> None:
        """Test für live_content mit Intervall."""
        template_string = """
        {% load insight_tags %}
        {% live_content url="/api/live-data/" interval=5000 %}
        """
        rendered = self.render_template(template_string)
        assert "/api/live-data/" in rendered


class WebsocketTemplateTagTest(TemplateTagsTestCase):
    """Tests für den insight_websocket Template Tag."""

    def test_websocket_basic(self) -> None:
        """Test für grundlegende WebSocket Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% insight_websocket ws_url="ws://localhost:8765" %}
        """
        rendered = self.render_template(template_string)
        assert "ws://localhost:8765" in rendered


class InfiniteScrollTemplateTagTest(TemplateTagsTestCase):
    """Tests für den infinite_scroll Template Tag."""

    def test_infinite_scroll_basic(self) -> None:
        """Test für grundlegende infinite_scroll Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% infinite_scroll request_view="more_items" %}
        """
        rendered = self.render_template(template_string)
        assert "/api/more-items/" in rendered


class LanguageSelectorTemplateTagTest(TemplateTagsTestCase):
    """Tests für den language_selector Template Tag."""

    def test_language_selector_basic(self) -> None:
        """Test für grundlegende language_selector Funktionalität."""
        template_string = """
        {% include "insight_ui/components/toggle_language.html" %}
        """
        rendered = self.render_template(template_string)
        assert "de" in rendered


class AlertTemplateTagTest(TemplateTagsTestCase):
    """Tests für den alert Template Tag."""

    def test_alert_basic(self) -> None:
        """Test für grundlegende alert Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% alert message="Test message" %}
        """
        rendered = self.render_template(template_string)
        assert "Test message" in rendered

    def test_alert_types(self) -> None:
        """Test für verschiedene alert Typen."""
        for alert_type in ["info", "success", "warning", "error"]:
            with self.subTest(alert_type=alert_type):
                template_string = f"""
                {{% load insight_tags %}}
                {{% alert message="Test message" type="{alert_type}" %}}
                """
                rendered = self.render_template(template_string)
                assert "Test message" in rendered


class SidebarTemplateTagTest(TemplateTagsTestCase):
    """Tests für den sidebar Template Tag."""

    def test_sidebar_basic(self) -> None:
        """Test für grundlegende sidebar Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% sidebar title="Navigation" %}
        """
        rendered = self.render_template(template_string)
        assert "Navigation" in rendered


class BreadcrumbsTemplateTagTest(TemplateTagsTestCase):
    """Tests für den breadcrumbs Template Tag."""

    def test_breadcrumbs_basic(self) -> None:
        """Test für grundlegende breadcrumbs Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% breadcrumbs %}
        """
        rendered = self.render_template(template_string)
        assert rendered is not None


class TableTemplateTagTest(TemplateTagsTestCase):
    """Tests für den table Template Tag."""

    def test_table_basic(self) -> None:
        """Test für grundlegende table Funktionalität."""
        table = {
            "caption": "Ein Beispiel einer Tabellen-Komponente.",
            "empty_msg": "Keine Daten vorhanden!",
            "headers": ["Name", "E-Mail", "Status"],
            "rows": [["Max Mustermann", "max@example.com", "Aktiv"]],
        }

        template_string = """
        {% load insight_tags %}
        {% table table_data=table_data %}
        """
        rendered = self.render_template(template_string, context={"table_data": table})
        assert rendered is not None


class ModalTemplateTagTest(TemplateTagsTestCase):
    """Tests für den modal Template Tag."""

    def test_modal_basic(self) -> None:
        """Test für grundlegende modal Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% modal html_tag_id="test-modal" title="Test Modal" %}
        """
        rendered = self.render_template(template_string)
        assert "test-modal" in rendered
        assert "Test Modal" in rendered


class CardTemplateTagTest(TemplateTagsTestCase):
    """Tests für den card Template Tag."""

    def test_card_basic(self) -> None:
        """Test für grundlegende card Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% card title="Test Card" content="Test Card Content" %}
        """
        rendered = self.render_template(template_string)
        assert "Test Card" in rendered


class FormTemplateTagTest(TemplateTagsTestCase):
    """Tests für den form Template Tag."""

    def test_form_basic(self) -> None:
        """Test für grundlegende form Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% form title="Test Form" %}
        """
        rendered = self.render_template(template_string)
        assert "Test Form" in rendered


class FooterTemplateTagTest(TemplateTagsTestCase):
    """Tests für den footer Template Tag."""

    def test_footer_basic(self) -> None:
        """Test für grundlegende footer Funktionalität."""
        footer_data = {
            "description": {"title": "Django Insight UI", "text": "-"},
            "links": [{"text": "Startseite", "view_name": "storybook_view"}],
        }

        template_string = """
        {% load insight_tags %}
        {% footer data=footer_data %}
        """
        rendered = self.render_template(template_string, context={"footer_data": footer_data})
        assert rendered is not None
