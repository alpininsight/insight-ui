"""Tests for the brand_mark component."""

from bs4 import BeautifulSoup

from tests.unit.components.test_template_tags import TemplateTagsTestCase


class TestBrandMark(TemplateTagsTestCase):
    """Test suite for the brand_mark component."""

    def test_brand_mark_defaults(self) -> None:
        """Default render carries the Alpin Insight wordmark + public icon."""
        rendered = self.render_template("{% load insight_tags %}{% brand_mark %}")
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

    def test_brand_mark_logo_position_start_is_default(self) -> None:
        """Default position keeps the group left-aligned (no justify-between)."""
        rendered = self.render_template("{% load insight_tags %}{% brand_mark %}")
        root = BeautifulSoup(rendered, "html.parser").find("div")
        assert "justify-between" not in root.get("class", [])

    def test_brand_mark_logo_position_end_pushes_logo_to_edge(self) -> None:
        """Position 'end' left-aligns the wordmark and pushes the logo out."""
        rendered = self.render_template('{% load insight_tags %}{% brand_mark logo_position="end" %}')
        root = BeautifulSoup(rendered, "html.parser").find("div")
        assert "justify-between" in root.get("class", [])

    def test_brand_mark_custom_text(self) -> None:
        """primary_text / secondary_text override the wordmark runs."""
        rendered = self.render_template(
            '{% load insight_tags %}{% brand_mark primary_text="Foo Bar" secondary_text="Cloud" %}'
        )
        assert "Foo Bar" in rendered
        assert "Cloud" in rendered

    def test_brand_mark_config_dict(self) -> None:
        """A config dict configures the mark (mirrors the logo tag style)."""
        rendered = self.render_template(
            "{% load insight_tags %}{% brand_mark config=cfg %}", context={"cfg": {"logo_position": "end"}}
        )
        root = BeautifulSoup(rendered, "html.parser").find("div")
        assert "justify-between" in root.get("class", [])
        assert "order: 2" in rendered

    def test_brand_mark_default_variant_uses_app_icon(self) -> None:
        """Default renders the public app icon."""
        rendered = self.render_template("{% load insight_tags %}{% brand_mark %}")
        svg = BeautifulSoup(rendered, "html.parser").find("svg")
        assert svg.get("viewbox") == "0 0 24 24"
        assert "M2.25 6a3 3" in rendered

    def test_brand_mark_develop_variant_uses_rocket_icon(self) -> None:
        """Develop renders the public rocket icon."""
        rendered = self.render_template('{% load insight_tags %}{% brand_mark variant="develop" %}')
        svg = BeautifulSoup(rendered, "html.parser").find("svg")
        assert svg.get("viewbox") == "0 0 24 24"
        assert "M15.59 14.37" in rendered

    def test_brand_mark_candidate_variant_uses_sparkles_icon(self) -> None:
        """Candidate renders the public sparkles icon."""
        rendered = self.render_template('{% load insight_tags %}{% brand_mark variant="candidate" %}')
        assert "M9.813 15.904" in rendered

    def test_brand_mark_unknown_variant_falls_back_to_main_icon(self) -> None:
        """An unknown variant falls back to the public app icon, not an empty SVG."""
        rendered = self.render_template('{% load insight_tags %}{% brand_mark variant="bogus" %}')
        svg = BeautifulSoup(rendered, "html.parser").find("svg")
        assert svg is not None
        assert "M2.25 6a3 3" in rendered

    def test_brand_mark_variant_via_config(self) -> None:
        """Variant is configurable through the config dict too."""
        rendered = self.render_template(
            "{% load insight_tags %}{% brand_mark config=cfg %}", context={"cfg": {"variant": "develop"}}
        )
        assert "M15.59 14.37" in rendered

    def test_brand_mark_preserves_positional_height_argument(self) -> None:
        """The fourth positional argument remains accepted for backwards compatibility."""
        rendered = self.render_template(
            '{% load insight_tags %}{% brand_mark "Alpin Insight" "Develop" "start" "2.5rem" %}'
        )
        svg = BeautifulSoup(rendered, "html.parser").find("svg")
        assert "Alpin Insight" in rendered
        assert "Develop" in rendered
        assert svg.get("viewbox") == "0 0 24 24"
