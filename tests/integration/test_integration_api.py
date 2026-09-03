"""Integration tests for HTMX/JSON endpoints."""

from __future__ import annotations

from http import HTTPStatus

import pytest
from django.urls import reverse


@pytest.mark.integration
@pytest.mark.django_db
def test_live_data_view_json(client) -> None:  # noqa: ANN001
    """When called without HTMX, live_data_view returns JSON payload."""
    url = reverse("live_data")

    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["status"] == "success"
    assert "time" in data
    assert "message" in data


@pytest.mark.integration
@pytest.mark.django_db
def test_live_data_view_htmx_partial(client) -> None:  # noqa: ANN001
    """When called with HX-Request header, live_data_view returns HTML partial."""
    url = reverse("live_data")

    response = client.get(url, HTTP_HX_REQUEST="true")

    assert response.status_code == HTTPStatus.OK
    content = response.content.decode()
    assert "<div" in content
    assert "success" in content


@pytest.mark.integration
@pytest.mark.django_db
def test_get_allowed_operators_validation_error(client) -> None:  # noqa: ANN001
    """get_allowed_operators returns 400 if field is missing."""
    url = reverse("get_allowed_operators")

    response = client.get(url)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["error"] == "Field is required!"
