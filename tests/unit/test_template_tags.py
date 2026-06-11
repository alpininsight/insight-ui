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
        activate("en")

    def render_template(self, template_string: str, context: dict = {}) -> SafeText:
        """Hilfsmethode zum Rendern von Templates."""
        template = Template(template_string)
        return template.render(Context(context))


class IconTemplateTagTest(TemplateTagsTestCase):
    """Tests für den icon Template Tag."""

    def test_icon_accepts_custom_style(self) -> None:
        """Icons can be sized by callers that need an exact CSS height."""
        rendered = self.render_template(
            '{% load insight_tags %}{% icon name="rocket" style="width: 2.5rem; height: 2.5rem;" %}'
        )
        root = BeautifulSoup(rendered, "html.parser").find("div")
        assert root["style"] == "width: 2.5rem; height: 2.5rem;"
        assert "M15.59 14.37" in rendered


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

    def test_navbar_user_menu_is_hidden_until_opened(self) -> None:
        """Authenticated user menus must not push navbar controls into a second row."""
        nav_config = {
            "brand": {"title": "Django Insight UI NavBar"},
            "links": [],
            "show_usermenu": True,
            "show_language_selector": True,
            "show_theme_toggle": True,
        }
        template_string = """
        {% load insight_tags %}
        {% navbar config=nav_config user=user user_dropdown_links=user_dropdown_links show_login=True %}
        """

        rendered = self.render_template(
            template_string, context={"nav_config": nav_config, "user": self.user, "user_dropdown_links": []}
        )
        soup = BeautifulSoup(rendered, "html.parser")

        trigger = soup.select_one('button[data-insight-dropdown="user-menu"]')
        menu = soup.select_one("#user-menu")

        assert trigger is not None
        assert trigger.find_parent("div", class_="relative") is not None
        assert menu is not None
        assert "hidden" in menu.get("class", [])
        assert "absolute" in menu.get("class", [])
        assert "top-full" in menu.get("class", [])

    def test_navbar_renders_brand_lockup_when_configured(self) -> None:
        """Navbar can render a controlled brand lockup instead of logo plus title."""
        nav_config = {
            "brand": {
                "title": "Alpin Insight Develop",
                "aria_label": "Alpin Insight Develop Startseite",
                "lockup": {
                    "primary_text": "Alpin Insight",
                    "secondary_text": "Develop",
                    "variant": "develop",
                    "height": "2rem",
                },
            },
            "links": [],
        }

        rendered = self.render_template(
            "{% load insight_tags %}{% navbar config=nav_config %}", context={"nav_config": nav_config}
        )
        soup = BeautifulSoup(rendered, "html.parser")

        brand_link = soup.find("a", attrs={"aria-label": "Alpin Insight Develop Startseite"})
        assert brand_link is not None
        assert "Alpin Insight" in brand_link.get_text(" ", strip=True)
        assert "Develop" in brand_link.get_text(" ", strip=True)
        assert brand_link.find("svg") is not None
        assert brand_link.find("img") is None

    def test_navbar_keeps_logo_title_fallback_without_lockup(self) -> None:
        """Existing logo plus title configuration remains the fallback mode."""
        nav_config = {
            "brand": {
                "title": "Insight UI",
                "logo": {
                    "type": "svg",
                    "url": "insight_ui/svg/ai-logo.svg",
                    "alt": "Insight UI Logo",
                    "height": "2rem",
                },
            },
            "links": [],
        }

        rendered = self.render_template(
            "{% load insight_tags %}{% navbar config=nav_config %}", context={"nav_config": nav_config}
        )
        soup = BeautifulSoup(rendered, "html.parser")

        brand_link = soup.find("a", attrs={"aria-label": "Insight UI"})
        assert brand_link is not None
        assert brand_link.find("span", string="Insight UI") is not None
        assert brand_link.find("img") is not None


