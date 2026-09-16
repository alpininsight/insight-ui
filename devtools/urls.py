# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Simple playground URL for component development."""

from django.urls import path
from django.views.i18n import JavaScriptCatalog

from devtools.views import playground

urlpatterns = [
    path("", playground, name="playground"),
    path("jsi18n/", JavaScriptCatalog.as_view(packages=["insight_ui"]), name="javascript-catalog"),
]
