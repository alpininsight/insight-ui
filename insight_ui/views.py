"""Views for Insight UI documentation and component demos."""

from datetime import UTC, datetime
from importlib import metadata
from pathlib import Path

import structlog
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_GET, require_POST

from insight_ui.component_details import component_context
from insight_ui.component_details.components import Component, ComponentCategory
from insight_ui.component_details.demo_context import (
    DEMO_FIELDS,
    get_component_demo_context,
    get_minimal_stepper_context,
)
from insight_ui.component_details.git_path_mapping import SCRIPT_PATHS, TEMPLATE_PATHS
from insight_ui.configs.base import IconConfig
from insight_ui.configs.card import ToggleViewConfig
from insight_ui.configs.input import ButtonConfig, RadioBlockConfig, RadioItemConfig
from insight_ui.configs.layout import BadgeConfig, HeroConfig
from insight_ui.configs.list import PaginationConfig, PaginationIppConfig, TableConfig
from insight_ui.context import (
    get_base_context,
    get_demo_container_context,
    get_icon_context,
    get_sidebar_context,
    get_storybook_context,
)
from insight_ui.demo_utils import generate_payload, map_payload_to_cards, map_payload_to_table
from insight_ui.forms import ChatForm
from insight_ui.utils.pagination import get_page
from insight_ui.utils.query_builder_utils import get_filter_settings_for_field
from insight_ui.utils.type_registry import get_all_type_definitions

logger = structlog.get_logger(__name__)

SOURCE_ROOT = Path(__file__).resolve().parent
SOURCE_PATHS = {"html": TEMPLATE_PATHS, "js": SCRIPT_PATHS}
COMPONENT_NOT_FOUND = "Component not found"
SOURCE_TYPE_NOT_FOUND = "Component source type not found"
SOURCE_NOT_FOUND = "Component source not found"
SOURCE_FILE_NOT_FOUND = "Component source file not found"
LICENSE_FILE_NOT_FOUND = "License file not found"
LICENSE_FILE_NAME = "LICENSE"
PACKAGE_DISTRIBUTION_NAME = "insight-ui"


def _resolve_component_source_path(component_name: str, source_kind: str) -> Path:
    """Resolve an allow-listed component source file from the deployed package.

    Args:
        component_name: The name of the component to look up.
        source_kind: The type of source file ('html' or 'js').

    Returns:
        The resolved path to the source file.

    Raises:
        Http404: If component, source type, or file is not found.

    """
    try:
        Component(component_name)
    except ValueError as exc:
        raise Http404(COMPONENT_NOT_FOUND) from exc

    source_mapping = SOURCE_PATHS.get(source_kind)
    if source_mapping is None:
        raise Http404(SOURCE_TYPE_NOT_FOUND)

    source_path_value = source_mapping.get(component_name)
    if not source_path_value:
        raise Http404(SOURCE_NOT_FOUND)

    source_path = (SOURCE_ROOT / source_path_value).resolve()
    if not source_path.is_relative_to(SOURCE_ROOT) or not source_path.is_file():
        raise Http404(SOURCE_FILE_NOT_FOUND)

    return source_path


def _component_source_url(component_name: str, source_kind: str) -> str:
    """Return an internal source URL only when the deployed file exists.

    Args:
        component_name: The name of the component.
        source_kind: The type of source file ('html' or 'js').

    Returns:
        The URL to the source file, or empty string if not found.

    """
    try:
        _resolve_component_source_path(component_name, source_kind)
    except Http404:
        return ""

    return reverse("component_source_view", kwargs={"component_name": component_name, "source_kind": source_kind})


def _distribution_license_path() -> Path | None:
    """Resolve the license file from installed wheel metadata when available.

    Returns:
        The path to the license file, or None if not found.

    """
    try:
        distribution = metadata.distribution(PACKAGE_DISTRIBUTION_NAME)
    except metadata.PackageNotFoundError:
        return None

    for distribution_file in distribution.files or ():
        if distribution_file.name != LICENSE_FILE_NAME:
            continue

        license_path = Path(distribution.locate_file(distribution_file)).resolve()
        if license_path.is_file():
            return license_path

    return None


def _source_tree_license_path() -> Path | None:
    """Resolve the license file from a local source-tree checkout.

    Returns:
        The path to the license file, or None if not found.

    """
    license_path = (SOURCE_ROOT.parent / LICENSE_FILE_NAME).resolve()
    if not license_path.is_file():
        return None

    return license_path


