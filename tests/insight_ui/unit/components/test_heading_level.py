# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the heading_level option of components with titles."""

import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template
from insight_ui.configs import (
    HEADING_LEVEL_VALUES,
    AccordionConfig,
    AccordionItemConfig,
    AppCardConfig,
    CardConfig,
    FlipCardConfig,
    InfiniteScrollConfig,
)

# Tag name and a config factory taking keyword overrides.
COMPONENTS = [
    pytest.param("card", lambda **kw: CardConfig(title="Title", content="Text", **kw), id="card"),
    pytest.param("app_card", lambda **kw: AppCardConfig(title="Title", content="Text", **kw), id="app_card"),
    pytest.param(
        "flip_card",
        lambda **kw: FlipCardConfig(title="Title", content="Text", back_title="Back", **kw),
        id="flip_card",
    ),
    pytest.param(
        "accordion",
        lambda **kw: AccordionConfig(tag_id="faq", items=[AccordionItemConfig(title="Title", content="Text")], **kw),
        id="accordion",
    ),
    pytest.param(
        "infinite_scroll",
        lambda **kw: InfiniteScrollConfig(request_url="/feed/", items=[{"title": "Title", "content": "Text"}], **kw),
        id="infinite_scroll",
    ),
]


def headings(tag: str, config: object) -> list:
    """Render a component and return its heading elements."""
    html = Template(f"{{% load insight_tags %}}{{% {tag} config=config %}}").render(Context({"config": config}))
    return BeautifulSoup(html, "html.parser").find_all(["h1", "h2", "h3", "h4", "h5", "h6"])


@pytest.mark.parametrize(("tag", "build"), COMPONENTS)
def test_titles_default_to_h3(tag: str, build: object) -> None:
    """Without heading_level the output stays as before."""
    found = headings(tag, build())  # type: ignore[operator]

    assert found
    assert {h.name for h in found} == {"h3"}


@pytest.mark.parametrize(("tag", "build"), COMPONENTS)
@pytest.mark.parametrize("level", HEADING_LEVEL_VALUES)
def test_heading_level_sets_the_tag_but_not_the_look(tag: str, build: object, level: int) -> None:
    """The level changes the element; the classes, and so the look, stay the same."""
    default = headings(tag, build())  # type: ignore[operator]
    configured = headings(tag, build(heading_level=level))  # type: ignore[operator]

    assert {h.name for h in configured} == {f"h{level}"}
    assert [h.get("class") for h in configured] == [h.get("class") for h in default]


@pytest.mark.parametrize(("tag", "build"), COMPONENTS)
@pytest.mark.parametrize("level", [1, 7, 0])
def test_invalid_heading_levels_are_rejected(tag: str, build: object, level: int) -> None:
    """h1 is reserved for the page title, and HTML has no h7."""
    with pytest.raises(ValueError, match=f"Invalid heading_level {level}"):
        build(heading_level=level)  # type: ignore[operator]


@pytest.mark.parametrize("tag", ["card", "app_card", "flip_card", "infinite_scroll"])
def test_heading_level_is_a_tag_argument(tag: str) -> None:
    """The kwargs form accepts heading_level like the config."""
    arguments = {
        "card": 'title="Title" content="Text"',
        "app_card": 'title="Title" content="Text"',
        "flip_card": 'title="Title" content="Text" back_title="Back"',
        "infinite_scroll": 'request_url="/feed/" items=items',
    }[tag]
    html = Template(f"{{% load insight_tags %}}{{% {tag} {arguments} heading_level=2 %}}").render(
        Context({"items": [{"title": "Title", "content": "Text"}]})
    )

    assert {h.name for h in BeautifulSoup(html, "html.parser").find_all(["h2", "h3"])} == {"h2"}


def test_infinite_scroll_items_follow_the_heading_level_in_the_context() -> None:
    """Items loaded later use the same level when the view passes heading_level."""
    template = Template('{% include "insight_ui/components/infinite_scroll_items.html" %}')
    items = [{"title": "Title", "content": "Text"}]

    default = BeautifulSoup(template.render(Context({"items": items})), "html.parser")
    configured = BeautifulSoup(template.render(Context({"items": items, "heading_level": 2})), "html.parser")

    assert default.find("h3") is not None
    assert configured.find("h2") is not None
