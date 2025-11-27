"""Tests für Insight UI Template Tags."""

# ruff: noqa: E501

import insight_ui.templatetags.insight_tags
import pytest
from bs4 import BeautifulSoup
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
                    "view_kwargs": {"storybook_name": "components"},
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
        sidebar_data = {"title": "Navigation", "categories": []}
        template_string = """
        {% load insight_tags %}
        {% sidebar sidebar_data=sidebar_data %}
        """
        rendered = self.render_template(template_string, context={"sidebar_data": sidebar_data})
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
            "links": [
                {"text": "Startseite", "view_name": "storybook_view", "view_kwargs": {"storybook_name": "components"}}
            ],
        }

        template_string = """
        {% load insight_tags %}
        {% footer data=footer_data %}
        """
        rendered = self.render_template(template_string, context={"footer_data": footer_data})
        assert rendered is not None


class CheckboxTemplateTagTest(TemplateTagsTestCase):
    """Tests for the {% checkbox %} component."""

    def test_checkbox_config_dict(self) -> None:
        """Test the {% checkbox %} tag with a config dictionary."""
        config = {
            "tag_id": "agb-box",
            "name": "accept_agb",
            "value": "accept_agb",
            "checked": False,
            "disabled": False,
            "label": "Accept AGBs",
        }

        result = insight_ui.templatetags.insight_tags.checkbox(config=config)
        print(result)
        assert result == config

    def test_checkbox_single_params(self) -> None:
        """Test the {% checkbox %} tag with single params."""
        template_string = """
        {% load insight_tags %}
        {% checkbox tag_id="agb-box" name="accept_agb" value="accept_agb" checked=False disabled=False label="Accept AGBs" %}
        {% checkbox tag_id="newsletter-box" name="newsletter" value="newsletter" checked=True disabled=True label="Subscribe for Newsletter" %}
        """
        rendered = self.render_template(template_string)
        soup = BeautifulSoup(rendered, "html.parser")

        checkboxes = soup.find_all("input")
        label_spans = soup.find_all("span")
        assert checkboxes[0]["id"] == "agb-box"
        assert checkboxes[0]["name"] == "accept_agb"
        assert checkboxes[0]["value"] == "accept_agb"
        assert not checkboxes[0].has_attr("checked")
        assert not checkboxes[0].has_attr("disabled")
        assert label_spans[0].get_text() == "Accept AGBs"
        assert "text-primary" in label_spans[0]["class"]

        assert checkboxes[1]["id"] == "newsletter-box"
        assert checkboxes[1]["name"] == "newsletter"
        assert checkboxes[1]["value"] == "newsletter"
        assert checkboxes[1].has_attr("checked")
        assert checkboxes[1].has_attr("disabled")
        assert label_spans[1].get_text() == "Subscribe for Newsletter"
        assert "text-secondary" in label_spans[1]["class"]

    def test_checkbox_group(self) -> None:
        """Test the {% checkbox_group %} tag."""
        checkbox_context = {
            "name": "language_select",
            "label": "Choose languages:",
            "as_row": True,
            "items": [
                {"id": "lang1", "value": "english", "label": "English", "disabled": False},
                {"id": "lang2", "value": "german", "label": "German", "checked": True, "disabled": False},
                {"id": "lang3", "value": "italian", "label": "Italian (currently not available)", "disabled": True},
            ],
        }

        template_string = """
        {% load insight_tags %}
        {% checkbox_group checkbox_config %}
        """

        rendered = self.render_template(template_string, {"checkbox_config": checkbox_context})
        soup = BeautifulSoup(rendered, "html.parser")

        wrapper = soup.find("div", {"data-insight-checkbox-group": True})
        assert wrapper["data-minimum-checked"] == "-1"

        # Check label
        label_span = wrapper.find("span")
        assert label_span.text == "Choose languages:"

        # Check layout
        container = wrapper.find("div", class_="flex")
        assert "space-x-4" in container["class"]

        # Check count of checkboxes
        inputs = container.find_all("input", type="checkbox")
        label_spans = container.find_all("span")
        assert len(inputs) == 3  # noqa: PLR2004
        assert len(label_spans) == 3  # noqa: PLR2004

        # First checkbox
        assert inputs[0]["id"] == "lang1"
        assert inputs[0]["name"] == "language_select"
        assert inputs[0]["value"] == "english"
        assert not inputs[0].has_attr("checked")
        assert not inputs[0].has_attr("disabled")
        assert label_spans[0].get_text() == "English"

        # Second checkbox
        assert inputs[1]["id"] == "lang2"
        assert inputs[1]["name"] == "language_select"
        assert inputs[1]["value"] == "german"
        assert inputs[1].has_attr("checked")
        assert not inputs[1].has_attr("disabled")
        assert label_spans[1].get_text() == "German"

        # Third checkbox
        assert inputs[2]["id"] == "lang3"
        assert inputs[2]["name"] == "language_select"
        assert inputs[2]["value"] == "italian"
        assert not inputs[2].has_attr("checked")
        assert inputs[2].has_attr("disabled")
        assert label_spans[2].get_text() == "Italian (currently not available)"


