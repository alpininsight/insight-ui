# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""One preview page and local JavaScript translations, not a component catalog."""

from django.urls import path
from django.views.i18n import JavaScriptCatalog

from devtools.preview import preview

urlpatterns = [
    path("", preview, name="component-preview"),
    path("jsi18n/", JavaScriptCatalog.as_view(packages=["insight_ui"]), name="javascript-catalog"),
]
