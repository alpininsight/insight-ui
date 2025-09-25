"""Template-Tags für Insight UI-Komponenten."""

from difflib import HtmlDiff, ndiff, unified_diff
from typing import Any

from django import template
from django.core.paginator import Page

from insight_ui.utils.diff import file_template, styles

register = template.Library()


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
def diff(text1: str, text2: str) -> str:
    """Generate a visualization of the differences between to texts."""
    diff = ndiff(text1.split(), text2.split())
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
        <p>{html}</p>
    """

    differentiator = HtmlDiff()
    differentiator._file_template = file_template
    differentiator._styles = styles
    diff = unified_diff(text1.splitlines(), text2.splitlines(), lineterm="")
    return "\n".join(list(diff))
    return differentiator.make_file(text1.splitlines(), text2.splitlines())


@register.inclusion_tag("insight_ui/components/navbar.html")
def navbar(config: dict, **kwargs) -> dict[str, Any]:
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
    return {
        "brand": config.get("brand"),
        "links": config.get("links"),
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
def bullet_point_list(items: list) -> dict:
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
        checkbox (dict): Ein Dictionary welches das Checkbox Komponente beschreibt.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"checkbox": checkbox}


@register.inclusion_tag("insight_ui/components/radio_button.html")
def radio(radio: dict) -> dict:
    """
    Rendert ein oder mehrere Radio-Buttons.

    Arguments:
    ---------
        radio (dict): Ein Dictionary welches das Radio Komponente beschreibt.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"radio": radio}


@register.inclusion_tag("insight_ui/components/toggle_button.html")
def toggle(toggle: dict) -> dict:
    """
    Rendert ein Toggle-Button.

    Arguments:
    ---------
        toggle (dict): Ein Dictionary welches den Toggle-Button beschreibt.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"toggle": toggle}


@register.inclusion_tag("insight_ui/components/range_slider.html")
def slider(slider: dict) -> dict:
    """
    Rendert ein Range-Slider.

    Arguments:
    ---------
        slider (dict): Ein Dictionary welches den Range-Slider beschreibt.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"slider": slider}


@register.inclusion_tag("insight_ui/components/radio_group.html")
def radio_group(
    radio_group: list, current_value: str, view_name: str = "", query_params: str = "", target_id: str = ""
) -> dict:
    """
    Rendert ein Gruppe von Radio-Buttons.

    Arguments:
    ---------
        radio_group (list): Ein Dictionary welches das Dropdown Menü beschreibt.
        current_value (str): Der Name der aktuell ausgewählten Wertes.
        view_name (str): (Optional) Der Name der View an welchen der Request beim wechseln, gesendet werden soll.
        query_params (str): (Optional) Ein String von Query-Parametern
        target_id (str): (Optional) Die ID des HTML-Tags, welches bei wechseln des Wertes ausgetauscht werden soll.

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
    }


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
def geo_map(data: list = []) -> dict:
    """
    Rendert eine integrierte geografische Karte.

    Arguments:
    ---------
        data (list): Eine Liste von Objekten, welche auf der Karte dargestellt werden sollen.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"data": data}


@register.inclusion_tag("insight_ui/components/list_partial.html")
def paginated_list(current_page: Page, surrounding_pages: list) -> dict:
    """
    Rendert ein Liste mit einer integrierten Pagination.

    Arguments:
    ---------
        current_page (Page): Ein von Django erzeugtes Pagination-Objekt.
        surrounding_pages (list): Eine liste der benachbarten Seiten.
            Siehe: from insight_ui.utils.pagination import get_page

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"current_page": current_page, "surrounding_pages": surrounding_pages}


@register.inclusion_tag("insight_ui/components/generic_filter.html")
def generic_filter(filters: list, view_name: str) -> dict:
    """
    Rendert eine generische Filterung, bestehend aus einem oder mehreren <select> Feldern.

    Arguments:
    ---------
        filters (list): Eine Liste der einzelnen Filter (<select> Feldern).
        view_name (str): Der Name der View an welche der Request gesendet werden soll.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"filters": filters, "view_name": view_name}


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
def live_content(url: str = "", interval: int = 0, initial_content: str = "", **kwargs) -> dict[str, Any]:
    """
    Rendert einen Container für Live-Updates via HTMX.

    Args:
    ----
        url (str): Die URL für HTMX-Updates
        interval (int): Intervall für automatische Updates in Millisekunden
        initial_content (str): Initialer Inhalt
        **kwargs: Zusätzliche Optionen

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    htmx_config = {}

    if url:
        htmx_config = {
            "url": url,
            "trigger": kwargs.get("trigger", f"load, every {interval}s"),
            "swap": kwargs.get("swap", "innerHTML"),
        }
        if interval != 0:
            htmx_config["interval"] = interval

    return {"initial_content": initial_content, "options": {**kwargs, "htmx": htmx_config if htmx_config else None}}


@register.inclusion_tag("insight_ui/components/websocket.html")
def insight_websocket(
    html_tag_id: str = "insight-websocket", ws_url: str = "", initial_content: str = "", **kwargs
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
    items: list[Any] = [],
    view_name: str = "",
    page: int = 1,
    has_next: bool = True,
    auto_fetch: bool = True,
    threshold: int = 100,
    **kwargs,
) -> dict[str, Any]:
    """
    Rendert einen Container für Infinite Scroll.

    Args:
    ----
        items (list): Liste der aktuellen Elemente
        view_name (str): Name der View für das Laden weiterer Elemente
        page (int): Die aktuelle "Seite" die geladen werden soll
        has_next (bool): Ob weitere Elemente verfügbar sind
        auto_fetch (bool): 'False' wenn der Nutzer aktiv weitere Elemente per Button anfordern soll.
        threshold (int): Pixel-Schwellenwert für das Laden
        **kwargs: Zusätzliche Optionen

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {
        "items": items,
        "view_name": view_name,
        "page": page,
        "has_next": has_next,
        "auto_fetch": auto_fetch,
        "threshold": threshold,
        "options": kwargs,
    }


