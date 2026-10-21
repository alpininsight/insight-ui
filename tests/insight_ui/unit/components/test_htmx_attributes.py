# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the shared HTMX attribute renderer and the components that use it."""

import json
import re
from dataclasses import replace
from pathlib import Path

import pytest
from bs4 import BeautifulSoup, Tag
from django.template import Context, Template
from insight_ui.configs import (
    BreadcrumbItemConfig,
    BreadcrumbsConfig,
    ButtonConfig,
    DropdownConfig,
    DropdownItemConfig,
    FormConfig,
    GenericFilterConfig,
    HtmxConfig,
    SearchBarConfig,
)

import insight_ui

TEMPLATES = Path(insight_ui.__file__).parent / "templates"

FULL_CONFIG = HtmxConfig(
    request_url="/save/",
    method="post",
    target="#result",
    swap_method="outerHTML",
    swap_settle="300ms",
    push_url=True,
    loading_indicator_id="#spinner",
    confirm="Sure?",
    vals={"source": "test"},
    show_global_loading_indicator=False,
)


def render(template: str, context: dict | None = None) -> BeautifulSoup:
    """Render a template string that uses insight_tags and parse the result."""
    return BeautifulSoup(Template("{% load insight_tags %}" + template).render(Context(context or {})), "html.parser")


def attributes(arguments: str = "", htmx: HtmxConfig | None = FULL_CONFIG) -> dict[str, str]:
    """Render the HTMX attributes on a dummy element and return them."""
    element = render(f"<div {{% htmx_attributes htmx {arguments} %}}></div>", {"htmx": htmx}).div
    return dict(element.attrs)


# --- Renderer -----------------------------------------------------------


def test_all_config_fields_are_rendered() -> None:
    """Every request option of the config reaches the HTML."""
    assert attributes() == {
        "hx-post": "/save/",
        "hx-target": "#result",
        "hx-swap": "outerHTML settle:300ms",
        "hx-push-url": "true",
        "hx-indicator": "#spinner",
        "hx-confirm": "Sure?",
        "hx-vals": json.dumps({"source": "test"}, separators=(",", ":")),
        "data-insight-global-indicator": "false",
    }


def test_unset_options_are_left_out() -> None:
    """Without values, only the request and the swap method are rendered; no trigger overrides the HTMX default."""
    assert attributes(htmx=HtmxConfig(request_url="/items/")) == {"hx-get": "/items/", "hx-swap": "innerHTML"}


def test_no_config_renders_nothing() -> None:
    """Components can call the renderer unconditionally."""
    assert attributes(htmx=None) == {}


def test_component_values_take_precedence() -> None:
    """Values the component fixes or derives win over the config."""
    rendered = attributes(
        'request_url="/item/7/" method="get" target="#own" swap="beforeend" trigger="submit" '
        'indicator="find .htmx-indicator" push_url=False swap_modifiers="show:window:top" global_indicator=True'
    )

    assert rendered["hx-get"] == "/item/7/"
    assert "hx-post" not in rendered
    assert rendered["hx-target"] == "#own"
    assert rendered["hx-trigger"] == "submit"
    assert rendered["hx-indicator"] == "find .htmx-indicator"
    assert "hx-push-url" not in rendered
    assert rendered["hx-swap"] == "beforeend settle:300ms show:window:top"
    # An explicit config value wins over the component default.
    assert rendered["data-insight-global-indicator"] == "false"


@pytest.mark.parametrize(
    ("config_value", "component_default", "shown"),
    [
        pytest.param(None, True, True, id="default-shown"),
        pytest.param(None, False, False, id="background-request-hidden"),
        pytest.param(True, False, True, id="config-opts-in"),
        pytest.param(False, True, False, id="config-opts-out"),
    ],
)
def test_global_loading_bar_falls_back_to_the_component_default(
    config_value: bool | None, component_default: bool, shown: bool
) -> None:
    """Without a value in the config, the component decides whether the global bar shows."""
    htmx = HtmxConfig(request_url="/items/", show_global_loading_indicator=config_value)
    rendered = attributes(f"global_indicator={component_default}", htmx=htmx)

    assert ("data-insight-global-indicator" not in rendered) is shown


def test_values_are_escaped() -> None:
    """Config values cannot break out of the attribute."""
    element = render(
        "<div {% htmx_attributes htmx %}></div>", {"htmx": HtmxConfig(request_url='/x" onclick="alert(1)')}
    ).div

    assert element["hx-get"] == '/x" onclick="alert(1)'
    assert not element.has_attr("onclick")


