"""Tests for the shared Insight UI base template."""

from __future__ import annotations

import sys

from django.template.loader import render_to_string
from django.test import TestCase, override_settings
from insight_ui.config import get_config

urlpatterns = []


class TestBaseTemplate(TestCase):
    """Test suite for the base template contract."""

    @override_settings(
        ROOT_URLCONF=__name__,
        STORAGES={
            "staticfiles": {
                "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
            },
        },
    )
    def test_base_template_does_not_require_javascript_catalog_url(self) -> None:
        """Host apps may render the base template without installing Django's JavaScriptCatalog URL."""
        sys.modules[__name__].urlpatterns = []

        rendered = render_to_string("insight_ui/base.html", get_config())

        assert "<!DOCTYPE html>" in rendered
        assert "javascript-catalog" not in rendered
