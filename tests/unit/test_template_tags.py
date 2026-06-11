"""Tests für Insight UI Template Tags."""

# ruff: noqa: E501

import insight_ui.templatetags.insight_tags
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.template import Context, Template
from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.safestring import SafeText
from django.utils.translation import activate
from insight_ui.component_details.demo_context import get_radio_block_context, get_radio_group_context
from insight_ui.configs.base import IconConfig
from insight_ui.configs.input import CheckboxConfig, CheckboxGroupConfig, CheckboxItemConfig, SliderConfig, ToggleConfig
from insight_ui.configs.list import TableConfig
from insight_ui.configs.navigation import (
    FooterConfig,
    FooterContactConfig,
    FooterDescriptionConfig,
    NavbarBrandConfig,
    NavbarConfig,
    NavbarLinkConfig,
)
from insight_ui.configs.popup import ModalConfig
from insight_ui.configs.utils import BrandLockupConfig, CopyrightNoticeConfig, LogoConfig


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


class NavbarTemplateTagTest(TemplateTagsTestCase):
    """Tests für den navbar Template Tag."""

    def test_navbar(self) -> None:
        """Test für grundlegende navbar Funktionalität."""
        nav_config = NavbarConfig(
            NavbarBrandConfig(
                "Insight UI",
                "/",
                LogoConfig(
                    "insight_ui/svg/ai-logo.svg", "insight_ui/svg/ai-logo.svg", "Insight UI Logo", height="2rem"
                ),
                "0.5rem",
            ),
            [
                NavbarLinkConfig("Startpage", "/", IconConfig("home", "s")),
                NavbarLinkConfig(
                    "About",
                    modal=ModalConfig(
                        "about-modal",
                        "About Insight-UI",
                        "A modern UI library for Django applications to get started quickly.",
                    ),
                ),
            ],
            "/",
            True,
            True,
            True,
        )

        template_string = """
        {% load insight_tags %}
        {% navbar config=nav_config %}
        """

        rendered = self.render_template(template_string, context={"nav_config": nav_config})
        assert "Insight UI" in rendered

    def test_navbar_user_menu_is_hidden_until_opened(self) -> None:
        """Authenticated user menus must not push navbar controls into a second row."""
        nav_config = NavbarConfig(
            NavbarBrandConfig(
                "Insight UI",
                "/",
                LogoConfig(
                    "insight_ui/svg/ai-logo.svg", "insight_ui/svg/ai-logo.svg", "Insight UI Logo", height="2rem"
                ),
                "0.5rem",
            ),
            show_usermenu=True,
            show_language_selector=True,
            show_theme_toggle=True,
        )

        template_string = """
        {% load insight_tags %}
        {% navbar config=nav_config user_dropdown_links=user_dropdown_links %}
        """

        rendered = self.render_template(
            template_string, context={"nav_config": nav_config, "user_dropdown_links": [], "user": self.user}
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
        nav_config = NavbarConfig(
            NavbarBrandConfig(
                "Insight UI",
                "/",
                aria_label="Alpin Insight Develop Startseite",
                lockup=BrandLockupConfig("Alpin Insight", "Develop", height="2rem", variant="develop"),
            )
        )

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
        nav_config = NavbarConfig(
            NavbarBrandConfig(
                "Insight UI",
                "/",
                LogoConfig(
                    "insight_ui/svg/ai-logo.svg", "insight_ui/svg/ai-logo.svg", "Insight UI Logo", height="2rem"
                ),
                "0.5rem",
            )
        )

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
        config = CopyrightNoticeConfig(
            2026,
            "Alpin Insight Solutions GmbH & Co. KG",
            "Open Source",
            "AGPL-3.0",
            "https://example.com/license",
            rights_text="All rights reserved.",
        )
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


class LogoTemplateTagTest(TemplateTagsTestCase):
    """Tests for the logo template tag."""

    def test_logo_renders_svg_asset(self) -> None:
        """SVG logo assets should render as static image tags."""
        template_string = """
        {% load insight_tags %}
        {% logo url="insight_ui/svg/ai-logo.svg" alt="Insight UI Logo" height="3rem" %}
        """
        rendered = self.render_template(template_string)
        soup = BeautifulSoup(rendered, "html.parser")

        logo = soup.find("img")
        assert logo is not None
        assert logo.name == "img"
        assert logo.get("src") == "/static/insight_ui/svg/ai-logo.svg"
        assert logo.get("alt") == "Insight UI Logo"
        assert "height: 3rem" in logo.get("style")

    def test_logo_renders_dark_variant(self) -> None:
        """Dark logo variants should render with dark-mode classes."""
        config = LogoConfig("light.png", "dark.png", "Insight UI Logo")
        template_string = """
        {% load insight_tags %}
        {% logo config=config %}
        """
        rendered = self.render_template(template_string, context={"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        logos = soup.find_all("img")
        assert len(logos) == 2  # noqa: PLR2004
        assert logos[0].get("src") == "/static/light.png"
        assert "dark:hidden" in logos[0].get("class")
        assert logos[1].get("src") == "/static/dark.png"
        assert "dark:inline-block" in logos[1].get("class")

    def test_logo_renders_icon(self) -> None:
        """Icon logos should use the existing Insight UI icon set."""
        config = LogoConfig(icon=IconConfig("sparkles", "xl"), alt="Decorative product icon")
        template_string = """
        {% load insight_tags %}
        {% logo config=config %}
        """
        rendered = self.render_template(template_string, context={"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        wrapper = soup.find("span", attrs={"role": "img", "aria-label": "Decorative product icon"})
        assert wrapper is not None
        assert wrapper.find("svg") is not None


class LiveContentTemplateTagTest(TemplateTagsTestCase):
    """Tests für den live_content Template Tag."""

    def test_live_content_basic(self) -> None:
        """Test für grundlegende live_content Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% live_content request_url="/api/live-data/" %}
        """
        rendered = self.render_template(template_string)
        assert "/api/live-data/" in rendered

    def test_live_content_with_interval(self) -> None:
        """Test für live_content mit Intervall."""
        template_string = """
        {% load insight_tags %}
        {% live_content request_url="/api/live-data/" interval=5000 %}
        """
        rendered = self.render_template(template_string)
        assert "/api/live-data/" in rendered


class WebsocketTemplateTagTest(TemplateTagsTestCase):
    """Tests für den websocket Template Tag."""

    def test_websocket_basic(self) -> None:
        """Test für grundlegende WebSocket Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% websocket request_url="/runtime/stream/" %}
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
        {% websocket request_url="/runtime/stream/" %}
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
        {% infinite_scroll request_url="/api/more-items/" %}
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


class TableTemplateTagTest(TemplateTagsTestCase):
    """Tests für den table Template Tag."""

    def test_table_basic(self) -> None:
        """Test für grundlegende table Funktionalität."""
        table = TableConfig(
            ["Name", "E-Mail", "Status", "Actions"],
            [
                ["Max Mustermann", "max@example.com", "Active", '<button class="btn btn-primary">Edit</button>'],
                ["Anna Schmidt", "anna@example.com", "Inactive", '<button class="btn btn-primary">Edit</button>'],
                ["Tom Weber", "tom@example.com", "Active", '<button class="btn btn-primary">Edit</button>'],
            ],
            "Example of a table component.",
        )

        template_string = """
        {% load insight_tags %}
        {% table config=user_data %}
        """
        rendered = self.render_template(template_string, context={"user_data": table})
        soup = BeautifulSoup(rendered, "html.parser")

        table = soup.find("table")

        assert table.find("caption") is not None

        header_row = table.find("thead").find("tr")
        headers = [th.get_text(strip=True) for th in header_row.find_all("th")]
        assert headers == ["Name", "E-Mail", "Status", "Actions"]

        rows = table.find("tbody").find_all("tr")
        assert len(rows) == 3  # noqa: PLR2004

        first_row = [td.get_text(strip=True) for td in rows[0].find_all("td")]
        assert first_row == ["Max Mustermann", "max@example.com", "Active", "Edit"]


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

    def test_card_content_allows_html(self) -> None:
        """Card content can render developer-provided HTML fragments."""
        rendered = self.render_template(
            '{% load insight_tags %}{% card title="Formatted" content="<strong>Important</strong><br>Line 2" %}'
        )
        assert "<strong>Important</strong>" in rendered
        assert "<br>Line 2" in rendered

    def test_card_actions_stay_inside_long_html_content_layout(self) -> None:
        """Long formatted card content must not push actions outside the card."""
        card = {
            "title": "Formatted card content",
            "content": (
                "<p>This card uses <strong>bold text</strong>, <em>line breaks</em>, "
                "and a short list:</p><ul><li>Safe developer supplied markup</li>"
                "<li>Structured text in cards</li><li>Additional content that should scroll</li></ul>"
            ),
            "actions": [{"text": "Learn more", "url": "/docs/", "type": "primary"}],
        }
        template_string = """
        {% load insight_tags %}
        {% card title=card.title content=card.content actions=card.actions %}
        """

        rendered = self.render_template(template_string, context={"card": card})
        soup = BeautifulSoup(rendered, "html.parser")

        outer_card = soup.find("div", class_="max-w-96")
        assert outer_card is not None
        assert "flex" in outer_card.get("class", [])
        assert "flex-col" in outer_card.get("class", [])
        assert "min-h-56" in outer_card.get("class", [])
        assert "h-56" not in outer_card.get("class", [])

        body = outer_card.find("div", class_="flex")
        assert body is not None
        assert "min-h-0" in body.get("class", [])
        assert "flex-1" in body.get("class", [])
        assert "min-h-56" not in body.get("class", [])

        content = outer_card.find("div", class_="overflow-auto")
        assert content is not None
        assert "min-h-0" in content.get("class", [])
        assert "grow" in content.get("class", [])
        assert content.find("strong", string="bold text") is not None

        actions = outer_card.find("div", class_="mt-auto")
        assert actions is not None
        assert "flex-wrap" in actions.get("class", [])
        action_link = actions.find("a")
        assert action_link is not None
        assert action_link.get_text(strip=True) == "Learn more"

    def test_app_card_content_allows_html(self) -> None:
        """App card content can render developer-provided HTML fragments."""
        card = {
            "title": "Catalog Product",
            "content": "Supports <strong>formatted</strong> content.",
            "image": {"url": "/static/product.png", "alt": "Product preview"},
        }
        template_string = """
        {% load insight_tags %}
        {% app_card title=card.title content=card.content image=card.image %}
        """

        rendered = self.render_template(template_string, context={"card": card})
        assert "<strong>formatted</strong>" in rendered

    def test_flip_card_back_content_and_style(self) -> None:
        """Flip card can render formatted content on a styled back side."""
        card = {
            "title": "Formatted Flip",
            "content": "Front <strong>content</strong>.",
            "image": {"url": "/static/product.png", "alt": "Product preview"},
            "back_content": "<p>Lorem ipsum</p>",
        }
        template_string = """
        {% load insight_tags %}
        {% flip_card title=card.title content=card.content image=card.image back_content=card.back_content %}
        """

        rendered = self.render_template(template_string, context={"card": card})
        assert "Front <strong>content</strong>." in rendered
        assert "<p>Lorem ipsum</p>" in rendered


class FormTemplateTagTest(TemplateTagsTestCase):
    """Tests für den form Template Tag."""

    def test_form_basic(self) -> None:
        """Test für grundlegende form Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% form title="Test Form" request_url="/api/form_submit/" %}
        """
        rendered = self.render_template(template_string)
        assert "Test Form" in rendered


class FooterTemplateTagTest(TemplateTagsTestCase):
    """Tests für den footer Template Tag."""

    def test_footer_basic(self) -> None:
        """Test für grundlegende footer Funktionalität."""
        footer_data = FooterConfig(
            FooterDescriptionConfig(
                "Insight UI",
                "A modern UI library for Django applications to get started quickly.",
                LogoConfig("insight_ui/svg/ai-logo.svg", alt="Insight UI Logo", height="6rem"),
            ),
            [
                NavbarLinkConfig("Startpage", "/", IconConfig("home", "xs")),
                NavbarLinkConfig("Storybook", "/"),
                NavbarLinkConfig("Documentation", "/"),
            ],
            FooterContactConfig(
                "support@alpininsight.com", "https://alpininsight.com/imprint/", "https://alpininsight.com/privacy/"
            ),
            CopyrightNoticeConfig(
                2026, "Alpin Insight Solutions GmbH & Co. KG", "Open Source", "AGPL-3.0", reverse_lazy("license_view")
            ),
            "v1.0.0",
        )

        template_string = """
        {% load insight_tags %}
        {% footer config=footer_data %}
        """
        rendered = self.render_template(template_string, context={"footer_data": footer_data})
        soup = BeautifulSoup(rendered, "html.parser")

        # --- Assert: description ---
        desc_title = soup.find("h4")
        assert desc_title.get_text() == "Insight UI"

        desc_text = soup.find("p")
        assert desc_text.get_text() == "A modern UI library for Django applications to get started quickly."

        # --- Assert: links ---
        link_elements = soup.select("ul li a")
        assert len(link_elements) == 3  # noqa: PLR2004
        for link, el in zip(footer_data.links, link_elements):
            assert el.get("href") == "/"
            assert link.text in el.text

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
        copyright_p = next((p for p in soup.find_all("p") if str(2026) in p.get_text(" ", strip=True)), None)
        assert copyright_p is not None
        assert "Alpin Insight Solutions GmbH & Co. KG" in copyright_p.text
        assert "Open Source" in copyright_p.text
        assert "AGPL-3.0" in copyright_p.text
        assert "All rights reserved." in copyright_p.text
        license_el = copyright_p.find("a", href="/docs/license/")
        assert license_el is not None
        assert license_el.get_text(strip=True) == "AGPL-3.0"


class CheckboxTemplateTagTest(TemplateTagsTestCase):
    """Tests for the {% checkbox %} component."""

    def test_checkbox_config(self) -> None:
        """Test the {% checkbox %} tag with config dataclass."""
        config = CheckboxConfig(
            "accept-terms", "accept_terms", "I accept the terms and conditions", required=True, value="accepted"
        )

        result = insight_ui.templatetags.insight_tags.checkbox(config=config)
        assert result["checkbox_config"] == config

    def test_checkbox_single_params(self) -> None:
        """Test the {% checkbox %} tag with single params."""
        template_string = """
        {% load insight_tags %}
        {% checkbox tag_id="accept-terms" name="accept_terms" value="accepted" checked=False disabled=False label="I accept the terms and conditions" %}
        {% checkbox tag_id="newsletter-box" name="newsletter" value="subscribed" checked=True disabled=True label="Subscribe for Newsletter" %}
        """
        rendered = self.render_template(template_string)
        soup = BeautifulSoup(rendered, "html.parser")

        checkboxes = soup.find_all("input")
        label_spans = soup.find_all("span")
        assert checkboxes[0]["id"] == "accept-terms"
        assert checkboxes[0]["name"] == "accept_terms"
        assert checkboxes[0]["value"] == "accepted"
        assert not checkboxes[0].has_attr("checked")
        assert not checkboxes[0].has_attr("disabled")
        assert label_spans[0].get_text() == "I accept the terms and conditions"
        assert "text-primary" in label_spans[0]["class"]

        assert checkboxes[1]["id"] == "newsletter-box"
        assert checkboxes[1]["name"] == "newsletter"
        assert checkboxes[1]["value"] == "subscribed"
        assert checkboxes[1].has_attr("checked")
        assert checkboxes[1].has_attr("disabled")
        assert label_spans[1].get_text() == "Subscribe for Newsletter"
        assert "text-secondary" in label_spans[1]["class"]

    def test_checkbox_group(self) -> None:
        """Test the {% checkbox_group %} tag."""
        checkbox_context = CheckboxGroupConfig(
            "language",
            "Choose languages: (max. 3)",
            [
                CheckboxItemConfig("english", "English", "english"),
                CheckboxItemConfig("german", "German", "german", checked=True),
                CheckboxItemConfig("french", "French", "french"),
                CheckboxItemConfig("spanish", "Spanish", "spanish"),
                CheckboxItemConfig("italian", "Italian (currently not available)", "italian", True),
            ],
            True,
            1,
            3,
        )

        template_string = """
        {% load insight_tags %}
        {% checkbox_group checkbox_config %}
        """

        rendered = self.render_template(template_string, {"checkbox_config": checkbox_context})
        soup = BeautifulSoup(rendered, "html.parser")

        wrapper = soup.find("div", {"data-insight-checkbox-group": True})
        assert wrapper["data-minimum-checked"] == "1"

        # Check label
        label_span = wrapper.find("span")
        assert label_span.text == "Choose languages: (max. 3)"

        # Check layout
        container = wrapper.find("div", class_="flex")
        assert "space-x-4" in container["class"]

        # Check count of checkboxes
        inputs = container.find_all("input", type="checkbox")
        label_spans = container.find_all("span")
        assert len(inputs) == 5  # noqa: PLR2004
        assert len(label_spans) == 5  # noqa: PLR2004

        # First checkbox
        assert inputs[0]["id"] == "english"
        assert inputs[0]["name"] == "language"
        assert inputs[0]["value"] == "english"
        assert not inputs[0].has_attr("checked")
        assert not inputs[0].has_attr("disabled")
        assert label_spans[0].get_text() == "English"

        # Second checkbox
        assert inputs[1]["id"] == "german"
        assert inputs[1]["name"] == "language"
        assert inputs[1]["value"] == "german"
        assert inputs[1].has_attr("checked")
        assert not inputs[1].has_attr("disabled")
        assert label_spans[1].get_text() == "German"

        # Third checkbox
        assert inputs[4]["id"] == "italian"
        assert inputs[4]["name"] == "language"
        assert inputs[4]["value"] == "italian"
        assert not inputs[4].has_attr("checked")
        assert inputs[4].has_attr("disabled")
        assert label_spans[4].get_text() == "Italian (currently not available)"


class RadioGroupTemplateTagTest(TemplateTagsTestCase):
    """Tests for the {% radio_group %} component."""

    def test_radio_block_block(self) -> None:
        """Test the {% radio_block %} tag."""
        context = get_radio_block_context()

        template_string = """
        {% load insight_tags %}
        {% radio_block size_radio_config %}
        """

        rendered = self.render_template(template_string, context)
        soup = BeautifulSoup(rendered, "html.parser")

        wrapper = soup.find("div")

        # Check label
        label_span = wrapper.find("span")
        assert label_span.text.strip() == "Select size:"

        form = wrapper.find("form", id="size")
        assert form is not None

        # Check count of radios
        inputs = form.find_all("input", type="radio")
        labels = form.find_all("label")
        assert len(inputs) == 3  # noqa: PLR2004

        # First radio
        assert inputs[0]["id"] == "size-small-size"
        assert inputs[0]["name"] == "size"
        assert inputs[0]["value"] == "small"
        assert inputs[0].has_attr("checked")
        assert not inputs[0].has_attr("disabled")
        assert inputs[0].has_attr("hx-get")
        assert inputs[0].has_attr("hx-target")
        assert inputs[0].has_attr("hx-swap")
        assert inputs[0].has_attr("data-radio-callback")
        assert labels[0]["for"] == "size-small-size"
        assert labels[0].get_text().strip() == "s"

        # Second radio
        assert inputs[1]["id"] == "size-medium-size"
        assert inputs[1]["name"] == "size"
        assert inputs[1]["value"] == "medium"
        assert not inputs[1].has_attr("checked")
        assert not inputs[1].has_attr("disabled")
        assert labels[1]["for"] == "size-medium-size"
        assert labels[1].get_text().strip() == "m"

        # Third radio
        assert inputs[2]["id"] == "size-large-size"
        assert inputs[2]["name"] == "size"
        assert inputs[2]["value"] == "large"
        assert not inputs[2].has_attr("checked")
        assert inputs[2].has_attr("disabled")
        assert labels[2]["for"] == "size-large-size"
        assert labels[2].get_text().strip() == "l"

    def test_radio_group(self) -> None:
        """Test the {% radio_group %} tag."""
        context = get_radio_group_context()

        template_string = """
        {% load insight_tags %}
        {% radio_group config=model_radio_config %}
        """

        rendered = self.render_template(template_string, context)
        soup = BeautifulSoup(rendered, "html.parser")

        wrapper = soup.find("div")

        # Check label
        label_span = wrapper.find("span")
        assert label_span.text.strip() == "Select AI Model:"

        # Check layout
        container = wrapper.find("div", class_="flex")
        assert "space-y-1" in container["class"]

        # Check count of radios
        inputs = container.find_all("input", type="radio")
        label_spans = container.find_all("span")
        assert len(inputs) == 3  # noqa: PLR2004

        # First radio
        assert inputs[0]["id"] == "model1"
        assert inputs[0]["name"] == "model"
        assert inputs[0]["value"] == "BERT"
        assert inputs[0].has_attr("checked")
        assert not inputs[0].has_attr("disabled")
        assert label_spans[0].get_text() == "BERT"

        # Second radio
        assert inputs[1]["id"] == "model2"
        assert inputs[1]["name"] == "model"
        assert inputs[1]["value"] == "PaLM 2"
        assert not inputs[1].has_attr("checked")
        assert not inputs[1].has_attr("disabled")
        assert label_spans[1].get_text() == "PaLM 2"

        # Third radio
        assert inputs[2]["id"] == "model3"
        assert inputs[2]["name"] == "model"
        assert inputs[2]["value"] == "LLaMA 2"
        assert not inputs[2].has_attr("checked")
        assert inputs[2].has_attr("disabled")
        assert label_spans[2].get_text() == "LLaMA 2 (currently not available)"


class ToggleButtonTemplateTagTest(TemplateTagsTestCase):
    """Tests for the {% toggle %} component."""

    def test_toggle_config(self) -> None:
        """Test the {% toggle %} tag with config dataclass."""
        config = ToggleConfig("toggle-switch", "toggle-switch", "Click me!", switch=True)
        result = insight_ui.templatetags.insight_tags.toggle(config=config)

        assert result["toggle_config"] == config

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

    def test_slider_config(self) -> None:
        """Test the {% slider %} tag with config dataclass."""
        config = SliderConfig(
            "range-slider-skip",
            "range_slider_skip",
            "Legend Mode: Skip",
            value=6,
            minimum=1,
            maximum=12,
            items=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            legend_mode="skip",
        )

        result = insight_ui.templatetags.insight_tags.slider(config=config)
        assert result["slider_config"] == config

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
            "{% load insight_tags %}{% brand_lockup config=cfg %}", context={"cfg": {"logo_position": "end"}}
        )
        root = BeautifulSoup(rendered, "html.parser").find("div")
        assert "justify-between" in root.get("class", [])
        assert "order: 2" in rendered

    def test_brand_lockup_default_variant_uses_app_icon(self) -> None:
        """Default renders the public app icon."""
        rendered = self.render_template("{% load insight_tags %}{% brand_lockup %}")
        svg = BeautifulSoup(rendered, "html.parser").find("svg")
        assert svg.get("viewbox") == "0 0 24 24"
        assert "M2.25 6a3 3" in rendered

    def test_brand_lockup_develop_variant_uses_rocket_icon(self) -> None:
        """Develop renders the public rocket icon."""
        rendered = self.render_template('{% load insight_tags %}{% brand_lockup variant="develop" %}')
        svg = BeautifulSoup(rendered, "html.parser").find("svg")
        assert svg.get("viewbox") == "0 0 24 24"
        assert "M15.59 14.37" in rendered

    def test_brand_lockup_candidate_variant_uses_sparkles_icon(self) -> None:
        """Candidate renders the public sparkles icon."""
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

    def test_brand_lockup_preserves_positional_height_argument(self) -> None:
        """The fourth positional argument remains accepted for backwards compatibility."""
        rendered = self.render_template(
            '{% load insight_tags %}{% brand_lockup "Alpin Insight" "Develop" "start" "2.5rem" %}'
        )
        svg = BeautifulSoup(rendered, "html.parser").find("svg")
        assert "Alpin Insight" in rendered
        assert "Develop" in rendered
        assert svg.get("viewbox") == "0 0 24 24"
