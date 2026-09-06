# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the chart component."""

from bs4 import BeautifulSoup
from insight_ui.configs import ChartConfig, ChartDatasetConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestChart(TemplateTagsTestCase):
    """Test suite for the chart component."""

    def test_chart_data_table_matches_each_category_to_its_series_values(self) -> None:
        """Screen-reader fallbacks must preserve every series value in its row."""
        chart_config = ChartConfig(
            tag_id="activity-chart",
            dataset=ChartDatasetConfig(
                title="Activity",
                x_axis_legend=["Mon", "Tue", "Wed"],
                series=["Accepted", "Rejected"],
                data=[[12, 16, 18], [1, 0, 2]],
            ),
        )

        rendered = self.render_template(
            """{% load insight_tags %}{% line_chart config=chart_config %}""",
            {"chart_config": chart_config},
        )
        table = BeautifulSoup(rendered, "html.parser").find("table")

        assert table is not None
        rows = table.find("tbody").find_all("tr")
        assert [[cell.get_text(strip=True) for cell in row.find_all(["th", "td"])] for row in rows] == [
            ["Mon", "12", "1"],
            ["Tue", "16", "0"],
            ["Wed", "18", "2"],
        ]
        assert "ResizeObserver" in rendered

    def test_bar_chart_reuses_the_correct_data_table_fallback(self) -> None:
        """The shared fallback has the same accessible values for bar charts."""
        chart_config = ChartConfig(
            tag_id="bar-chart",
            dataset=ChartDatasetConfig(
                title="Activity",
                x_axis_legend=["Mon", "Tue"],
                series=["Accepted"],
                data=[[3, 5]],
            ),
        )

        rendered = self.render_template(
            """{% load insight_tags %}{% bar_chart config=chart_config %}""",
            {"chart_config": chart_config},
        )
        table = BeautifulSoup(rendered, "html.parser").find("table")

        assert table is not None
        assert [cell.get_text(strip=True) for cell in table.find_all("tr")[2].find_all(["th", "td"])] == [
            "Tue",
            "5",
        ]
        assert "ResizeObserver" in rendered
