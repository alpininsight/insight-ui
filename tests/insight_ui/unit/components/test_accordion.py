# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the accordion component."""

import pytest
from insight_ui.configs import AccordionConfig, AccordionItemConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase

# TODO: Implement tests for Accordion component  # noqa: TD002, TD003


class TestAccordion(TemplateTagsTestCase):
    """Test suite for the accordion component."""

    def test_accordion_config_requires_tag_id(self) -> None:
        """AccordionConfig requires tag_id (avoids duplicate IDs across instances)."""
        with pytest.raises(TypeError):
            AccordionConfig(items=[AccordionItemConfig(title="Q", content="A")])  # type: ignore[call-arg]
