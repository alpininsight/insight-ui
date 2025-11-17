"""Template-Tags für Insight UI-Komponenten."""

from collections.abc import Mapping, Sequence
from copy import deepcopy
from difflib import HtmlDiff, ndiff, unified_diff
from typing import Any

from django import template
from django.core.paginator import Page
from django.urls import NoReverseMatch, reverse

from insight_ui.utils.diff import file_template, styles

register = template.Library()

JsonPrimitive = str | int | float | bool | None
type JsonMapping = dict[str, "JsonValue"]
type JsonSequence = list["JsonValue"]
type JsonValue = JsonPrimitive | JsonMapping | JsonSequence


def _resolve_view_urls(value: JsonValue) -> JsonValue:
    """Resolve `view_name` entries within nested structures to concrete URLs."""
    if isinstance(value, list):
        return [_resolve_view_urls(item) for item in value]

    if isinstance(value, dict):
        return _resolve_mapping(value)

    return value


def _resolve_mapping(mapping: JsonMapping) -> JsonMapping:
    """Return a copy of the given mapping with resolved view-based URLs."""
    result: JsonMapping = deepcopy(mapping)
    _ensure_resolved_url(result)

    for key, nested_value in list(result.items()):
        if isinstance(nested_value, list | dict):
            result[key] = _resolve_view_urls(nested_value)

    href_value = result.get("href") or result.get("url") or ""
    result["href"] = href_value
    return result


def _ensure_resolved_url(mapping: JsonMapping) -> None:
    """Populate the `url` field when a `view_name` (and optional args) are provided."""
    view_name = mapping.get("view_name")
    if not isinstance(view_name, str) or not view_name:
        return

    view_args = mapping.get("view_args")
    view_arg = mapping.get("view_arg")
    view_kwargs = mapping.get("view_kwargs")

    try:
        if isinstance(view_args, list | tuple):
            mapping["url"] = reverse(view_name, args=list(view_args))
        elif view_arg is not None:
            mapping["url"] = reverse(view_name, args=[view_arg])
        elif isinstance(view_kwargs, dict):
            mapping["url"] = reverse(view_name, kwargs=view_kwargs)
        else:
            mapping["url"] = reverse(view_name)
    except NoReverseMatch:
        mapping["url"] = None


@register.filter
def get_item(dictionary: dict, key: str) -> Any:  # noqa: ANN401
    """Get the specified item of a dictionary."""
    return dictionary.get(key)


@register.inclusion_tag("insight_ui/components/icons.html")
def icon(name: str = "", size: str = "") -> dict[str, Any]:
    """
    Render specified icon with given size.

    Arguments:
    ---------
        name (str or dict): name of the icon or a dict with "name" and "size".
        size (str): size of the icon.

    Returns:
    -------
        icon_dict (dict): a dictionary with the information about the icon.

    """
    if isinstance(name, dict):
        return {"name": name.get("name", ""), "size": name.get("size", "")}

    return {"name": name, "size": size}


@register.filter
def diff(textA: str, textB: str) -> str:  # noqa: N803 (Should be lowercase)
    """
    Generate a visualization of the differences between to texts.

    Arguments:
    ---------
        textA (str): Die ursprüngliche Version des Textes.
        textB (str): Die veränderte Version des Textes.

    Returns:
    -------
        diff (str): Ein HTML Ausschnitt zur grafischen Darstellung der Unterschiede.

    """
    diff = ndiff(textA.split(), textB.split())
    html = ""

    for word in diff:
        if word.startswith("  "):
            html += f"{word[2:]} "
        elif word.startswith("- "):
            html += f"<span class='del'>{word[2:]}</span> "
        elif word.startswith("+ "):
            html += f"<span class='ins'>{word[2:]}</span> "

    return f"""
        <style>
            .del {{ background-color: #f8d7da; color: #721c24; text-decoration: line-through; }}
            .ins {{ background-color: #d4edda; color: #155724; }}
        </style>
        <p class='text-primary'>{html}</p>
    """

    differentiator = HtmlDiff()
    differentiator._file_template = file_template
    differentiator._styles = styles
    diff = unified_diff(textA.splitlines(), textB.splitlines(), lineterm="")
    return "\n".join(list(diff))
    return differentiator.make_file(textA.splitlines(), textB.splitlines())


