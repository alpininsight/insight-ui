from django.conf.urls.i18n import set_language
from django.urls import path

from . import views

urlpatterns = [
    path("api/live-data/", views.live_data_view, name="live_data"),
    path("api/more-items/", views.more_items_view, name="more_items"),
    path("api/form-submit/", views.form_submit, name="form_submit"),
    path("api/chat-response/", views.chat_response, name="chat_response"),
    path("get-allowed-operators/", views.get_allowed_operators, name="get_allowed_operators"),
    path("toggle_view/", views.toggle_view, name="toggle_view"),
    path("pagination/", views.pagination, name="pagination"),
    path("i18n/setlang/", set_language, name="set_language"),
    path("filters", views.filter_storybook_view, name="filter_storybook_view"),
    path("cards", views.card_storybook_view, name="card_storybook_view"),
    path("forms", views.form_storybook_view, name="form_storybook_view"),
    path("tables", views.table_storybook_view, name="table_storybook_view"),
    path("docs/<str:page_name>/", views.component_detail_page_view, name="component_detail_page_view"),
    path("", views.storybook_view, name="storybook_view"),
]
