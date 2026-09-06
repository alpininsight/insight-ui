"""Tests for the page_header component."""

from bs4 import BeautifulSoup
from insight_ui.configs.layout import PageHeaderConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestPageHeader(TemplateTagsTestCase):
    """Test suite for the page_header component."""

    def render_page_header(self, style: str = "docs") -> BeautifulSoup:
        """Render the page header with a title, a chapter and a description."""
        config = PageHeaderConfig(
            title="Example Page",
            chapter="Insight UI",
            description=["A header component for documentation pages."],
            style=style,
        )
        html = self.render_template("{% load insight_tags %}{% page_header config=config %}", {"config": config})
        return BeautifulSoup(html, "html.parser")

    def test_title_is_the_single_h1(self) -> None:
        """WCAG 1.3.1 and 2.4.6: the title is rendered as one semantic h1."""
        soup = self.render_page_header()
        headings = soup.find_all("h1")
        assert len(headings) == 1
        assert "Example Page" in headings[0].get_text(" ", strip=True)

    def test_title_uses_the_primary_foreground_token(self) -> None:
        """WCAG 1.4.3: the title colour is the foreground token that keeps 3:1 on dark surfaces.

        ``text-insight-primary`` is the decoration accent (#0856C0) and only reaches 2.97:1 on the
        dark background, so the title must use ``text-insight-primary-foreground``.
        """
        soup = self.render_page_header()
        title = soup.find("h1").find("span")
        classes = title.get("class", [])
        assert "text-insight-primary-foreground" in classes
        assert "text-insight-primary" not in classes

    def test_description_is_a_paragraph(self) -> None:
        """The description is rendered as paragraph text below the heading."""
        soup = self.render_page_header()
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
        assert "A header component for documentation pages." in paragraphs

    def test_fancy_style_hides_the_decorative_graphic(self) -> None:
        """WCAG 1.1.1: the decorative background of the fancy style is aria-hidden."""
        soup = self.render_page_header(style="fancy")
        hidden = soup.select('[aria-hidden="true"]')
        assert hidden, "fancy style must hide its decorative graphic from assistive technology"
        assert not any(node.find(["a", "button", "input"]) for node in hidden)
