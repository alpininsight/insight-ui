"""Tests for the accessibility wording on the documentation index page.

WCAG conformance is defined for complete web pages only (WCAG 2.2, section 5) and
there is no W3C certification. The public index page therefore must describe the
package as "built to WCAG 2.1 AA" and must never claim compliance or certification.
"""

import re
from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

FORBIDDEN_CLAIMS = (
    "AA-compliant",
    "compliance built-in",
    "compliance from the start",
    "completely accessible",
    "certified",
)


@pytest.fixture
def index_html(client: Client) -> str:
    """Render the English index page once for all claim assertions."""
    response = client.get(reverse("index_view"), HTTP_ACCEPT_LANGUAGE="en")
    assert response.status_code == HTTPStatus.OK
    return response.content.decode("utf-8")


def test_index_page_states_designed_to_conform_wording(index_html: str) -> None:
    """Hero, feature tile, stats tile and 'Built for everyone' carry the qualified claim."""
    assert "accessibility-first Django Component Framework" in index_html
    assert "built to WCAG 2.1 AA and WCAG 2.2 ready" in index_html
    assert "Built to WCAG 2.1 AA" in index_html
    assert "self-assessed conformance and known limitations" in index_html
    assert "is produced through our Enterprise Service" in index_html
    assert "is available through our Enterprise Service" not in index_html


@pytest.mark.parametrize("claim", FORBIDDEN_CLAIMS)
def test_index_page_makes_no_conformance_or_certification_claim(index_html: str, claim: str) -> None:
    """Unqualified compliance or certification wording must not reappear on the index page."""
    assert re.search(re.escape(claim), index_html, flags=re.IGNORECASE) is None, claim
