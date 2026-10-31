# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the footer component."""

import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template
from insight_ui.configs.base import IconConfig
from insight_ui.configs.navigation import FooterConfig, FooterContactConfig, FooterDescriptionConfig, NavbarLinkConfig
from insight_ui.configs.utils import LegalNoticeConfig, LogoConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestFooter(TemplateTagsTestCase):
    """Test suite for the footer component."""

    def test_footer_basic(self) -> None:
        """Test für grundlegende footer Funktionalität."""
        footer_data = FooterConfig(
            FooterDescriptionConfig(
                "Insight UI",
                "A modern UI library for Django applications to get started quickly.",
                LogoConfig("insight_ui/svg/insight-ui-logo.svg", alt="Insight UI Logo", height="6rem"),
            ),
            [
                NavbarLinkConfig("Startpage", "/", IconConfig("home", "xs")),
                NavbarLinkConfig("Storybook", "/"),
                NavbarLinkConfig("Documentation", "/"),
            ],
            FooterContactConfig(
                "support@alpininsight.com", "https://alpininsight.com/imprint/", "https://alpininsight.com/privacy/"
            ),
            LegalNoticeConfig(2026, "Alpin Insight Solutions GmbH & Co. KG", "Open Source", "AGPL-3.0", "/license/"),
            "v1.0.0",
        )

        template_string = """
        {% load insight_tags %}
        {% footer config=footer_data %}
        """
        rendered = self.render_template(template_string, context={"footer_data": footer_data})
        soup = BeautifulSoup(rendered, "html.parser")

        # --- Assert: description ---
        desc_title = soup.find("h2")
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
        license_el = copyright_p.find("a", href="/license/")
        assert license_el is not None
        assert license_el.get_text(strip=True) == "AGPL-3.0"


def test_footer_section_headings_are_h2() -> None:
    """Footer sections are top-level sections of the page, so they must not jump from h1/h2 to h4."""
    footer = FooterConfig(
        FooterDescriptionConfig("Insight UI", "Summary"),
        [NavbarLinkConfig("Startpage", "/")],
        FooterContactConfig("support@example.com"),
    )
    html = Template("{% load insight_tags %}{% footer config=footer %}").render(Context({"footer": footer}))
    soup = BeautifulSoup(html, "html.parser")

    headings = soup.find("footer").find_all(["h2", "h3", "h4"])
    assert [h.name for h in headings] == ["h2", "h2", "h2"]
    assert [h.get_text(strip=True) for h in headings] == ["Insight UI", "Links", "Contact"]


def test_contact_email_is_shown_and_linked_with_mailto() -> None:
    """The address is the link text; the link adds mailto: itself."""
    footer = FooterConfig(
        FooterDescriptionConfig("Insight UI", "Summary"), [], FooterContactConfig(email="team@example.com")
    )
    html = Template("{% load insight_tags %}{% footer config=footer %}").render(Context({"footer": footer}))
    link = BeautifulSoup(html, "html.parser").find("a", href="mailto:team@example.com")

    assert link.get_text(strip=True) == "team@example.com"


def test_contact_email_is_an_address() -> None:
    """A mailto: URL or text that is no address is rejected instead of rendering a broken link."""
    with pytest.raises(ValueError, match="without mailto:"):
        FooterContactConfig(email="mailto:team@example.com")
    with pytest.raises(ValueError, match="is not an email address"):
        FooterContactConfig(email="team at example")


def test_external_footer_link_opens_a_new_tab_and_says_so() -> None:
    """Footer links share NavbarLinkConfig, so external opens a new tab here too, with the hidden hint."""
    footer = FooterConfig(
        links=[
            NavbarLinkConfig(text="Docs", request_url="https://docs.example.com/", external=True),
            NavbarLinkConfig(text="Home", request_url="/"),
        ]
    )
    html = Template("{% load insight_tags %}{% footer config=footer %}").render(Context({"footer": footer}))
    soup = BeautifulSoup(html, "html.parser")

    docs = soup.find("a", href="https://docs.example.com/")
    home = soup.find("footer").find("a", href="/")
    assert docs["target"] == "_blank"
    assert docs.get_text(" ", strip=True) == "Docs (opens in a new tab)"
    assert not home.has_attr("target")
    assert home.get_text(" ", strip=True) == "Home"
