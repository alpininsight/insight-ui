"""Tests for the status_screen component."""

import pytest
from bs4 import BeautifulSoup
from insight_ui.configs.input import ButtonConfig
from insight_ui.configs.utils import StatusScreenConfig

from tests.unit.components.test_template_tags import TemplateTagsTestCase


class TestStatusScreen(TemplateTagsTestCase):
    """Test suite for the status_screen component."""

    def test_status_screen_renders_tokenized_surface(self) -> None:
        """The status card uses semantic Insight UI surface tokens."""
        rendered = self.render_template(
            """
            {% load insight_tags %}
            {% status_screen title="Ready" description="Everything is prepared." status="success" %}
            """
        )
        soup = BeautifulSoup(rendered, "html.parser")

        card = soup.select_one(".insight-surface-raised")
        assert card is not None
        classes = card.get("class", [])
        assert "insight-border-subtle" in classes
        assert "insight-radius-raised" in classes
        assert "insight-shadow-raised" in classes
        assert "bg-white" not in classes
        assert "border-gray-200" not in classes
        assert "rounded-lg" not in classes
        assert "shadow-lg" not in classes

    def test_status_screen_renders_dict_config_actions_as_buttons(self) -> None:
        """Nested action dictionaries are coerced to ButtonConfig instances."""
        rendered = self.render_template(
            "{% load insight_tags %}{% status_screen config=cfg %}",
            context={
                "cfg": {
                    "title": "Sign-in failed",
                    "description": "Try again.",
                    "status": "error",
                    "primary_action": {"label": "Retry", "request_url": "/login/", "type": "primary"},
                    "secondary_action": {"label": "Support", "request_url": "/support/", "type": "secondary"},
                }
            },
        )
        soup = BeautifulSoup(rendered, "html.parser")

        retry = soup.find("a", href="/login/")
        support = soup.find("a", href="/support/")
        assert retry is not None
        assert support is not None
        assert "btn-primary" in retry.get("class", [])
        assert "btn-secondary" in support.get("class", [])

    def test_status_screen_disabled_action_renders_disabled_button(self) -> None:
        """Disabled actions are rendered as disabled buttons, not as navigable links."""
        rendered = self.render_template(
            "{% load insight_tags %}{% status_screen config=cfg %}",
            context={
                "cfg": StatusScreenConfig(
                    title="Deployment running",
                    status="info",
                    primary_action=ButtonConfig(label="Continue", request_url="/next/", type="disabled"),
                )
            },
        )
        soup = BeautifulSoup(rendered, "html.parser")

        href = soup.find("a", disabled=True)
        assert href is not None
        assert "btn-disabled" in href.get("class", [])

    def test_status_screen_error_notice_uses_alert_role(self) -> None:
        """Error notices use alert semantics and a semantic danger border."""
        rendered = self.render_template(
            """
            {% load insight_tags %}
            {% status_screen title="Failed" status="error" notice_title="Reason" notice="OIDC failed." %}
            """
        )
        soup = BeautifulSoup(rendered, "html.parser")

        notice = soup.find(role="alert")
        assert notice is not None
        assert "border-s-insight-danger" in notice.get("class", [])
        assert "insight-surface-muted" in notice.get("class", [])

    def test_status_screen_rejects_unknown_status(self) -> None:
        """Unknown status values fail early instead of rendering broken classes."""
        with pytest.raises(ValueError, match="status_screen status must be one of"):
            self.render_template(
                """
                {% load insight_tags %}
                {% status_screen title="Unknown" status="unknown" %}
                """
            )
