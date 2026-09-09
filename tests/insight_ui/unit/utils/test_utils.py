# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for pagination utilities."""

import pytest
from django.core.paginator import Page
from insight_ui.utils.pagination import get_page


@pytest.fixture
def sample_data() -> list:
    """Generate a list of 100 entries."""
    return list(range(1, 101))  # 100 elements


# --- Basics ------------------------------------------------------------


def test_get_page_with_custom_items_per_page(sample_data: list) -> None:
    """Test page generation with custom item count."""
    page, _ = get_page(sample_data, page=1, items_per_page=20)
    assert isinstance(page, Page)
    assert page.number == 1
    # 20 Elemente per page
    assert page.object_list == list(range(1, 21))


def test_get_page_last_page_with_custom_items_per_page(sample_data: list) -> None:
    """Test page numbers of the last page with custom item count."""
    page, _ = get_page(sample_data, page=5, items_per_page=20)
    assert page.number == 5  # noqa: PLR2004
    # Page 5 contains items 81-100
    assert page.object_list == list(range(81, 101))


# --- Tests for links and neighbor pages --------------------------------


def test_neighbor_links_with_custom_items_per_page(sample_data: list) -> None:
    """Test neighbor page generation at the beginning of the list."""
    # 100 items, 20 per page -> 5 pages
    _, links = get_page(sample_data, page=3, items_per_page=20, max_neighbor_pages=4)
    # half = 2 -> Pages 1-5, but total pages = 5 -> all pages
    assert links == [1, 2, 3, 4, 5]


def test_neighbor_links_small_items_per_page(sample_data: list) -> None:
    """Test neighbor page generation in the middle of the list."""
    # items_per_page = 5 → 20 pages
    _, links = get_page(sample_data, page=10, items_per_page=5, max_neighbor_pages=6)
    # 6 neighbors each side of page 10 -> Pages 4-16
    assert links == [1, -1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, -1, 20]


# --- Tests for small datasets ------------------------------------------


def test_small_dataset_less_than_one_page() -> None:
    """Test with a data set that is so small that it only results in a single page."""
    data = list(range(8))
    page, links = get_page(data, page=1, items_per_page=10)
    assert page.number == 1
    assert links == [1]  # only one page


def test_small_dataset_multiple_pages() -> None:
    """Test with a small dataset and just a few items per page."""
    data = list(range(1, 21))
    page, links = get_page(data, page=2, items_per_page=5)
    assert page.number == 2  # noqa: PLR2004
    assert links == [1, 2, 3, 4]


# --- Tests for stability of the links ("...") --------------------------


def test_no_duplicate_dot_entries(sample_data: list) -> None:
    """Check ellipsis entries (-1) are not duplicated."""
    _, links = get_page(sample_data, page=5, items_per_page=5)
    # no direct "-1, -1"
    assert all(not (links[i] == links[i + 1] == -1) for i in range(len(links) - 1))


# --- Tests for peripheral areas ----------------------------------------


def test_first_page_neighbor_links(sample_data: list) -> None:
    """Test first and last page number on the first page."""
    _, links = get_page(sample_data, page=1, items_per_page=5, max_neighbor_pages=6)
    assert links[0] == 1  # should be 1
    assert links[-1] == 20  # noqa: PLR2004


def test_last_page_neighbor_links(sample_data: list) -> None:
    """Test first and last page number on the last page."""
    _, links = get_page(sample_data, page=20, items_per_page=5, max_neighbor_pages=6)
    assert links[0] == 1
    assert links[-1] == 20  # noqa: PLR2004


# --- Tests for invalid pages -------------------------------------------


def test_page_too_high(sample_data: list) -> None:
    """Test a too high page number clamps to the last page."""
    page, _ = get_page(sample_data, page=999, items_per_page=10)
    # Paginator clamps to last page
    assert page.number == 10  # noqa: PLR2004


def test_page_too_low(sample_data: list) -> None:
    """Test a negative number clamps to page 1."""
    page, _ = get_page(sample_data, page=-3, items_per_page=10)
    # Paginator clamps to page 1
    assert page.number == 1


# --- Test: different items_per_page affect the total number of pages ---


def test_items_per_page_change_num_pages(sample_data: list) -> None:
    """Test items per page impacts page count."""
    _, links_10 = get_page(sample_data, items_per_page=10)
    _, links_25 = get_page(sample_data, items_per_page=25)
    # Page numbers vary
    assert links_10[-1] == 10  # noqa: PLR2004
    assert links_25[-1] == 4  # noqa: PLR2004
