"""
Smoke tests for the Insight UI demo project.

These tests are intentionally small and fast. They answer the question:
"Does the main app basically start and render key pages?"
"""

from http import HTTPStatus

import pytest


@pytest.mark.smoke
@pytest.mark.django_db
def test_root_url_responds_ok(client) -> None:  # noqa: ANN001
    """Basic smoke test for the index page."""
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    content = response.content.decode()
    assert "Insight UI" in content or "Components" in content


@pytest.mark.smoke
@pytest.mark.django_db
def test_login_url_responds_ok(client) -> None:  # noqa: ANN001
    """Basic smoke test for the login page."""
    response = client.get("/login/")

    assert response.status_code == HTTPStatus.OK
    assert "Login" in response.content.decode()
