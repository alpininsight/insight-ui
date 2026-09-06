# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the search_bar component."""

import json

from bs4 import BeautifulSoup
from insight_ui.configs import HtmxConfig, SearchBarConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestSearchBar(TemplateTagsTestCase):
    """Test suite for the search_bar component."""

    def test_search_bar_serializes_htmx_vals_as_json(self) -> None:
        """Mappings render as valid JSON in the HTMX attribute."""
        vals = {"entity": "de", "filter": {"query": '<script>&"'}}
        rendered = self.render_template(
            "{% load insight_tags %}{% search_bar config %}",
            {
                "config": SearchBarConfig(
                    request_url="/search/",
                    htmx_config=HtmxConfig(target="#results", vals=vals),
                )
            },
        )

        form = BeautifulSoup(rendered, "html.parser").find("form", {"role": "search"})

        assert form is not None
        assert json.loads(form["hx-vals"]) == vals

    def test_search_bar_renders_configured_search_index_url(self) -> None:
        """Documentation hosts can supply their own localized search index."""
        rendered = self.render_template(
            "{% load insight_tags %}"
            '{% search_bar enable_search=True search_index_url="/static/documentation/data/search-index-de.json" %}'
        )
        search_container = BeautifulSoup(rendered, "html.parser").select_one("[data-insight-search]")

        assert search_container is not None
        assert search_container["data-search-index"] == "/static/documentation/data/search-index-de.json"
