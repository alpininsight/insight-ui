from http import HTTPStatus
from pathlib import Path

import pytest
from django.test import Client, override_settings
from django.urls import reverse


@pytest.mark.django_db
def test_component_detail_uses_internal_source_link(client: Client) -> None:
    """Component docs should link to source files served from the deployed package."""
    response = client.get(reverse("component_detail_page_view", kwargs={"component_name": "breadcrumbs"}))

    assert response.status_code == HTTPStatus.OK
    html = response.content.decode()
    assert 'href="/docs/components/breadcrumbs/source/html/"' in html
    assert "/docs/components/breadcrumbs/source/js/" not in html
    assert "github.com/alpininsight/insight-ui" not in html


def test_component_source_view_serves_template_source(client: Client) -> None:
    """HTML source should be read from the component template shipped in the container."""
    response = client.get(
        reverse("component_source_view", kwargs={"component_name": "breadcrumbs", "source_kind": "html"})
    )

    assert response.status_code == HTTPStatus.OK
    assert response.headers["Content-Type"].startswith("text/plain")
    assert response.headers["Content-Disposition"] == 'inline; filename="breadcrumbs.html"'
    content = response.content.decode()
    assert "{% load i18n insight_tags %}" in content
    assert "Breadcrumb-Navigation" in content


def test_component_source_view_serves_script_source(client: Client) -> None:
    """JavaScript source should be read from the static file shipped in the container."""
    response = client.get(reverse("component_source_view", kwargs={"component_name": "accordion", "source_kind": "js"}))

    assert response.status_code == HTTPStatus.OK
    assert response.headers["Content-Type"].startswith("text/plain")
    assert response.headers["Content-Disposition"] == 'inline; filename="insight-ui-accordion.js"'
    assert "export class Accordion" in response.content.decode()


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
