"""Utility functions for component demos."""

from django.utils.translation import gettext as _
from insight_ui.configs import ButtonConfig, CardConfig


def generate_payload(count: int = 5) -> list:
    """Generate example data.

    Args:
        count: The amount of generated entries.

    Returns:
        A list of generated entries.

    """
    return [
        {
            "title": _("Element %(i)s") % {"i": i},
            "content": _("Content for element %(i)s") % {"i": i},
            "status": _("Active") if i % 2 == 0 else _("Inactive"),
            "actions": [
                ButtonConfig(label=_("Learn more"), request_url="#", type="primary"),
                ButtonConfig(label=_("Share"), request_url="#", type="secondary"),
            ],
            "action_link": _(
                "<a href='#' class='underline text-insight-text-link hover:text-insight-text-link-hover'>Details %(i)s</a>"  # noqa: E501
            )
            % {"i": i},
        }
        for i in range(1, count + 1)
    ]


def map_payload_to_cards(payload: list) -> list[CardConfig]:
    """Map given data to required data layout for the cards examples.

    Args:
        payload: Data to be transformed.

    Returns:
        Transformed data as list of CardConfig objects.

    """
    return [CardConfig(title=item["title"], content=item["content"], actions=item["actions"]) for item in payload]


def map_payload_to_table(payload: list) -> tuple[list[str], list]:
    """Map given data to required data layout for table examples.

    Args:
        payload: Data to be transformed.

    Returns:
        A tuple of headers and rows for table display.

    """
    headers = [_("Title"), _("Status"), _("Content"), _("URL")]
    rows = [[item["title"], item["status"], item["content"], item["action_link"]] for item in payload]
    return headers, rows
