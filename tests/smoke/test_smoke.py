"""
Smoke tests for the Insight UI demo project.

These tests are intentionally small and fast. They answer the question:
"Does the main app basically start and render key pages?"
"""

from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from insight_ui.component_details.component_context import COMPONENT_CONTEXT_BUILDERS
from insight_ui.component_details.components import Component, ComponentCategory


@pytest.mark.smoke
@pytest.mark.django_db
def test_root_url_responds_ok(client: Client) -> None:  # noqa: ANN001
    """Basic smoke test for the index page."""
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    content = response.content.decode()
    assert "Insight UI" in content or "Components" in content


@pytest.mark.smoke
def test_healthz_responds_ok(client: Client) -> None:  # noqa: ANN001
    """Health endpoint should stay cheap and stable for probes."""
    response = client.get("/healthz/")

    assert response.status_code == HTTPStatus.OK
    assert response.content.decode() == "OK"


@pytest.mark.smoke
@pytest.mark.django_db
def test_login_url_responds_ok(client: Client) -> None:  # noqa: ANN001
    """Basic smoke test for the login page."""
    response = client.get("/login/")

    assert response.status_code == HTTPStatus.OK
    assert "Login" in response.content.decode()


@pytest.mark.smoke
@pytest.mark.django_db
@pytest.mark.parametrize("category", list(ComponentCategory))
def test_storybook_urls_responds_ok(category: ComponentCategory, client: Client) -> None:  # noqa: ANN001
    """Basic smoke test for the storybook pages."""
    response = client.get(reverse("storybook_view", kwargs={"storybook_name": category.value}))

    assert response.status_code == HTTPStatus.OK


@pytest.mark.smoke
@pytest.mark.django_db
@pytest.mark.parametrize("component", list(Component))
def test_component_urls_responds_ok(component: Component, client: Client) -> None:  # noqa: ANN001
    """Basic smoke test for the component pages."""
    response = client.get(reverse("component_detail_page_view", kwargs={"component_name": component.value}))

    assert response.status_code == HTTPStatus.OK


@pytest.mark.smoke
@pytest.mark.django_db
@pytest.mark.parametrize("component_name", COMPONENT_CONTEXT_BUILDERS.keys())
def test_component_demo_urls_responds_ok(component_name: str, client: Client) -> None:  # noqa: ANN001
    """Basic smoke test for the component demo pages."""
    response = client.get(reverse("component_demo_view", kwargs={"component_name": component_name}))

    assert response.status_code == HTTPStatus.OK
