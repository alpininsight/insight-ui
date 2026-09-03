"""Tests for the infinite_scroll component."""

import pytest
from insight_ui.configs import InfiniteScrollConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestInfiniteScroll(TemplateTagsTestCase):
    """Test suite for the infinite_scroll component."""

    def test_infinite_scroll_basic(self) -> None:
        """Test für grundlegende infinite_scroll Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% infinite_scroll request_url="/api/more-items/" %}
        """
        rendered = self.render_template(template_string)
        assert "/api/more-items/" in rendered

    def test_infinite_scroll_config_requires_request_url(self) -> None:
        """InfiniteScrollConfig requires request_url."""
        with pytest.raises(TypeError):
            InfiniteScrollConfig()  # type: ignore[call-arg]