@register.inclusion_tag("insight_ui/components/navbar.html")
def navbar(config: Mapping[str, Any], **kwargs: JsonValue) -> dict[str, Any]:
    """
    Rendert eine konfigurierbare Navigationsleiste.

    Die folgenden Einstellungen können über das "config" Dictionary angepasst werden.

    brand (dict[str, str]): Title der Anwendung und Logo Informationen
    links (dict[str, str]): Eine Liste von Dictionaries mit Link-Informationen
    show_searchbar (bool):  'True' wenn eine Suchzeile angezeigt werden soll
    show_usermenu (bool): 'True' wenn ein Login/Usermenü angezeigt werden soll
    show_language_selector (bool): 'True' wenn ein Menü zum wechseln der Sprache angezeigt werden soll
    show_theme_toggle (bool): 'True' wenn ein Button zum wechseln Des Themes (Hell/Dunkel) angezeigt werden soll

    Beispiel Branding:
        {
            "title": "Insight UI",
            "logo_url": "path/to/logo.svg or png",
            "logo_alt": "Unser Logo"
        }

    Beispiel Links:
        {
            "text": _("Startseite"),
            "view_name": "storybook_view",  # Wenn eine separate Seite geöffnet werden soll
            "open_modal": "modal-tag-id",  # Wenn ein Modal-Dialog geöffnet werden soll (nur eins von beiden verwenden)
            "active": True,
            "need_auth": False,
            "staff_only": False
        }

    Args:
    ----
        config (dict): Navbar Konfiguration
        **kwargs: Zusätzliche Optionen für die Navbar

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    brand = _resolve_view_urls(config.get("brand")) if config.get("brand") else None
    links = _resolve_view_urls(config.get("links", []))

    return {
        "brand": brand,
        "links": links,
        "searchbar_request_view": config.get("searchbar_request_view"),
        "show_usermenu": config.get("show_usermenu"),
        "show_language_selector": config.get("show_language_selector"),
        "show_theme_toggle": config.get("show_theme_toggle"),
        "options": {**kwargs},
    }


@register.inclusion_tag("insight_ui/components/steps_bar.html")
def step_bar(items: list) -> dict:
    """
    Rendert eine grafische Darstellung von Prozessschritten.

    Arguments:
    ---------
        items (list): Eine Liste der einzelnen Schritte.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"items": items}


@register.inclusion_tag("insight_ui/components/bullet_point_list.html")
def bullet_point_list(items: list = []) -> dict:
    """
    Rendert eine grafische Darstellung einer Bullet-Point Liste.

    Arguments:
    ---------
        items (list): Eine Liste der einzelnen Bullet-Points.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"items": items}


@register.inclusion_tag("insight_ui/components/dropdown.html")
def dropdown(dropdown_menu: list) -> dict:
    """
    Rendert ein Dropdown Menü.

    Arguments:
    ---------
        dropdown_menu (dict): Ein Dictionary welches das Dropdown Menü beschreibt.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"dropdown_menu": dropdown_menu}


@register.inclusion_tag("insight_ui/components/checkbox.html")
def checkbox(checkbox: dict) -> dict:
    """
    Rendert ein oder mehrere Checkbox.

    Arguments:
    ---------
        checkbox (dict): Beschreibt die Checkbox Komponente.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"checkbox": checkbox}


@register.inclusion_tag("insight_ui/components/radio_button.html")
def radio(radio_group: dict, current_value: str) -> dict:
    """
    Rendert ein oder mehrere Radio-Buttons.

    Arguments:
    ---------
        radio_group (dict): Beschreibt die Radio Komponente und deren Items.
        current_value (str): Der Name der aktuell ausgewählten Wertes.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"radio_group": radio_group, "current_value": current_value}


