"""Regression tests for review findings from the main release PR."""

from __future__ import annotations

from bs4 import BeautifulSoup
from django.template import Context, Template
from django.test import TestCase
from django.urls import reverse
from insight_ui.configs import (
    AccordionConfig,
    AccordionItemConfig,
    InfiniteScrollConfig,
    LiveContentConfig,
    RadioBlockConfig,
    RadioItemConfig,
    TabConfig,
    TabsConfig,
    WebSocketConfig,
)

HTTP_OK = 200


class Pr291ReviewRegressionTests(TestCase):
    """Keep Dataclass migration regressions covered by focused tests."""

    def render_template(self, template_string: str, context: dict | None = None) -> str:
        """Render a small template snippet with Insight UI tags loaded."""
        return Template(template_string).render(Context(context or {}))

    def test_hx_pagination_renders_config_backed_previous_link(self) -> None:
        """HTMX pagination partials must keep working after page one."""
        response = self.client.get(reverse("pagination"), {"page": 2}, headers={"hx-request": "true"})

        assert response.status_code == HTTP_OK
        html = response.content.decode()
        assert f"{reverse('pagination')}?page=1" in html
        assert "?page=" in html
        assert "?page=&" not in html

    def test_live_content_uses_resolved_config_values(self) -> None:
        """Live content must not render UNSET when only config/defaults are used."""
        rendered = self.render_template(
            """
            {% load insight_tags %}
            {% live_content config=live_config %}
            """,
            {"live_config": LiveContentConfig(request_url="/api/live-data/")},
        )

        assert 'hx-get="/api/live-data/"' in rendered
        assert 'hx-trigger="load, every 10s"' in rendered
        assert "UNSET" not in rendered

    def test_websocket_connects_to_configured_url(self) -> None:
        """The HTMX ws extension must receive the configured endpoint."""
        rendered = self.render_template(
            """
            {% load insight_tags %}
            {% websocket config=websocket_config %}
            """,
            {"websocket_config": WebSocketConfig(request_url="/runtime/stream/")},
        )

        assert 'ws-connect="/runtime/stream/"' in rendered
        assert "websocket_config.." not in rendered

    def test_manual_infinite_scroll_uses_config_page(self) -> None:
        """Manual load buttons must include the configured next page."""
        rendered = self.render_template(
            """
            {% load insight_tags %}
            {% infinite_scroll config=scroll_config %}
            """,
            {"scroll_config": InfiniteScrollConfig(request_url="/api/more-items/", page=3, auto_fetch=False)},
        )

        assert 'hx-get="/api/more-items/?page=3&auto_fetch=False"' in rendered
        assert "page=&" not in rendered

    def test_toggle_view_endpoint_passes_toggle_view_config(self) -> None:
        """The HTMX toggle endpoint must render the config-backed partial."""
        response = self.client.get(reverse("toggle_view"), {"products-view-toggle": "card"})

        assert response.status_code == HTTP_OK
        html = response.content.decode()
        assert 'id="products-view"' in html
        assert "products-view-toggle" in html
        assert "<form" in html

    def test_heading_decoration_template_tag_is_registered(self) -> None:
        """The documented heading_decoration tag must compile and render."""
        rendered = self.render_template(
            """
            {% load insight_tags %}
            {% heading_decoration style="gradient" height=64 %}
            """
        )

        assert 'data-heading-decoration="gradient"' in rendered
        assert "height: 64px" in rendered

    def test_dict_config_is_converted_before_dataclass_replace(self) -> None:
        """Legacy dictionary configs should still render through build_config."""
        rendered = self.render_template(
            """
            {% load insight_tags %}
            {% corner_ribbon config=ribbon_config %}
            """,
            {"ribbon_config": {"text": "Beta", "position": "top-left", "color": "warning"}},
        )

        assert "Beta" in rendered
        assert "warning" in rendered

    def test_integrated_radio_block_does_not_render_nested_form(self) -> None:
        """Integrated radio blocks are meant to live inside an existing form."""
        rendered = self.render_template(
            """
            {% load insight_tags %}
            {% radio_block config=radio_config %}
            """,
            {
                "radio_config": RadioBlockConfig(
                    name="view",
                    integrated=True,
                    request_url="/switch/",
                    hx_target_id="target",
                    items=[RadioItemConfig(tag_id="table", value="table", label="Table")],
                )
            },
        )

        soup = BeautifulSoup(rendered, "html.parser")
        assert soup.find("form") is None
        assert soup.find("div", id="view") is not None
        radio_input = soup.find("input", {"name": "view"})
        assert radio_input is not None
        assert radio_input["hx-get"] == "/switch/"
        assert radio_input["hx-target"] == "#target"

    def test_nested_dict_config_values_are_converted_to_dataclasses(self) -> None:
        """Legacy dict configs should coerce nested dataclass values too."""
        rendered = self.render_template(
            """
            {% load insight_tags %}
            {% radio_block config=radio_config %}
            """,
            {
                "radio_config": {
                    "name": "view",
                    "items": [{"tag_id": "table", "value": "table", "label": "Table"}],
                    "request_url": "/switch/",
                    "hx_target_id": "target",
                }
            },
        )

        soup = BeautifulSoup(rendered, "html.parser")
        radio_input = soup.find("input", {"name": "view"})
        assert radio_input is not None
        assert radio_input["id"] == "view-table"
        assert radio_input["value"] == "table"
        assert radio_input["hx-get"] == "/switch/"

    def test_accordion_panel_ids_use_config_tag_id(self) -> None:
        """Accordion IDs must stay unique for each configured accordion."""
        rendered = self.render_template(
            """
            {% load insight_tags %}
            {% accordion config=accordion_config %}
            """,
            {"accordion_config": AccordionConfig("faq", [AccordionItemConfig("Question", "Answer")])},
        )

        assert 'data-insight-accordion="faq"' in rendered
        assert 'id="faq-panel-0"' in rendered
        assert 'aria-controls="faq-panel-0"' in rendered

    def test_tabs_template_uses_dataclass_field_names(self) -> None:
        """Tabs should use tag_id fields from TabsConfig and TabConfig."""
        rendered = self.render_template(
            """
            {% load insight_tags %}
            {% tabs config=tabs_config %}
            """,
            {"tabs_config": TabsConfig("settings-tabs", [TabConfig("general", "General", "/tabs/general")])},
        )

        assert 'data-insight-tabs="settings-tabs"' in rendered
        assert 'id="general"' in rendered
        assert 'hx-target="#settings-tabs-tab-content"' in rendered
        assert 'id="settings-tabs-tab-content"' in rendered
