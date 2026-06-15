from http import HTTPStatus
from pathlib import Path

from django.test import Client, override_settings
from django.urls import reverse


def test_component_source_view_rejects_missing_or_invalid_sources(client: Client) -> None:
    """Only allow-listed package source files should be exposed."""
    missing_script = client.get(
        reverse("component_source_view", kwargs={"component_name": "breadcrumbs", "source_kind": "js"})
    )
    invalid_kind = client.get(
        reverse("component_source_view", kwargs={"component_name": "breadcrumbs", "source_kind": "py"})
    )

    assert missing_script.status_code == HTTPStatus.NOT_FOUND
    assert invalid_kind.status_code == HTTPStatus.NOT_FOUND


def test_license_view_serves_deployed_license_file(client: Client) -> None:
    """Footer license links should resolve to the license bundled with the deployment."""
    response = client.get(reverse("license_view"))

    assert response.status_code == HTTPStatus.OK
    assert response.headers["Content-Type"].startswith("text/plain")
    assert response.headers["Content-Disposition"] == 'inline; filename="LICENSE"'
    assert "GNU AFFERO GENERAL PUBLIC LICENSE" in response.content.decode()


def test_license_view_does_not_depend_on_host_project_base_dir(client: Client, tmp_path: Path) -> None:
    """Package consumers should not need a LICENSE file in their Django project root."""
    with override_settings(BASE_DIR=tmp_path):
        response = client.get(reverse("license_view"))

    assert response.status_code == HTTPStatus.OK
    assert "GNU AFFERO GENERAL PUBLIC LICENSE" in response.content.decode()
