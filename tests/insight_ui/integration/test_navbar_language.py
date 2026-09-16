# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Exercise the rendered navbar with Django's unmodified language endpoint."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.template import RequestContext, Template
from django.test import Client, SimpleTestCase, override_settings
from django.urls import include, path
from django.views.decorators.http import require_GET, require_POST
from insight_ui.configs import NavbarConfig

if TYPE_CHECKING:
    from django.http import HttpRequest

DETAIL_URL = "/cases/42/?queue=mine&page=2"
ACTION_URL = "/cases/42/actions/"
LANGUAGE_URL = "/i18n/setlang/"


def _navbar_response(request: HttpRequest, *, status: int = HTTPStatus.OK) -> HttpResponse:
    """Render a synthetic host's canonical destination, including override fixtures."""
    context = RequestContext(
        request,
        {
            "nav_config": NavbarConfig(show_language_selector=True, hide_login=True),
            "redirect_to": request.GET.get("return_to", DETAIL_URL),
        },
    )
    html = Template("{% load insight_tags %}{% navbar config=nav_config %}").render(context)
    return HttpResponse(html, status=status)


@require_GET
def _detail(request: HttpRequest) -> HttpResponse:
    """Provide a GET destination without an application or database dependency."""
    return _navbar_response(request)


@require_POST
def _invalid_action(request: HttpRequest) -> HttpResponse:
    """Represent a rejected host action that renders its normal navigation."""
    return _navbar_response(request, status=HTTPStatus.BAD_REQUEST)


urlpatterns = [
    path("", _detail),
    path("cases/42/", _detail),
    path("cases/42/actions/", _invalid_action),
    path("i18n/", include("django.conf.urls.i18n")),
]


def _language_data(response: HttpResponse) -> dict[str, str]:
    """Submit the actual rendered inputs instead of reconstructing host context."""
    form = BeautifulSoup(response.content, "html.parser").select_one(f'form[action="{LANGUAGE_URL}"]')
    assert form is not None
    data = {field["name"]: field["value"] for field in form.select('input[type="hidden"]')}
    return {**data, "language": "de"}


@override_settings(
    ROOT_URLCONF=__name__,
    MIDDLEWARE=[
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.locale.LocaleMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
    ],
)
class TestNavbarLanguage(SimpleTestCase):
    """Keep host return navigation inside Django's CSRF and redirect boundary."""

    def test_language_after_invalid_post_returns_to_get_page(self) -> None:
        """An action Referer must not replace the rendered canonical GET URL."""
        client = Client(enforce_csrf_checks=True)
        initial = client.get(DETAIL_URL)
        rejected = client.post(ACTION_URL, _language_data(initial))
        assert rejected.status_code == HTTPStatus.BAD_REQUEST
        data = _language_data(rejected)
        assert data["next"] == DETAIL_URL

        response = client.post(LANGUAGE_URL, data, HTTP_REFERER=f"http://testserver{ACTION_URL}", follow=True)

        assert response.redirect_chain == [(DETAIL_URL, HTTPStatus.FOUND)]
        assert response.status_code == HTTPStatus.OK
        assert response["Content-Language"] == "de"
        assert client.get(DETAIL_URL)["Content-Language"] == "de"
        assert client.get(ACTION_URL).status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_language_rejects_unsafe_rendered_return_urls(self) -> None:
        """Django still rejects foreign hosts and HTTPS downgrades from the form."""
        for return_url in ("https://other.example/path", "//other.example/path", "http://testserver/cases/42/"):
            with self.subTest(return_url=return_url):
                client = Client(enforce_csrf_checks=True)
                initial = client.get("/cases/42/", {"return_to": return_url}, secure=True)
                data = _language_data(initial)
                assert data["next"] == return_url
                response = client.post(
                    LANGUAGE_URL,
                    data,
                    secure=True,
                    HTTP_REFERER=f"https://testserver{DETAIL_URL}",
                )
                assert response.status_code == HTTPStatus.FOUND
                assert response["Location"] == f"https://testserver{DETAIL_URL}"

    def test_language_requires_csrf_and_trusted_origin(self) -> None:
        """Propagating the return URL does not weaken the existing POST checks."""
        client = Client(enforce_csrf_checks=True)
        data = _language_data(client.get(DETAIL_URL))
        assert client.post(LANGUAGE_URL, {"next": data["next"], "language": "de"}).status_code == HTTPStatus.FORBIDDEN
        assert client.post(LANGUAGE_URL, data, HTTP_ORIGIN="https://other.example").status_code == HTTPStatus.FORBIDDEN
