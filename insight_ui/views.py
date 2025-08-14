from datetime import UTC, datetime

import structlog
from django.core.paginator import Page, Paginator
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET, require_http_methods

from insight_ui import config
from insight_ui.forms import ChatForm

logger = structlog.get_logger(__name__)


def get_nav_and_footer_context() -> dict:
    """Stellt Inhalt für die Navigation und den Footer bereit."""
    return config.get_config() | {
        "nav_config": {
            "brand": {
                "title": "Django Insight UI NavBar",
                "view_name": "storybook_view",
                "logo_url": "insight_ui/svg/ai-logo.svg",
                "logo_alt": "Insight UI Logo",
            },
            "links": [
                {
                    "text": _("Startseite"),
                    "icon": {"name": "home", "size": "small"},
                    "view_name": "storybook_view",
                    "active": True,
                    "need_auth": False,
                    "staff_only": False,
                },
                {
                    "text": _("Dokumentation"),
                    "view_name": "storybook_view",
                    "active": False,
                    "need_auth": False,
                    "staff_only": False,
                },
                {
                    "text": _("Über"),
                    "open_modal": "about-modal",
                    "active": False,
                    "need_auth": False,
                    "staff_only": False,
                },
                {
                    "text": _("Test"),
                    "view_name": "storybook_view",
                    "active": False,
                    "need_auth": True,
                    "staff_only": False,
                },
                {
                    "text": _("Test2"),
                    "view_name": "storybook_view",
                    "active": False,
                    "need_auth": True,
                    "staff_only": True,
                },
            ],
            "searchbar_request_view": "storybook_view",
            "show_usermenu": True,
            "show_language_selector": True,
            "show_theme_toggle": True,
        },
        "user_dropdown_links": [
            {
                "text": _("Einstellungen"),
                "view_name": "storybook_view",
                "staff_only": False,
                "icon": {"name": "cog", "size": "small"},
            },
            {
                "text": _("Administration"),
                "view_name": "admin:index",
                "staff_only": True,
                "icon": {"name": "home", "size": "small"},
            },
            {
                "text": _("Übersetzung"),
                "view_name": "storybook_view",  # rosetta-home
                "staff_only": True,
                "icon": {"name": "globe", "size": "small"},
            },
        ],
        "footer_data": {
            "description": {
                "title": "Django Insight UI",
                "text": "Eine moderne UI-Bibliothek für Django-Anwendungen mit Fokus auf Barrierefreiheit und Benutzerfreundlichkeit.",  # noqa: E501
            },
            "links": [
                {"text": _("Startseite"), "icon": {"name": "home", "size": "small"}, "view_name": "storybook_view"},
                {"text": _("Storybook"), "view_name": "storybook_view"},
                {"text": _("Dokumentation"), "view_name": "storybook_view"},
            ],
        },
    }


