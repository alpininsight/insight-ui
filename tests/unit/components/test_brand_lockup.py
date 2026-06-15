"""Tests for the brand_lockup component."""

# ruff: noqa: E501

from bs4 import BeautifulSoup

from tests.unit.components.test_template_tags import TemplateTagsTestCase


class TestBrandLockup(TemplateTagsTestCase):
    """Test suite for the brand_lockup component."""

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
