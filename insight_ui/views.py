from datetime import UTC, datetime
from typing import Any, cast

import structlog
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET, require_http_methods

from insight_ui.demo_context import (
    DEMO_FIELDS,
    get_3d_carousel_context,
    get_accordion_context,
    get_alert_context,
    get_base_context,
    get_breadcrumb_context,
    get_bullet_point_list_context,
    get_card_carousel_context,
    get_card_storybook_context,
    get_cards_context,
    get_charts_context,
    get_checkbox_context,
    get_differentiator_context,
    get_drawer_context,
    get_dropdown_context,
    get_empty_context,
    get_filter_storybook_context,
    get_footer_context,
    get_form_context,
    get_form_storybook_context,
    get_generic_filter_context,
    get_geo_map_context,
    get_image_carousel_context,
    get_infinite_scroll_context,
    get_inputs_storybook_context,
    get_main_storybook_context,
    get_modal_context,
    get_navbar_context,
    get_pagination_context,
    get_popup_storybook_context,
    get_query_builder_context,
    get_radio_button_context,
    get_range_slider_context,
    get_sidebar_context,
    get_step_bar_context,
    get_table_context,
    get_table_storybook_context,
    get_tabs_context,
    get_toggle_button_context,
    get_toggle_view_context,
    get_utils_storybook_context,
)
from insight_ui.demo_utils import generate_payload, map_payload_to_cards, map_payload_to_table
from insight_ui.forms import ChatForm
from insight_ui.utils.pagination import get_page
from insight_ui.utils.query_builder_utils import FilterFieldConfig, get_filter_settings_for_field

logger = structlog.get_logger(__name__)


@require_GET
def get_allowed_operators(request: HttpRequest) -> JsonResponse:
    """Retrieve all allowed operator of the given model field."""
    field = request.GET.get("field")

    if not field:
        return JsonResponse({"error": "Field is required!"}, status=400)

    field_config = cast(list[FilterFieldConfig], DEMO_FIELDS)
    input_type, allowed_operators, possible_values = get_filter_settings_for_field(field_config, field)
    return JsonResponse({"operators": allowed_operators, "values": possible_values, "inputType": input_type})


def chat_response(request: HttpRequest) -> HttpResponse:
    """Chat request endpoint to answer on chat messages."""
    form = ChatForm(request.POST)

    if form.is_valid():
        return render(request, "insight_ui/components/chat_response.html", {"msg": form.cleaned_data["msg"]})

    return HttpResponse(status=204)  # no content


def pagination(request: HttpRequest) -> HttpResponse:
    """Pagination endpoint to retrieve data of the desired page."""
    page_param = request.GET.get("page")
    try:
        page_number = int(page_param) if page_param is not None else 1
    except (TypeError, ValueError):
        page_number = 1

    page_obj, surrounding_pages = get_page(generate_payload(100), page_number)

    if request.headers.get("HX-Request"):
        return render(
            request,
            "insight_ui/components/list_partial.html",
            {"current_page": page_obj, "surrounding_pages": surrounding_pages},
        )

    context = get_table_storybook_context()
    context["current_page"] = page_obj
    context["surrounding_pages"] = surrounding_pages
    return render(request, "insight_ui/storybook.html", context)


@require_http_methods(["GET"])
def live_data_view(request: HttpRequest) -> HttpResponse | JsonResponse:
    """HTMX endpoint for live data feed."""
    current_time = datetime.now(tz=UTC).strftime("%H:%M:%S")
    data = {
        "time": current_time,
        "message": _("Data updated at %(time)s") % {"time": current_time},
        "status": "success",
    }

    if request.headers.get("HX-Request"):
        html = render_to_string(
            "insight_ui/components/live_content_partial.html", {"data": data, "timestamp": current_time}
        )
        return HttpResponse(html)

    return JsonResponse(data)


