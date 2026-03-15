from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.urls import include, path
from insight_ui.component_details.demo_context import get_login_screen_context


def health(request):
    """Health check endpoint for Kubernetes probes."""
    return HttpResponse("OK", content_type="text/plain")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="insight_ui/login.html", extra_context=get_login_screen_context()),
        name="login",
    ),
    path("healthz/", health, name="health"),
    path("i18n/", include("django.conf.urls.i18n")),
    path("", include("insight_ui.urls")),
]
