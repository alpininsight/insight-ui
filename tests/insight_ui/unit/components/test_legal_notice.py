# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the legal_notice component."""

from bs4 import BeautifulSoup
from insight_ui.configs.utils import LegalNoticeConfig, LogoConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestLegalNotice(TemplateTagsTestCase):
    """Test suite for the legal_notice component."""

    def test_legal_notice_renders_full_legal_line(self) -> None:
        """Check legal notice output with license metadata."""
        config = LegalNoticeConfig(
            2026,
            "Alpin Insight Solutions GmbH & Co. KG",
            "Open Source",
            "AGPL-3.0",
            "https://example.com/license",
            rights_text="All rights reserved.",
        )
        template_string = """
        {% load insight_tags %}
        {% legal_notice config=config %}
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
        assert "dark:text-insight-text-link-hover" in notice.find("a")["class"]
        assert len(notice.select("span[aria-hidden='true']")) == 3  # noqa: PLR2004

    def test_holder_link_composes_a_decorative_theme_aware_logo(self) -> None:
        """The host owns the link and logo; the visible name supplies the link label."""
        config = LegalNoticeConfig(
            year=2026,
            holder="Example Company",
            holder_url="https://company.example/",
            holder_logo=LogoConfig(
                url="https://assets.example/logo-light.svg",
                url_dark="https://assets.example/logo-dark.svg",
                alt="",
                height="1.25rem",
            ),
        )
        rendered = self.render_template("{% load insight_tags %}{% legal_notice config=config %}", {"config": config})
        soup = BeautifulSoup(rendered, "html.parser")
        link = soup.find("a", href="https://company.example/")

        assert link.get_text(strip=True) == "Example Company"
        assert "dark:text-insight-text-link-hover" in link["class"]
        images = link.find_all("img")
        assert [image["src"] for image in images] == [
            "https://assets.example/logo-light.svg",
            "https://assets.example/logo-dark.svg",
        ]
        assert all(image["alt"] == "" for image in images)
        assert "dark:hidden" in images[0]["class"]
        assert "dark:inline-block" in images[1]["class"]
        assert link.find("img").find_next("span").get_text(strip=True) == "Example Company"

    def test_holder_url_can_be_passed_as_a_tag_argument(self) -> None:
        """Direct arguments can override a config without modifying the caller's object."""
        config = LegalNoticeConfig(holder="Example Company", holder_url="/original/")
        rendered = self.render_template(
            '{% load insight_tags %}{% legal_notice config=config holder_url="/company/" holder_logo=logo %}',
            {"config": config, "logo": LogoConfig(url="logo.svg", alt="")},
        )
        link = BeautifulSoup(rendered, "html.parser").find("a", href="/company/")

        assert link.get_text(strip=True) == "Example Company"
        assert link.find("img")["src"] == "/static/logo.svg"
        assert config.holder_url == "/original/"
        assert config.holder_logo is None

    def test_holder_logo_without_a_url_does_not_create_a_link(self) -> None:
        """The logo can accompany plain copyright text without an empty anchor."""
        config = LegalNoticeConfig(holder="Example Company", holder_logo=LogoConfig(url="logo.svg", alt=""))
        rendered = self.render_template("{% load insight_tags %}{% legal_notice config=config %}", {"config": config})
        notice = BeautifulSoup(rendered, "html.parser").find("p")

        assert notice.find("a") is None
        assert notice.find("img")["src"] == "/static/logo.svg"
        assert "Example Company" in notice.get_text()

    def test_holder_link_without_a_logo_preserves_legacy_metadata(self) -> None:
        """The name may be linked independently of the optional logo."""
        config = LegalNoticeConfig(2026, "Example Company", "Open Source", holder_url="/company/", version="v1.2.3")
        rendered = self.render_template("{% load insight_tags %}{% legal_notice config=config %}", {"config": config})
        notice = BeautifulSoup(rendered, "html.parser").find("p")

        assert notice.find("a", href="/company/").get_text(strip=True) == "Example Company"
        assert notice.find("img") is None
        assert "Open Source" in notice.get_text()
        assert "v1.2.3" in notice.get_text()

    def test_empty_holder_does_not_render_an_unlabelled_link(self) -> None:
        """Without a visible holder, optional publisher settings cannot create an empty link."""
        config = LegalNoticeConfig(holder_url="/company/", holder_logo=LogoConfig(url="logo.svg", alt=""))
        rendered = self.render_template("{% load insight_tags %}{% legal_notice config=config %}", {"config": config})
        notice = BeautifulSoup(rendered, "html.parser").find("p")

        assert notice.find("a") is None
        assert notice.find("img") is None

    def test_holder_is_escaped_inside_the_link(self) -> None:
        """Publisher names remain plain text rather than an HTML injection surface."""
        config = LegalNoticeConfig(holder="<b>Example & Company</b>", holder_url="/company/")
        rendered = self.render_template("{% load insight_tags %}{% legal_notice config=config %}", {"config": config})
        link = BeautifulSoup(rendered, "html.parser").find("a", href="/company/")

        assert link.find("b") is None
        assert link.get_text(strip=True) == "<b>Example & Company</b>"
