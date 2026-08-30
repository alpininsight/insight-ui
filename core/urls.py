"""URL configuration for the core application."""

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.i18n import JavaScriptCatalog
from documentation.component_details.demo_context import get_login_screen_context

from core.runtime_views import api_info_view, healthz_view, readyz_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="insight_ui/login.html", extra_context=get_login_screen_context()),
        name="login",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
    path("healthz", healthz_view, name="healthz"),
    path("healthz/", healthz_view),
    path("readyz", readyz_view, name="readyz"),
    path("readyz/", readyz_view),
    path("api/info", api_info_view, name="api_info"),
    path("api/info/", api_info_view),
    path("i18n/", include("django.conf.urls.i18n")),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path("", include("documentation.urls")),
]

# Add rosetta's urls for translation
if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [path("rosetta/", include("rosetta.urls"))]
