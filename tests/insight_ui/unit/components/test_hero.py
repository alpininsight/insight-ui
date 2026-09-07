# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the hero component."""

from bs4 import BeautifulSoup
from insight_ui.configs.layout import HeroConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestHero(TemplateTagsTestCase):
    """Test suite for the hero component."""

    def render_hero(self) -> BeautifulSoup:
        """Render a hero with a title, subtitle and description."""
        config = HeroConfig(
            title="Identity without ambiguity",
            subtitle="A governed identity plane",
            description="OIDC for people, applications and service clients.",
        )
        html = self.render_template("{% load insight_tags %}{% hero config=config %}", {"config": config})
        return BeautifulSoup(html, "html.parser")

    def test_title_is_the_single_h1(self) -> None:
        """The hero title provides the page's primary heading."""
        soup = self.render_hero()
        headings = soup.find_all("h1")
        assert len(headings) == 1
        assert headings[0].get_text(strip=True) == "Identity without ambiguity"

    def test_subtitle_uses_the_semantic_heading_token(self) -> None:
        """The subtitle remains readable for every configured light or dark theme."""
        soup = self.render_hero()
        subtitle = soup.find("p", string="A governed identity plane")
        assert subtitle is not None
        classes = subtitle.get("class", [])
        assert "text-insight-headline" in classes
        assert "text-insight-primary" not in classes
