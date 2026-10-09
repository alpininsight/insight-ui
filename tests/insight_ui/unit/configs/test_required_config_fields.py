# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests that IDs, names, URLs and button labels the components depend on must not be empty."""

from collections.abc import Callable
from dataclasses import replace

import pytest
from django.core.paginator import Paginator
from django.template import Context, Template
from insight_ui.configs import (
    AccordionConfig,
    ButtonConfig,
    ChartConfig,
    ChatConfig,
    CheckboxItemConfig,
    DropdownConfig,
    DropdownItemConfig,
    FilterConfig,
    ImageCarouselItemConfig,
    ImageConfig,
    InfiniteScrollConfig,
    LiveContentConfig,
    ModalConfig,
    PaginationConfig,
    QueryBuilderFieldConfig,
    TabConfig,
    ThreeDCarouselConfig,
    ToggleViewConfig,
    UserMenuLinkConfig,
    WebSocketConfig,
)

REQUIRED_FIELDS: list = [
    # Names and identifiers
    pytest.param(lambda: FilterConfig(name="status"), "name", id="FilterConfig.name"),
    pytest.param(
        lambda: QueryBuilderFieldConfig(field="status", label="Status"), "field", id="QueryBuilderFieldConfig.field"
    ),
    # Element IDs that JavaScript and ARIA attributes refer to
    pytest.param(lambda: AccordionConfig(tag_id="faq"), "tag_id", id="AccordionConfig.tag_id"),
    pytest.param(lambda: ChartConfig(tag_id="sales"), "tag_id", id="ChartConfig.tag_id"),
    pytest.param(lambda: DropdownConfig(tag_id="menu", title="Menu"), "tag_id", id="DropdownConfig.tag_id"),
    pytest.param(lambda: ModalConfig(id="dialog"), "id", id="ModalConfig.id"),
    pytest.param(
        lambda: TabConfig(tag_id="general", title="General", request_url="/tabs/general/"),
        "tag_id",
        id="TabConfig.tag_id",
    ),
    pytest.param(lambda: ThreeDCarouselConfig(tag_id="showcase"), "tag_id", id="ThreeDCarouselConfig.tag_id"),
    pytest.param(lambda: ToggleViewConfig(tag_id="products"), "tag_id", id="ToggleViewConfig.tag_id"),
    pytest.param(
        lambda: CheckboxItemConfig(tag_id="en", label="English", value="en"), "tag_id", id="CheckboxItemConfig.tag_id"
    ),
    # URLs that are requested or loaded
    pytest.param(
        lambda: TabConfig(tag_id="general", title="General", request_url="/tabs/general/"),
        "request_url",
        id="TabConfig.request_url",
    ),
    pytest.param(lambda: ChatConfig(request_url="/chat/"), "request_url", id="ChatConfig.request_url"),
    pytest.param(
        lambda: InfiniteScrollConfig(request_url="/items/"), "request_url", id="InfiniteScrollConfig.request_url"
    ),
    pytest.param(lambda: LiveContentConfig(request_url="/status/"), "request_url", id="LiveContentConfig.request_url"),
    pytest.param(
        lambda: PaginationConfig(request_url="/items/", current_page=Paginator([1, 2], 1).page(1)),
        "request_url",
        id="PaginationConfig.request_url",
    ),
    pytest.param(lambda: WebSocketConfig(request_url="/ws/updates/"), "request_url", id="WebSocketConfig.request_url"),
    pytest.param(
        lambda: DropdownItemConfig(text="Edit", request_url="/edit/"),
        "request_url",
        id="DropdownItemConfig.request_url",
    ),
    pytest.param(
        lambda: UserMenuLinkConfig(text="Profile", request_url="/profile/"),
        "request_url",
        id="UserMenuLinkConfig.request_url",
    ),
    pytest.param(lambda: ImageConfig(url="/static/logo.png"), "url", id="ImageConfig.url"),
    pytest.param(
        lambda: ImageCarouselItemConfig(url="/static/slide.png", alt=""), "url", id="ImageCarouselItemConfig.url"
    ),
    # Accessible name of a button, also for icon-only buttons
    pytest.param(lambda: ButtonConfig(label="Save"), "label", id="ButtonConfig.label"),
]


@pytest.mark.parametrize(("build", "field_name"), REQUIRED_FIELDS)
@pytest.mark.parametrize("empty", ["", None], ids=["empty-string", "none"])
def test_required_field_rejects_empty_value(build: Callable[[], object], field_name: str, empty: str | None) -> None:
    """A valid config cannot be created or copied with an empty value in a field the component depends on."""
    config = build()

    with pytest.raises(ValueError, match=f"requires a non-empty {field_name}"):
        replace(config, **{field_name: empty})


def test_empty_alt_text_stays_allowed() -> None:
    """Decorative images use an empty alt text on purpose, so it is not treated like a missing URL."""
    assert ImageCarouselItemConfig(url="/static/slide.png", alt="").alt == ""


def test_undefined_template_variable_is_rejected() -> None:
    """Django resolves an unknown variable to an empty string, which must not render an unlabeled button."""
    with pytest.raises(ValueError, match="requires a non-empty label"):
        Template("{% load insight_tags %}{% button label=undefined_label %}").render(Context())
