"""Tests for the button component."""

from bs4 import BeautifulSoup

from tests.unit.components.test_template_tags import TemplateTagsTestCase


class TestButton(TemplateTagsTestCase):
    """Test suite for the button component."""

    def test_button_renders_custom_attributes_as_separate_html_attributes(self) -> None:
        """Button tag kwargs should remain valid HTML attributes."""
        rendered = self.render_template(
            "{% load insight_tags %}"
            '{% button label="Open" request_url="/demo/" data_catalog_auth_action="true" '
            'data_insight_modal="hub-login-modal" aria_controls="hub-login-dialog-panel" '
            'hx_get="/dialog/" hx_target="#hub-login-dialog-panel" %}'
        )
        soup = BeautifulSoup(rendered, "html.parser")

        button = soup.find("a", href="/demo/")

        assert button is not None
        assert button["data-catalog-auth-action"] == "true"
        assert button["data-insight-modal"] == "hub-login-modal"
        assert button["aria-controls"] == "hub-login-dialog-panel"
        assert button["hx-get"] == "/dialog/"
        assert button["hx-target"] == "#hub-login-dialog-panel"