def get_storybook_context() -> dict:
    """Hilfsfunktion für Index-Seiten Context."""
    page_obj, surrounding_pages = get_page(generate_payload(100))

    # Toggle-View: Initiale Tabellendaten für das Storybook bereitstellen
    payload = generate_payload()
    headers, rows = map_payload_to_table(payload)

    return get_nav_and_footer_context() | {
        "breadcrumb_items": [
            {"text": _("Startseite"), "view_name": "storybook_view", "icon": {"name": "home", "size": "small"}},
            {"text": _("Demo"), "view_name": "storybook_view"},
            {"text": _("Komponenten")},
        ],
        "table": {
            "caption": _("Ein Beispiel einer Tabellen-Komponente."),
            "empty_msg": _("Keine Daten vorhanden!"),
            "headers": [_("Name"), _("E-Mail"), _("Status"), _("Aktionen")],
            "rows": [
                [
                    "Max Mustermann",
                    "max@example.com",
                    _("Aktiv"),
                    format_html(
                        '<button class="bg-insight-primary border-insight-primary border-2 rounded-sm text-white px-6 py-2 hover:bg-insight-primary-hover active:bg-insight-primary-active hover:border-insight-primary-hover active:border-insight-primary-active transition">Bearbeiten</button>'  # noqa: E501
                    ),
                ],
                [
                    "Anna Schmidt",
                    "anna@example.com",
                    _("Inaktiv"),
                    format_html(
                        '<button class="bg-insight-primary border-insight-primary border-2 rounded-sm text-white px-6 py-2 hover:bg-insight-primary-hover active:bg-insight-primary-active hover:border-insight-primary-hover active:border-insight-primary-active transition">Bearbeiten</button>'  # noqa: E501
                    ),
                ],
                [
                    "Tom Weber",
                    "tom@example.com",
                    _("Aktiv"),
                    format_html(
                        '<button class="bg-insight-primary border-insight-primary border-2 rounded-sm text-white px-6 py-2 hover:bg-insight-primary-hover active:bg-insight-primary-active hover:border-insight-primary-hover active:border-insight-primary-active transition">Bearbeiten</button>'  # noqa: E501
                    ),
                ],
            ],
        },
        "cards": [
            {
                "title": "Beispiel-Karte",
                "subtitle": "Untertitel",
                "content": "Dies ist der Inhalt einer Karte.",
                "actions": [
                    {"text": _("Mehr erfahren"), "url": "#", "type": "secondary"},
                    {"text": _("Teilen"), "url": "#", "type": "primary"},
                ],
            },
            {
                "title": "Karte mit Aktionen",
                "content": "Diese Karte hat Aktions-Buttons.",
                "actions": [
                    {"text": _("Mehr erfahren"), "url": "#", "type": "secondary"},
                    {"text": _("Teilen"), "url": "#", "type": "primary"},
                ],
            },
        ],
        "horizontale_cards": [
            {
                "title": "Horizontale Karte",
                "content": "Eine Karte dessen Inhalt horizontal angeordnet ist.",
                "image": {"url": static("insight_ui/img/thumbnail.png"), "alt": "Card-Image"},
                "tags": ["Test", "Test2", "Test3"],
                "actions": [
                    {"text": _("Mehr erfahren"), "url": "#", "type": "secondary"},
                    {"text": _("Teilen"), "url": "#", "type": "primary"},
                ],
            }
        ],
        "flip_cards": [
            {
                "title": "Flip Karte",
                "content": "Eine Karte die sich um 180° dreht und weiteren Inhalt auf der Rückseite bereit hält.",
                "image": {"url": static("insight_ui/img/thumbnail.png"), "alt": "Card-Image"},
                "tags": ["Test", "Test2", "Test3"],
                "actions": [
                    {"text": _("Mehr erfahren"), "url": "#", "type": "secondary"},
                    {"text": _("Teilen"), "url": "#", "type": "primary"},
                ],
            }
        ],
        "form_fields": [
            {
                "type": "text",
                "name": "name",
                "label": _("Name"),
                "placeholder": _("Ihr vollständiger Name"),
                "required": True,
            },
            {
                "type": "email",
                "name": "email",
                "label": _("E-Mail"),
                "placeholder": _("ihre.email@example.com"),
                "required": True,
            },
            {
                "type": "textarea",
                "name": "message",
                "label": _("Nachricht"),
                "placeholder": _("Ihre Nachricht..."),
                "rows": 4,
            },
        ],
        "form_actions": [
            {"text": _("Absenden"), "type": "submit", "style": "primary"},
            {"text": _("Zurücksetzen"), "type": "reset", "style": "secondary"},
        ],
        "confirm_modal_actions": [
            {"text": _("Ja, fortfahren"), "type": "primary", "onclick": 'alert("Aktion bestätigt!")'},
            {"text": _("Abbrechen"), "type": "cancel", "dismiss": True},
        ],
        "right_sidebar_items": [
            {
                "text": _("Benachrichtigungen"),
                "icon": {"name": "home", "size": "small"},
                "url": reverse("storybook_view"),
            },
            {"text": _("Nachrichten"), "icon": {"name": "home", "size": "small"}, "url": reverse("storybook_view")},
            {"text": _("Aufgaben"), "icon": {"name": "home", "size": "small"}, "url": reverse("storybook_view")},
            {"text": _("Kalender"), "icon": {"name": "home", "size": "small"}, "url": reverse("storybook_view")},
            {"text": _("Profil"), "icon": {"name": "home", "size": "small"}, "url": reverse("storybook_view")},
        ],
        "left_sidebar_items": [
            {"text": _("Dashboard"), "icon": {"name": "home", "size": "small"}, "url": reverse("storybook_view")},
            {"text": _("Benutzer"), "icon": {"name": "home", "size": "small"}, "url": reverse("storybook_view")},
            {"text": _("Einstellungen"), "icon": {"name": "home", "size": "small"}, "url": reverse("storybook_view")},
            {"text": _("Hilfe"), "icon": {"name": "home", "size": "small"}, "url": reverse("storybook_view")},
        ],
        "scroll_items": [{"title": f"Element {i}", "content": f"Inhalt für Element {i}"} for i in range(1, 11)],
        "htmx_config": {"url": "/api/form-submit/", "method": "post", "target": "#htmx-form", "swap": "innerHTML"},
        "carousel_items": map_payload_to_cards(generate_payload()),
        "image_carousel_items": [
            {"description": "Test Bild 1", "url": static("insight_ui/img/text-services-main.png"), "alt": "Image 1"},
            {
                "description": "Test Bild 2",
                "url": static("insight_ui/img/text-services-response.png"),
                "alt": "Image 2",
            },
            {
                "description": "Test Bild 3",
                "url": static("insight_ui/img/text-services-response2.png"),
                "alt": "Image 3",
            },
        ],
        "range_total_slides": range(3),
        "start_page": {"page_obj": page_obj, "surrounding_pages": surrounding_pages},
        "toggle_table": {"empty_msg": "Keine Daten vorhanden!", "headers": headers, "rows": rows},
        "toggle_start_view": "table",
        "view_options": {
            "name": "view-options",
            "param_name": "view",
            "options": [
                {"id": "card-view", "value": "card", "icon": {"name": "card"}},
                {"id": "table-view", "value": "table", "icon": {"name": "list"}},
                {"id": "carousel-view", "value": "carousel", "icon": {"name": "carousel"}},
            ],
        },
    }


