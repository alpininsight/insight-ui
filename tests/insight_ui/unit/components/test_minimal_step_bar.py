# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
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

    def test_minimal_stepper_renders_every_legacy_state_and_icon_size(self) -> None:
        """The patch retains the released items API and renders the failed branch."""
        states = ["success", "failed", "active", ""]
        for icon_size in ("xs", "s", "m", "l", "xl"):
            with self.subTest(icon_size=icon_size):
                config = MinimalStepperConfig(items=states, icon_size=icon_size)
                rendered = self.render_template(
                    "{% load insight_tags %}{% minimal_stepper config %}", {"config": config}
                )
                soup = BeautifulSoup(rendered, "html.parser")
                steps = soup.find("ol", {"aria-label": "Progress indicator"}).find_all("li", recursive=False)

                assert len(steps) == len(states)
                assert steps[2]["aria-current"] == "step"
                assert "Failed" in steps[1]["aria-label"]
                expected = BeautifulSoup(
                    self.render_template(
                        '{% load insight_tags %}{% icon name="x-mark" size=icon_size %}', {"icon_size": icon_size}
                    ),
                    "html.parser",
                ).find("svg")
                assert str(steps[1].find("svg")) == str(expected)
                assert all(step.find("svg") is not None for step in steps)
