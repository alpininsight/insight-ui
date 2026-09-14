# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Context processors for Insight UI templates.

Add to your Django settings TEMPLATES configuration::

    TEMPLATES = [
        {
            ...
            "OPTIONS": {
                "context_processors": [
                    ...
                    "insight_ui.context_processors.insight_ui_context",
                ],
            },
        },
    ]

"""

from django.http import HttpRequest

from insight_ui.config import get_config


def insight_ui_context(_request: HttpRequest) -> dict:
    """Provide INSIGHT_UI configuration to all templates.

    Returns a dictionary with the ``INSIGHT_UI`` key containing the merged
    configuration (user settings + library defaults).

    """
    return get_config()