@require_http_methods(["GET"])
def more_items_view(request: HttpRequest) -> HttpResponse | JsonResponse:
    """HTMX endpoint for infinite scroll."""
    page = int(request.GET.get("page", 1))
    items_per_page = 5

    # Simuliere mehr Items
    start = (page - 1) * items_per_page + 11  # +11 weil wir schon 10 Items haben
    end = start + items_per_page

    new_items = [
        {"title": f"Element {i}", "content": f"Dynamisch geladener Inhalt für Element {i}"} for i in range(start, end)
    ]

    has_next = page < 5  # noqa: PLR2004 Simuliere max 5 Seiten
    view_name = "more_items" if has_next else ""
    auto_fetch = request.GET.get("auto_fetch", True)

    if request.headers.get("HX-Request"):
        html = render_to_string(
            "insight_ui/components/infinite_scroll_items.html",
            {
                "items": new_items,
                "view_name": view_name,
                "has_next": has_next,
                "auto_fetch": auto_fetch,
                "page": page + 1,
            },
        )
        return HttpResponse(html)

    return JsonResponse({"items": new_items, "has_next": has_next, "auto_fetch": auto_fetch, "view_name": view_name})


@require_http_methods(["POST"])
def form_submit(request: HttpRequest) -> HttpResponse | JsonResponse:
    """
    Endpoint for form validation and handling.

    Works with standard and htmx requests. Handle form issues and return either
    partial template data if this is a htmx request or do a whole page reload.
    """
    logger.debug("Empfangene POST-Daten: %s", request.POST)
    logger.debug("Content-Type: %s", request.content_type)

    name = request.POST.get("name", "")
    email = request.POST.get("email", "")
    message = request.POST.get("message", "")

    logger.info("Extrahierte Werte - Name: '%s', Email: '%s', Message: '%s'", name, email, message)

    # Simple validation
    errors = {}
    if not name:
        errors["name"] = _("Name ist erforderlich")
    if not email:
        errors["email"] = _("E-Mail ist erforderlich")
    elif "@" not in email:
        errors["email"] = _("Ungültige E-Mail-Adresse")

    if errors:
        logger.warning("Formular-Validierungsfehler: %s", errors)

        # Return error with partial template as it is a htmx request
        if request.headers.get("HX-Request"):
            html = render_to_string("insight_ui/components/form_errors.html", {"errors": errors, "type": "error"})
            return HttpResponse(html, status=400)

        # Retrieve necessary context data and perform a whole page reload to present form issues
        context = get_form_storybook_context()
        context["form_errors"] = errors
        context["form_data"] = {"name": name, "email": email, "message": message}
        return render(request, "insight_ui/storybook.html", context)

    logger.info("Formular erfolgreich verarbeitet")

    # Return partial template without redirect as it is a htmx request
    if request.headers.get("HX-Request"):
        success_html = render_to_string(
            "insight_ui/components/form_success.html",
            {"message": _("Formular erfolgreich übermittelt!"), "name": name, "email": email, "type": "success"},
        )
        return HttpResponse(success_html)

    # Retrieve necessary context data and perform a whole page reload to present form success
    context = get_form_storybook_context()
    context["form_success"] = {
        "message": _("Normales Formular erfolgreich übermittelt!"),
        "name": name,
        "email": email,
        "type": "success",
    }

    return render(request, "insight_ui/storybook.html", context)


def index_view(request: HttpRequest) -> HttpResponse:
    """Render index page."""
    context = get_base_context() | get_sidebar_context()
    return render(request, "insight_ui/index.html", context)


def component_detail_page_view(request: HttpRequest, component_name: str) -> HttpResponse:
    """
    Render detailpage of the specified component.

    Arguments:
    ---------
        request (HttpRequest): request object.
        component_name (str): name of the component.

    Returns:
    -------
        response (HttpResponse): response object.

    """
    context_func_map = {
        "alert": get_alert_context,
        "breadcrumb": get_breadcrumb_context,
        "chat": get_empty_context,
        "code_block": get_empty_context,
        "differentiator": get_differentiator_context,
        "geo_map": get_geo_map_context,
        "button": get_empty_context,
        "checkbox": get_checkbox_context,
        "dropdown": get_dropdown_context,
        "radio_button": get_radio_button_context,
        "range_slider": get_range_slider_context,
        "toggle_button": get_toggle_button_context,
        "live_content": get_empty_context,
        "modal": get_modal_context,
        "popover": get_empty_context,
        "step_bar": get_step_bar_context,
        "tooltip": get_empty_context,
        "web_socket": get_empty_context,
        "infinite_scroll": get_infinite_scroll_context,
        "pagination": get_pagination_context,
        "table": get_table_context,
        "generic_filter": get_generic_filter_context,
        "search_bar": get_empty_context,
        "query_builder": get_query_builder_context,
        "card": get_cards_context,
        "card_carousel": get_card_carousel_context,
        "image_carousel": get_image_carousel_context,
        "toggle_view": get_toggle_view_context,
        "form": get_form_context,
        "navbar": get_navbar_context,
        "sidebar": get_drawer_context,
        "footer": get_footer_context,
        "bullet_point_list": get_bullet_point_list_context,
        "progress_bar": get_empty_context,
        "tabs": get_tabs_context,
        "accordion": get_accordion_context,
        "3D_carousel": get_3d_carousel_context,
        "chart": get_charts_context,
    }

    context_func = context_func_map.get(component_name)

    if not context_func:
        return HttpResponse("Page not found", status=404)

    if request.headers.get("HX-Request"):
        context = context_func()
        context["search_query"] = request.GET.get("search", "")
        return render(request, f"insight_ui/docs/partial/{component_name}_detailpage.html", context)

    context = get_base_context() | get_sidebar_context() | context_func()
    context["template_name"] = f"insight_ui/docs/partial/{component_name}_detailpage.html"
    return render(request, "insight_ui/docs/component_detailpage.html", context)


