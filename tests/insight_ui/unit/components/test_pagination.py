# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the pagination component."""

import warnings

import pytest
from bs4 import BeautifulSoup
from django.core.paginator import Paginator
from django.template import Context, Template
from insight_ui.configs import HtmxConfig, PaginationConfig, PaginationIppConfig


def render_pagination(page_number: int = 2, total: int = 30, **options: object) -> BeautifulSoup:
    """Render the pagination with 10 items per page, turning warnings into errors like strict hosts do."""
    options.setdefault("request_url", "/items/")
    page = Paginator(range(total), 10).get_page(page_number)
    config = PaginationConfig(current_page=page, **options)  # type: ignore[arg-type]

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        rendered = Template("{% load insight_tags %}{% pagination config %}").render(Context({"config": config}))
    return BeautifulSoup(rendered, "html.parser")


def page_links(soup: BeautifulSoup) -> dict[str, str]:
    """Return the page number links as {visible number: href}."""
    return {a.get_text(strip=True): a["href"] for a in soup.select("nav a[href]") if a.get_text(strip=True).isdigit()}


@pytest.mark.parametrize(
    ("page_number", "direction", "disabled_label"),
    [
        pytest.param(
            1,
            "previous",
            "To previous page (Deactivated because there are no more previous pages)",
            id="first-page",
        ),
        pytest.param(
            3,
            "next",
            "To next page (Deactivated because there are no more next pages)",
            id="last-page",
        ),
    ],
)
def test_disabled_page_button_keeps_its_id(page_number: int, direction: str, disabled_label: str) -> None:
    """Boundary buttons keep their focus-restoration ID and explain why they are disabled."""
    soup = render_pagination(page_number)

    button = soup.find(attrs={"aria-label": disabled_label})
    assert button is not None
    assert button["id"] == f"pagination-{direction}"
    assert button.has_attr("disabled")
    assert button["data-insight-tooltip"] == disabled_label


def test_middle_page_has_no_disabled_buttons() -> None:
    """Between the first and last page both directions are available."""
    soup = render_pagination(2)

    assert soup.select("nav.pagination [disabled]") == []


def test_links_keep_the_query_string_of_the_request_url() -> None:
    """Filters in request_url survive paging, and an existing page parameter is replaced."""
    soup = render_pagination(2, request_url="/search/?q=chair&page=7&country=de")

    assert page_links(soup)["3"] == "/search/?q=chair&country=de&page=3"
    assert soup.find("a", attrs={"aria-label": "To next page"})["href"] == "/search/?q=chair&country=de&page=3"


def test_page_parameter_name_is_configurable() -> None:
    """Hosts with their own parameter name need no alias."""
    soup = render_pagination(2, request_url="/search/", page_param="filter_page")

    assert page_links(soup)["1"] == "/search/?filter_page=1"


def test_long_ranges_are_shortened_with_an_ellipsis() -> None:
    """Django's elided page range keeps the start, the end and the neighbors of the current page."""
    soup = render_pagination(25, total=500)

    assert list(page_links(soup)) == ["1", "23", "24", "26", "27", "50"]
    assert [span.get_text() for span in soup.select("nav span[aria-hidden=true]") if span.get_text() == "…"] == [
        "…",
        "…",
    ]


def test_on_each_side_and_on_ends_control_the_range() -> None:
    """The number of neighbors and end pages can be set."""
    soup = render_pagination(25, total=500, on_each_side=1, on_ends=2)

    assert list(page_links(soup)) == ["1", "2", "24", "26", "49", "50"]


def test_page_links_have_a_spoken_label_and_mark_the_current_page() -> None:
    """Screen readers hear "Page 3" instead of a bare number; the current page is marked."""
    soup = render_pagination(2)

    assert soup.find("a", string=lambda text: text and text.strip() == "3")["aria-label"] == "Page 3"
    current = soup.find(attrs={"aria-current": "page"})
    assert current.get_text(" ", strip=True).startswith("Page 2")


def test_without_htmx_the_links_load_the_whole_page() -> None:
    """No hidden target: without an HtmxConfig the pagination works on any page."""
    soup = render_pagination(2)

    assert soup.find(attrs={"hx-get": True}) is None
    assert soup.find(attrs={"hx-target": True}) is None


