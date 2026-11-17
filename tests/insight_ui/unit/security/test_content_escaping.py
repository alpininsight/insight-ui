# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Content fields escape plain strings and render safe strings as HTML."""

from collections.abc import Callable

import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from insight_ui.configs import (
    AppCardConfig,
    ArticleConfig,
    CardConfig,
    FlipCardConfig,
    LiveContentConfig,
    TableConfig,
    WebSocketConfig,
)

PLAIN = '<img src="x" onerror="alert(1)">Ada'
TRUSTED = mark_safe("<strong>Ada</strong>")

# Each case: template tag, and a factory that puts the value into the content field under test.
CASES: dict[str, tuple[str, Callable[[str], object]]] = {
    "article.content": ("article", lambda value: ArticleConfig(content=value)),
    "card.content": ("card", lambda value: CardConfig(title="Card", content=value)),
    "app_card.content": ("app_card", lambda value: AppCardConfig(title="App", content=value)),
    "flip_card.content": ("flip_card", lambda value: FlipCardConfig(title="Flip", content=value)),
    "flip_card.back_content": (
        "flip_card",
        lambda value: FlipCardConfig(title="Flip", content="Front", back_content=value),
    ),
    "live_content.initial_content": (
        "live_content",
        lambda value: LiveContentConfig(request_url="/live/", initial_content=value),
    ),
    "websocket.initial_content": (
        "websocket",
        lambda value: WebSocketConfig(request_url="/ws/", initial_content=value),
    ),
    "table.rows": ("table", lambda value: TableConfig(headers=["Name"], rows=[[value]])),
}


def render(tag: str, config: object) -> BeautifulSoup:
    """Render one component tag with the given config."""
    html = Template(f"{{% load insight_tags %}}{{% {tag} config=config %}}").render(Context({"config": config}))
    return BeautifulSoup(html, "html.parser")


@pytest.mark.parametrize(("tag", "build"), CASES.values(), ids=CASES.keys())
def test_plain_string_content_is_escaped(tag: str, build: Callable[[str], object]) -> None:
    """Text from users or the database shows as text and never becomes markup."""
    soup = render(tag, build(PLAIN))

    assert soup.select_one("img[onerror]") is None
    assert PLAIN in soup.get_text()


@pytest.mark.parametrize(("tag", "build"), CASES.values(), ids=CASES.keys())
def test_safe_string_content_renders_as_html(tag: str, build: Callable[[str], object]) -> None:
    """HTML the host marked as safe keeps its markup."""
    soup = render(tag, build(TRUSTED))

    strong = soup.find("strong", string="Ada")
    assert strong is not None


def test_format_html_escapes_only_the_interpolated_values() -> None:
    """format_html is the way to mix trusted markup with user values."""
    value = format_html("<strong>{}</strong>", PLAIN)
    soup = render("card", CardConfig(title="Card", content=value))

    strong = soup.find("strong")
    assert strong is not None
    assert strong.get_text() == PLAIN
    assert soup.select_one("img[onerror]") is None


def test_template_string_literal_still_renders_as_html() -> None:
    """A literal written in a template is trusted by Django and keeps its markup."""
    html = Template('{% load insight_tags %}{% card title="Card" content="<em>Note</em>" %}').render(Context())

    assert BeautifulSoup(html, "html.parser").find("em", string="Note") is not None
