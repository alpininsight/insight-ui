# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the bullet_point_list component."""

import pytest
from bs4 import BeautifulSoup
from insight_ui.configs import BulletPointItemConfig, BulletPointListConfig, HtmxConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestBulletPointList(TemplateTagsTestCase):
    """Test suite for the bullet_point_list component."""

    def render_items(self, *items: BulletPointItemConfig, htmx: HtmxConfig | None = None) -> BeautifulSoup:
        """Render a bullet point list with the given items."""
        config = BulletPointListConfig(items=list(items), htmx=htmx)
        rendered = self.render_template("{% load insight_tags %}{% bullet_point_list config %}", {"config": config})
        return BeautifulSoup(rendered, "html.parser")

    def test_status_defaults_to_pending(self) -> None:
        """Items without a status are pending."""
        assert BulletPointItemConfig(title="Review").status == "pending"

    def test_invalid_status_raises(self) -> None:
        """Unknown status values are rejected."""
        with pytest.raises(ValueError, match="status"):
            BulletPointItemConfig(title="Review", status="done")  # type: ignore[arg-type]

    def test_renders_items_in_ordered_list(self) -> None:
        """Each item renders as a list item with title and description."""
        soup = self.render_items(
            BulletPointItemConfig(title="Setup", description="Initial configuration"),
            BulletPointItemConfig(title="Deploy"),
        )

        items = soup.select("ol > li")
        assert len(items) == 2  # noqa: PLR2004
        assert "Setup" in items[0].get_text()
        assert "Initial configuration" in items[0].get_text()

    def test_current_item_is_marked_for_assistive_technology(self) -> None:
        """Only the current item carries aria-current."""
        soup = self.render_items(
            BulletPointItemConfig(title="Setup", status="completed"),
            BulletPointItemConfig(title="Configure", status="current"),
            BulletPointItemConfig(title="Deploy"),
        )

        marked = soup.select('[aria-current="step"]')
        assert len(marked) == 1
        assert "Configure" in marked[0].get_text()

    def test_status_icons(self) -> None:
        """Completed items show a check, failed items an x-mark."""

        def svg(soup: BeautifulSoup) -> str:
            return str(soup.find("svg"))

        def icon(name: str) -> str:
            rendered = self.render_template(f'{{% load insight_tags %}}{{% icon name="{name}" size="s" %}}')
            return svg(BeautifulSoup(rendered, "html.parser"))

        check = icon("check")
        x_mark = icon("x-mark")

        assert svg(self.render_items(BulletPointItemConfig(title="Setup", status="completed"))) == check
        assert svg(self.render_items(BulletPointItemConfig(title="Setup", status="failed"))) == x_mark
        assert self.render_items(BulletPointItemConfig(title="Setup")).find("svg") is None

    def test_request_url_renders_link(self) -> None:
        """request_url is used as the href of the item."""
        soup = self.render_items(BulletPointItemConfig(title="Setup", request_url="/setup/", status="completed"))

        link = soup.find("a")
        assert link is not None
        assert link["href"] == "/setup/"

    def test_item_without_request_url_is_not_a_link(self) -> None:
        """Items without request_url render no anchor."""
        soup = self.render_items(BulletPointItemConfig(title="Setup"))

        assert soup.find("a") is None

    def test_current_item_is_not_a_link(self) -> None:
        """The current item is not linked, even with request_url."""
        soup = self.render_items(BulletPointItemConfig(title="Setup", request_url="/setup/", status="current"))

        assert soup.find("a") is None

    def test_htmx_uses_item_url(self) -> None:
        """With htmx, the link requests the URL of the item."""
        soup = self.render_items(
            BulletPointItemConfig(title="Setup", request_url="/setup/"),
            htmx=HtmxConfig(target="#content"),
        )

        link = soup.find("a")
        assert link["hx-get"] == "/setup/"
        assert link["hx-target"] == "#content"

    def test_tag_accepts_kwargs(self) -> None:
        """Items and htmx can be passed as tag arguments."""
        rendered = self.render_template(
            "{% load insight_tags %}{% bullet_point_list items=items htmx=htmx %}",
            {"items": [BulletPointItemConfig(title="Setup", request_url="/setup/")], "htmx": HtmxConfig()},
        )

        assert 'hx-get="/setup/"' in rendered