def test_htmx_config_drives_the_page_links() -> None:
    """Target, push_url and the link URL come from the HtmxConfig and the page links."""
    soup = render_pagination(2, htmx=HtmxConfig(target="#results", push_url=True))
    link = soup.find("a", attrs={"aria-label": "Page 3"})

    assert link["hx-get"] == link["href"] == "/items/?page=3"
    assert link["hx-target"] == "#results"
    assert link["hx-push-url"] == "true"


@pytest.mark.parametrize("target", ["", "   "])
def test_htmx_config_requires_a_target(target: str) -> None:
    """An HTMX pagination must not replace only the clicked link with the list response."""
    with pytest.raises(ValueError, match=r"PaginationConfig\.htmx needs a target"):
        render_pagination(2, htmx=HtmxConfig(target=target))


def test_include_sends_filters_and_the_page_size_with_htmx_requests() -> None:
    """hx-include on the nav is inherited by links and the page size form."""
    soup = render_pagination(
        2, htmx=HtmxConfig(target="#results"), include="#filters", items_per_page=PaginationIppConfig(options=[10, 25])
    )

    assert soup.find("nav")["hx-include"] == "#pagination-ipp, #filters"


def test_page_size_selector_renders_its_options() -> None:
    """The selector shows every option and the selected one."""
    soup = render_pagination(2, items_per_page=PaginationIppConfig(options=[10, 25, 50], selected_option=25))
    options = soup.select("#pagination-ipp select option")

    assert [option["value"] for option in options] == ["10", "25", "50"]
    assert [option["value"] for option in options if option.has_attr("selected")] == ["25"]


def test_page_size_form_keeps_filters_and_starts_at_page_one() -> None:
    """Without HTMX the form submits normally: filters as hidden fields, no page number, an apply button."""
    soup = render_pagination(
        2, request_url="/search/?q=chair&page=2&ipp=10", items_per_page=PaginationIppConfig(options=[10, 25])
    )
    form = soup.find("form", id="pagination-ipp")

    assert form["action"] == "/search/"
    assert {(i["name"], i["value"]) for i in form.find_all("input", type="hidden")} == {("q", "chair")}
    button = form.find("button", type="submit")
    assert button is not None
    assert "btn-secondary" in button["class"]


def test_page_size_form_reloads_on_change_with_htmx() -> None:
    """With HTMX the selector applies itself; no extra button."""
    soup = render_pagination(
        2, htmx=HtmxConfig(target="#results"), items_per_page=PaginationIppConfig(options=[10, 25])
    )
    form = soup.find("form", id="pagination-ipp")

    assert form["hx-get"] == "/items/"
    assert form["hx-trigger"] == "change"
    assert form.find("button", type="submit") is None


def test_two_paginations_have_distinct_ids() -> None:
    """tag_id prefixes the ids, so two paginations can share a page."""
    ipp = PaginationIppConfig(options=[10, 25])
    ids = [
        element["id"]
        for tag_id in ("top", "bottom")
        for element in render_pagination(2, tag_id=tag_id, items_per_page=ipp).find_all(id=True)
    ]

    assert len(ids) == len(set(ids))


@pytest.mark.parametrize("field", ["request_url", "tag_id", "page_param"])
def test_identifying_fields_must_not_be_empty(field: str) -> None:
    """Empty values would produce broken URLs or duplicate ids."""
    with pytest.raises(ValueError, match=field):
        render_pagination(2, **{field: ""})


def test_ids_stay_the_same_across_pages_so_htmx_can_restore_the_focus() -> None:
    """The link of page 3 and the current-page marker of page 3 share an id; previous/next keep theirs."""
    htmx = HtmxConfig(target="#results")
    before = render_pagination(2, total=50, htmx=htmx)
    after = render_pagination(3, total=50, htmx=htmx)

    assert before.find(id="pagination-page-3").name == "a"
    marker = after.find(id="pagination-page-3")
    assert marker["aria-current"] == "page"
    assert marker["tabindex"] == "-1"
    for direction in ("previous", "next"):
        assert before.find(id=f"pagination-{direction}") is not None
        assert after.find(id=f"pagination-{direction}") is not None