def test_templates_render_htmx_configs_only_through_the_renderer() -> None:
    """Hand-written attributes drifted apart before (e.g. reading a non-existent htmx.swap), so none are left."""
    field_access = re.compile(
        r"\b(?:htmx_config|htmx)\.(?:request_url|method|target|swap\w*|push_url|loading_indicator_id|indicator|"
        r"confirm|vals|trigger|show_global_loading_indicator)\b"
    )
    offenders = [
        f"{path.relative_to(TEMPLATES)}:{number}"
        for path in TEMPLATES.rglob("*.html")
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1)
        if field_access.search(line) and "htmx_attributes" not in line
    ]

    assert offenders == []


# --- Components ---------------------------------------------------------


def find_requesting_element(soup: BeautifulSoup) -> Tag:
    """Return the element that sends the HTMX request."""
    return soup.find(lambda tag: any(name in tag.attrs for name in ("hx-get", "hx-post")))


@pytest.mark.parametrize(
    ("template", "context"),
    [
        pytest.param("{% button config=c %}", {"c": ButtonConfig(label="Save", htmx_config=FULL_CONFIG)}, id="button"),
        pytest.param(
            "{% button config=c %}",
            {"c": ButtonConfig(label="Save", request_url="/save/", htmx_config=replace(FULL_CONFIG, request_url=""))},
            id="link-button",
        ),
        pytest.param("{% form config=c %}", {"c": FormConfig(tag_id="f", htmx_config=FULL_CONFIG)}, id="form"),
        pytest.param("{% search_bar config=c %}", {"c": SearchBarConfig(htmx_config=FULL_CONFIG)}, id="search-bar"),
        pytest.param(
            "{% dropdown c %}",
            {
                "c": DropdownConfig(
                    tag_id="menu", title="Menu", items=[DropdownItemConfig("Edit", "/edit/", htmx=FULL_CONFIG)]
                )
            },
            id="dropdown",
        ),
    ],
)
def test_components_render_the_shared_request_options(template: str, context: dict) -> None:
    """Components pass their HtmxConfig through the renderer, so shared options like confirm reach the HTML."""
    element = find_requesting_element(render(template, context))

    assert element["hx-target"] == "#result"
    assert element["hx-confirm"] == "Sure?"
    assert element["data-insight-global-indicator"] == "false"


def test_link_button_requests_its_href() -> None:
    """A link button without its own HTMX URL requests the URL of the link, like the navigation links."""
    config = ButtonConfig(label="Docs", request_url="/docs/", htmx_config=HtmxConfig(target="#main"))
    link = render("{% button config=c %}", {"c": config}).a

    assert link["href"] == "/docs/"
    assert link["hx-get"] == "/docs/"


def test_button_without_trigger_uses_the_click_default() -> None:
    """Buttons no longer get trigger="submit" from the config, which never fired on a button."""
    button = render("{% button config=c %}", {"c": ButtonConfig(label="Load", htmx_config=HtmxConfig("/items/"))})

    assert not button.find("button").has_attr("hx-trigger")


def test_form_fixes_its_trigger_and_indicator() -> None:
    """The form always submits on submit and shows only its own indicator."""
    form = render("{% form config=c %}", {"c": FormConfig(tag_id="f", htmx_config=HtmxConfig("/save/"))}).form

    assert form["hx-trigger"] == "submit"
    assert form["hx-indicator"] == "find .htmx-indicator"


def test_search_bar_sends_on_submit_only() -> None:
    """The search runs on the search button and Return, the default trigger of its form."""
    element = find_requesting_element(
        render("{% search_bar config=c %}", {"c": SearchBarConfig(htmx_config=HtmxConfig("/search/"))})
    )

    assert element.name == "form"
    assert not element.has_attr("hx-trigger")


def test_breadcrumbs_request_their_own_item_urls() -> None:
    """Each breadcrumb requests its own URL with the shared target and swap."""
    config = BreadcrumbsConfig(
        items=[BreadcrumbItemConfig("Home", "/"), BreadcrumbItemConfig("Docs", "/docs/"), BreadcrumbItemConfig("Now")],
        htmx=HtmxConfig(target="#main"),
    )
    links = render("{% breadcrumbs config=c %}", {"c": config}).find_all("a")

    assert [link["hx-get"] for link in links] == ["/", "/docs/"]
    assert all(link["hx-target"] == "#main" for link in links)


def test_generic_filter_keeps_its_fixed_trigger_and_history_entry() -> None:
    """Filters send on submit and change and always update the browser URL."""
    config = GenericFilterConfig(request_url="/orders/", htmx_config=HtmxConfig(target="#results"))
    element = find_requesting_element(render("{% generic_filter config=c %}", {"c": config}))

    assert element["hx-get"] == "/orders/"
    assert element["hx-trigger"] == "submit, change"
    assert element["hx-push-url"] == "true"
