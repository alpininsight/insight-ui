# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Simple playground view for component development.

Edit the context dict below to test your component with different configurations.
"""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from insight_ui.configs import ButtonConfig


def playground(request: HttpRequest) -> HttpResponse:
    """Render the component playground.

    Add your component configs here to preview them in the browser.
    The template renders these inside a demo container with viewport,
    RTL, and theme controls.
    """
    context = {
        "button": ButtonConfig(label="Example Button"),
    }
    return render(request, "devtools/demo_container.html", context)