def _resolve_license_path() -> Path:
    """Resolve the license file from the package, independent of host BASE_DIR.

    Returns:
        The path to the license file.

    Raises:
        Http404: If the license file is not found.

    """
    license_path = _distribution_license_path() or _source_tree_license_path()
    if license_path is None:
        raise Http404(LICENSE_FILE_NOT_FOUND)
    return license_path


def _plain_text_response(file_path: Path) -> HttpResponse:
    """Serve source-like files inline without relying on a remote repository.

    Args:
        file_path: The path to the file to serve.

    Returns:
        An HTTP response with the file contents as plain text.

    """
    response = HttpResponse(file_path.read_text(encoding="utf-8"), content_type="text/plain; charset=utf-8")
    response["Content-Disposition"] = f'inline; filename="{file_path.name}"'
    response["X-Content-Type-Options"] = "nosniff"
    return response


@require_GET
def get_allowed_operators(request: HttpRequest) -> JsonResponse:
    """Retrieve all allowed operators of the given model field.

    Args:
        request: The HTTP request containing 'field' parameter.

    Returns:
        JSON response with operators, values, and input type.

    """
    field = request.GET.get("field")

    if not field:
        return JsonResponse({"error": "Field is required!"}, status=400)

    input_type, allowed_operators, possible_values = get_filter_settings_for_field(DEMO_FIELDS, field)
    return JsonResponse({"operators": allowed_operators, "values": possible_values, "inputType": input_type})


@require_POST
def chat_response(request: HttpRequest) -> HttpResponse:
    """Chat request endpoint to answer on chat messages.

    Args:
        request: The HTTP request containing the chat message.

    Returns:
        Rendered chat response or 204 No Content if invalid.

    """
    form = ChatForm(request.POST)

    if form.is_valid():
        return render(request, "insight_ui/components/chat_response.html", {"msg": form.cleaned_data["msg"]})

    return HttpResponse(status=204)  # no content


