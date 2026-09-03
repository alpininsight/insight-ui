"""Minimal URL configuration for reusable Insight UI tests."""

from django.urls import include, path
from django.views.generic import TemplateView
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path("docs/license/", TemplateView.as_view(), name="license_view"),
]
