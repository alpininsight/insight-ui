from http import HTTPStatus

import pytest
from bs4 import BeautifulSoup
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_component_docs_keep_primary_sidebar_visible(client: Client) -> None:
    """The primary component navigation must not disappear below xl viewports."""
    response = client.get(reverse("component_detail_page_view", kwargs={"component_name": "breadcrumbs"}))

    assert response.status_code == HTTPStatus.OK
    soup = BeautifulSoup(response.content.decode(), "html.parser")
    primary_sidebar = soup.select_one("#left-aside #left-sidebar aside")
    secondary_sidebar = soup.select_one("#right-aside #right-sidebar aside")

    assert primary_sidebar is not None
    primary_classes = primary_sidebar.get("class", [])
    assert "hidden" not in primary_classes
    assert "xl:block" not in primary_classes

    assert secondary_sidebar is not None
    secondary_classes = secondary_sidebar.get("class", [])
    assert "hidden" in secondary_classes
    assert "xl:block" in secondary_classes