@require_GET
def pagination(request: HttpRequest) -> HttpResponse:
    """Pagination endpoint to retrieve data of the desired page.

    Args:
        request: The HTTP request with 'page' and 'ipp' parameters.

    Returns:
        Rendered pagination component or full storybook page.

    """
    page_param = request.GET.get("page")
    ipp_param = request.GET.get("ipp")
    try:
        page_number = int(page_param) if page_param is not None else 1
        ipp = int(ipp_param) if ipp_param is not None else 10
    except (TypeError, ValueError):
        page_number = 1
        ipp = 10

    page_obj, surrounding_pages = get_page(generate_payload(500), ipp, page_number)
    ipp_config = PaginationIppConfig("ipp", _("Items per page"), options=[10, 20, 30], selected_option=ipp)

    if request.headers.get("HX-Request"):
        return render(
            request,
            "insight_ui/components/pagination.html",
            {
                "pagination_config": PaginationConfig(
                    request_url=reverse("pagination"),
                    current_page=page_obj,
                    surrounding_pages=surrounding_pages,
                    ipp_config=ipp_config,
                )
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
    """Endpoint to sort table data.

    Args:
        request: The HTTP request with 'sort' and 'dir' parameters.

    Returns:
        Rendered table component or full storybook page.

    """
    sort = request.GET.get("sort", "name")
    direction = request.GET.get("dir", "asc")

    _, rows = map_payload_to_table(generate_payload())

    context = {"data": rows, "sort": sort, "dir": direction}

    if request.headers.get("HX-Request"):
        return render(request, "insight_ui/components/table.html", context)

    return render(request, "insight_ui/storybook.html", context)


@require_GET
def live_data_view(request: HttpRequest) -> HttpResponse | JsonResponse:
    """HTMX endpoint for live data feed demo.

    Args:
        request: The HTTP request.

    Returns:
        Rendered partial template for HTMX or JSON response.

    """
    current_time = datetime.now(tz=UTC).strftime("%H:%M:%S")
    data = {
        "time": current_time,
        "message": _("Data updated at %(time)s") % {"time": current_time},
        "status": "success",
    }

    if request.headers.get("HX-Request"):
        return render(
            request, "insight_ui/components/live_content_partial.html", {"data": data, "timestamp": current_time}
        )

    return JsonResponse(data)


@require_GET
def more_items_view(request: HttpRequest) -> HttpResponse | JsonResponse:
    """HTMX endpoint for infinite scroll demo.

    Args:
        request: The HTTP request with 'page' and 'auto_fetch' parameters.

    Returns:
        Rendered partial template for HTMX or JSON response.

    """
    page = int(request.GET.get("page", 1))
    items_per_page = 5

    # Simulate more items
    start = (page - 1) * items_per_page + 11  # +11 because we already have 10 items
    end = start + items_per_page

    new_items = [
        {
            "title": _("Element %(i)s") % {"i": i},
            "content": _("Dynamically loaded content for element %(i)s") % {"i": i},
        }
        for i in range(start, end)
    ]

    has_next = page < 5  # noqa: PLR2004 Simulate up to 5 pages
    request_url = reverse("more_items") if has_next else ""
    auto_fetch = request.GET.get("auto_fetch", True)

    if request.headers.get("HX-Request"):
        return render(
            request,
            "insight_ui/components/infinite_scroll_items.html",
            {
                "items": new_items,
                "request_url": request_url,
                "has_next": has_next,
                "auto_fetch": auto_fetch,
                "page": page + 1,
            },
        )

    return JsonResponse(
        {"items": new_items, "has_next": has_next, "auto_fetch": auto_fetch, "request_url": request_url}
    )


@require_GET
def index_view(request: HttpRequest) -> HttpResponse:
    """Render index page."""
    context = get_base_context() | get_sidebar_context()
    context["default_padding"] = False
    context["hero"] = HeroConfig(
        title="Insight UI",
        subtitle=_("A Django Component Framework"),
        description=_(
            "60+ production-ready, WCAG 2.1 AA-compliant components. "
            "Build accessible Django applications without frontend expertise."
        ),
        cta_primary=ButtonConfig(label=_("Get started"), request_url=reverse("installation_view"), type="primary"),
        cta_secondary=ButtonConfig(
            label=_("Browse components"),
            request_url=reverse("storybook_view", kwargs={"storybook_name": "input"}),
            type="secondary",
        ),
        badge_config=BadgeConfig(label=_("Open Source"), icon=IconConfig(name="git", size="s")),
    )
    context["features"] = [
        {
            "icon": "rectangle-group",
            "title": _("60+ Components"),
            "description": _("Pre-built, production-ready components from buttons to charts and data tables."),
        },
        {
            "icon": "check",
            "title": _("WCAG 2.1 AA"),
            "description": _(
                "Full accessibility compliance built-in. Screen reader support, keyboard navigation, ARIA."
            ),
        },
        {
            "icon": "rocket-launch",
            "title": _("HTMX-Powered"),
            "description": _(
                "Interactive components without JavaScript complexity. Partial page updates out of the box."
            ),
        },
        {
            "icon": "code-bracket",
            "title": _("Django-Native"),
            "description": _("Template tags and dataclass configs. Use Python, not JavaScript, to build your UI."),
        },
        {
            "icon": "moon",
            "title": _("Dark Mode"),
            "description": _("Light and dark themes with smooth transitions. Respects user system preferences."),
        },
        {
            "icon": "globe-alt",
            "title": _("RTL Support"),
            "description": _("Full right-to-left layout support for Arabic, Hebrew, Persian and other RTL languages."),
        },
    ]
    context["stats"] = [
        {"value": "60+", "label": _("Components")},
        {"value": "WCAG 2.1", "label": _("Accessibility")},
        {"value": "RTL", "label": _("Layout Support")},
        {"value": "0", "label": _("JavaScript Required")},
    ]
    context["checklist"] = [
        _("You have a Django application that needs a frontend?"),
        _("You need to quickly prototype a PoC?"),
        _("You prefer backend development over frontend?"),
        _("You want accessibility compliance without the complexity?"),
        _("You'd rather not design basic UI components from scratch?"),
    ]
    context["base_template_blocks"] = [
        {"name": "{% block navbar %}", "icon": "bars-3", "description": _("Fixed navigation bar")},
        {"name": "{% block sidebar_left %}", "icon": "rectangle-group", "description": _("Static left sidebar")},
        {"name": "{% block content %}", "icon": "document-text", "description": _("Main content area")},
        {"name": "{% block sidebar_right %}", "icon": "rectangle-group", "description": _("Static right sidebar")},
        {"name": "{% block footer %}", "icon": "computer-desktop", "description": _("Page footer")},
    ]
    context["customization_options"] = [
        {
            "icon": "adjustments-horizontal",
            "title": _("Settings"),
            "description": _("Configure favicons, SEO, external libraries, and UI behavior via Django settings."),
            "file": "settings.py",
        },
        {
            "icon": "sparkles",
            "title": _("Theming"),
            "description": _("Define colors, fonts, and component styles with CSS tokens. Dark mode included."),
            "file": "input.css",
        },
        {
            "icon": "code-bracket",
            "title": _("Templates"),
            "description": _("Override any component template by placing it in your project's template directory."),
            "file": "templates/",
        },
    ]
    context["a11y_features"] = [
        _("Semantic HTML elements"),
        _("ARIA labels & roles"),
        _("Keyboard navigation"),
        _("Screen reader support"),
        _("Focus management"),
        _("4.5:1 contrast ratios"),
    ]
    # Build component categories with counts
    category_icons = {
        ComponentCategory.LAYOUT: "rectangle-group",
        ComponentCategory.NAVIGATION: "globe-alt",
        ComponentCategory.INPUT: "cursor-arrow-rays",
        ComponentCategory.POPUP: "chat-bubble-bottom-center-text",
        ComponentCategory.UTIL: "wrench-screwdriver",
        ComponentCategory.LIST: "queue-list",
        ComponentCategory.FILTER: "magnifying-glass",
        ComponentCategory.CARD: "squares-2x2",
        ComponentCategory.FORM: "clipboard",
    }
    category_counts: dict[ComponentCategory, int] = {}
    for component in Component:
        category_counts[component.group] = category_counts.get(component.group, 0) + 1
    context["component_categories"] = [
        {
            "name": category.formatted_name,
            "icon": category_icons.get(category, "rectangle-group"),
            "count": category_counts.get(category, 0),
            "url": reverse("storybook_view", kwargs={"storybook_name": category.value}),
        }
        for category in ComponentCategory
    ]
    context["addon_packages"] = [
        {
            "name": "Insight UI User",
            "icon": "user",
            "status": "available",
            "description": _("User profile components — avatars, profile cards, account settings, and activity feeds."),
            "url": "#",
        },
        {
            "name": "Insight UI Flows",
            "icon": "cube-transparent",
            "status": "available",
            "description": _(
                "Visual node editor for workflows — perfect for AI agent pipelines, "
                "automation builders, or logic designers."
            ),
            "url": "#",
        },
        {
            "name": "Insight UI WebGL",
            "icon": "computer-desktop",
            "status": "early",
            "description": _(
                "3D components for web applications — scene viewers, model inspectors, and interactive visualizations."
            ),
            "url": "#",
        },
        {
            "name": "Insight UI Diagrams",
            "icon": "share",
            "status": "planned",
            "description": _("Diagram components — flowcharts, org charts, mind maps, and data visualizations."),
            "url": "#",
        },
    ]
    return render(request, "insight_ui/index.html", context)


@require_GET
def customization_view(request: HttpRequest) -> HttpResponse:
    """Render customization page."""
    context = get_base_context() | get_sidebar_context()
    return render(request, "insight_ui/docs/customization.html", context)


@require_GET
def installation_view(request: HttpRequest) -> HttpResponse:
    """Render installation page."""
    context = get_base_context() | get_sidebar_context()
    return render(request, "insight_ui/docs/installation.html", context)


@require_GET
def base_template_view(request: HttpRequest) -> HttpResponse:
    """Render base_template page."""
    context = get_base_context() | get_sidebar_context()
    return render(request, "insight_ui/docs/base_template.html", context)


@require_GET
def icon_view(request: HttpRequest) -> HttpResponse:
    """Render icon page."""
    context = get_icon_context() | get_base_context() | get_sidebar_context()
    return render(request, "insight_ui/docs/icons.html", context)


@require_GET
def types_view(request: HttpRequest) -> HttpResponse:
    """Render types documentation page."""
    context = get_base_context() | get_sidebar_context()
    context["type_definitions"] = get_all_type_definitions()
    return render(request, "insight_ui/docs/types.html", context)


@require_GET
def playground_view(request: HttpRequest) -> HttpResponse:
    """Render playground page."""
    context = get_base_context() | get_sidebar_context() | get_minimal_stepper_context()

    return render(request, "insight_ui/playground.html", context)


@require_GET
def component_detail_page_view(request: HttpRequest, component_name: str) -> HttpResponse:
    """Render detailpage of the specified component.

    Args:
        request: The HTTP request object.
        component_name: Name of the component.

    Returns:
        Rendered component detail page or partial template for HTMX.

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

    if request.headers.get("HX-Request") and not request.headers.get("HX-History-Restore-Request"):
        return render(request, "insight_ui/docs/component_detailpage_partial.html", context)

    context |= get_base_context() | get_sidebar_context()
    return render(request, "insight_ui/docs/component_detailpage.html", context)


@require_GET
def component_source_view(_request: HttpRequest, component_name: str, source_kind: str) -> HttpResponse:
    """Serve component source code from the deployed container package."""
    return _plain_text_response(_resolve_component_source_path(component_name, source_kind))


@require_GET
def license_view(_request: HttpRequest) -> HttpResponse:
    """Serve the license text from the deployed container instead of GitHub."""
    return _plain_text_response(_resolve_license_path())


@require_GET
@xframe_options_exempt
def component_demo_view(request: HttpRequest, component_name: str) -> HttpResponse:
    """Render a demo of the specified component.

    Args:
        request: The HTTP request object.
        component_name: Name of the component.

    Returns:
        Rendered component demo page.

    """
    component = Component(component_name)

    context = get_base_context() | get_component_demo_context(component)
    context["component"] = component

    return render(request, "insight_ui/docs/components.html", context)


@require_GET
def storybook_view(request: HttpRequest, storybook_name: str) -> HttpResponse:
    """Render all components of the specified storybook.

    Args:
        request: The HTTP request object.
        storybook_name: Name of the storybook category.

    Returns:
        Rendered storybook page or partial template for HTMX.

    """
    storybook = ComponentCategory(storybook_name)

    context = get_storybook_context(storybook)
    context["storybook"] = storybook

    # Retrieve demo information for each component
    demos = [
        {
            "url": reverse("component_demo_view", kwargs={"component_name": component.value}),
            "title": component.value,
            "id": component.value,
        }
        for component in context["components"]
    ]

    # Connect components with related demo information
    context["components"] = zip(context["components"], demos, strict=True)

    if not context:
        return HttpResponse("Page not found", status=404)

    if request.headers.get("HX-Request") and not request.headers.get("HX-History-Restore-Request"):
        context["search_query"] = request.GET.get("search", "")
        return render(request, "insight_ui/docs/storybook_partial.html", context)

    return render(request, "insight_ui/docs/storybook.html", context)


@require_GET
def toggle_view(request: HttpRequest) -> HttpResponse:
    """Toggle between table and card views, based on the `view` GET parameter.

    Loads and maps payload data to the appropriate format.

    Args:
        request: The HTTP request with 'products-view-toggle' parameter.

    Returns:
        Rendered toggle view component.

    """
    current_view = request.GET.get("products-view-toggle", "table")
    valid_views = {"table", "card", "carousel"}

    if current_view not in valid_views:
        logger.warning("log: toggle_view - Received invalid 'view' parameter: %s. Fallback to 'table'.", current_view)
        current_view = "table"

    view_radio_config = RadioBlockConfig(
        "products-view-toggle",
        items=[
            RadioItemConfig("card-view", "card", icon=IconConfig("squares-2x2")),
            RadioItemConfig("table-view", "table", icon=IconConfig("list-bullet")),
            RadioItemConfig("carousel-view", "carousel", icon=IconConfig("square-3-stack-3d")),
        ],
        request_url=reverse("toggle_view"),
        current_value=current_view,
    )

    # Generate the base payload
    payload = generate_payload()
    cards = []
    table_config = None
    if current_view == "card":
        cards = map_payload_to_cards(payload)
        logger.debug("log: toggle_view - Card view selected")
    elif current_view == "carousel":
        cards = map_payload_to_cards(payload)
        logger.debug("log: toggle_view - Carousel view selected")
    else:
        # default: table view
        headers, rows = map_payload_to_table(payload)
        table_config = TableConfig(headers, rows)
        logger.debug("log: toggle_view - Table view selected")

    return render(
        request,
        "insight_ui/components/toggle_view.html",
        {
            "toggle_view_config": ToggleViewConfig(
                tag_id="products-view",
                cards=cards,
                table_config=table_config,
                view_radio_config=view_radio_config,
                current_view=current_view,
            )
        },
    )


@require_GET
def tabs_view(request: HttpRequest, tab_id: str) -> HttpResponse:
    """Switch content of the Tabs-Component corresponding to the given 'tab_id'.

    Args:
        request: The HTTP request.
        tab_id: The identifier of the tab to display ('second', 'third', etc.).

    Returns:
        Rendered tab content template.

    """
    msg = _("This is the content of the first tab!")
    match tab_id:
        case "second":
            msg = _("This is the content of the second tab!")
        case "third":
            msg = _("This is the content of the third tab!")

    return render(request, "insight_ui/components/tabs_content.html", {"message": msg})