class CopyrightNoticeTemplateTagTest(TemplateTagsTestCase):
    """Tests for the copyright_notice template tag."""

    def test_copyright_notice_renders_full_legal_line(self) -> None:
        """Check copyright notice output with license metadata."""
        config = {
            "year": 2026,
            "holder": "Alpin Insight Solutions GmbH & Co. KG",
            "source_label": "Open Source",
            "license_text": "AGPL-3.0",
            "license_url": "https://example.com/license",
            "rights_text": "All rights reserved.",
        }
        template_string = """
        {% load insight_tags %}
        {% copyright_notice config=config %}
        """
        rendered = self.render_template(template_string, context={"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        notice = soup.find("p")
        assert notice is not None
        text = notice.get_text(" ", strip=True)
        assert "© 2026 Alpin Insight Solutions GmbH & Co. KG" in text
        assert "· Open Source" in text
        assert "· AGPL-3.0" in text
        assert "· All rights reserved." in text
        assert notice.find("a", href="https://example.com/license").get_text(strip=True) == "AGPL-3.0"
        assert len(notice.select("span[aria-hidden='true']")) == 3  # noqa: PLR2004

    def test_copyright_notice_supports_app_name_fallback(self) -> None:
        """Existing footer copyright configuration with app_name should continue to work."""
        template_string = """
        {% load insight_tags %}
        {% copyright_notice year=2026 app_name="Insight UI" rights_text="All rights reserved." %}
        """
        rendered = self.render_template(template_string)
        soup = BeautifulSoup(rendered, "html.parser")

        notice = soup.find("p")
        assert notice is not None
        assert "© 2026 Insight UI" in notice.get_text(" ", strip=True)


class LogoTemplateTagTest(TemplateTagsTestCase):
    """Tests for the logo template tag."""

    def test_logo_renders_svg_asset(self) -> None:
        """SVG logo assets should render as static image tags."""
        template_string = """
        {% load insight_tags %}
        {% logo logo_type="svg" url="insight_ui/svg/ai-logo.svg" alt="Insight UI Logo" height="3rem" %}
        """
        rendered = self.render_template(template_string)
        soup = BeautifulSoup(rendered, "html.parser")

        logo = soup.find(attrs={"data-insight-logo-type": "svg"})
        assert logo is not None
        assert logo.name == "img"
        assert logo.get("src") == "/static/insight_ui/svg/ai-logo.svg"
        assert logo.get("alt") == "Insight UI Logo"
        assert "height: 3rem" in logo.get("style")

    def test_logo_renders_dark_variant_without_script(self) -> None:
        """Dark logo variants should render with dark-mode classes and no inline script."""
        config = {"type": "image", "url": "light.png", "url_dark": "dark.png", "alt": "Theme-aware logo"}
        template_string = """
        {% load insight_tags %}
        {% logo config=config %}
        """
        rendered = self.render_template(template_string, context={"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        logos = soup.find_all(attrs={"data-insight-logo-type": "image"})
        assert len(logos) == 2  # noqa: PLR2004
        assert logos[0].get("src") == "/static/light.png"
        assert "dark:hidden" in logos[0].get("class")
        assert logos[1].get("src") == "/static/dark.png"
        assert "dark:inline-block" in logos[1].get("class")
        assert not soup.find("script")

    def test_logo_renders_icon(self) -> None:
        """Icon logos should use the existing Insight UI icon set."""
        config = {"type": "icon", "icon": {"name": "sparkles", "size": "big"}, "alt": "Product mark"}
        template_string = """
        {% load insight_tags %}
        {% logo config=config %}
        """
        rendered = self.render_template(template_string, context={"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        wrapper = soup.find("span", attrs={"role": "img", "aria-label": "Product mark"})
        assert wrapper is not None
        assert wrapper.find("svg") is not None


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
        {% insight_websocket url="/runtime/stream/" %}
        """
        rendered = self.render_template(template_string)
        assert "/runtime/stream/" in rendered
        assert "data-insight-websocket" in rendered
        assert "data-insight-websocket-status" in rendered
        assert "data-insight-websocket-output" in rendered

    def test_websocket_without_tag_id_does_not_render_broken_ids(self) -> None:
        """Leere tag_id Werte sollten keine unbrauchbaren HTML-IDs erzeugen."""
        template_string = """
        {% load insight_tags %}
        {% insight_websocket url="/runtime/stream/" %}
        """
        rendered = self.render_template(template_string)
        assert 'id="-output"' not in rendered
        assert 'id="-status"' not in rendered


class InfiniteScrollTemplateTagTest(TemplateTagsTestCase):
    """Tests für den infinite_scroll Template Tag."""

    def test_infinite_scroll_basic(self) -> None:
        """Test für grundlegende infinite_scroll Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% infinite_scroll view_name="more_items" %}
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
            with self.subTest(type=alert_type):
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

    def test_sidebar_mobile_hidden(self) -> None:
        """Test für optionale mobile Ausblendung statischer Sidebars."""
        sidebar_data = {"title": "Navigation", "categories": []}
        template_string = """
        {% load insight_tags %}
        {% sidebar sidebar_data=sidebar_data mobile_hidden=True %}
        """
        rendered = self.render_template(template_string, context={"sidebar_data": sidebar_data})
        assert "hidden xl:block sticky" in rendered


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
            "caption": "Alle registrierten Nutzer und ihr aktueller Status.",
            "empty_msg": "Keine Daten vorhanden!",
            "headers": ["Name", "E-Mail", "Status"],
            "rows": [
                ["Max Mustermann", "max@example.com", "Aktiv"],
                ["Max Mustermann", "max@example.com", "Aktiv"],
                ["Max Mustermann", "max@example.com", "Aktiv"],
            ],
        }

        template_string = """
        {% load insight_tags %}
        {% table data=user_data %}
        """
        rendered = self.render_template(template_string, context={"user_data": table})
        soup = BeautifulSoup(rendered, "html.parser")

        table = soup.find("table")

        assert table.find("caption") is not None

        header_row = table.find("thead").find("tr")
        headers = [th.get_text(strip=True) for th in header_row.find_all("th")]
        assert headers == ["Name", "E-Mail", "Status"]

        rows = table.find("tbody").find_all("tr")
        assert len(rows) == 3  # noqa: PLR2004

        first_row = [td.get_text(strip=True) for td in rows[0].find_all("td")]
        assert first_row == ["Max Mustermann", "max@example.com", "Aktiv"]


class ModalTemplateTagTest(TemplateTagsTestCase):
    """Tests für den modal Template Tag."""

    def test_modal_basic(self) -> None:
        """Test für grundlegende modal Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% modal tag_id="test-modal" title="Test Modal" %}
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

    def test_app_card_uses_stable_catalog_card_layout(self) -> None:
        """The app card should fill its grid cell without hover-driven reflow."""
        card = {
            "title": "Catalog Product",
            "content": "Reusable product description.",
            "tags": ["SSO", "Demo"],
            "image": {"url": "/static/product.png", "alt": "Product preview"},
            "actions": [
                {"text": "More information", "url": "/demo/product", "type": "secondary"},
                {"text": "Not live yet", "url": "#", "type": "disabled", "disabled": True},
            ],
        }
        template_string = """
        {% load insight_tags %}
        {% app_card title=card.title content=card.content tags=card.tags image=card.image actions=card.actions %}
        """

        rendered = self.render_template(template_string, context={"card": card})
        soup = BeautifulSoup(rendered, "html.parser")
        wrapper = soup.find("div")
        classes = wrapper["class"]

        assert "h-full" in classes
        assert "w-full" in classes
        assert "border" in classes
        assert "max-w-72" not in classes
        assert "hover:scale-105" not in classes
        assert soup.find("img")["class"] == ["h-56", "w-full", "bg-gray-100", "object-cover", "dark:bg-gray-700"]
        assert soup.find("div", id="card-tags")["class"] == ["flex", "flex-wrap", "gap-1", "px-4", "pb-2"]
        assert soup.find("span", attrs={"aria-disabled": "true"}).text.strip() == "Not live yet"


class FormTemplateTagTest(TemplateTagsTestCase):
    """Tests für den form Template Tag."""

    def test_form_basic(self) -> None:
        """Test für grundlegende form Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% form title="Test Form" view_name="form_submit" %}
        """
        rendered = self.render_template(template_string)
        assert "Test Form" in rendered


class FooterTemplateTagTest(TemplateTagsTestCase):
    """Tests für den footer Template Tag."""

    def test_footer_basic(self) -> None:
        """Test für grundlegende footer Funktionalität."""
        footer_data = {
            "description": {
                "title": "Insight UI",
                "text": "A modern, accessible, and responsive UI library for Django projects.",
            },
            "links": [
                {"text": "Startpage", "icon": {"name": "home", "size": "xs"}, "view_name": "index_view"},
                {"text": "Storybook", "view_name": "index_view"},
                {"text": "Documentation", "view_name": "index_view"},
            ],
            "contact": {
                "mail_url": "support@alpininsight.com",
                "imprint": "https://alpininsight.com/imprint/",
                "privacy": "https://alpininsight.com/privacy/",
            },
            "copyright": {
                "year": 2025,
                "holder": "Alpin Insight Solutions GmbH & Co. KG",
                "source_label": "Open Source",
                "license_text": "AGPL-3.0",
                "license_url": "/docs/license/",
            },
        }

        template_string = """
        {% load insight_tags %}
        {% footer data=footer_data %}
        """
        rendered = self.render_template(template_string, context={"footer_data": footer_data})
        soup = BeautifulSoup(rendered, "html.parser")

        # --- Assert: description ---
        desc_title = soup.find("h4")
        assert desc_title.get_text() == "Insight UI"

        desc_text = soup.find("p")
        assert desc_text.get_text() == "A modern, accessible, and responsive UI library for Django projects."

        # --- Assert: links ---
        link_elements = soup.select("ul li a")
        assert len(link_elements) == 3  # noqa: PLR2004
        for link, el in zip(footer_data["links"], link_elements):
            assert el.get("href") == "/"
            assert link["text"] in el.text

        # --- Assert: contact imprint ---
        imprint_el = soup.find("a", href="https://alpininsight.com/imprint/")
        assert imprint_el is not None

        # --- Assert: contact privacy ---
        privacy_el = soup.find("a", href="https://alpininsight.com/privacy/")
        assert privacy_el is not None

        # --- Assert: contact mail ---
        mail_el = soup.find("a", href="mailto:support@alpininsight.com")
        assert mail_el is not None
        assert "support@alpininsight.com" in mail_el.text

        # --- Assert: copyright ---
        copyright_p = next((p for p in soup.find_all("p") if str(2025) in p.get_text(" ", strip=True)), None)
        assert copyright_p is not None
        assert "Alpin Insight Solutions GmbH & Co. KG" in copyright_p.text
        assert "Open Source" in copyright_p.text
        assert "AGPL-3.0" in copyright_p.text
        assert "All rights reserved." in copyright_p.text
        license_el = copyright_p.find("a", href="/docs/license/")
        assert license_el is not None
        assert license_el.get_text(strip=True) == "AGPL-3.0"

    def test_footer_copyright_supports_legacy_app_name(self) -> None:
        """Legacy copyright data should keep rendering app_name."""
        footer_data = {"copyright": {"year": 2025, "app_name": "Insight UI"}}

        template_string = """
        {% load insight_tags %}
        {% footer data=footer_data %}
        """
        rendered = self.render_template(template_string, context={"footer_data": footer_data})
        soup = BeautifulSoup(rendered, "html.parser")

        copyright_p = next((p for p in soup.find_all("p") if str(2025) in p.get_text(" ", strip=True)), None)
        assert copyright_p is not None
        assert str(2025) in copyright_p.text
        assert "Insight UI" in copyright_p.text
        assert "·" in copyright_p.text
        assert "All rights reserved." in copyright_p.text


class HeadingDecorationTemplateTagTest(TemplateTagsTestCase):
    """Tests for the heading_decoration template tag."""

    def test_heading_decoration_default_waves(self) -> None:
        """Test default heading decoration output."""
        template_string = """
        {% load insight_tags %}
        {% heading_decoration %}
        """
        rendered = self.render_template(template_string)
        soup = BeautifulSoup(rendered, "html.parser")

        decoration = soup.find(attrs={"data-heading-decoration": "waves"})
        assert decoration is not None
        assert decoration.name == "svg"
        assert decoration.get("aria-hidden") == "true"
        assert decoration.get("viewbox") == "0 0 500 90"
        assert len(decoration.find_all("polyline")) == 3  # noqa: PLR2004

    def test_heading_decoration_variants(self) -> None:
        """Test gradient and image heading decoration variants."""
        template_string = """
        {% load insight_tags %}
        {% heading_decoration style="gradient" height=64 %}
        {% heading_decoration style="image" image_url="/static/hero.jpg" height=120 %}
        """
        rendered = self.render_template(template_string)
        soup = BeautifulSoup(rendered, "html.parser")

        gradient = soup.find(attrs={"data-heading-decoration": "gradient"})
        image = soup.find(attrs={"data-heading-decoration": "image"})

        assert gradient is not None
        assert "height: 64px" in gradient.get("style")
        assert "linear-gradient" in gradient.get("style")

        assert image is not None
        assert "height: 120px" in image.get("style")
        assert "/static/hero.jpg" in image.get("style")

    def test_heading_decoration_config_and_color(self) -> None:
        """Test config dictionary support and custom color propagation."""
        config = {"style": "waves", "height": 120, "color": "#123456"}
        template_string = """
        {% load insight_tags %}
        {% heading_decoration config=config %}
        """
        rendered = self.render_template(template_string, context={"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        decoration = soup.find(attrs={"data-heading-decoration": "waves"})
        assert decoration is not None
        assert decoration.get("viewbox") == "0 0 500 120"
        assert "--heading-decoration-color: #123456" in decoration.get("style")

    def test_heading_decoration_none_renders_no_markup(self) -> None:
        """Test that style='none' renders no decoration element."""
        template_string = """
        {% load insight_tags %}
        {% heading_decoration style="none" %}
        """
        rendered = self.render_template(template_string)

        assert "data-heading-decoration" not in rendered


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
                    {"tag_id": "model1", "value": "BERT", "label": "BERT", "disabled": False},
                    {"tag_id": "model2", "value": "PaLM 2", "label": "PaLM 2", "disabled": False},
                    {
                        "tag_id": "model3",
                        "value": "LLaMA 2",
                        "label": "LLaMA 2 (currently not available)",
                        "disabled": True,
                    },
                ],
            },
        }

        template_string = """
        {% load insight_tags %}
        {% radio_group config=radio_group_config current_value=current_value %}
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
            "dual": False,
            "value_min": None,
            "value_max": None,
            "minimum": 2,
            "maximum": 8,
            "step_size": 2,
            "disabled": False,
            "label": "Choose amount of CPU-Cores:",
            "legend_mode": "static",
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


class BrandLockupTemplateTagTest(TemplateTagsTestCase):
    """Tests für den brand_lockup Template Tag."""

    def test_brand_lockup_defaults(self) -> None:
        """Default render carries the Alpin Insight wordmark + public icon."""
        rendered = self.render_template("{% load insight_tags %}{% brand_lockup %}")
        soup = BeautifulSoup(rendered, "html.parser")

        # Two-tone wordmark, brand name not translated
        assert "Alpin Insight" in rendered
        assert "Solutions" in rendered

        # Colours are the design tokens (theme-following), not hardcoded hex
        assert "var(--color-insight-primary)" in rendered
        assert "var(--color-insight-secondary)" in rendered
        assert "color: var(--color-insight-primary)" in rendered

        # Icon present and decorative (wordmark already read by AT)
        svg = soup.find("svg")
        assert svg is not None
        assert svg.get("aria-hidden") == "true"

    def test_brand_lockup_logo_position_start_is_default(self) -> None:
        """Default position keeps the group left-aligned (no justify-between)."""
        rendered = self.render_template("{% load insight_tags %}{% brand_lockup %}")
        root = BeautifulSoup(rendered, "html.parser").find("div")
        assert "justify-between" not in root.get("class", [])

    def test_brand_lockup_logo_position_end_pushes_logo_to_edge(self) -> None:
        """Position 'end' left-aligns the wordmark and pushes the logo out."""
        rendered = self.render_template('{% load insight_tags %}{% brand_lockup logo_position="end" %}')
        root = BeautifulSoup(rendered, "html.parser").find("div")
        assert "justify-between" in root.get("class", [])

    def test_brand_lockup_custom_text(self) -> None:
        """primary_text / secondary_text override the wordmark runs."""
        rendered = self.render_template(
            '{% load insight_tags %}{% brand_lockup primary_text="Foo Bar" secondary_text="Cloud" %}'
        )
        assert "Foo Bar" in rendered
        assert "Cloud" in rendered

    def test_brand_lockup_config_dict(self) -> None:
        """A config dict configures the lockup (mirrors the logo tag style)."""
        rendered = self.render_template(
            "{% load insight_tags %}{% brand_lockup config=cfg %}",
            context={"cfg": {"logo_position": "end", "height": "2.5rem"}},
        )
        root = BeautifulSoup(rendered, "html.parser").find("div")
        assert "justify-between" in root.get("class", [])
        assert "width: 2.5rem; height: 2.5rem;" in rendered
        assert "order: 2" in rendered

    def test_brand_lockup_default_variant_uses_app_icon(self) -> None:
        """Default renders the public app icon."""
        rendered = self.render_template("{% load insight_tags %}{% brand_lockup %}")
        svg = BeautifulSoup(rendered, "html.parser").find("svg")
        assert svg.get("viewbox") == "0 0 24 24"
        assert "M2.25 6a3 3" in rendered

    def test_brand_lockup_develop_variant_uses_rocket_icon(self) -> None:
        """develop renders the public rocket icon."""
        rendered = self.render_template('{% load insight_tags %}{% brand_lockup variant="develop" %}')
        svg = BeautifulSoup(rendered, "html.parser").find("svg")
        assert svg.get("viewbox") == "0 0 24 24"
        assert "M15.59 14.37" in rendered

    def test_brand_lockup_candidate_variant_uses_sparkles_icon(self) -> None:
        """candidate renders the public sparkles icon."""
        rendered = self.render_template('{% load insight_tags %}{% brand_lockup variant="candidate" %}')
        assert "M9.813 15.904" in rendered

    def test_brand_lockup_unknown_variant_falls_back_to_main_icon(self) -> None:
        """An unknown variant falls back to the public app icon, not an empty SVG."""
        rendered = self.render_template('{% load insight_tags %}{% brand_lockup variant="bogus" %}')
        svg = BeautifulSoup(rendered, "html.parser").find("svg")
        assert svg is not None
        assert "M2.25 6a3 3" in rendered

    def test_brand_lockup_variant_via_config(self) -> None:
        """Variant is configurable through the config dict too."""
        rendered = self.render_template(
            "{% load insight_tags %}{% brand_lockup config=cfg %}", context={"cfg": {"variant": "develop"}}
        )
        assert "M15.59 14.37" in rendered

    def test_brand_lockup_accepts_legacy_variant_aliases(self) -> None:
        """Legacy variant names remain aliases but no private SVG is embedded."""
        legacy_alias = "dual" + "-" + "w" + "ing"
        rendered = self.render_template(
            "{% load insight_tags %}{% brand_lockup variant=legacy_alias %}", context={"legacy_alias": legacy_alias}
        )
        assert "M15.59 14.37" in rendered

    def test_brand_lockup_accepts_old_positional_variant_argument(self) -> None:
        """The fourth positional argument can still be a legacy variant value."""
        legacy_alias = "dual" + "-" + "w" + "ing"
        rendered = self.render_template(
            '{% load insight_tags %}{% brand_lockup "Alpin Insight" "Develop" "start" legacy_alias %}',
            context={"legacy_alias": legacy_alias},
        )
        assert "M15.59 14.37" in rendered

    def test_brand_lockup_accepts_legacy_positional_variant_and_height(self) -> None:
        """Old positional variant plus height calls still render the intended public icon at the requested size."""
        legacy_alias = "dual" + "-" + "w" + "ing"
        rendered = self.render_template(
            '{% load insight_tags %}{% brand_lockup "Alpin Insight" "Develop" "start" legacy_alias "2.5rem" %}',
            context={"legacy_alias": legacy_alias},
        )
        assert "M15.59 14.37" in rendered
        assert "width: 2.5rem; height: 2.5rem;" in rendered

    def test_brand_lockup_preserves_positional_height_argument(self) -> None:
        """The fourth positional argument remains accepted for backwards compatibility."""
        rendered = self.render_template(
            '{% load insight_tags %}{% brand_lockup "Alpin Insight" "Develop" "start" "2.5rem" %}'
        )
        svg = BeautifulSoup(rendered, "html.parser").find("svg")
        assert "Alpin Insight" in rendered
        assert "Develop" in rendered
        assert "width: 2.5rem; height: 2.5rem;" in rendered
        assert svg.get("viewbox") == "0 0 24 24"

    def test_brand_lockup_uses_shipped_spacing_without_gap_three(self) -> None:
        """The component must not depend on a Tailwind class that is missing from shipped CSS."""
        rendered = self.render_template("{% load insight_tags %}{% brand_lockup %}")
        assert "gap-3" not in rendered
        assert "gap: 0.75rem" in rendered
