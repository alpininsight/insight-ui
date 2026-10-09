# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the pagination component."""

import warnings

import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template
from insight_ui.configs import PaginationConfig
from insight_ui.utils.pagination import get_page


def render_pagination(page_number: int) -> BeautifulSoup:
    """Render the pagination for 30 items with 10 per page, turning warnings into errors like strict hosts do."""
    page, surrounding_pages = get_page(list(range(30)), items_per_page=10, page=page_number)
    config = PaginationConfig(request_url="/items/", current_page=page, surrounding_pages=surrounding_pages)

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        rendered = Template("{% load insight_tags %}{% pagination config %}").render(Context({"config": config}))
    return BeautifulSoup(rendered, "html.parser")


@pytest.mark.parametrize(
    ("page_number", "disabled_label"),
    [
        pytest.param(1, "To previous page (Deactivated because there are no more previous pages)", id="first-page"),
        pytest.param(3, "To next page (Deactivated because there are no more next pages)", id="last-page"),
    ],
)
def test_disabled_page_button_renders_without_warning(page_number: int, disabled_label: str) -> None:
    """On the first and last page the disabled button explains itself without emitting a warning."""
    soup = render_pagination(page_number)

    button = soup.find(attrs={"aria-label": disabled_label})
    assert button is not None
    assert button.has_attr("disabled")
    assert button["data-insight-tooltip"] == disabled_label


def test_middle_page_has_no_disabled_buttons() -> None:
    """Between the first and last page both directions are available."""
    soup = render_pagination(2)

    assert soup.select("nav.pagination [disabled]") == []
