"""Integration coverage for the runtime deployment contract."""

from __future__ import annotations

from http import HTTPStatus

import pytest
from core.runtime_contract import build_runtime_info
from django.test import override_settings


@pytest.mark.integration
@pytest.mark.django_db
@override_settings(
    SERVICE_NAMESPACE="alpininsight",
    SERVICE_NAME="insight-ui",
    PLATFORM_NAMESPACE="demo",
    DEPLOYMENT_ENVIRONMENT="develop",
    DEPLOYMENT_LANE="develop",
    DEPLOYMENT_SLOT="green",
    PUBLIC_BASE_URL="https://insight-ui.demo.alpininsight.ai",
    ARTIFACT_VERSION="v1.2.3",
    GIT_COMMIT_SHA="deadbeef",
)
def test_api_info_exposes_runtime_contract(client) -> None:  # noqa: ANN001
    """The runtime identity endpoint should follow the repo-side contract shape."""
    response = client.get("/api/info")

    assert response.status_code == HTTPStatus.OK
    payload = response.json()
    assert payload["service"] == {
        "namespace": "alpininsight",
        "name": "insight-ui",
        "version": "v1.2.3",
        "instance_id": payload["service"]["instance_id"],
    }
    assert payload["deployment"] == {
        "environment": {"name": "develop"},
        "platform_namespace": "demo",
        "lane": "develop",
        "slot": "green",
    }
    assert payload["build"] == {"revision": "deadbeef"}
    assert payload["urls"] == {"public_base": "https://insight-ui.demo.alpininsight.ai"}


@pytest.mark.integration
@override_settings(
    SERVICE_NAMESPACE="alpininsight",
    SERVICE_NAME="insight-ui",
    PLATFORM_NAMESPACE="demo",
    DEPLOYMENT_ENVIRONMENT="develop",
    DEPLOYMENT_LANE="develop",
    DEPLOYMENT_SLOT="green",
    PUBLIC_BASE_URL="https://insight-ui.demo.alpininsight.ai",
    ARTIFACT_VERSION="v1.2.3",
    GIT_COMMIT_SHA="deadbeef",
)
def test_build_runtime_info_matches_http_payload() -> None:
    """The helper should return the same metadata shape used by the view."""
    payload = build_runtime_info()

    assert payload["service"]["namespace"] == "alpininsight"
    assert payload["service"]["name"] == "insight-ui"
    assert payload["service"]["version"] == "v1.2.3"
    assert payload["deployment"]["environment"]["name"] == "develop"
    assert payload["deployment"]["lane"] == "develop"
    assert payload["deployment"]["slot"] == "green"
    assert payload["deployment"]["platform_namespace"] == "demo"
    assert payload["build"]["revision"] == "deadbeef"
    assert payload["urls"]["public_base"] == "https://insight-ui.demo.alpininsight.ai"
