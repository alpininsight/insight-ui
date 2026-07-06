"""Tests for the footer component."""

from bs4 import BeautifulSoup
from django.urls import reverse_lazy
from insight_ui.configs.base import IconConfig
from insight_ui.configs.navigation import FooterConfig, FooterContactConfig, FooterDescriptionConfig, NavbarLinkConfig
from insight_ui.configs.utils import CopyrightNoticeConfig, LogoConfig

from tests.unit.components.test_template_tags import TemplateTagsTestCase


class TestFooter(TemplateTagsTestCase):
    """Test suite for the footer component."""

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
        for link, el in zip(footer_data.links, link_elements, strict=True):
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
