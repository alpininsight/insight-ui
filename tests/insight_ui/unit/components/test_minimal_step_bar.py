# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the minimal_stepper component."""

import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template
from django.utils.translation import override
from insight_ui.configs import STEP_STATUS_VALUES, MinimalStepperConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase

# TODO: Implement tests for MinimalStepBar component  # noqa: TD002, TD003


class TestMinimalStepBar(TemplateTagsTestCase):
    """Test suite for the minimal_stepper component."""

    def test_minimal_stepper_uses_list_items_for_progress_steps(self) -> None:
        """Progress state is exposed with list semantics, not ARIA on generic divs."""
        config = MinimalStepperConfig(steps=["completed", "current", "pending"])

        rendered = self.render_template("{% load insight_tags %}{% minimal_stepper config %}", {"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        progress = soup.find("ol", {"aria-label": "Progress indicator"})
        items = progress.find_all("li", recursive=False)
        assert len(items) == len(config.steps)
        assert items[1]["aria-current"] == "step"

    def test_minimal_stepper_renders_an_icon_for_every_step_status(self) -> None:
        """Every status renders its icon, so an unknown icon name for any status fails here."""
        config = MinimalStepperConfig(steps=list(STEP_STATUS_VALUES))

        rendered = self.render_template("{% load insight_tags %}{% minimal_stepper config %}", {"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        steps = soup.find("ol", {"aria-label": "Progress indicator"}).find_all("li", recursive=False)
        assert len(steps) == len(STEP_STATUS_VALUES)
        for status, step in zip(STEP_STATUS_VALUES, steps, strict=True):
            assert step.find("svg") is not None, f"No icon rendered for status {status!r}"


@pytest.mark.parametrize("icon_size", ["xs", "s", "m", "l", "xl"])
@pytest.mark.parametrize("mode", ["explicit_steps", "generated_steps"])
def test_failed_step_uses_canonical_x_mark_in_every_supported_size(icon_size: str, mode: str) -> None:
    """Guard both 2.0 status APIs against a wrong but valid failure glyph."""
    config = (
        MinimalStepperConfig(steps=["failed"], icon_size=icon_size)
        if mode == "explicit_steps"
        else MinimalStepperConfig(step_count=3, current_step=2, current_step_status="failed", icon_size=icon_size)
    )
    with override("en"):
        html = Template("{% load insight_tags %}{% minimal_stepper config %}").render(Context({"config": config}))
        canonical = Template('{% load insight_tags %}{% icon name="x-mark" size=icon_size %}').render(
            Context({"icon_size": icon_size})
        )
    failed = BeautifulSoup(html, "html.parser").select_one('li[aria-label$="Failed"] svg')
    expected = BeautifulSoup(canonical, "html.parser").find("svg")
    assert failed is not None
    assert failed["viewbox"] == expected["viewbox"]
    assert failed.parent.name == "span"
    assert failed.parent["class"] == expected.parent["class"]
    assert failed.decode_contents() == expected.decode_contents()