@register.inclusion_tag("insight_ui/components/radio_group.html")
def radio_group(  # noqa: PLR0913 (too many arguments)
    radio_group: dict,
    current_value: str,
    view_name: str = "",
    query_params: str = "",
    target_id: str = "",
    method: str = "",
) -> dict:
    """
    Rendert ein Gruppe von Radio-Buttons.

    Arguments:
    ---------
        radio_group (dict): Beschreibt die Radio Komponente und deren Items.
        current_value (str): Der Name der aktuell ausgewählten Wertes.
        view_name (str): (Optional) Der Name der View an welchen der Request beim wechseln, gesendet werden soll.
        query_params (str): (Optional) Ein String von Query-Parametern
        target_id (str): (Optional) Die ID des HTML-Tags, welches bei wechseln des Wertes ausgetauscht werden soll.
        method (str): Der Name der JavaScript Methode welche ausgeführt werden soll.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {
        "radio_group": radio_group,
        "current_value": current_value,
        "view_name": view_name,
        "query_params": query_params,
        "target_id": target_id,
        "method": method,
    }


@register.inclusion_tag("insight_ui/components/toggle_button.html")
def toggle(toggle: dict, method: str = "") -> dict:
    """
    Rendert ein Toggle-Button.

    Arguments:
    ---------
        toggle (dict): Beschreibt den Toggle-Button.
        method (str): Der Name der JavaScript Methode welche ausgeführt werden soll.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"toggle": toggle, "method": method}


@register.inclusion_tag("insight_ui/components/range_slider.html")
def slider(slider: dict) -> dict:
    """
    Rendert ein Range-Slider.

    Arguments:
    ---------
        slider (dict): Beschreibt den Range-Slider.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"slider": slider}


@register.inclusion_tag("insight_ui/components/chat.html")
def chat(view_name: str) -> dict:
    """
    Rendert ein Chat mit Input Zeile und ein Platz für den Response.

    Arguments:
    ---------
        view_name (str): Der Name der View an welchen der Request gesendet werden soll.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"view_name": view_name}


@register.inclusion_tag("insight_ui/components/geo_map.html")
def geo_map(data: dict = {}, map_height: int = 36) -> dict:
    """
    Rendert eine integrierte geografische Karte.

    Arguments:
    ---------
        data (dict): Einstellungen für die Karte und Daten welche auf der Karte dargestellt werden sollen.
        map_height (int): Die Höhe der Karte in 'rem'.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"data": data, "map_height": map_height}


@register.inclusion_tag("insight_ui/components/list_partial.html")
def paginated_list(current_page: Page, surrounding_pages: list) -> dict:
    """
    Rendert ein Liste mit einer integrierten Pagination.

    Arguments:
    ---------
        current_page (Page): Ein von Django erzeugtes Pagination-Objekt der aktuellen Seite.
        surrounding_pages (list): Eine liste der benachbarten Seiten.
            Siehe: from insight_ui.utils.pagination import get_page

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"current_page": current_page, "surrounding_pages": surrounding_pages}