def storybook_view(request: HttpRequest, storybook_name: str) -> HttpResponse:
    """
    Render all components of the specified storybook.

    Arguments:
    ---------
        request (HttpRequest): request object.
        storybook_name (str): name of the storybook.

    Returns:
    -------
        response (HttpResponse): response object.

    """
    context_func_map = {
        "main": get_main_storybook_context,
        "input": get_inputs_storybook_context,
        "popup": get_popup_storybook_context,
        "util": get_utils_storybook_context,
        "table": get_table_storybook_context,
        "card": get_card_storybook_context,
        "form": get_form_storybook_context,
        "filter": get_filter_storybook_context,
    }

    context_func = context_func_map.get(storybook_name)

    if not context_func:
        return HttpResponse("Page not found", status=404)

    if request.headers.get("HX-Request"):
        context = context_func()
        context["search_query"] = request.GET.get("search", "")
        return render(request, f"insight_ui/docs/partial/storybooks/{storybook_name}_storybook.html", context)

    context = context_func()
    context["template_name"] = f"insight_ui/docs/partial/storybooks/{storybook_name}_storybook.html"
    return render(request, "insight_ui/docs/component_detailpage.html", context)


@require_GET
def toggle_view(request: HttpRequest) -> HttpResponse:
    """
    Toggle between table and card views, based on the `view` GET parameter.

    Load and map payload data to the appropriate format.
    """
    view = request.GET.get("view", "table")
    valid_views = {"table", "card", "carousel"}

    if view not in valid_views:
        logger.warning("log: toggle_view - Ungültiger 'view'-Parameter empfangen: %s. Fallback auf 'table'.", view)
        view = "table"

    # Generate the base payload
    payload = generate_payload()
    context: dict[str, Any] = {"current_view": view, "tag_id": request.GET.get("tag_id", "")}
    context["view_options"] = {
        "name": "view-options",
        "param_name": "view",
        "options": [
            {"id": "card-view", "value": "card", "icon": {"name": "cards"}},
            {"id": "table-view", "value": "table", "icon": {"name": "list"}},
            {"id": "carousel-view", "value": "carousel", "icon": {"name": "carousel"}},
        ],
    }

    if view == "card":
        context["cards"] = map_payload_to_cards(payload)
        logger.info("log: toggle_view - Kartenansicht ausgewählt")
    elif view == "carousel":
        context["cards"] = map_payload_to_cards(payload)
        logger.info("log: toggle_view - Karussell-Ansicht ausgewählt")
    else:
        # default: table view
        headers, rows = map_payload_to_table(payload)
        context["table_data"] = {"empty_msg": "Keine Daten vorhanden!", "headers": headers, "rows": rows}
        logger.info("log: toggle_view - Tabellenansicht ausgewählt")

    return render(request, "insight_ui/components/toggle_view.html", context)


@require_GET
def tabs_view(request: HttpRequest, tab_id: str) -> HttpResponse:
    """Switch content of the Tabs-Component corresponding to the given 'tab_id'."""
    msg = "This is the content of the first tab!"
    match tab_id:
        case "second":
            msg = "This is the content of the second tab!"
        case "third":
            msg = "This is the content of the third tab!"

    return render(request, "insight_ui/components/tabs_content.html", {"message": msg})
