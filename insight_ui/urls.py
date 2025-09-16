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
    path("alert", views.alert_detailpage_view, name="alert_detailpage_view"),
    path("breadcrumbs", views.breadcrumbs_detailpage_view, name="breadcrumbs_detailpage_view"),
    path("chat", views.chat_detailpage_view, name="chat_detailpage_view"),
    path("code_block", views.code_block_detailpage_view, name="code_block_detailpage_view"),
    path("differentiator", views.differentiator_detailpage_view, name="differentiator_detailpage_view"),
    path("geo_map", views.geo_map_detailpage_view, name="geo_map_detailpage_view"),
    path("input_elements", views.input_elements_detailpage_view, name="input_elements_detailpage_view"),
    path("live_content", views.live_content_detailpage_view, name="live_content_detailpage_view"),
    path("modal", views.modal_detailpage_view, name="modal_detailpage_view"),
    path("popover", views.popover_detailpage_view, name="popover_detailpage_view"),
    path("step_bar", views.steps_bar_detailpage_view, name="step_bar_detailpage_view"),
    path("tooltip", views.tooltip_detailpage_view, name="tooltip_detailpage_view"),
    path("web_socket", views.web_socket_detailpage_view, name="web_socket_detailpage_view"),
    path("", views.storybook_view, name="storybook_view"),
]
