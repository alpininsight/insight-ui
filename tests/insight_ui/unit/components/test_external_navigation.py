# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""External navigation retains the native browser action alongside shared HTMX options."""

import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template
from insight_ui.configs import FooterConfig, HtmxConfig, NavbarConfig, NavbarLinkConfig


@pytest.mark.parametrize(("tag", "config_class"), [("navbar", NavbarConfig), ("footer", FooterConfig)])
@pytest.mark.parametrize("external", [False, True])
def test_native_external_link_is_not_intercepted_by_htmx(tag: str, config_class: type, external: bool) -> None:
    """A new-tab announcement matches native navigation; internal links retain their enhancement."""
    options = HtmxConfig(target="#content")
    link = NavbarLinkConfig(text="Docs", request_url="https://example.com/docs/", external=external, htmx=options)
    rendered = Template("{% load insight_tags %}{% " + tag + " config=config %}").render(
        Context({"config": config_class(links=[link])})
    )
    anchor = BeautifulSoup(rendered, "html.parser").find("a", href="https://example.com/docs/")
    if external:
        assert anchor["target"] == "_blank"
        assert "noopener" in anchor["rel"]
        assert "opens in a new tab" in anchor.get_text()
        assert not any(name.startswith("hx-") for name in anchor.attrs)
    else:
        assert anchor["hx-get"] == "https://example.com/docs/"
        assert anchor["hx-target"] == "#content"
    assert link.htmx is options
    assert options.target == "#content"
