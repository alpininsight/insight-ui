# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the web_socket component."""

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestWebSocket(TemplateTagsTestCase):
    """Test suite for the web_socket component."""

    def test_websocket_basic(self) -> None:
        """Test für grundlegende WebSocket Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% websocket request_url="/runtime/stream/" %}
        """
        rendered = self.render_template(template_string)
        assert "/runtime/stream/" in rendered
        assert "data-insight-websocket" in rendered
        assert "data-insight-websocket-status" in rendered
        assert "data-insight-websocket-output" in rendered

    def test_websocket_without_tag_id_does_not_render_broken_ids(self) -> None:
        """Leere tag_id Werte sollten keine unbrauchbaren HTML-IDs erzeugen."""
        template_string = """
        {% load insight_tags %}
        {% websocket request_url="/runtime/stream/" %}
        """
        rendered = self.render_template(template_string)
        assert 'id="-output"' not in rendered
        assert 'id="-status"' not in rendered
