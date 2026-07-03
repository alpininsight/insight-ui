"""Tests for the copyright_notice component."""

from bs4 import BeautifulSoup
from insight_ui.configs.utils import CopyrightNoticeConfig

from tests.unit.components.test_template_tags import TemplateTagsTestCase


class TestCopyrightNotice(TemplateTagsTestCase):
    """Test suite for the copyright_notice component."""

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
