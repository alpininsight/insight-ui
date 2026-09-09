# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the alert component."""

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestAlert(TemplateTagsTestCase):
    """Test suite for the alert component."""

    def test_alert_basic(self) -> None:
        """Test für grundlegende alert Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% alert message="Test message" %}
        """
        rendered = self.render_template(template_string)
        assert "Test message" in rendered

    def test_alert_types(self) -> None:
        """Test für verschiedene alert Typen."""
        for alert_type in ["info", "success", "warning", "error"]:
            with self.subTest(type=alert_type):
                template_string = f"""
                {{% load insight_tags %}}
                {{% alert message="Test message" type="{alert_type}" %}}
                """
                rendered = self.render_template(template_string)
                assert "Test message" in rendered
