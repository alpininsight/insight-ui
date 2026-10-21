# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for mirroring directional icons in right-to-left layouts."""

import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template
from insight_ui.configs import BreadcrumbItemConfig, IconConfig, PaginationConfig, StepperConfig, StepperItemConfig
from insight_ui.configs.base import DIRECTIONAL_ICON_NAMES
from insight_ui.utils.pagination import get_page

MIRROR = "rtl:-scale-x-100"


def render(body: str, context: dict | None = None) -> BeautifulSoup:
    """Render a template snippet with insight_tags and layout_tags loaded."""
    html = Template("{% load insight_tags layout_tags %}" + body).render(Context(context or {}))
    return BeautifulSoup(html, "html.parser")


def icon_wrappers(soup: BeautifulSoup) -> list:
    """Return the wrapper spans of all rendered icons."""
    return [svg.parent for svg in soup.find_all("svg", attrs={"data-slot": "icon"})]


@pytest.mark.parametrize("name", sorted(DIRECTIONAL_ICON_NAMES))
def test_built_in_directional_icons_mirror_by_default(name: str) -> None:
    """Arrows and chevrons point along the reading direction, so they flip in right-to-left layouts."""
    (wrapper,) = icon_wrappers(render(f'{{% icon name="{name}" %}}'))

    assert MIRROR in wrapper["class"]


@pytest.mark.parametrize("name", ["home", "chevron-up", "arrow-top-right-on-square", "chat-bubble-left"])
def test_other_icons_do_not_mirror_by_default(name: str) -> None:
    """Icons without a reading direction keep their orientation."""
    (wrapper,) = icon_wrappers(render(f'{{% icon name="{name}" %}}'))

    assert MIRROR not in wrapper["class"]


@pytest.mark.parametrize(
    ("name", "mirror_rtl", "mirrors"),
    [
        pytest.param("home", True, True, id="force-on"),
        pytest.param("chevron-right", False, False, id="force-off"),
    ],
)
def test_mirror_rtl_overrides_the_default(name: str, *, mirror_rtl: bool, mirrors: bool) -> None:
    """Custom icons opt in with mirror_rtl=True; a directional icon can opt out with False."""
    assert IconConfig(name=name, mirror_rtl=mirror_rtl).mirrors_in_rtl is mirrors
    (wrapper,) = icon_wrappers(render(f'{{% icon name="{name}" mirror_rtl={mirror_rtl} %}}'))

    assert (MIRROR in wrapper["class"]) is mirrors


@pytest.mark.parametrize("tag", ["button", "badge"])
def test_icon_shorthand_accepts_mirror_rtl(tag: str) -> None:
    """Buttons and badges pass icon_mirror_rtl to their icon like icon_name and icon_size."""
    soup = render(f'{{% {tag} label="Next" icon_name="home" icon_mirror_rtl=True %}}')

    assert MIRROR in icon_wrappers(soup)[0]["class"]


def test_pagination_arrows_mirror() -> None:
    """Previous and next point the right way in right-to-left layouts."""
    page, surrounding_pages = get_page(list(range(30)), items_per_page=10, page=2)
    config = PaginationConfig(request_url="/items/", current_page=page, surrounding_pages=surrounding_pages)
    wrappers = icon_wrappers(render("{% pagination config %}", {"config": config}))

    assert wrappers
    assert all(MIRROR in wrapper["class"] for wrapper in wrappers)


@pytest.mark.parametrize(
    "body",
    [
        pytest.param("{% breadcrumbs items=items %}", id="breadcrumbs"),
        pytest.param('{% sidebar side="left" static=False %}x{% endsidebar %}', id="sidebar-drawer"),
    ],
)
def test_former_special_cases_render_one_mirrored_icon(body: str) -> None:
    """Breadcrumbs and sidebar use the automatic mirroring instead of their own rotation or duplicate icons."""
    items = [BreadcrumbItemConfig(text="Home", request_url="/"), BreadcrumbItemConfig(text="Docs")]
    soup = render(body, {"items": items})
    chevrons = [w for w in icon_wrappers(soup) if MIRROR in w["class"]]

    assert len(chevrons) == 1
    assert "rotate-y-180" not in str(soup)
    assert "rtl:hidden" not in str(soup)


def test_stepper_connector_is_mirrored_not_rotated() -> None:
    """The arrow between steps flips horizontally only, like the directional icons."""
    config = StepperConfig(items=[StepperItemConfig(title="Address"), StepperItemConfig(title="Review")])
    connector = render("{% stepper config %}", {"config": config}).find("li", attrs={"aria-hidden": "true"}).find("svg")

    assert MIRROR in connector["class"]
    assert "rtl:rotate-180" not in connector["class"]