class RadioGroupTemplateTagTest(TemplateTagsTestCase):
    """Tests for the {% radio_group %} component."""

    @pytest.mark.skip(reason="Needs to be finished!")
    def test_radio_block_block(self) -> None:
        """Test the {% radio_block %} tag."""
        context = {
            "current_value": "BERT",
            "view_name": "index",
            "query_params": "lang=german",
            "target_id": "test-container",
            "method": "loadOptions",
            "integrated": False,
            "radio_group_config": {
                "name": "model_select",
                "label": "Choose model:",
                "items": [
                    {"id": "model1", "value": "BERT", "label": "BERT", "disabled": False},
                    {"id": "model2", "value": "PaLM 2", "label": "PaLM 2", "disabled": False},
                    {
                        "id": "model3",
                        "value": "LLaMA 2",
                        "label": "LLaMA 2 (currently not available)",
                        "disabled": True,
                    },
                ],
            },
        }

        template_string = """
        {% load insight_tags %}
        {% radio_block radio_group_config current_value=current_value %}
        """

        rendered = self.render_template(template_string, context)
        soup = BeautifulSoup(rendered, "html.parser")

        wrapper = soup.find("div")

        # Check label
        label_span = wrapper.find("span")
        assert label_span.text.strip() == "Choose model:"

        form = wrapper.find("form", id="model_select")
        assert form is not None

        # Check count of radios
        inputs = form.find_all("input", type="radio")
        labels = form.find_all("label")
        assert len(inputs) == 3  # noqa: PLR2004

        # First radio
        assert inputs[0]["id"] == "model1"
        assert inputs[0]["name"] == "model_select"
        assert inputs[0]["value"] == "BERT"
        assert inputs[0].has_attr("checked")
        assert not inputs[0].has_attr("disabled")
        assert inputs[0].has_attr("hx-get")
        assert inputs[0].has_attr("hx-target")
        assert inputs[0].has_attr("hx-swap")
        assert inputs[0].has_attr("onclick")
        assert labels[0]["for"] == "model1"
        assert labels[0].get_text() == "BERT"

        # Second radio
        assert inputs[1]["id"] == "model2"
        assert inputs[1]["name"] == "model_select"
        assert inputs[1]["value"] == "PaLM 2"
        assert not inputs[1].has_attr("checked")
        assert not inputs[1].has_attr("disabled")
        assert labels[1]["for"] == "model2"
        assert labels[1].get_text() == "PaLM 2"

        # Third radio
        assert inputs[2]["id"] == "model3"
        assert inputs[2]["name"] == "model_select"
        assert inputs[2]["value"] == "LLaMA 2"
        assert not inputs[2].has_attr("checked")
        assert inputs[2].has_attr("disabled")
        assert labels[2]["for"] == "model3"
        assert labels[2].get_text() == "LLaMA 2 (currently not available)"

    def test_radio_group(self) -> None:
        """Test the {% radio_group %} tag."""
        context = {
            "current_value": "BERT",
            "radio_group_config": {
                "name": "model_select",
                "label": "Choose model:",
                "as_row": True,
                "items": [
                    {"id": "model1", "value": "BERT", "label": "BERT", "disabled": False},
                    {"id": "model2", "value": "PaLM 2", "label": "PaLM 2", "disabled": False},
                    {
                        "id": "model3",
                        "value": "LLaMA 2",
                        "label": "LLaMA 2 (currently not available)",
                        "disabled": True,
                    },
                ],
            },
        }

        template_string = """
        {% load insight_tags %}
        {% radio_group radio_group_config current_value=current_value %}
        """

        rendered = self.render_template(template_string, context)
        soup = BeautifulSoup(rendered, "html.parser")

        wrapper = soup.find("div")

        # Check label
        label_span = wrapper.find("span")
        assert label_span.text.strip() == "Choose model:"

        # Check layout
        container = wrapper.find("div", class_="flex")
        assert "space-x-4" in container["class"]

        # Check count of radios
        inputs = container.find_all("input", type="radio")
        label_spans = container.find_all("span")
        assert len(inputs) == 3  # noqa: PLR2004

        # First radio
        assert inputs[0]["id"] == "model1"
        assert inputs[0]["name"] == "model_select"
        assert inputs[0]["value"] == "BERT"
        assert inputs[0].has_attr("checked")
        assert not inputs[0].has_attr("disabled")
        assert label_spans[0].get_text() == "BERT"

        # Second radio
        assert inputs[1]["id"] == "model2"
        assert inputs[1]["name"] == "model_select"
        assert inputs[1]["value"] == "PaLM 2"
        assert not inputs[1].has_attr("checked")
        assert not inputs[1].has_attr("disabled")
        assert label_spans[1].get_text() == "PaLM 2"

        # Third radio
        assert inputs[2]["id"] == "model3"
        assert inputs[2]["name"] == "model_select"
        assert inputs[2]["value"] == "LLaMA 2"
        assert not inputs[2].has_attr("checked")
        assert inputs[2].has_attr("disabled")
        assert label_spans[2].get_text() == "LLaMA 2 (currently not available)"


