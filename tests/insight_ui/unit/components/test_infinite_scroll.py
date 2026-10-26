# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the infinite_scroll component."""

import pytest
from bs4 import BeautifulSoup
from django.core.paginator import Paginator
from django.template import Context, Template
from insight_ui.configs import HtmxConfig, InfiniteScrollConfig

ITEMS = [{"title": f"Title {number}", "content": f"Text {number}"} for number in range(1, 6)]


def feed_config(page: int = 1, items: list | None = None, **options: object) -> InfiniteScrollConfig:
    """Return a feed config for a page of the test items, two items per page."""
    current_page = Paginator(ITEMS if items is None else items, 2).page(page)
    fields = {"tag_id": "news", "request_url": "/news/", "current_page": current_page, **options}
    return InfiniteScrollConfig(**fields)  # type: ignore[arg-type]


def render(tag: str, config: InfiniteScrollConfig) -> BeautifulSoup:
    """Render the feed or a next-page response and parse it."""
    html = Template(f"{{% load insight_tags %}}{{% {tag} config %}}").render(Context({"config": config}))
    return BeautifulSoup(html, "html.parser")


def test_feed_holds_only_the_item_articles() -> None:
    """ARIA feeds own articles; the loading control lives after the feed."""
    soup = render("infinite_scroll", feed_config())

    feed = soup.find(id="news")
    assert feed["role"] == "feed"
    assert [child.name for child in feed.find_all(recursive=False)] == ["article", "article"]
    assert feed.find_next_sibling(id="news-more")


def test_articles_carry_their_position_in_the_whole_feed() -> None:
    """aria-posinset counts across pages, aria-setsize is the number of all items."""
    articles = render("infinite_scroll_items", feed_config(page=2)).find_all("article")

    assert [article["aria-posinset"] for article in articles] == ["3", "4"]
    assert {article["aria-setsize"] for article in articles} == {"5"}


def test_scrolling_to_the_end_loads_the_next_page_into_the_feed() -> None:
    """The control requests the next page when revealed and appends it to the feed."""
    control = render("infinite_scroll", feed_config()).find(id="news-more").find(attrs={"hx-get": True})

    assert control["hx-get"] == "/news/?page=2"
    assert control["hx-trigger"] == "revealed"
    assert control["hx-target"] == "#news"
    assert control["hx-swap"] == "beforeend"


def test_load_more_button_without_auto_fetch() -> None:
    """With auto_fetch=False a button loads the next page instead of scrolling."""
    button = render("infinite_scroll", feed_config(auto_fetch=False)).find(id="news-more").find("button")

    assert button.get_text(strip=True) == "Load more"
    assert button["hx-get"] == "/news/?page=2"
    assert button["hx-target"] == "#news"
    assert not button.has_attr("hx-trigger")


def test_next_page_replaces_the_control_out_of_band() -> None:
    """A response appends its articles and swaps the control for the one of the following page."""
    control = render("infinite_scroll_items", feed_config(page=2)).find(id="news-more")

    assert control["hx-swap-oob"] == "true"
    assert control.find(attrs={"hx-get": True})["hx-get"] == "/news/?page=3"


def test_last_page_says_that_all_content_is_loaded() -> None:
    """Without a next page there is nothing left to request."""
    control = render("infinite_scroll_items", feed_config(page=3)).find(id="news-more")

    assert not control.find(attrs={"hx-get": True})
    assert control.get_text(strip=True) == "All content loaded."


def test_empty_feed_renders_no_status() -> None:
    """An empty feed neither loads nor claims that content was loaded."""
    control = render("infinite_scroll", feed_config(items=[])).find(id="news-more")

    assert control.get_text(strip=True) == ""


def test_focus_moves_to_the_first_new_item_after_load_more() -> None:
    """After a button click HTMX focuses the first new article; on scroll the focus stays."""
    with_button = render("infinite_scroll_items", feed_config(page=2, auto_fetch=False)).find_all("article")
    on_scroll = render("infinite_scroll_items", feed_config(page=2)).find_all("article")

    assert with_button[0].has_attr("autofocus")
    assert not with_button[1].has_attr("autofocus")
    assert not any(article.has_attr("autofocus") for article in on_scroll)


def test_request_url_keeps_its_query_and_page_param() -> None:
    """Filters in request_url stay; only the configured page parameter is set."""
    config = feed_config(request_url="/news/?topic=tech&p=9", page_param="p")

    control = render("infinite_scroll", config).find(attrs={"hx-get": True})

    assert control["hx-get"] == "/news/?topic=tech&p=2"


def test_shared_htmx_options_are_kept() -> None:
    """Options like the indicator come from htmx; URL, target, swap and history stay fixed by the feed."""
    config = feed_config(htmx=HtmxConfig(target="#elsewhere", loading_indicator_id="#spinner", push_url=True))

    control = render("infinite_scroll", config).find(attrs={"hx-get": True})

    assert control["hx-target"] == "#news"
    assert control["hx-indicator"] == "#spinner"
    assert not control.has_attr("hx-push-url")


def test_default_item_template_renders_title_and_content() -> None:
    """Each article shows the item's title as heading and its content."""
    articles = render("infinite_scroll", feed_config()).find_all("article")

    assert [article.find("h3").get_text(strip=True) for article in articles] == ["Title 1", "Title 2"]
    assert articles[0].find("p").get_text(strip=True) == "Text 1"


def test_tag_accepts_keyword_arguments() -> None:
    """The feed can be configured without a config object."""
    tag = '{% infinite_scroll tag_id="news" request_url="/news/" current_page=page auto_fetch=False %}'
    html = Template("{% load insight_tags %}" + tag).render(Context({"page": Paginator(ITEMS, 2).page(1)}))

    assert BeautifulSoup(html, "html.parser").find("button").get_text(strip=True) == "Load more"


@pytest.mark.parametrize("field", ["tag_id", "request_url", "page_param", "item_template"])
def test_required_fields_reject_empty_values(field: str) -> None:
    """The IDs, URLs and templates the feed depends on must not be empty."""
    with pytest.raises(ValueError, match=f"requires a non-empty {field}"):
        feed_config(**{field: ""})


@pytest.mark.parametrize("auto_fetch", [True, False], ids=["scroll", "button"])
def test_loading_text_shows_in_the_control_while_loading(auto_fetch: bool) -> None:
    """Without an own indicator the control container is marked during the request and shows its text."""
    more = render("infinite_scroll", feed_config(auto_fetch=auto_fetch)).find(id="news-more")

    assert more.find(attrs={"hx-get": True})["hx-indicator"] == "#news-more"
    text = more.find(class_="htmx-indicator")
    assert text.get_text(strip=True) == "More content is loading..."
    assert text["aria-hidden"] == "true"


def test_load_more_button_is_disabled_while_loading() -> None:
    """A second click during the request would load the same page twice."""
    button = render("infinite_scroll", feed_config(auto_fetch=False)).find(id="news-more").find("button")

    assert button["hx-disabled-elt"] == "this"
