# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the search_bar component."""

import json

import pytest
from bs4 import BeautifulSoup
from insight_ui.configs import HtmxConfig, SearchBarConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestSearchBar(TemplateTagsTestCase):
    """Test suite for the search_bar component."""

    def test_existing_positional_config_arguments_keep_their_meaning(self) -> None:
        """New IDs and names do not silently remap existing positional calls."""
        config = SearchBarConfig("/search/", True, "term", "Find")
        assert config.simple is True
        assert config.search_query == "term"
        assert config.placeholder == "Find"
        assert config.tag_id == "search"
        assert config.name == "search"

    def test_search_bar_serializes_htmx_vals_as_json(self) -> None:
        """Mappings render as valid JSON in the HTMX attribute."""
        vals = {"entity": "de", "filter": {"query": '<script>&"'}}
        rendered = self.render_template(
            "{% load insight_tags %}{% search_bar config %}",
            {
                "config": SearchBarConfig(
                    request_url="/search/",
                    htmx=HtmxConfig(target="#results", vals=vals),
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

    def test_search_bar_ids_and_name_default_to_search(self) -> None:
        """Without tag_id and name the markup stays as before."""
        soup = BeautifulSoup(
            self.render_template("{% load insight_tags %}{% search_bar enable_search=True %}"), "html.parser"
        )
        search = soup.find("input", {"type": "search"})

        assert search["id"] == "search"
        assert search["name"] == "search"
        assert soup.find("label", {"for": "search"}) is not None
        assert soup.find(id=search["aria-controls"]).has_attr("data-search-results")

    def test_two_search_bars_on_one_page_keep_their_own_ids(self) -> None:
        """A second search bar, e.g. next to the one in the navbar, gets its own label and results list."""
        rendered = self.render_template(
            "{% load insight_tags %}"
            "{% search_bar enable_search=True %}"
            '{% search_bar tag_id="product-search" name="q" enable_search=True %}'
        )
        soup = BeautifulSoup(rendered, "html.parser")
        search = soup.find(id="product-search")

        assert search["name"] == "q"
        assert soup.find("label", {"for": "product-search"}) is not None
        assert search["aria-controls"] == "product-search-results"
        assert len(soup.find_all(id="search")) == 1
        assert len(soup.find_all(id="search-results")) == 1

    def test_search_bar_rejects_an_empty_id_or_name(self) -> None:
        """An empty id or name would break the label or never submit the query."""
        for field in ("tag_id", "name"):
            with self.subTest(field=field), pytest.raises(ValueError, match=field):
                SearchBarConfig(**{field: ""})
