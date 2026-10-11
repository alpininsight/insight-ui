# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the optional Turnstile component and form integration."""

import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template
from insight_ui.configs import FormConfig, HtmxConfig, TurnstileConfig


def render(template: str, **context: object) -> BeautifulSoup:
    """Render an Insight UI template tag for assertions."""
    html = Template("{% load insight_tags %}" + template).render(Context(context))
    return BeautifulSoup(html, "html.parser")


def test_turnstile_tag_renders_only_public_widget_configuration() -> None:
    """Never put a server secret or a vendor script URL in the widget markup."""
    soup = render(
        "{% turnstile config=challenge %}",
        challenge=TurnstileConfig(site_key="public-site-key", theme="dark", size="compact", action="contact"),
    )
    widget = soup.select_one("[data-insight-turnstile]")

    assert widget is not None
    assert widget["data-sitekey"] == "public-site-key"
    assert widget["data-theme"] == "dark"
    assert widget["data-size"] == "compact"
    assert widget["data-action"] == "contact"
    assert widget.select_one("[data-insight-turnstile-widget]") is not None
    assert widget.select_one("[data-insight-turnstile-error][role=alert]") is not None
    assert soup.select_one("script") is None


def test_form_renders_optional_challenge_inside_the_post_form() -> None:
    """A configured challenge is part of the submitted form, not a visual sibling."""
    config = FormConfig(tag_id="contact", turnstile=TurnstileConfig(site_key="public-site-key"))
    soup = render("{% form config=config %}", config=config)

    assert soup.select_one("form[method=post] [data-insight-turnstile]") is not None
    assert soup.select_one("form [data-insight-turnstile] [data-insight-turnstile-widget]") is not None
    assert soup.select_one("form button[type=submit]") is not None


def test_form_without_challenge_does_not_load_or_render_turnstile() -> None:
    """Existing and private forms remain unchanged by default."""
    soup = render("{% form config=config %}", config=FormConfig())

    assert soup.select_one("[data-insight-turnstile]") is None


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"site_key": ""}, "site_key"),
        ({"site_key": "public", "theme": "invalid"}, "theme"),
        ({"site_key": "public", "size": "invalid"}, "size"),
        ({"site_key": "public", "action": "contains spaces"}, "action"),
        ({"site_key": "public", "action": "x" * 33}, "action"),
    ],
)
def test_turnstile_config_rejects_invalid_options(kwargs: dict[str, str], message: str) -> None:
    """Invalid vendor options fail before rendering the page."""
    with pytest.raises(ValueError, match=message):
        TurnstileConfig(**kwargs)


def test_protected_form_rejects_get_method() -> None:
    """Tokens must never be sent in URLs, including HTMX GET submissions."""
    challenge = TurnstileConfig(site_key="public")
    with pytest.raises(ValueError, match="POST"):
        FormConfig(method="get", turnstile=challenge)
    with pytest.raises(ValueError, match="POST"):
        FormConfig(htmx_config=HtmxConfig(request_url="/submit/", method="get"), turnstile=challenge)


def test_protected_form_accepts_htmx_post() -> None:
    """The challenge works with HTMX as long as the request method is POST."""
    config = FormConfig(
        htmx_config=HtmxConfig(request_url="/submit/", method="post"),
        turnstile=TurnstileConfig(site_key="public"),
    )

    assert render("{% form config=config %}", config=config).select_one("form[hx-post] [data-insight-turnstile]")
