"""Tests for the progress_bar component."""

from bs4 import BeautifulSoup
from insight_ui.configs.utils import ProgressBarConfig

from tests.unit.components.test_template_tags import TemplateTagsTestCase


class TestProgressBar(TemplateTagsTestCase):
    """Test suite for the progress_bar component."""

    def test_progress_bar_uses_semantic_track_and_fill_classes(self) -> None:
        """Progress track and fill use semantic classes instead of hard-coded colors."""
        progress_bar_config = ProgressBarConfig(tag_id="upload", label="Upload", value=66)

        rendered = self.render_template(
            "{% load insight_tags %}{% progress_bar config=progress_bar_config %}",
            context={"progress_bar_config": progress_bar_config},
        )
        soup = BeautifulSoup(rendered, "html.parser")

        track = soup.select_one("[data-progress-track] .insight-progress-track")
        fill = soup.select_one("[data-progress-fill]")

        assert track is not None
        assert fill is not None
        assert fill.get("class") == ["insight-progress-fill"]
        assert "bg-gray-200" not in track.get("class", [])
        assert "dark:bg-gray-700" not in track.get("class", [])
        assert "bg-blue-600" not in fill.get("class", [])
