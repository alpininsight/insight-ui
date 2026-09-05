"""Tests for the minimal_stepper component."""

from bs4 import BeautifulSoup
from insight_ui.configs import MinimalStepperConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase

# TODO: Implement tests for MinimalStepBar component  # noqa: TD002, TD003


class TestMinimalStepBar(TemplateTagsTestCase):
    """Test suite for the minimal_stepper component."""

    def test_minimal_stepper_uses_list_items_for_progress_steps(self) -> None:
        """Progress state is exposed with list semantics, not ARIA on generic divs."""
        config = MinimalStepperConfig(items=["success", "active", ""])

        rendered = self.render_template("{% load insight_tags %}{% minimal_stepper config %}", {"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        progress = soup.find("ol", {"aria-label": "Progress indicator"})
        items = progress.find_all("li", recursive=False)
        assert len(items) == len(config.items)
        assert items[1]["aria-current"] == "step"
