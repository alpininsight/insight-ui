# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the form component."""

import warnings

import pytest
from insight_ui.configs import FormConfig, HtmxConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestForm(TemplateTagsTestCase):
    """Test suite for the form component."""

    def test_form_basic(self) -> None:
        """Test für grundlegende form Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% form title="Test Form" request_url="/api/form_submit/" %}
        """
        rendered = self.render_template(template_string)
        assert "Test Form" in rendered

    def test_form_config_warns_on_conflicting_request_url_and_htmx(self) -> None:
        """FormConfig warns when both request_url and htmx_config.request_url are set."""
        with pytest.warns(UserWarning, match="both 'request_url' and 'htmx_config.request_url'"):
            FormConfig(request_url="/submit/", htmx_config=HtmxConfig(request_url="/submit-htmx/"))

    def test_form_config_no_warning_with_only_request_url(self) -> None:
        """FormConfig does not warn when only request_url is set."""
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            FormConfig(request_url="/submit/")
        assert len(caught) == 0
