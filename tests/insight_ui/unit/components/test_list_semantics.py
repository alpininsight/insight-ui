# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Lists without visible markers keep their list semantics in Safari.

Tailwind's preflight removes the markers of every ul and ol. Safari then no longer exposes such a list as a list
(VoiceOver announces neither "list" nor the number of items) unless it has role="list" or sits inside a nav element.
Every package list outside a nav therefore sets the role itself.
"""

from typing import Any

import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template
from insight_ui.configs import (
    BulletPointItemConfig,
    BulletPointListConfig,
    GeoMapConfig,
    GeoMapDatasetConfig,
    GeoMapMarkerConfig,
    MinimalStepperConfig,
    StepperConfig,
    StepperItemConfig,
)
from insight_ui.configs.navigation import FooterConfig, NavbarLinkConfig

LISTS: list[tuple[str, str, dict[str, Any], str]] = [
    (
        "list tag",
        "{% load layout_tags %}{% list %}{% listitem %}One{% endlistitem %}"
        "{% listitem %}Two{% endlistitem %}{% endlist %}",
        {},
        "ul",
    ),
    (
        "ordered list tag",
        "{% load layout_tags %}{% list ordered %}{% listitem %}One{% endlistitem %}{% endlist %}",
        {},
        "ol",
    ),
    (
        "stepper",
        "{% load insight_tags %}{% stepper config %}",
        {"config": StepperConfig(items=[StepperItemConfig(title="Address"), StepperItemConfig(title="Review")])},
        "ol",
    ),
    (
        "minimal stepper",
        "{% load insight_tags %}{% minimal_stepper config %}",
        {"config": MinimalStepperConfig(steps=["completed", "current", "pending"])},
        "ol",
    ),
    (
        "bullet point list",
        "{% load insight_tags %}{% bullet_point_list config %}",
        {"config": BulletPointListConfig(items=[BulletPointItemConfig(title="Install")])},
        "ol",
    ),
    (
        "footer links",
        "{% load insight_tags %}{% footer config=config %}",
        {"config": FooterConfig(links=[NavbarLinkConfig(text="Startpage", request_url="/")])},
        "footer ul",
    ),
    (
        "map locations for screen readers",
        "{% load insight_tags %}{% geo_map config=config %}",
        {
            "config": GeoMapConfig(
                datasets=[
                    GeoMapDatasetConfig(name="Offices", data=[GeoMapMarkerConfig(title="HQ", lat=48.1, lon=11.6)])
                ]
            )
        },
        "#map-locations-list ul",
    ),
]


@pytest.mark.parametrize(("template", "context", "selector"), [case[1:] for case in LISTS], ids=[c[0] for c in LISTS])
def test_list_without_markers_keeps_its_list_role(template: str, context: dict[str, Any], selector: str) -> None:
    """The list carries role="list", so Safari still announces it as a list with its number of items."""
    html = Template(template).render(Context(context))
    element = BeautifulSoup(html, "html.parser").select_one(selector)

    assert element is not None, f"No list found with {selector!r}"
    assert element.get("role") == "list"
