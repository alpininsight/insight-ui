# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the form component."""

import re
import warnings
from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from insight_ui.configs import FormConfig, FormFieldConfig, HtmxConfig

import insight_ui
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

    def test_form_htmx_error_container_is_an_alert_live_region(self) -> None:
        """The #form-error container announces swapped-in errors assertively."""
        config = FormConfig(title="Test Form", htmx_config=HtmxConfig(request_url="/submit/", target="#result"))
        rendered = self.render_template("{% load insight_tags %}{% form config %}", {"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        container = soup.find(id="form-error")
        assert container is not None
        assert container["role"] == "alert"
        assert container["aria-live"] == "assertive"
        assert container["aria-atomic"] == "true"

    def test_form_field_passes_help_text_and_error_to_input(self) -> None:
        """FormFieldConfig help_text / error reach the rendered input field."""
        config = FormConfig(
            request_url="/submit/",
            fields=[
                FormFieldConfig(
                    "email", "email", "email", "E-Mail", required=True, help_text="Work address", error="Invalid"
                )
            ],
        )
        rendered = self.render_template("{% load insight_tags %}{% form config %}", {"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        field = soup.find("input", {"name": "email"})
        assert field["aria-required"] == "true"
        assert field["aria-invalid"] == "true"
        assert field["aria-describedby"] == "email-help email-error"
        assert field["aria-errormessage"] == "email-error"
        assert not soup.find("p", id="email-error").has_attr("role")

    def test_css_source_applies_target_size_token_to_labels_and_small_buttons(self) -> None:
        """input.css defines --insight-target-min (WCAG 2.2 SC 2.5.8) for checkbox/radio labels and small buttons.

        The native controls keep their size; the wrapping label is the pointer target.
        """
        css = (Path(insight_ui.__file__).parent / "utils" / "input.css").read_text(encoding="utf-8")

        assert "--insight-target-min: 1.5rem" in css
        assert "2.5.8" in css
        assert 'label:has(> input[type="checkbox"]' in css
        label_rule = re.search(r'label:has\(> input\[type="radio"\][^{]*\{([^}]*)\}', css)
        assert label_rule is not None
        assert "min-height: var(--insight-target-min)" in label_rule.group(1)
        assert re.search(r'\n\s*input\[type="checkbox"\][^{]*\{[^}]*--insight-target-min', css) is None
        for size_class in (".btn-xs", ".btn-s", ".btn-icon"):
            size_rule = re.search(re.escape(size_class) + r"\s*\{([^}]*)\}", css)
            assert size_rule is not None
            assert "var(--insight-target-min)" in size_rule.group(1)