@register.inclusion_tag("insight_ui/components/generic_filter.html")
def generic_filter(  # noqa: PLR0913 (too many arguments)
    filters: list,
    view_name: str,
    hx_target: str,
    hx_push_url: str = "true",
    vertical: bool = False,
    query_params: dict[str, str] = {},
) -> dict:
    """
    Rendert eine generische Filterung, bestehend aus einem oder mehreren <select> Feldern.

    Arguments:
    ---------
        filters (list): Eine Liste der einzelnen Filter (<select> Feldern).
        view_name (str): Der Name der View an welche der Request gesendet werden soll.
        hx_target (str): Die ID des Containers, dessen Inhalt vom Response ausgetauscht werden soll.
        hx_push_url (str): "true" wenn die ausgewählten Filterwerte in der URL abgebildet werden sollen.
        vertical (bool): 'True' wenn die Filter übereinander angeordnet sein sollen.
        query_params (dict): Ein Dictionary um die Werte der Filter zu setzen.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {
        "filters": filters,
        "view_name": view_name,
        "hx_target": hx_target,
        "hx_push_url": hx_push_url,
        "vertical": vertical,
        "query_params": query_params,
    }


@register.inclusion_tag("insight_ui/components/search_bar.html")
def search_bar(request_view: str, simple: bool = False, search_query: str = "") -> dict:
    """
    Rendert eine Texteingabe für eine beispielsweise eine Suchfunktion.

    Arguments:
    ---------
        request_view (str): Der Name der View an welche der Request gesendet werden soll.
        simple (bool): True wenn die Suchleiste ohne Button und kleiner angezeigt werden soll.
        search_query (str): Ein optionaler Wert der automatisch in dem Textfeld steht.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"request_view": request_view, "simple": simple, "search_query": search_query}


@register.inclusion_tag("insight_ui/components/search_query_builder/sq_builder.html")
def sq_builder(model_fields: list) -> dict:
    """
    Rendert eine Filterung mit welcher sich angelehnt an SQL Queries bauen lassen.

    Arguments:
    ---------
        model_fields (list): Eine Liste der Modell Felder mit möglichen Operatoren, etc.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"model_fields": model_fields}


@register.inclusion_tag("insight_ui/components/toggle_view.html")
def toggle_view(tag_id: str, table_data: list, view_options: list, current_view: str) -> dict:
    """
    Rendert eine Ansicht von Daten, welche auf verschiedene Arten dargestellt werden kann.

    Arguments:
    ---------
        tag_id (str):Eine einzigartige ID für die Komponente. (Wird für den wechsel der Ansicht benötigt).
        table_data (list): Die Daten, welche angezeigt werden sollen.
        view_options (list): Eine Liste aller möglichen Ansichtsarten (Möglichkeiten: "card", "list", "carousel").
        current_view (str): Der name der aktuellen Ansichtsart.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"tag_id": tag_id, "table_data": table_data, "view_options": view_options, "current_view": current_view}


