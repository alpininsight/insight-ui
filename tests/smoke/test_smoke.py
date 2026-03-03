"""
Smoke tests for the Insight UI demo project.

These tests are intentionally small and fast. They answer the question:
"Does the main app basically start and render key pages?"
"""

from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from insight_ui.component_details.component_context import CONTEXT_BUILDERS


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
@pytest.mark.parametrize("component_name", CONTEXT_BUILDERS.keys())
def test_component_urls_responds_ok(component_name: str, client: Client) -> None:  # noqa: ANN001
    """Basic smoke test for the component pages."""
    response = client.get(reverse("component_detail_page_view", kwargs={"component_name": component_name}))

    assert response.status_code == HTTPStatus.OK


@pytest.mark.smoke
@pytest.mark.django_db
@pytest.mark.parametrize(
    "component_name", [*CONTEXT_BUILDERS.keys(), "accordion_exclusive", "outline_button", "button_sizes"]
)
def test_component_demo_urls_responds_ok(component_name: str, client: Client) -> None:  # noqa: ANN001
    """Basic smoke test for the component demo pages."""
    response = client.get(reverse("component_demo_view", kwargs={"component_name": component_name}))

    assert response.status_code == HTTPStatus.OK