def chat_response(request: HttpRequest) -> HttpResponse:
    """Chat request endpoint to answer on chat messages."""
    form = ChatForm(request.POST)

    if form.is_valid():
        return render(request, "insight_ui/components/chat_response.html", {"msg": form.cleaned_data["msg"]})

    return HttpResponse(status=204)  # no content


def get_page(data: list, page: int = 1, max_neighbor_pages: int = 6) -> tuple[Page, list[str]]:
    """
    Create pagination for given data.

    Retrieve data of the desired page and calculate page number of neighboring pages.

    Arguments:
    ---------
        data (list): data to create pagination for.
        page (int): desired page number.
        max_neighbor_pages (int): the maximal amount of pages, next to the desired page.

    Returns:
    -------
        page, neighbor_pages (Page, List[str]): the desired page and a list of neighboring pages.

    """
    paginator = Paginator(data, 10)

    # Calculate neighboring pages
    surrounding_pages = []
    half = max_neighbor_pages // 2

    # Calculate start page and end page
    start = max(1, page - half)
    end = min(paginator.num_pages, page + half)

    # Adjust if there are not enough pages before the current page
    if page - start < half:
        end = min(paginator.num_pages, end + (half - (page - start)))

    # Adjust if there are not enough pages after the current page
    if end - page < half:
        start = max(1, start - (half - (end - page)))

    # Create list of neighboring pages
    surrounding_pages = list(range(start, end + 1))

    page_links = []
    for i in range(1, paginator.num_pages + 1):
        if i in surrounding_pages:
            page_links.append(i)
        elif i == 1 or i == paginator.num_pages or (i in surrounding_pages and i not in page_links[-1:]):
            page_links.append("...")

    return paginator.get_page(page), page_links


def pagination(request: HttpRequest) -> HttpResponse:
    """Pagination endpoint to retrieve data of the desired page."""
    page_obj, surrounding_pages = get_page(generate_payload(100), int(request.GET.get("page")))

    if request.htmx:
        return render(
            request,
            "insight_ui/components/list_partial.html",
            {"pagination": {"page_obj": page_obj, "surrounding_pages": surrounding_pages}},
        )

    context = get_storybook_context()
    context["page_obj"] = {"page_obj": page_obj, "surrounding_pages": surrounding_pages}
    return render(request, "insight_ui/storybook.html", context)


