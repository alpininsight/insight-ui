from django.conf.urls.i18n import set_language
from django.urls import path

from . import views

urlpatterns = [
    path("api/live-data/", views.live_data_view, name="live_data"),
    path("api/more-items/", views.more_items_view, name="more_items"),
    path("api/form-submit/", views.form_submit, name="form_submit"),
    path("api/chat-response/", views.chat_response, name="chat_response"),
    path("toggle_view/", views.toggle_view, name="toggle_view"),
    path("pagination/", views.pagination, name="pagination"),
    path("i18n/setlang/", set_language, name="set_language"),
    path("", views.storybook_view, name="storybook_view"),
]
