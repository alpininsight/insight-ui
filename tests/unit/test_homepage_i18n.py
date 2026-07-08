"""Tests for localized homepage copy."""

from http import HTTPStatus

import pytest
from django.test import Client
from django.utils import translation


@pytest.mark.django_db
def test_homepage_renders_german_marketing_copy(client: Client) -> None:
    """The German homepage should not fall back to English marketing copy."""
    with translation.override("de"):
        response = client.get("/")

    content = response.content.decode()

    assert response.status_code == HTTPStatus.OK
    assert "Ein Django-Komponenten-Framework" in content
    assert "Alles, was du brauchst" in content
    assert "JavaScript erforderlich" in content
    assert "Komponenten durchsuchen" in content
    assert "Nach Kategorien entdecken" in content
    assert "Über 60 Komponenten" in content
    assert "Eingabe" in content
    assert "Karten" in content

    assert "A Django Component Framework" not in content
    assert "Everything you need" not in content
    assert "JavaScript Required" not in content
    assert "Browse components" not in content
