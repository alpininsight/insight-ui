def generate_payload(count: int = 5) -> list:
    """
    Generate example data.

    Arguments:
    ---------
        count (int): the amount of generated entries.

    Returns:
    -------
        data (list): a list of generated entries.

    """
    return [
        {
            "title": f"Element {i}",
            "content": f"Dies ist der Inhalt von Eintrag {i}.",
            "status": "Aktiv" if i % 2 == 0 else "Inaktiv",
            "actions": [
                {"text": "Mehr erfahren", "url": "#", "type": "primary"},
                {"text": "Teilen", "url": "#", "type": "secondary"},
            ],
            "action_link": f"<a href='#' class='underline text-insight-text-link hover:text-insight-text-link-hover'>Details {i}</a>",  # noqa: E501
        }
        for i in range(1, count + 1)
    ]


def map_payload_to_cards(payload: list) -> list:
    """
    Map given data to required data layout for the cards examples.

    Arguments:
    ---------
        payload (list): data to be transformed.

    Returns:
    -------
        data (list): transformed data.

    """
    return [
        {"title": item["title"], "subtitle": item["status"], "content": item["content"], "actions": item["actions"]}
        for item in payload
    ]


def map_payload_to_table(payload: list) -> tuple[list[str], list]:
    """
    Map given data to required data layout for table examples.

    Arguments:
    ---------
        payload (list): data to be transformed.

    Returns:
    -------
        data (list): transformed data.

    """
    headers = ["Title", "Status", "Content", "URL"]
    rows = [[item["title"], item["status"], item["content"], item["action_link"]] for item in payload]
    return headers, rows
