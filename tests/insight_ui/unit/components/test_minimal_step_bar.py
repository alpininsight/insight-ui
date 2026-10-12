# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the minimal_stepper component."""

from bs4 import BeautifulSoup
from insight_ui.configs import STEP_STATUS_VALUES, MinimalStepperConfig

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

    def test_minimal_stepper_renders_an_icon_for_every_step_status(self) -> None:
        """Every status renders its icon, so an unknown icon name for any status fails here."""
        config = MinimalStepperConfig(items=list(STEP_STATUS_VALUES))

        rendered = self.render_template("{% load insight_tags %}{% minimal_stepper config %}", {"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        steps = soup.find("ol", {"aria-label": "Progress indicator"}).find_all("li", recursive=False)
        assert len(steps) == len(STEP_STATUS_VALUES)
        for status, step in zip(STEP_STATUS_VALUES, steps, strict=True):
            assert step.find("svg") is not None, f"No icon rendered for status {status!r}"
