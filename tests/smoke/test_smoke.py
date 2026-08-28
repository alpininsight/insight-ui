"""
Smoke tests for the Insight UI demo project.

These tests are intentionally small and fast. They answer the question:
"Does the main app basically start and render key pages?"
"""

from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from documentation.component_details.component_context import COMPONENT_CONTEXT_BUILDERS
from documentation.component_details.components import Component, ComponentCategory


@pytest.mark.smoke
def test_healthz_responds_ok(client: Client) -> None:
    """Health endpoint should stay cheap and stable for probes."""
    response = client.get("/healthz")

    assert response.status_code == HTTPStatus.OK
    assert response.content.decode() == "OK"


@pytest.mark.smoke
@pytest.mark.django_db
def test_readyz_responds_ok(client: Client) -> None:
    """Readiness endpoint should confirm cheap local prerequisites."""
    response = client.get("/readyz")

    assert response.status_code == HTTPStatus.OK
    assert response.json()["status"] == "ok"


@pytest.mark.smoke
@pytest.mark.django_db
def test_api_info_responds_ok(client: Client) -> None:
    """Runtime identity endpoint should expose the canonical service metadata."""
    response = client.get("/api/info")

    assert response.status_code == HTTPStatus.OK
    payload = response.json()
    assert payload["service"]["name"] == "insight-ui"
    assert payload["service"]["namespace"] == "alpininsight"
    assert payload["deployment"]["platform_namespace"] == "demo"
    assert payload["deployment"]["environment"]["name"] == "local"


@pytest.mark.smoke
@pytest.mark.django_db
@pytest.mark.parametrize(
    "view_name",
    [
        "index_view",
        "login",
        "icon_view",
        "types_view",
        "config_reference_view",
        "customization_view",
        "installation_view",
        "base_template_view",
        "license_view",
    ],
)
def test_docs_pages_respond_ok(view_name: str, client: Client) -> None:
    """Core and documentation pages should render without errors."""
    response = client.get(reverse(view_name))

    assert response.status_code == HTTPStatus.OK


@pytest.mark.smoke
@pytest.mark.django_db
@pytest.mark.parametrize("category", list(ComponentCategory))
def test_storybook_urls_responds_ok(category: ComponentCategory, client: Client) -> None:
    """Storybook category pages should render without errors."""
    response = client.get(reverse("storybook_view", kwargs={"storybook_name": category.value}))

    assert response.status_code == HTTPStatus.OK


@pytest.mark.smoke
@pytest.mark.django_db
@pytest.mark.parametrize("component", list(Component))
def test_component_urls_responds_ok(component: Component, client: Client) -> None:
    """Component detail pages should render without errors."""
    response = client.get(reverse("component_detail_page_view", kwargs={"component_name": component.value}))

    assert response.status_code == HTTPStatus.OK


@pytest.mark.smoke
@pytest.mark.django_db
@pytest.mark.parametrize("component_name", COMPONENT_CONTEXT_BUILDERS.keys())
def test_component_demo_urls_responds_ok(component_name: str, client: Client) -> None:
    """Component demo pages should render without errors."""
    response = client.get(reverse("component_demo_view", kwargs={"component_name": component_name}))

    assert response.status_code == HTTPStatus.OK
