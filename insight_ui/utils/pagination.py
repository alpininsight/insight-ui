from django.core.paginator import Page, Paginator


def get_page(data: list, page: int = 1, max_neighbor_pages: int = 6) -> tuple[Page, list[str]]:
    """
    Create pagination for given data.

    Retrieve data of the desired page and calculate page number of neighboring pages.

    Arguments:
    ---------
        data (list): data to create pagination for.
        page (int): desired page number.
        max_neighbor_pages (int): the maximal amount of pages, next to the desired page.

    Returns:
    -------
        page, neighbor_pages (Page, List[str]): the desired page and a list of neighboring pages.

    """
    paginator = Paginator(data, 10)

    # Calculate neighboring pages
    surrounding_pages = []
    half = max_neighbor_pages // 2

    # Calculate start page and end page
    start = max(1, page - half)
    end = min(paginator.num_pages, page + half)

    # Adjust if there are not enough pages before the current page
    if page - start < half:
        end = min(paginator.num_pages, end + (half - (page - start)))

    # Adjust if there are not enough pages after the current page
    if end - page < half:
        start = max(1, start - (half - (end - page)))

    # Create list of neighboring pages
    surrounding_pages = list(range(start, end + 1))

    page_links = []
    for i in range(1, paginator.num_pages + 1):
        if i in surrounding_pages or i in {1, paginator.num_pages}:
            page_links.append(i)
        elif not page_links or page_links[-1] != "...":
            page_links.append("...")

    return paginator.get_page(page), page_links
