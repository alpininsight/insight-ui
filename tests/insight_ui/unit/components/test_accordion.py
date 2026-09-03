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
