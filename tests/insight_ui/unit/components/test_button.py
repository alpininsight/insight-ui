# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the button component."""

import json
import warnings

import pytest
from bs4 import BeautifulSoup, Tag
from django.template import Context, Template
from insight_ui.configs import ButtonConfig, HtmxConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


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
        """Button variant preserves typed additional HTMX values."""
        vals = {"parleq_id": "de--1", "tracked": False}
        htmx = HtmxConfig(request_url="/track/", target="#result", method="post", vals=vals)
        config = ButtonConfig(label="Track", htmx=htmx)

        rendered = self.render_template(
            "{% load insight_tags %}{% button config=config %}",
            {"config": config},
        )
        element = BeautifulSoup(rendered, "html.parser").find("button")

        assert element is not None
        assert json.loads(element["hx-vals"]) == vals

    def test_anchor_serializes_htmx_vals_as_json(self) -> None:
        """Anchor variant preserves typed additional HTMX values."""
        vals = {"parleq_id": "de--1", "tracked": False}
        htmx = HtmxConfig(request_url="/track/", target="#result", method="post", vals=vals)
        config = ButtonConfig(label="Track", request_url="/track/", htmx=htmx)
        rendered = self.render_template("{% load insight_tags %}{% button config=config %}", {"config": config})

        element = BeautifulSoup(rendered, "html.parser").find("a")

        assert element is not None
        assert json.loads(element["hx-vals"]) == vals

    def render_button(self, config: ButtonConfig) -> Tag:
        """Render a button config and return the <a> or <button> element."""
        rendered = self.render_template("{% load insight_tags %}{% button config=config %}", {"config": config})
        return BeautifulSoup(rendered, "html.parser").find(["a", "button"])

    def test_htmx_url_without_link_renders_an_action_button(self) -> None:
        """Only an HTMX URL renders a <button> that sends the request."""
        element = self.render_button(ButtonConfig(label="Save", htmx=HtmxConfig(request_url="/save/")))

        assert element.name == "button"
        assert element["hx-get"] == "/save/"

    def test_link_with_htmx_requests_the_link_url(self) -> None:
        """A link with an HtmxConfig without URL works without JavaScript and loads the same URL via HTMX."""
        config = ButtonConfig(label="Orders", request_url="/orders/", htmx=HtmxConfig(target="#main"))
        element = self.render_button(config)

        assert element.name == "a"
        assert element["href"] == "/orders/"
        assert element["hx-get"] == "/orders/"

    def test_link_can_load_a_separate_htmx_url(self) -> None:
        """A dedicated partial URL is a valid choice: the link opens the full page, HTMX loads the partial."""
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            config = ButtonConfig(
                label="Orders",
                request_url="/orders/",
                htmx=HtmxConfig(request_url="/orders/partial/", target="#main"),
            )
        element = self.render_button(config)

        assert element["href"] == "/orders/"
        assert element["hx-get"] == "/orders/partial/"

    def test_disabled_link_sends_no_request(self) -> None:
        """Browsers do not block clicks on links, so a disabled link has neither href nor HTMX attributes."""
        config = ButtonConfig(
            label="Orders",
            request_url="/orders/",
            disabled=True,
            disabled_reason="",
            htmx=HtmxConfig(target="#main"),
        )
        element = self.render_button(config)

        assert element.name == "a"
        assert element["aria-disabled"] == "true"
        assert not element.has_attr("href")
        assert not any(name.startswith("hx-") for name in element.attrs)

    def test_button_config_requires_label(self) -> None:
        """ButtonConfig requires label (used as visible text or screen-reader name)."""
        with pytest.raises(TypeError):
            ButtonConfig()  # type: ignore[call-arg]

    def test_button_rejects_unknown_parameter_with_invalid_prefix(self) -> None:
        """Button tag raises ValueError for kwargs without valid dynamic prefix."""
        with pytest.raises(ValueError, match=r"Unknown parameter 'lable'.*Only data_\*, aria_\*, hx_\*"):
            self.render_template('{% load insight_tags %}{% button lable="Test" %}')

    def test_button_rejects_unknown_parameter_without_prefix(self) -> None:
        """Button tag raises ValueError for unknown parameters without dynamic prefix."""
        with pytest.raises(ValueError, match=r"Unknown parameter 'foobar'"):
            self.render_template('{% load insight_tags %}{% button label="Test" foobar="xyz" %}')

    def test_button_accepts_valid_dynamic_attributes(self) -> None:
        """Button tag accepts data_*, aria_*, and hx_* dynamic attributes."""
        rendered = self.render_template(
            '{% load insight_tags %}{% button label="Test" data_foo="bar" aria_label="Test" hx_get="/api" %}'
        )
        soup = BeautifulSoup(rendered, "html.parser")
        button = soup.find("button")
        assert button is not None
        assert button.get("data-foo") == "bar"
        assert button.get("aria-label") == "Test"
        assert button.get("hx-get") == "/api"


def render_button(arguments: str) -> Tag:
    """Render a button with the given tag arguments and return its element."""
    html = Template("{% load insight_tags %}{% button " + arguments + " %}").render(Context())
    return BeautifulSoup(html, "html.parser").find(["a", "button"])


def test_external_link_tells_screen_readers_about_the_new_tab() -> None:
    """A new tab is a change of context; the hint is hidden text after the visible label."""
    link = render_button('label="Docs" request_url="https://example.com/" external=True')

    assert link["target"] == "_blank"
    assert link.get_text(" ", strip=True) == "Docs (opens in a new tab)"
    assert link.find("span", class_="sr-only").get_text(strip=True) == "(opens in a new tab)"


def test_external_icon_link_names_the_new_tab() -> None:
    """An icon-only link has its name in aria-label, so the hint goes there."""
    link = render_button('label="Docs" icon_name="arrow-right" icon_only=True request_url="/x/" external=True')

    assert link["aria-label"] == "Docs (opens in a new tab)"


def test_internal_link_has_no_new_tab_hint() -> None:
    """Links that stay in the tab announce only their label."""
    link = render_button('label="Docs" request_url="/docs/"')

    assert link.get_text(" ", strip=True) == "Docs"
