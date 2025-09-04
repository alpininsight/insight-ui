from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from insight_ui.demo_context import get_nav_and_footer_context

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="insight_ui/login.html", extra_context=get_nav_and_footer_context()),
        name="login",
    ),
    path("i18n/", include("django.conf.urls.i18n")),
    path("", include("insight_ui.urls")),
]
