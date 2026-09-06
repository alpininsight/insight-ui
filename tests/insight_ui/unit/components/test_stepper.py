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
                StepperItemConfig(title="Address", success=True),
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
