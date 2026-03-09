from datetime import UTC, datetime
from typing import Any, cast

import structlog
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_GET, require_POST

from insight_ui.component_details import component_context
from insight_ui.component_details.components import Component, ComponentCategory
from insight_ui.component_details.demo_context import (
    DEMO_FIELDS,
    get_component_demo_context,
    get_minimal_step_bar_context,
)
from insight_ui.component_details.git_path_mapping import SCRIPT_PATHS, TEMPLATE_PATHS
from insight_ui.context import (
    get_base_context,
    get_demo_container_context,
    get_icon_context,
    get_sidebar_context,
    get_storybook_context,
)
from insight_ui.demo_utils import generate_payload, map_payload_to_cards, map_payload_to_table
from insight_ui.forms import ChatForm, FormDemoForm
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


@require_POST
def chat_response(request: HttpRequest) -> HttpResponse:
    """Chat request endpoint to answer on chat messages."""
    form = ChatForm(request.POST)

    if form.is_valid():
        return render(request, "insight_ui/components/chat_response.html", {"msg": form.cleaned_data["msg"]})

    return HttpResponse(status=204)  # no content


@require_GET
def pagination(request: HttpRequest) -> HttpResponse:
    """Pagination endpoint to retrieve data of the desired page."""
    page_param = request.GET.get("page")
    ipp_param = request.GET.get("ipp")
    try:
        page_number = int(page_param) if page_param is not None else 1
        ipp = int(ipp_param) if ipp_param is not None else 10
    except (TypeError, ValueError):
        page_number = 1
        ipp = 10

    page_obj, surrounding_pages = get_page(generate_payload(500), ipp, page_number)
    ipp_config = {"name": "ipp", "label": "Items per page", "options": [10, 20, 30], "selected_option": ipp}

    if request.headers.get("HX-Request"):
        return render(
            request,
            "insight_ui/components/pagination.html",
            {
                "current_page": page_obj,
                "surrounding_pages": surrounding_pages,
                "items_per_page": ipp,
                "ipp_config": ipp_config,
            },
        )

    context = get_storybook_context(ComponentCategory.LIST)
    context["current_page"] = page_obj
    context["surrounding_pages"] = surrounding_pages
    context["items_per_page"] = ipp
    context["ipp_config"] = ipp_config
    return render(request, "insight_ui/storybook.html", context)


@require_GET
def sort_table(request: HttpRequest) -> HttpResponse:
    """Endpoint to sort table data."""
    sort = request.GET.get("sort", "name")
    direction = request.GET.get("dir", "asc")

    _, rows = map_payload_to_table(generate_payload())

    context = {"data": rows, "sort": sort, "dir": direction}

    if request.headers.get("HX-Request"):
        return render(request, "insight_ui/components/table.html", context)

    return render(request, "insight_ui/storybook.html", context)


@require_GET
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


@require_GET
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


@require_POST
def form_submit(request: HttpRequest) -> HttpResponse | JsonResponse:
    """
    Endpoint for form validation and handling.

    Works with standard and htmx requests. Handle form issues and return either
    partial template data if this is a htmx request or do a whole page reload.
    """
    logger.debug("Empfangene POST-Daten: %s", request.POST)

    form = FormDemoForm(request.POST)
    if form.is_valid():
        # Return partial template without redirect as it is a htmx request
        if request.headers.get("HX-Request"):
            success_html = render_to_string(
                "insight_ui/components/form_success.html",
                {
                    "message": _("AJAX Formular erfolgreich übermittelt!"),
                    "title": form.cleaned_data["title"],
                    "firstname": form.cleaned_data["firstname"],
                    "lastname": form.cleaned_data["lastname"],
                    "type": "success",
                },
            )
            return HttpResponse(success_html, status=200)

        # Retrieve necessary context data and perform a whole page reload to present form success
        context = get_storybook_context(ComponentCategory.FORM)
        context["form_success"] = {
            "message": _("Formular erfolgreich übermittelt!"),
            "title": form.cleaned_data["title"],
            "firstname": form.cleaned_data["firstname"],
            "lastname": form.cleaned_data["lastname"],
            "type": "success",
        }

    # Return error with partial template as it is a htmx request
    if request.headers.get("HX-Request"):
        html = render_to_string("insight_ui/components/form_errors.html", {"errors": form.errors, "type": "error"})
        return HttpResponse(html, status=400)

    # Retrieve necessary context data and perform a whole page reload to present form issues
    context = get_storybook_context(ComponentCategory.FORM)
    context["errors"] = form.errors
    context["type"] = "error"
    return render(request, "insight_ui/storybook.html", context)


@require_GET
def index_view(request: HttpRequest) -> HttpResponse:
    """Render index page."""
    context = get_base_context() | get_sidebar_context()
    return render(request, "insight_ui/index.html", context)


@require_GET
def customization_view(request: HttpRequest) -> HttpResponse:
    """Render customization page."""
    context = get_base_context("customization_view") | get_sidebar_context()
    return render(request, "insight_ui/docs/customization.html", context)


