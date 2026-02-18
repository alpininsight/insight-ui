"""
Smoke tests for the Insight UI demo project.

These tests are intentionally small and fast. They answer the question:
"Does the main app basically start and render key pages?"
"""

from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.smoke
@pytest.mark.django_db
def test_root_url_responds_ok(client: Client) -> None:  # noqa: ANN001
    """Basic smoke test for the index page."""
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    content = response.content.decode()
    assert "Insight UI" in content or "Components" in content


@pytest.mark.smoke
@pytest.mark.django_db
def test_login_url_responds_ok(client: Client) -> None:  # noqa: ANN001
    """Basic smoke test for the login page."""
    response = client.get("/login/")

    assert response.status_code == HTTPStatus.OK
    assert "Login" in response.content.decode()


@pytest.mark.smoke
@pytest.mark.django_db
@pytest.mark.parametrize("viewname", ["layout", "main", "input", "popup", "util", "table", "card", "form", "filter"])
def test_storybook_urls_responds_ok(viewname: str, client: Client) -> None:  # noqa: ANN001
    """Basic smoke test for the storybook pages."""
    response = client.get(reverse("storybook_view", kwargs={"storybook_name": viewname}))

    assert response.status_code == HTTPStatus.OK


@pytest.mark.smoke
@pytest.mark.django_db
@pytest.mark.parametrize(
    "component_name",
    [
        "page_header",
        "article",
        "hero",
        "navbar",
        "sidebar",
        "footer",
        "breadcrumb",
        "step_bar",
        "bullet_point_list",
        "accordion",
        "tabs",
        "button",
        "input_field",
        "checkbox",
        "checkbox_group",
        "dropdown",
        "radio_group",
        "range_slider",
        "toggle_button",
        "select",
        "multiselect",
        "chat",
        "alert",
        "modal",
        "popover",
        "tooltip",
        "code_block",
        "differentiator",
        "progress_bar",
        "geo_map",
        "chart",
        "live_content",
        "web_socket",
        "infinite_scroll",
        "pagination",
        "table",
        "generic_filter",
        "search_bar",
        "query_builder",
        "card",
        "card_carousel",
        "image_carousel",
        "3D_carousel",
        "toggle_view",
        "form",
    ],
)
def test_component_urls_responds_ok(component_name: str, client: Client) -> None:  # noqa: ANN001
    """Basic smoke test for the component pages."""
    response = client.get(reverse("component_detail_page_view", kwargs={"component_name": component_name}))

    assert response.status_code == HTTPStatus.OK


@pytest.mark.smoke
@pytest.mark.django_db
@pytest.mark.parametrize(
    "component_name",
    [
        "page_header",
        "article",
        "hero",
        "navbar",
        "sidebar",
        "footer",
        "breadcrumb",
        "step_bar",
        "bullet_point_list",
        "accordion",
        "accordion_exclusive",
        "tabs",
        "button",
        "outline_button",
        "button_sizes",
        "input_field",
        "checkbox",
        "checkbox_group",
        "dropdown",
        "radio_group",
        "radio_block",
        "range_slider",
        "toggle_button",
        "select",
        "multiselect",
        "chat",
        "alert",
        "modal",
        "popover",
        "tooltip",
        "code_block",
        "differentiator",
        "progress_bar",
        "geo_map",
        "chart",
        "live_content",
        "web_socket",
        "infinite_scroll",
        "pagination",
        "table",
        "generic_filter",
        "search_bar",
        "query_builder",
        "card",
        "card_carousel",
        "image_carousel",
        "3D_carousel",
        "toggle_view",
        "form",
    ],
)
def test_component_demo_urls_responds_ok(component_name: str, client: Client) -> None:  # noqa: ANN001
    """Basic smoke test for the component demo pages."""
    response = client.get(reverse("component_demo_view", kwargs={"component_name": component_name}))

    assert response.status_code == HTTPStatus.OK