@require_http_methods(["GET"])
def live_data_view(request: HttpRequest) -> HttpResponse | JsonResponse:
    """HTMX Endpoint für Live-Daten."""
    current_time = datetime.now(tz=UTC).strftime("%H:%M:%S")
    data = {
        "time": current_time,
        "message": _("Daten aktualisiert um %(time)s") % {"time": current_time},
        "status": "success",
    }

    if request.headers.get("HX-Request"):
        # HTMX Request - nur den Inhalt zurückgeben
        html = render_to_string(
            "insight_ui/components/live_content_partial.html", {"data": data, "timestamp": current_time}
        )
        return HttpResponse(html)

    # Normale Request - JSON zurückgeben
    return JsonResponse(data)


@require_http_methods(["GET"])
def more_items_view(request: HttpRequest) -> HttpResponse | JsonResponse:
    """HTMX Endpoint für Infinite Scroll."""
    page = int(request.GET.get("page", 1))
    items_per_page = 5

    # Simuliere mehr Items
    start = (page - 1) * items_per_page + 11  # +11 weil wir schon 10 Items haben
    end = start + items_per_page

    new_items = [
        {"title": f"Element {i}", "content": f"Dynamisch geladener Inhalt für Element {i}"} for i in range(start, end)
    ]

    has_next = page < 5  # noqa: PLR2004 Simuliere max 5 Seiten
    request_view = "more_items" if has_next else ""

    if request.headers.get("HX-Request"):
        html = render_to_string(
            "insight_ui/components/infinite_scroll_items.html",
            {"items": new_items, "request_view": request_view, "has_next": has_next, "page": page + 1},
        )
        return HttpResponse(html)

    return JsonResponse({"items": new_items, "has_next": has_next, "request_view": request_view})


@require_http_methods(["POST"])
def form_submit(request: HttpRequest) -> HttpResponse | JsonResponse:
    """
    Endpoint for form validation and handling.

    Works with standard and htmx requests. Handle form issues and return either
    partial template data if this is a htmx request or do a whole page reload.
    """
    # Debug: Alle POST-Daten loggen
    logger.debug("Empfangene POST-Daten: %s", request.POST)
    logger.debug("Content-Type: %s", request.content_type)

    # Eingabedaten extrahieren
    name = request.POST.get("name", "")
    email = request.POST.get("email", "")
    message = request.POST.get("message", "")

    logger.info("Extrahierte Werte - Name: '%s', Email: '%s', Message: '%s'", name, email, message)

    # Einfache Validierung
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
        context = get_storybook_context()
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
    context = get_storybook_context()
    context["form_success"] = {
        "message": _("Normales Formular erfolgreich übermittelt!"),
        "name": name,
        "email": email,
        "type": "success",
    }

    return render(request, "insight_ui/storybook.html", context)


def storybook_view(request: HttpRequest) -> HttpResponse:
    """Hauptseite mit allen Insight UI Komponenten."""
    context = get_storybook_context()
    context["search_query"] = request.GET.get("search", "")

    return render(request, "insight_ui/storybook.html", context)


def generate_payload(count: int = 5) -> list:
    """Erstellt eine zufällige Anzahl von Einträgen als Payload-Daten."""
    return [
        {
            "title": f"Element {i}",
            "content": f"Dies ist der Inhalt von Eintrag {i}.",
            "status": "Aktiv" if i % 2 == 0 else "Inaktiv",
            "actions": [
                {"text": "Mehr erfahren", "url": "#", "type": "primary"},
                {"text": "Teilen", "url": "#", "type": "secondary"},
            ],
            "action_link": f"<a href='#' class='underline text-insight-text-link hover:text-insight-text-link-hover'>Details {i}</a>",  # noqa: E501
        }
        for i in range(1, count + 1)
    ]


def map_payload_to_cards(payload: list) -> list:
    """Mappt Payload-Daten auf Karten-Darstellung."""
    return [
        {"title": item["title"], "subtitle": item["status"], "content": item["content"], "actions": item["actions"]}
        for item in payload
    ]


def map_payload_to_table(payload: list) -> tuple[list[str], list]:
    """Mappt Payload-Daten auf Tabellen-Darstellung."""
    headers = ["Title", "Status", "Content", "URL"]
    rows = [[item["title"], item["status"], item["content"], item["action_link"]] for item in payload]
    return headers, rows


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
    context = {"current_view": view, "id": request.GET.get("id", "")}
    context["view_options"] = {
        "name": "view-options",
        "param_name": "view",
        "options": [
            {"id": "card-view", "value": "card", "icon": {"name": "card"}},
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