@register.inclusion_tag("insight_ui/components/live_content.html")
def live_content(url: str = "", interval: int = 0, initial_content: str = "", **kwargs: JsonValue) -> dict[str, Any]:
    """
    Rendert einen Container für Live-Updates via HTMX.

    Args:
    ----
        url (str): Die URL an welche der Request für das updaten des Inhalts gesendet werden soll.
        interval (int): Das Intervall für automatische Updates in Sekunden.
        initial_content (str): Initialer Inhalt.
        **kwargs: Zusätzliche Optionen ('id' = Tag-ID).

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    htmx_config = {"url": url, "trigger": f"load, every {interval}s", "swap": "innerHTML"}

    return {"initial_content": initial_content, "htmx": htmx_config, "options": kwargs}


@register.inclusion_tag("insight_ui/components/websocket.html")
def insight_websocket(
    html_tag_id: str = "insight-websocket", ws_url: str = "", initial_content: str = "", **kwargs: JsonValue
) -> dict[str, Any]:
    """
    Rendert eine WebSocket-Komponente als Wrapper für die htmx v2 ws-Extension.

    Args:
    ----
        html_tag_id: Die ID des WebSocket-Containers
        ws_url: Die WebSocket-URL (z.B. ws://localhost:8765)
        initial_content: Initialer Inhalt
        **kwargs: Zusätzliche Optionen

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {"options": {"id": html_tag_id, "ws_url": ws_url, "initial_content": initial_content, **kwargs}}


@register.inclusion_tag("insight_ui/components/infinite_scroll.html")
def infinite_scroll(  # noqa: PLR0913 (Too many arguments)
    items: Sequence[Any] | None = None,
    view_name: str = "",
    request_view: str = "",
    page: int = 1,
    has_next: bool = True,
    auto_fetch: bool = True,
    threshold: int = 100,
    **kwargs: JsonValue,
) -> dict[str, Any]:
    """
    Rendert einen Container für Infinite Scroll.

    Args:
    ----
        items (list): Liste der bereits geladenen Elemente.
        view_name (str): Name der View für das Laden weiterer Elemente.
        request_view (str): Veralteter Alias für `view_name` (wird weiterhin unterstützt)
        page (int): Die Nummer der aktuellen "Seite", welche geladen werden soll.
        has_next (bool): 'True' wenn noch weitere Elemente verfügbar sind.
        auto_fetch (bool): 'False' wenn der Nutzer aktiv weitere Elemente per Button anfordern soll.
        threshold (int): Der Pixel-Schwellenwert für das Laden weiterer Elemente.
        **kwargs: Zusätzliche Optionen ('id' = Tag-ID).

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    resolved_view = view_name or request_view

    resolved_items = list(items) if items is not None else []

    return {
        "items": resolved_items,
        "view_name": resolved_view,
        "page": page,
        "has_next": has_next,
        "auto_fetch": auto_fetch,
        "threshold": threshold,
        "options": kwargs,
    }


@register.inclusion_tag("insight_ui/components/alert.html")
def alert(message: str, alert_type: str = "info", dismissible: bool = True, **kwargs: JsonValue) -> dict[str, Any]:
    """
    Rendert eine barrierefreie Benachrichtigung.

    Args:
    ----
        message: Die Hauptnachricht der Benachrichtigung.
        alert_type: Der Typ der Benachrichtigung ('info', 'success', 'warning', 'error').
        dismissible: True wenn die Benachrichtigung schließbar sein soll.
        **kwargs: Zusätzliche Optionen für die Benachrichtigung ('id' = Tag-ID).

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {"message": message, "type": alert_type, "dismissible": dismissible, "options": kwargs}


@register.inclusion_tag("insight_ui/components/sidebar.html")
def sidebar(
    sidebar_data: Mapping[str, Any] | None = None, side: str = "right", static: bool = True, auto_close: bool = False
) -> dict[str, Any]:
    """
    Rendert eine konfigurierbare Seitennavigation.

    Args:
    ----
        sidebar_data (dict): Der Inhalt der Sidebar (Titel und Navigations-Elemente).
        side (str): Gibt an, an welcher Seite die Sidebar dargestellt werden soll.
        static (bool): True wenn die Sidebar nicht einklappbar sein soll.
        auto_close (bool): True wenn die Sidebar sich automatisch schließen soll, wenn der Cursor sie verlässt.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    resolved_sidebar = _resolve_view_urls(dict(sidebar_data)) if sidebar_data else {}

    return {"sidebar_data": resolved_sidebar, "side": side, "static": static, "auto_close": auto_close}


@register.inclusion_tag("insight_ui/components/breadcrumbs.html")
def breadcrumbs(items: Sequence[Mapping[str, Any]] | None = None) -> dict[str, Any]:
    """
    Rendert eine Breadcrumb-Navigation.

    Args:
    ----
        items (list): Eine Liste von Dictionaries mit den Breadcrumb-Elementen.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    resolved_items = [dict(item) for item in items] if items is not None else []
    return {"items": resolved_items}


@register.inclusion_tag("insight_ui/components/table.html")
def table(table_data: dict) -> dict[str, Any]:
    """
    Rendert eine einfache Tabelle.

    Args:
    ----
        table_data (dict): Ein Dictionary mit den Headern, den Rows und einer Überschrift
        **kwargs: Zusätzliche Optionen für die Tabelle

        Beispiel der Tabellen-Daten:

        "table": {
            "caption": _("Ein Beispiel einer Tabellen-Komponente."),
            "empty_msg": _("Keine Daten vorhanden!"),
            "headers": [...],
            "rows": [...],

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {"table_data": table_data}


@register.inclusion_tag("insight_ui/components/modal.html")
def modal(  # noqa: PLR0913 (too many args)
    html_tag_id: str,
    title: str,
    description: str = "",
    content: str = "",
    actions: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """
    Rendert ein barrierefreies Modal-Dialog.

    Args:
    ----
        html_tag_id (str): Eine eindeutige ID für das Modal.
        title (str): Der Titel des Modals.
        description (str): Eine optionale Beschreibung des Modals.
        content (str): Der Inhalt des Modals (frei definierbarer HTML-Code).
        actions (list): Eine Liste von Aktion-Buttons.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template,

    """
    return {
        "id": html_tag_id,
        "title": title,
        "content": content,
        "description": description,
        "actions": [dict(action) for action in actions] if actions is not None else [],
    }


@register.inclusion_tag("insight_ui/components/carousels/card_carousel.html")
def carousel(  # noqa: PLR0913 (too many args)
    carousel_items: Sequence[Mapping[str, Any]] | None = None,
    autoplay: bool = False,
    show_dots: bool = True,
    show_index: bool = False,
    slides_count: Sequence[int] | None = None,
    items_per_slide: int = 1,
) -> dict[str, Any]:
    """
    Rendert ein Karussell.

    Args:
    ----
        carousel_items (list): Darzustellender Inhalt (Karten)
        autoplay (bool): Wechsle automatisch nach einer bestimmten Zeit (5s) zur nächsten Seite
        show_dots (bool): Zeige Pagination Dots unter dem Inhalt
        show_index (bool): Zeige Anzahl und aktuelle Seite in der unteren rechten Ecke
        slides_count (range): Anzahl der Seiten als Iterable
        items_per_slide (int): Anzahl der Items pro Seite

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {
        "carousel_items": [dict(item) for item in carousel_items] if carousel_items is not None else [],
        "autoplay": autoplay,
        "show_dots": show_dots,
        "show_index": show_index,
        "slides_count": list(slides_count) if slides_count is not None else [],
        "items_per_slide": items_per_slide,
    }


@register.inclusion_tag("insight_ui/components/cards/card.html")
def card(
    title: str, content: str, subtitle: str = "", image: dict[str, str] = {}, actions: list[dict[str, str]] = []
) -> dict[str, Any]:
    """
    Rendert eine Karte mit dem Seitenverhältnis einer Visitenkarte.

    Args:
    ----
        title (str): Der Title der Karte.
        content (str): Der Hauptinhalt der Karte.
        subtitle (str): Der Untertitel der Karte.
        image (dict[url: str, alt: str]): Informationen über das Bild der Karte.
        actions (list[dict[text: str, url: str, type: str]]): Eine Liste von Aktion-Buttons.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"title": title, "subtitle": subtitle, "content": content, "image": image, "actions": actions}


@register.inclusion_tag("insight_ui/components/cards/horizontale_card.html")
def card_horizontale(  # noqa: PLR0913
    title: str,
    content: str,
    tags: list[str] = [],
    url: str = "",
    image: dict[str, str] = {},
    actions: list[dict[str, str]] = [],
) -> dict[str, Any]:
    """
    Rendert eine horizontal ausgerichtete Karte.

    Mit einem Bild am oberen Rand. Darunter befindet sich der Titel und der Content, sowie wenn angegeben,
    eine Liste von Tags. Am Ende werden die angegebenen Action Buttons übereinander dargestellt.

    Args:
    ----
        title (str): Title der Karte
        content (str): Inhalt der Karte
        tags (list[str]): Eine Liste von Buttons
        url (str): Eine URL
        image (dict[url: str, alt: str]): Informationen über das Bild der Karte
        actions (list[dict[text: str, url: str, type: str]]): Eine Liste von Aktionsbuttons

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {"title": title, "content": content, "tags": tags, "url": url, "image": image, "actions": actions}


@register.inclusion_tag("insight_ui/components/cards/flip_card.html")
def card_flip(  # noqa: PLR0913
    title: str,
    content: str,
    tags: list[str] = [],
    url: str = "",
    image: dict[str, str] = {},
    actions: list[dict[str, str]] = [],
) -> dict[str, Any]:
    """
    Rendert eine Karte welche sich um 180° drehen kann und auf der Rückseite weitere Informationen enthält.

    Args:
    ----
        title (str): Title der Karte
        content (str): Inhalt der Karte
        tags (list[str]): Eine Liste von Buttons
        url (str): Eine URL
        image (dict[url: str, alt: str]): Informationen über das Bild der Karte
        actions (list[dict[text: str, url: str, type: str]]): Eine Liste von Aktionsbuttons

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {"title": title, "content": content, "tags": tags, "url": url, "image": image, "actions": actions}


@register.inclusion_tag("insight_ui/components/form.html")
def form(  # noqa: PLR0913 (too many args)
    fields: Sequence[Mapping[str, Any]] | None = None,
    title: str = "",
    description: str = "",
    view_name: str = "",
    method: str = "post",
    actions: Sequence[Mapping[str, Any]] | None = None,
    htmx: Mapping[str, Any] | None = None,
    **kwargs: JsonValue,
) -> dict[str, Any]:
    """
    Rendert ein Formular mit HTMX-Unterstützung.

    Args:
    ----
        fields (list): Eine Liste von Formularfeldern
        title (str): Der Titel des Formulars
        description (str): Eine optionale Beschreibung
        view_name (str): Die Name des Endpunktes für die Formular-Übermittlung
        method (str): Die HTTP-Methode ('post', 'get')
        actions (list): Eine Liste von Aktions-Buttons
        htmx (dict): HTMX Konfiguration für AJAX-Requests
        **kwargs: Zusätzliche Optionen für das Formular

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    # HTMX-Konfiguration
    htmx_config = None
    if htmx:
        htmx_config = {
            "url": htmx.get("url"),
            "method": htmx.get("method"),
            "target": htmx.get("target"),
            "swap": htmx.get("swap"),
            "trigger": htmx.get("trigger"),
            "confirm": htmx.get("confirm"),
            "boost": htmx.get("boost"),
            "validate": kwargs.get("htmx_validate", True),
            "indicator": kwargs.get("htmx_indicator", ".htmx-indicator"),
        }

    return {
        "fields": [dict(field) for field in fields] if fields is not None else [],
        "title": title,
        "description": description,
        "action": view_name,
        "method": method,
        "actions": [dict(action) for action in actions] if actions is not None else [],
        "htmx": htmx_config,
        "options": {**kwargs},
    }


@register.inclusion_tag("insight_ui/components/footer.html")
def footer(data: dict) -> dict[str, Any]:
    """
    Rendert einen Footer mit optionaler Beschreibung, Links und einer Copyright Zeile.

    Args:
    ----
        data (dict): Die Daten welche im Footer angezeigt werden sollen.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"data": _resolve_view_urls(data)}


@register.inclusion_tag("insight_ui/components/accordion.html")
def accordion(items: list, group_id: str = "accordion", exclusive: bool = True) -> dict:
    """
    Rendert ein Accordion welches ein oder mehrere Bereiche geöffnet haben kann.

    Args:
    ----
        items (list): Die einzelnen Bereiche mit Caption und Content.
        group_id (str): Eine eindeutige ID für das Accordion.
        exclusive (bool): True wenn nur ein Bereich gleichzeitig offen sein darf.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {"items": items, "group_id": group_id, "exclusive": exclusive}


@register.inclusion_tag("insight_ui/components/tabs.html")
def tabs(config: dict) -> dict:
    """
    Rendert eine Gruppe von Tabs/Registrierkarten und einen Container für den Inhalt des jeweiligen Tabs.

    Args:
    ----
        config (dict): Enthält die einzelnen Tabs und ein paar allgemeine Informationen über die Komponente.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {"config": config}


@register.inclusion_tag("insight_ui/components/carousels/3D_carousel.html")
def three_d_carousel(
    tag_id: str,
    velocity: int = 1000,
    tilt: int = 0,
    face_camera: bool = False,
    carousel_items: Sequence[Mapping[str, Any]] = [],
) -> dict[str, Any]:
    """
    Rendert eine 3D Variante der Karussell Komponente.

    Args:
    ----
        tag_id (str): Eine eindeutige ID für das Karussell.
        velocity (int): Die Geschwindigkeit mit welcher sich das Karussell drehen soll.
        tilt (int): Die Neigung des Karussell zur Kamera.
        face_camera (bool): True wenn die Karten immer in Richtung der Kamera ausgerichtet sein sollen.
        carousel_items (list): Darzustellender Inhalt (Karten)

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {
        "id": tag_id,
        "velocity": velocity,
        "tilt": tilt,
        "face_camera": face_camera,
        "carousel_items": [dict(item) for item in carousel_items],
    }


@register.inclusion_tag("insight_ui/components/multiselect.html")
def multiselect(  # noqa: PLR0913 (too many arguments)
    name: str = None,
    label: str = None,
    maximum: int = None,
    show_buttons: bool = None,
    values: list[str] = None,
    selected_values: list[str] = None,
    config: dict[str, Any] = None,
) -> dict[str, Any]:
    """
    Rendert eine Auswahlbox, welche mehrere ausgewählte Werte zulässt und eine integrierte Suchzeile hat.

    Args:
    ----
        name (str): Der Name des Multiselect Elements.
        label (str): Ein kurzer Titel, welche rüber dem Multiselect angezeigt wird.
        maximum (int): Gibt an wie viele Werte maximal ausgewählt sein dürfen.
        show_buttons (bool): 'True' zeigt zusätzlich "Alle Auswählen" und "Alle Abwählen" Buttons an.
        values (list[str]): Alle Werte welche ausgewählt werden können.
        selected_values (list[str]): Alle Werte welche bereits ausgewählt sein sollen.
        config (dict[str, Any]): Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    print(config)
    if config is not None:
        name = config.get("name", name)
        label = config.get("label", label)
        maximum = config.get("maximum", maximum)
        show_buttons = config.get("show_buttons", show_buttons)
        values = config.get("values", values)
        selected_values = config.get("selected_values", selected_values)

    return {
        "name": name,
        "label": label,
        "maximum": maximum,
        "show_buttons": show_buttons,
        "values": values,
        "selected_values": selected_values,
    }


@register.inclusion_tag("insight_ui/components/charts/bar_chart.html")
def bar_chart(chart_id: str, chart: dict, chart_height: int = 24) -> dict:
    """
    Rendert ein Bar-Chart mit Apache ECharts.

    Args:
    ----
        chart_id (str): Eine eindeutige ID für das Diagramm.
        chart (dict): Enthält die Informationen und die Daten des Diagramms.
        chart_height (int): Die Höhe des Diagramms in 'rem'.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {"chart_id": chart_id, "chart": chart, "chart_height": chart_height}


@register.inclusion_tag("insight_ui/components/charts/line_chart.html")
def line_chart(chart_id: str, chart: dict, chart_height: int = 24) -> dict:
    """
    Rendert ein Line-Chart mit Apache ECharts.

    Args:
    ----
        chart_id (str): Eine eindeutige ID für das Diagramm.
        chart (dict): Enthält die Informationen und die Daten des Diagramms.
        chart_height (int): Die Höhe des Diagramms in 'rem'.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {"chart_id": chart_id, "chart": chart, "chart_height": chart_height}
