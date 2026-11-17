# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the stepper component."""

from bs4 import BeautifulSoup
from insight_ui.configs import StepperConfig, StepperItemConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestStepper(TemplateTagsTestCase):
    """Test suite for the stepper component."""

    def test_stepper_keeps_connectors_inside_list_items(self) -> None:
        """The ordered list contains only list items, including visual connectors."""
        config = StepperConfig(
            items=[
                StepperItemConfig(title="Address", status="completed"),
                StepperItemConfig(title="Review"),
            ]
        )

        rendered = self.render_template("{% load insight_tags %}{% stepper config %}", {"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        stepper = soup.find("ol")
        children = [child for child in stepper.children if getattr(child, "name", None)]
        assert all(child.name == "li" for child in children)
        assert len(children) == len(config.items) + (len(config.items) - 1)

    def test_pending_step_uses_readable_muted_text(self) -> None:
        """Pending labels are informational content, not disabled controls."""
        config = StepperConfig(items=[StepperItemConfig(title="Review", description="Check the data")])

        rendered = self.render_template("{% load insight_tags %}{% stepper config %}", {"config": config})

        assert "text-insight-muted" in rendered
        assert "text-insight-disabled" not in rendered

    def test_current_step_is_marked_for_assistive_technology(self) -> None:
        """Only the current step carries aria-current."""
        config = StepperConfig(
            items=[
                StepperItemConfig(title="Address", status="completed"),
                StepperItemConfig(title="Payment", status="current"),
                StepperItemConfig(title="Review"),
            ]
        )

        rendered = self.render_template("{% load insight_tags %}{% stepper config %}", {"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        current = soup.find_all("li", attrs={"aria-current": "step"})
        assert len(current) == 1
        assert "Payment" in current[0].get_text()

    def test_failed_step_shows_its_title_and_description(self) -> None:
        """A failed step keeps its content visible."""
        config = StepperConfig(items=[StepperItemConfig(title="Payment", description="Card declined", status="failed")])

        rendered = self.render_template("{% load insight_tags %}{% stepper config %}", {"config": config})

        assert "Payment" in rendered
        assert "Card declined" in rendered
        assert 'aria-current="step"' not in rendered
