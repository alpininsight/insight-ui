# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the query_builder component."""

import json
from datetime import date

from bs4 import BeautifulSoup
from insight_ui.configs import HtmxConfig, QueryBuilderConfig, QueryBuilderFieldConfig, QueryBuilderFilterConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase

FIELDS = [
    QueryBuilderFieldConfig(field="title", label="Title", operations={"icontains": "contains", "iexact": "is"}),
    QueryBuilderFieldConfig(field="published", label="Published", type="date", operations={"gte": "after"}),
    QueryBuilderFieldConfig(field="available", label="Available", type="boolean", operations={"exact": "is"}),
]


class TestQueryBuilder(TemplateTagsTestCase):
    """Test suite for the query_builder component."""

    def render_builder(self, **kwargs: object) -> BeautifulSoup:
        """Render the component with the test fields and parse the HTML."""
        config = QueryBuilderConfig(tag_id="books", fields=FIELDS, **kwargs)
        html = self.render_template("{% load insight_tags %}{% query_builder config=config %}", {"config": config})
        return BeautifulSoup(html, "html.parser")

    def rows(self, soup: BeautifulSoup) -> list:
        """Return the rendered filter rows, without the row template."""
        return soup.select("[data-insight-query-builder-rows] > [data-insight-query-builder-row]")

    def test_renders_a_get_form_with_one_empty_filter(self) -> None:
        """Without active filters the form offers one empty filter row."""
        soup = self.render_builder(request_url="/books/")

        form = soup.find("form", id="books")
        assert form["action"] == "/books/"
        assert form["method"] == "get"
        assert form["role"] == "search"
        rows = self.rows(soup)
        assert len(rows) == 1
        field = rows[0].find("select", attrs={"name": "filters-0-field"})
        assert [option.text for option in field.find_all("option")][1:] == ["Title", "Published", "Available"]
        assert rows[0].find(attrs={"name": "filters-0-operator"}).has_attr("disabled")

    def test_field_definitions_are_provided_for_the_script(self) -> None:
        """The browser builds operator and value controls from the JSON definitions."""
        soup = self.render_builder()

        definitions = json.loads(soup.find("script", id="books-fields").string)
        assert definitions[0] == {
            "field": "title",
            "label": "Title",
            "operations": {"icontains": "contains", "iexact": "is"},
            "choices": {},
            "input_type": "text",
        }
        assert definitions[1]["input_type"] == "date"
        assert definitions[2]["choices"] == {"true": "Yes", "false": "No"}

    def test_restores_active_filters(self) -> None:
        """Active filters render as rows with their field, operator, value and logic selected."""
        soup = self.render_builder(
            filters=[
                QueryBuilderFilterConfig(field="title", operator="iexact", value="Dune"),
                QueryBuilderFilterConfig(field="published", operator="gte", value=date(2026, 1, 1), logic="OR"),
                QueryBuilderFilterConfig(field="available", operator="exact", value=True),
            ]
        )

        first, second, third = self.rows(soup)
        assert first.find("select", attrs={"name": "filters-0-field"}).find("option", selected=True)["value"] == "title"
        assert first.find(attrs={"name": "filters-0-operator"}).find("option", selected=True)["value"] == "iexact"
        assert first.find("input", attrs={"name": "filters-0-value"})["value"] == "Dune"
        assert second.find("input", attrs={"name": "filters-1-value"})["type"] == "date"
        assert second.find("input", attrs={"name": "filters-1-value"})["value"] == "2026-01-01"
        assert second.find("input", attrs={"name": "filters-1-logic", "value": "OR"}).has_attr("checked")
        assert third.find("select", attrs={"name": "filters-2-value"}).find("option", selected=True)["value"] == "true"

    def test_first_filter_has_no_logic_choice(self) -> None:
        """The AND/OR choice of the first row is invisible and not submitted."""
        soup = self.render_builder(
            filters=[
                QueryBuilderFilterConfig(field="title", operator="iexact", value="Dune"),
                QueryBuilderFilterConfig(field="title", operator="iexact", value="Emma", logic="OR"),
            ]
        )

        first, second = self.rows(soup)
        first_logic = first.find(attrs={"data-insight-query-builder-logic": True})
        assert "invisible" in first_logic["class"]
        assert first_logic.has_attr("disabled")
        assert not second.find(attrs={"data-insight-query-builder-logic": True}).has_attr("disabled")

    def test_rows_are_labelled_groups(self) -> None:
        """Each row is a fieldset with a legend, and every control has a label."""
        soup = self.render_builder()

        row = self.rows(soup)[0]
        assert row.name == "fieldset"
        assert row.find("legend").text.strip() == "Filter 1"
        for part in ("field", "operator", "value"):
            control = row.find(attrs={"data-insight-query-builder-part": part})
            assert control["id"] == f"books-0-{part}"
            assert row.find("label", attrs={"for": f"books-0-{part}"})

    def test_param_name_prefixes_the_submitted_names(self) -> None:
        """The submitted names follow param_name, so several builders can share a page."""
        soup = self.render_builder(param_name="books")

        assert soup.find("form")["data-param-name"] == "books"
        assert self.rows(soup)[0].find("select", attrs={"name": "books-0-field"})

    def test_offers_a_row_template_and_status_region(self) -> None:
        """The script clones new rows from a template and announces changes in a status region."""
        soup = self.render_builder()

        assert soup.find("template", attrs={"data-insight-query-builder-template": True})
        assert soup.find(attrs={"data-insight-query-builder-status": True})["role"] == "status"
        assert soup.find("button", attrs={"data-insight-query-builder-add": True})
        assert soup.find("button", attrs={"type": "submit"})

    def test_htmx_sends_the_form_to_request_url(self) -> None:
        """With htmx the form is sent without a page load and the URL is pushed."""
        soup = self.render_builder(request_url="/books/", htmx=HtmxConfig(target="#results"))

        form = soup.find("form")
        assert form["hx-get"] == "/books/"
        assert form["hx-target"] == "#results"
        assert form["hx-push-url"] == "true"
        assert form["hx-disabled-elt"] == "#books button[type='submit']"

    def test_tag_accepts_keyword_arguments(self) -> None:
        """The fields can be passed without a config."""
        html = self.render_template(
            '{% load insight_tags %}{% query_builder tag_id="shop" fields=fields param_name="shop" %}',
            {"fields": FIELDS},
        )

        assert 'id="shop"' in html
        assert 'name="shop-0-field"' in html

    def test_controls_are_required(self) -> None:
        """An incomplete filter cannot be sent; the browser points to the missing control."""
        row = self.rows(self.render_builder())[0]

        for part in ("field", "operator", "value"):
            assert row.find(attrs={"data-insight-query-builder-part": part}).has_attr("required")

    def test_summary_is_optional(self) -> None:
        """The sentence of active filters is only shown with show_summary."""
        filters = [QueryBuilderFilterConfig(field="title", operator="iexact", value="Dune")]

        assert not self.render_builder(filters=filters).find(attrs={"data-insight-query-builder-summary": True})
        summary = self.render_builder(filters=filters, show_summary=True).find(
            attrs={"data-insight-query-builder-summary": True}
        )
        assert summary.text.strip() == "Active filters: Title is “Dune”"

    def test_summary_without_filters(self) -> None:
        """Without filters the summary says so instead of staying empty."""
        summary = self.render_builder(show_summary=True).find(attrs={"data-insight-query-builder-summary": True})

        assert summary.text.strip() == "No active filters."

    def test_column_labels_are_shown_once_on_wide_screens(self) -> None:
        """From md on, only the first row shows the labels; the others keep them for screen readers."""
        soup = self.render_builder(
            filters=[
                QueryBuilderFilterConfig(field="title", operator="iexact", value="Dune"),
                QueryBuilderFilterConfig(field="title", operator="iexact", value="Emma"),
            ]
        )

        first, second = self.rows(soup)
        for label in first.find_all("label", attrs={"data-insight-query-builder-label": True}):
            assert "md:sr-only" not in label["class"]
        for label in second.find_all("label", attrs={"data-insight-query-builder-label": True}):
            assert "md:sr-only" in label["class"]
            assert second.find(id=label["for"])

    def test_or_starts_a_group_with_a_divider(self) -> None:
        """A row combined with OR shows a divider above it; screen readers rely on the radio buttons."""
        soup = self.render_builder(
            filters=[
                QueryBuilderFilterConfig(field="title", operator="iexact", value="Dune"),
                QueryBuilderFilterConfig(field="title", operator="iexact", value="Emma"),
                QueryBuilderFilterConfig(field="title", operator="iexact", value="Ulysses", logic="OR"),
            ]
        )

        dividers = [row.find(attrs={"data-insight-query-builder-divider": True}) for row in self.rows(soup)]
        assert [divider.has_attr("hidden") for divider in dividers] == [True, True, False]
        assert dividers[2]["aria-hidden"] == "true"
        assert "OR" in dividers[2].text

    def test_empty_row_explains_what_to_do_first(self) -> None:
        """Condition and value of an empty row say that a field has to be chosen first."""
        row = self.rows(self.render_builder())[0]

        operator = row.find(attrs={"data-insight-query-builder-part": "operator"})
        assert operator.find("option").text.strip() == "Choose a field first"
        assert row.find(attrs={"data-insight-query-builder-part": "value"})["placeholder"] == "Choose a field first"

    def test_precedence_hint_needs_two_filters(self) -> None:
        """The AND/OR rule is only shown once two filters can be combined."""
        one = [QueryBuilderFilterConfig(field="title", operator="iexact", value="Dune")]

        assert self.render_builder(filters=one).find(id="books-help").has_attr("hidden")
        assert not self.render_builder(filters=one * 2).find(id="books-help").has_attr("hidden")

    def test_max_filters_is_passed_to_the_script(self) -> None:
        """The script stops adding rows at the same limit that parse_filters reads."""
        soup = self.render_builder(max_filters=5)

        assert soup.find("form")["data-max-filters"] == "5"
        assert "up to 5 filters" in soup.find(attrs={"data-insight-query-builder-limit": True}).text

    def test_reset_link_only_with_active_filters(self) -> None:
        """Reset loads the request URL without filters; it is not shown when nothing is filtered."""
        filters = [QueryBuilderFilterConfig(field="title", operator="iexact", value="Dune")]

        assert not self.render_builder(request_url="/books/").find("a", string=lambda text: "Reset" in (text or ""))
        reset = self.render_builder(request_url="/books/", filters=filters).find("a", href="/books/")
        assert reset
        assert "Reset" in reset.text

    def test_reset_with_htmx_pushes_the_url(self) -> None:
        """With HTMX the reset request also clears the filters from the browser URL."""
        filters = [QueryBuilderFilterConfig(field="title", operator="iexact", value="Dune")]
        soup = self.render_builder(filters=filters, htmx=HtmxConfig(target="#results"))

        reset = soup.find("a", attrs={"hx-get": "?"})
        assert reset["hx-target"] == "#results"
        assert reset["hx-push-url"] == "true"
