"""Tests for the progress_bar component."""

import warnings

import pytest
from insight_ui.configs import ProgressBarConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase

# TODO: Implement tests for ProgressBar component  # noqa: TD002, TD003


class TestProgressBar(TemplateTagsTestCase):
    """Test suite for the progress_bar component."""

    def test_progress_bar_config_warns_on_conflicting_request_url_and_sse_url(self) -> None:
        """ProgressBarConfig warns when both request_url and sse_url are set."""
        with pytest.warns(UserWarning, match="both 'request_url' and 'sse_url'"):
            ProgressBarConfig(request_url="/poll/", sse_url="/sse/")

    def test_progress_bar_config_no_warning_with_only_sse_url(self) -> None:
        """ProgressBarConfig does not warn when only sse_url is set."""
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            ProgressBarConfig(sse_url="/sse/")
        assert len(caught) == 0