class ToggleButtonTemplateTagTest(TemplateTagsTestCase):
    """Tests for the {% toggle %} component."""

    def test_toggle_config_dict(self) -> None:
        """Test the {% toggle %} tag with a config dictionary."""
        config = {
            "tag_id": "theme-toggle",
            "name": "toggle_theme",
            "value": "toggle_theme",
            "checked": False,
            "disabled": False,
            "label": "Dark",
            "icon": {"name": "moon"},
            "switch": True,
        }

        result = insight_ui.templatetags.insight_tags.toggle(config=config)

        # Add 'method' parameter to dict, to match with the result dict
        # 'method' is an additional parameter.
        config["method"] = ""
        assert result == config

    def test_toggle(self) -> None:
        """Test the {% toggle %} tag."""
        template_string = """
        {% load insight_tags %}
        {% toggle tag_id="theme-toggle" name="toggle_theme" value="toggle_theme" checked=False disabled=False label="Dark" method="changeTheme" switch=True %}
        """
        rendered = self.render_template(template_string)
        soup = BeautifulSoup(rendered, "html.parser")

        switch = soup.find("label")

        label = switch.find("span")
        assert "Dark" in label.get_text()

        input_element = switch.find("input")
        assert input_element["id"] == "theme-toggle"
        assert input_element["name"] == "toggle_theme"
        assert input_element["value"] == "toggle_theme"
        assert input_element["onclick"] == "changeTheme()"
        assert not input_element.has_attr("checked")
        assert not input_element.has_attr("disabled")

    def test_toggle_switch(self) -> None:
        """Test the {% toggle %} tag."""
        template_string = """
        {% load insight_tags %}
        {% toggle tag_id="theme-toggle" name="toggle_theme" value="toggle_theme" checked=False disabled=False label="Dark" method="changeTheme" %}
        """
        rendered = self.render_template(template_string)
        soup = BeautifulSoup(rendered, "html.parser")

        wrapper = soup.find("div")

        label = wrapper.find("label")
        assert "Dark" in label.get_text()
        assert label["for"] == "theme-toggle"

        input_element = wrapper.find("input")
        assert input_element["id"] == "theme-toggle"
        assert input_element["name"] == "toggle_theme"
        assert input_element["value"] == "toggle_theme"
        assert input_element["onclick"] == "changeTheme()"
        assert not input_element.has_attr("checked")
        assert not input_element.has_attr("disabled")


class SliderTemplateTagTest(TemplateTagsTestCase):
    """Tests for the {% toggle %} component."""

    def test_slider_config_dict(self) -> None:
        """Test the {% slider %} tag with a config dictionary."""
        config = {
            "tag_id": "cpu-cores",
            "name": "cpu_core_count",
            "value": 4,
            "minimum": 2,
            "maximum": 8,
            "step_size": 2,
            "disabled": False,
            "label": "Choose amount of CPU-Cores:",
            "items": ["2", "4", "6", "8"],
        }

        result = insight_ui.templatetags.insight_tags.slider(config=config)
        assert result == config

    def test_slider(self) -> None:
        """Test the {% slider %} tag."""
        template_string = """
        {% load insight_tags %}
        {% slider tag_id="cpu-cores" name="cpu_core_count" value=4 minimum=2 maximum=8 step_size=2 disabled=False label="Choose amount of CPU-Cores:" %}
        """
        rendered = self.render_template(template_string)
        soup = BeautifulSoup(rendered, "html.parser")

        wrapper = soup.find("div")

        label = wrapper.find("label")
        assert "Choose amount of CPU-Cores:" in label.get_text()
        assert label["for"] == "cpu-cores"

        input_element = wrapper.find("input")
        assert input_element["id"] == "cpu-cores"
        assert input_element["name"] == "cpu_core_count"
        assert input_element["value"] == "4"
        assert input_element["min"] == "2"
        assert input_element["max"] == "8"
        assert input_element["step"] == "2"
        assert not input_element.has_attr("disabled")
