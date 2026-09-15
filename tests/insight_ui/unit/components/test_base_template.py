# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the shared Insight UI base template."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import pytest
from django.core.management import call_command
from django.template import Context, Template
from django.template.loader import render_to_string
from django.test import TestCase, override_settings
from insight_ui.config import get_config

if TYPE_CHECKING:
    from pathlib import Path

urlpatterns = []


class TestBaseTemplate(TestCase):
    """Test suite for the base template contract."""

    @override_settings(
        ROOT_URLCONF=__name__,
        STORAGES={"staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}},
    )
    def test_base_template_does_not_require_javascript_catalog_url(self) -> None:
        """Host apps may render the base template without installing Django's JavaScriptCatalog URL."""
        sys.modules[__name__].urlpatterns = []

        rendered = render_to_string("insight_ui/base.html", get_config())

        assert "<!DOCTYPE html>" in rendered
        assert "javascript-catalog" not in rendered

    @override_settings(
        ROOT_URLCONF=__name__,
        STORAGES={"staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}},
        INSIGHT_UI={"webmanifest": "example_app/favicon/site.webmanifest"},
    )
    def test_base_template_uses_configured_webmanifest(self) -> None:
        """Host apps should be able to provide their own web app manifest."""
        sys.modules[__name__].urlpatterns = []

        rendered = render_to_string("insight_ui/base.html", get_config())

        assert '<link rel="manifest" href="/static/example_app/favicon/site.webmanifest">' in rendered

    @override_settings(
        ROOT_URLCONF=__name__,
        STORAGES={"staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}},
        INSIGHT_UI={"safari_mask_icon_color": "#123456"},
    )
    def test_base_template_renders_mobile_icon_contract(self) -> None:
        """Default manifest and platform icon metadata should remain complete."""
        sys.modules[__name__].urlpatterns = []

        rendered = render_to_string("insight_ui/base.html", get_config())

        assert '<link rel="manifest" href="/static/insight_ui/favicon/site.webmanifest">' in rendered
        assert '<link rel="apple-touch-icon" sizes="180x180"' in rendered
        assert 'color="#123456"' in rendered


@pytest.mark.parametrize("brand", [{}, {"title": "Host application"}, {"title": "<Host>"}])
def test_base_page_title_preserves_host_configuration(brand: dict[str, str]) -> None:
    """The fallback stays nonempty, while legacy host titles remain escaped."""
    with override_settings(
        ROOT_URLCONF=__name__,
        STORAGES={"staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}},
        INSIGHT_UI={"brand": brand},
    ):
        rendered = render_to_string("insight_ui/base.html", get_config())
        expected = {"Host application": "Host application", "<Host>": "&lt;Host&gt;"}.get(
            brand.get("title", ""), "Django-Insight-UI"
        )
        assert f"<title>{expected}</title>" in rendered
        override = Template(
            '{% extends "insight_ui/base.html" %}{% block title %}Page-specific title{% endblock %}'
        ).render(Context(get_config()))
        assert "<title>Page-specific title</title>" in override


def test_default_base_page_renders_with_strict_staticfiles(tmp_path: Path) -> None:
    """Production defaults must work without icon overrides or lenient storage."""
    with override_settings(
        DEBUG=False,
        ROOT_URLCONF=__name__,
        STATIC_ROOT=tmp_path,
        STORAGES={"staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"}},
        INSIGHT_UI={},
    ):
        call_command("collectstatic", interactive=False, verbosity=0)
        rendered = render_to_string("insight_ui/base.html", get_config())
        assert "<title>Django-Insight-UI</title>" in rendered
        assert 'rel="mask-icon" href="/static/insight_ui/svg/insight-ui-logo.' in rendered
