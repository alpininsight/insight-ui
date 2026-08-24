"""Tests for the button component."""

import json

from bs4 import BeautifulSoup
from insight_ui.configs import ButtonConfig, HtmxConfig

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

    def test_button_serializes_htmx_vals_as_json(self) -> None:
        """Button and anchor variants preserve typed additional HTMX values."""
        vals = {"parleq_id": "de--1", "tracked": False}
        htmx_config = HtmxConfig(request_url="/track/", target="#result", method="post", vals=vals)
        configs = (
            (ButtonConfig(label="Track", htmx_config=htmx_config), "button"),
            (ButtonConfig(label="Track", request_url="/track/", htmx_config=htmx_config), "a"),
        )

        for config, element_name in configs:
            rendered = self.render_template(
                "{% load insight_tags %}{% button config=config %}",
                {"config": config},
            )
            element = BeautifulSoup(rendered, "html.parser").find(element_name)

            assert element is not None
            assert json.loads(element["hx-vals"]) == vals