@require_GET
def installation_view(request: HttpRequest) -> HttpResponse:
    """Render installation page."""
    context = get_base_context("installation_view") | get_sidebar_context()
    return render(request, "insight_ui/docs/installation.html", context)


@require_GET
def base_template_view(request: HttpRequest) -> HttpResponse:
    """Render base_template page."""
    context = get_base_context("base_template_view") | get_sidebar_context()
    return render(request, "insight_ui/docs/base_template.html", context)


@require_GET
def icon_view(request: HttpRequest) -> HttpResponse:
    """Render icon page."""
    context = get_icon_context() | get_base_context("icon_view") | get_sidebar_context()
    return render(request, "insight_ui/docs/icons.html", context)


@require_GET
def playground_view(request: HttpRequest) -> HttpResponse:
    """Render playground page."""
    context = get_base_context() | get_sidebar_context() | get_minimal_step_bar_context()

    return render(request, "insight_ui/playground.html", context)


@require_GET
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
    demo_info = {
        "url": reverse("component_demo_view", kwargs={"component_name": component_name}),
        "template_repo_url": TEMPLATE_PATHS.get(component_name, ""),
        "script_repo_url": SCRIPT_PATHS.get(component_name, ""),
        "title": component_name,
        "id": component_name,
    }

    context = get_demo_container_context() | component_context.get_component_context(Component(component_name))
    context["demo"] = demo_info

    # Temporary fix for components with more complex detailpage
    if component_name == "button":
        context["outline_button_demo"] = {
            "url": reverse("component_demo_view", kwargs={"component_name": "outline_button"}),
            "title": "outline_button",
            "id": "outline_button",
        }

        context["button_sizes_demo"] = {
            "url": reverse("component_demo_view", kwargs={"component_name": "button_sizes"}),
            "title": "button_sizes",
            "id": "button_sizes",
        }
    elif component_name == "radio_group":
        context["radio_block_demo"] = {
            "url": reverse("component_demo_view", kwargs={"component_name": "radio_block"}),
            "title": "radio_block",
            "id": "radio_block",
        }
    elif component_name == "card":
        context["effect_cards_demo"] = {
            "url": reverse("component_demo_view", kwargs={"component_name": "effect_cards"}),
            "title": "effect_cards",
            "id": "effect_cards",
        }

    if request.headers.get("HX-Request") and not request.headers.get("HX-History-Restore-Request"):
        # Temporary fix for components with more complex detailpage
        if component_name in ["button", "radio_group", "card"]:
            return render(request, f"insight_ui/docs/partial/{component_name}_detailpage.html", context)

        return render(request, "insight_ui/docs/component_doc.html", context)

    context |= get_base_context("component_detail_page_view") | get_sidebar_context()
    return render(request, "insight_ui/docs/component_detailpage2.html", context)


@require_GET
@xframe_options_exempt
def component_demo_view(request: HttpRequest, component_name: str) -> HttpResponse:
    """
    Render a demo of the specified component.

    Arguments:
    ---------
        request (HttpRequest): request object.
        component_name (str): name of the component.

    Returns:
    -------
        response (HttpResponse): response object.

    """
    component = Component(component_name)

    context = get_base_context() | get_component_demo_context(component)
    context["component"] = component

    # The demo container has a padding but some components should get the whole space
    if component_name in ["navbar", "sidebar", "footer"]:
        context["no_padding"] = True

    return render(request, "insight_ui/docs/components.html", context)


@require_GET
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
    storybook = ComponentCategory(storybook_name)

    context = get_storybook_context(storybook)
    context["storybook"] = storybook

    if not context:
        return HttpResponse("Page not found", status=404)

    if request.headers.get("HX-Request") and not request.headers.get("HX-History-Restore-Request"):
        context["search_query"] = request.GET.get("search", "")
        return render(request, "insight_ui/docs/partial/storybooks/storybook.html", context)

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
    context["view_radio_config"] = {
        "name": "view",
        "param_name": "view",
        "items": [
            {"tag_id": "card-view", "value": "card", "icon": {"name": "cards"}},
            {"tag_id": "table-view", "value": "table", "icon": {"name": "list"}},
            {"tag_id": "carousel-view", "value": "carousel", "icon": {"name": "carousel"}},
        ],
    }

    if view == "card":
        context["cards"] = map_payload_to_cards(payload)
        logger.debug("log: toggle_view - Kartenansicht ausgewählt")
    elif view == "carousel":
        context["cards"] = map_payload_to_cards(payload)
        logger.debug("log: toggle_view - Karussell-Ansicht ausgewählt")
    else:
        # default: table view
        headers, rows = map_payload_to_table(payload)
        context["data"] = {"empty_msg": "Keine Daten vorhanden!", "headers": headers, "rows": rows}
        logger.debug("log: toggle_view - Tabellenansicht ausgewählt")

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
