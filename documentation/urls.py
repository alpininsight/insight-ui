"""URL configuration for Insight UI."""

from django.urls import path
from django.views.i18n import set_language

from . import views

urlpatterns = [
    path("api/live-data/", views.live_data_view, name="live_data"),
    path("api/more-items/", views.more_items_view, name="more_items"),
    path("api/chat-response/", views.chat_response, name="chat_response"),
    path("get-allowed-operators/", views.get_allowed_operators, name="get_allowed_operators"),
    path("toggle_view/", views.toggle_view, name="toggle_view"),
    path("tabs_view/<str:tab_id>", views.tabs_view, name="tabs_view"),
    path("pagination/", views.pagination, name="pagination"),
    path("i18n/setlang/", set_language, name="set_language"),
    path("docs/components/<str:component_name>/", views.component_detail_page_view, name="component_detail_page_view"),
    path(
        "docs/components/<str:component_name>/source/<str:source_kind>/",
        views.component_source_view,
        name="component_source_view",
    ),
    path("docs/components/demo/<str:component_name>/", views.component_demo_view, name="component_demo_view"),
    path("docs/license/", views.license_view, name="license_view"),
    path("docs/<str:storybook_name>/", views.storybook_view, name="storybook_view"),
    path("playground", views.playground_view, name="playground_view"),
    path("docs/customization", views.customization_view, name="customization_view"),
    path("docs/installation", views.installation_view, name="installation_view"),
    path("docs/base_template", views.base_template_view, name="base_template_view"),
    path("docs/icons", views.icon_view, name="icon_view"),
    path("docs/types", views.types_view, name="types_view"),
    path("docs/configs", views.config_reference_view, name="config_reference_view"),
    path("", views.index_view, name="index_view"),
]