@register.inclusion_tag("insight_ui/components/alert.html")
def alert(message: str, alert_type: str = "info", dismissible: bool = True, **kwargs) -> dict[str, Any]:
    """
    Rendert eine barrierefreie Benachrichtigung.

    Args:
    ----
        message: Die Nachricht, die angezeigt werden soll
        alert_type: Der Typ der Benachrichtigung ('info', 'success', 'warning', 'error')
        dismissible: Ob die Benachrichtigung schließbar sein soll
        **kwargs: Zusätzliche Optionen für die Benachrichtigung

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {"message": message, "type": alert_type, "dismissible": dismissible, "options": kwargs}


@register.inclusion_tag("insight_ui/components/sidebar.html")
def sidebar(
    sidebar_data: dict = {}, side: str = "right", static: bool = True, auto_close: bool = False
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
    return {"sidebar_data": sidebar_data, "side": side, "static": static, "auto_close": auto_close}


@register.inclusion_tag("insight_ui/components/breadcrumbs.html")
def breadcrumbs(items: list[dict[str, Any]] = []) -> dict[str, Any]:
    """
    Rendert eine Breadcrumb-Navigation.

    Args:
    ----
        items (list): Eine Liste von Dictionaries mit Breadcrumb-Elementen

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {"items": items}


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
    html_tag_id: str, title: str, content: str = "", description: str = "", actions: list[dict[str, Any]] = []
) -> dict[str, Any]:
    """
    Rendert ein barrierefreies Modal-Dialog.

    Args:
    ----
        html_tag_id (str): Die eindeutige ID des Modals
        title (str): Der Titel des Modals
        content (str): Der Inhalt des Modals
        description (str): Eine optionale Beschreibung
        actions (list): Eine Liste von Aktions-Buttons

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {"id": html_tag_id, "title": title, "content": content, "description": description, "actions": actions}


@register.inclusion_tag("insight_ui/components/carousels/card_carousel.html")
def carousel(  # noqa: PLR0913 (too many args)
    carousel_items: list = [],
    autoplay: bool = False,
    show_dots: bool = True,
    show_index: bool = False,
    slides_count: range = [],
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
        "carousel_items": carousel_items,
        "autoplay": autoplay,
        "show_dots": show_dots,
        "show_index": show_index,
        "slides_count": slides_count,
        "items_per_slide": items_per_slide,
    }


@register.inclusion_tag("insight_ui/components/cards/card.html")
def card(
    title: str, content: str, subtitle: str = "", image: dict[str, str] = {}, actions: list[dict[str, str]] = []
) -> dict[str, Any]:
    """
    Rendert eine Karte.

    Args:
    ----
        title (str): Title der Karte
        content (str): Inhalt der Karte
        subtitle (str): Untertitel der Karte
        image (dict[url: str, alt: str]): Informationen über das Bild der Karte
        actions (list[dict[text: str, url: str, type: str]]): Eine Liste von Aktionsbuttons

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

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
    fields: list[dict[str, Any]] = [],
    title: str = "",
    description: str = "",
    view_name: str = "",
    method: str = "post",
    actions: list[dict[str, Any]] = [],
    htmx: dict[str, Any] = {},
    **kwargs,
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
        "fields": fields,
        "title": title,
        "description": description,
        "action": view_name,
        "method": method,
        "actions": actions,
        "htmx": htmx_config,
        "options": {**kwargs},
    }


@register.inclusion_tag("insight_ui/components/footer.html")
def footer(data: dict) -> dict[str, Any]:
    """
    Rendert einen Footer mit optionaler Beschreibung, Links und einer Copyright Zeile.

    Args:
    ----
        data (dict): Inhalt des Footers

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {"data": data}
