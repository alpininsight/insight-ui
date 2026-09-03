"""Tests for the live_content component."""

import pytest
from insight_ui.configs import LiveContentConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestLiveContent(TemplateTagsTestCase):
    """Test suite for the live_content component."""

    def test_live_content_basic(self) -> None:
        """Test für grundlegende live_content Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% live_content request_url="/api/live-data/" %}
        """
        rendered = self.render_template(template_string)
        assert "/api/live-data/" in rendered

    def test_live_content_config_requires_request_url(self) -> None:
        """LiveContentConfig requires request_url."""
        with pytest.raises(TypeError):
            LiveContentConfig()  # type: ignore[call-arg]

    def test_live_content_with_interval(self) -> None:
        """Test für live_content mit Intervall."""
        template_string = """
        {% load insight_tags %}
        {% live_content request_url="/api/live-data/" interval=5000 %}
        """
        rendered = self.render_template(template_string)
        assert "/api/live-data/" in rendered
