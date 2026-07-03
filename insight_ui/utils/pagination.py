"""Pagination utilities for Insight UI."""

from collections.abc import Sequence

from django.core.paginator import Page, Paginator


def get_page(
    data: Sequence[object], items_per_page: int = 10, page: int = 1, max_neighbor_pages: int = 2
) -> tuple[Page[object], list[int]]:
    """Create pagination for given data.

    Retrieves data of the desired page and calculates page numbers of neighboring pages.

    Args:
        data: Data to create pagination for.
        items_per_page: The amount of items per page.
        page: Desired page number.
        max_neighbor_pages: The maximal amount of pages next to the desired page.

    Returns:
        A tuple of the desired page and a list of neighboring page numbers.

    """
    paginator = Paginator(data, items_per_page)

    # Prevent page number out of range
    if page > paginator.num_pages:
        page = paginator.num_pages
    elif page < 1:
        page = 1

    # Calculate start page and end page
    start = max(1, page - max_neighbor_pages)
    end = min(paginator.num_pages, page + max_neighbor_pages)

    # Adjust if there are not enough pages before the current page
    if page - start < max_neighbor_pages:
        end = min(paginator.num_pages, end + (max_neighbor_pages - (page - start)))

    # Adjust if there are not enough pages after the current page
    if end - page < max_neighbor_pages:
        start = max(1, start - (max_neighbor_pages - (end - page)))

    # Create list of neighboring pages
    surrounding_pages = list(range(start, end + 1))

    page_links: list[int] = []
    for i in range(1, paginator.num_pages + 1):
        if i in surrounding_pages or i in {1, paginator.num_pages}:
            page_links.append(i)
        elif not page_links or page_links[-1] != -1:
            page_links.append(-1)

    page_obj: Page[object] = paginator.get_page(page)
    return page_obj, page_links
