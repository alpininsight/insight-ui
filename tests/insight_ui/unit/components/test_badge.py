# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the badge and badge_list components."""

import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template
from insight_ui.configs import BadgeConfig, BadgeListConfig, HtmxConfig


def render(template: str, context: dict | None = None) -> BeautifulSoup:
    """Render a template string that uses insight_tags and parse the result."""
    rendered = Template("{% load insight_tags %}" + template).render(Context(context or {}))
    return BeautifulSoup(rendered, "html.parser")


def removable_badge(label: str, url: str) -> BadgeConfig:
    """Create a badge that removes itself via a request to the given URL."""
    return BadgeConfig(label, remove_htmx=HtmxConfig(request_url=url, target="#results"))


# --- badge ---------------------------------------------------------------


def test_badge_without_remove_request_has_no_button() -> None:
    """A plain badge stays a non-interactive label."""
    soup = render("{% badge label='New' %}")

    assert soup.select_one(".badge").get_text(strip=True) == "New"
    assert soup.find("button") is None


def test_badge_remove_button_sends_request_on_click() -> None:
    """The remove button names the badge for screen readers and sends the configured request."""
    config = BadgeConfig(
        "Country: Germany",
        remove_htmx=HtmxConfig(request_url="?status=open", target="#results", push_url=True),
    )
    button = render("{% badge config=config %}", {"config": config}).select_one(".badge button")

    assert button["type"] == "button"
    assert button["aria-label"] == "Remove: Country: Germany"
    assert button["hx-get"] == "?status=open"
    assert button["hx-target"] == "#results"
    assert button["hx-push-url"] == "true"
    # HtmxConfig defaults to trigger="submit", which would never fire on a button.
    assert button["hx-trigger"] == "click"
    assert button.has_attr("data-insight-badge-remove")


def test_badge_remove_label_can_be_customized() -> None:
    """The accessible name of the remove button uses the configured text."""
    config = BadgeConfig(
        "Germany", remove_label="Remove filter", remove_htmx=HtmxConfig(request_url="?", target="#results")
    )
    button = render("{% badge config=config %}", {"config": config}).select_one(".badge button")

    assert button["aria-label"] == "Remove filter: Germany"


def test_badge_remove_request_requires_a_target() -> None:
    """Without a target HTMX would swap the response into the button itself."""
    with pytest.raises(ValueError, match=r"remove_htmx needs a target"):
        BadgeConfig("Germany", remove_htmx=HtmxConfig(request_url="?"))


# --- badge_list ----------------------------------------------------------


def test_badge_list_renders_badges_as_labelled_list() -> None:
    """Badges are list items of a named list, so screen readers announce the count."""
    config = BadgeListConfig(
        tag_id="active-filters",
        label="Active filters",
        items=[removable_badge("Country: Germany", "?status=open"), removable_badge("Status: Open", "?country=de")],
    )
    soup = render("{% badge_list config %}", {"config": config})

    container = soup.select_one("#active-filters")
    assert container.has_attr("data-insight-badge-list")
    badge_list = container.select_one("ul")
    assert badge_list["role"] == "list"
    assert badge_list["aria-label"] == "Active filters"
    items = badge_list.find_all("li", recursive=False)
    assert [item.select_one("span").get_text(strip=True) for item in items] == ["Country: Germany", "Status: Open"]
    assert all(item.select_one("button[data-insight-badge-remove]") for item in items)


def test_empty_badge_list_keeps_focusable_list() -> None:
    """The empty list stays in place as focus target after the last badge was removed."""
    soup = render("{% badge_list tag_id='active-filters' label='Active filters' %}")

    badge_list = soup.select_one("#active-filters ul")
    assert badge_list is not None
    assert badge_list["tabindex"] == "-1"
    assert badge_list.find("li") is None


@pytest.mark.parametrize("has_items", [True, False], ids=["with-badges", "without-badges"])
def test_remove_all_button_is_opt_in_and_hidden_without_badges(has_items: bool) -> None:
    """The remove-all button appears only if configured and only while there is something to remove."""
    items = [removable_badge("Country: Germany", "?status=open")] if has_items else []
    config = BadgeListConfig(
        tag_id="active-filters",
        label="Active filters",
        items=items,
        clear_all_htmx=HtmxConfig(request_url="?", target="#results"),
        clear_all_label="Remove all filters",
    )
    button = render("{% badge_list config %}", {"config": config}).select_one("[data-insight-badge-clear-all]")

    if has_items:
        assert button["type"] == "button"
        assert button.get_text(strip=True) == "Remove all filters"
        assert button["hx-get"] == "?"
        # HtmxConfig defaults to trigger="submit", which would never fire on a button.
        assert button["hx-trigger"] == "click"
    else:
        assert button is None


def test_remove_all_button_is_not_rendered_by_default() -> None:
    """Without clear_all_htmx there is no remove-all button."""
    config = BadgeListConfig(tag_id="active-filters", label="Active filters", items=[removable_badge("Germany", "?")])

    assert render("{% badge_list config %}", {"config": config}).select_one("[data-insight-badge-clear-all]") is None


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        pytest.param({"tag_id": "", "label": "Active filters"}, "non-empty tag_id", id="empty-tag-id"),
        pytest.param({"tag_id": "active-filters", "label": ""}, "non-empty label", id="empty-label"),
        pytest.param(
            {"tag_id": "active-filters", "label": "Active filters", "clear_all_htmx": HtmxConfig(request_url="?")},
            "clear_all_htmx needs a target",
            id="remove-all-without-target",
        ),
    ],
)
def test_badge_list_config_rejects_incomplete_values(kwargs: dict, message: str) -> None:
    """The focus restore needs the ID, the list needs a name and the remove-all request a target."""
    with pytest.raises(ValueError, match=message):
        BadgeListConfig(**kwargs)
