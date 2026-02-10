"""Template-Tags für Insight UI-Komponenten."""

import math
from collections.abc import Mapping, Sequence
from copy import deepcopy
from difflib import HtmlDiff, ndiff, unified_diff
from typing import Any

from django import template
from django.core.paginator import Page
from django.urls import reverse

from insight_ui.config import get_config
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

    if isinstance(view_args, list | tuple):
        mapping["url"] = reverse(view_name, args=list(view_args))
    elif view_arg is not None:
        mapping["url"] = reverse(view_name, args=[view_arg])
    elif isinstance(view_kwargs, dict):
        mapping["url"] = reverse(view_name, kwargs=view_kwargs)
    else:
        mapping["url"] = reverse(view_name)


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
def diff(a: str, b: str, simple: bool = True) -> str:
    """
    Generate a visualization of the differences between to texts.

    Arguments:
    ---------
        a (str): Die ursprüngliche Version des Textes.
        b (str): Die veränderte Version des Textes.
        simple (bool): 'True' für eine vereinfachte Darstellung.

    Returns:
    -------
        diff (str): Ein HTML Ausschnitt zur grafischen Darstellung der Unterschiede.

    """
    if not simple:
        differentiator = HtmlDiff()
        differentiator._file_template = file_template
        differentiator._styles = styles
        diff = unified_diff(a.splitlines(), b.splitlines(), lineterm="")
        return "\n".join(list(diff))
        return differentiator.make_file(a.splitlines(), b.splitlines())

    diff = ndiff(a.split(), b.split())
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


@register.inclusion_tag("insight_ui/components/navbar.html")
def navbar(config: Mapping[str, Any], **kwargs: JsonValue) -> dict[str, Any]:
    """
    Rendert eine konfigurierbare Navigationsleiste.

    Args:
    ----
        config (dict): Navbar Konfiguration:
            {
                "brand": {
                    "title": "Insight UI",
                    "view_name": "storybook_view",
                    "gap": "0.5rem",
                    "logo": {
                        "url": "insight_ui/svg/logo.svg",
                        "url_dark": "insight_ui/svg/ai-logo-dark.svg",
                        "alt": "Insight UI Logo",
                        "height": "2rem",
                    },
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
                        "text": _("Über"),
                        "open_modal": "about-modal",
                        "active": False,
                        "need_auth": False,
                        "staff_only": False,
                    },
                ],
                "searchbar_request_view": "search_view",
                "show_usermenu": True,
                "show_language_selector": True,
                "show_theme_toggle": True,
            }
        **kwargs: Zusätzliche Optionen für die Navbar

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

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
        "fixed": get_config("navbar_fixed"),
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


@register.inclusion_tag("insight_ui/components/input.html")
def input_field(  # noqa: PLR0913 (too many arguments)
    tag_id: str | None = None,
    name: str | None = None,
    input_type: str | None = None,
    placeholder: str | None = None,
    value: str | None = None,
    minimum: int | None = None,
    maximum: int | None = None,
    min_length: int | None = None,
    max_length: int | None = None,
    checked: bool | None = None,
    required: bool | None = None,
    disabled: bool | None = None,
    label: str | None = None,
    config: dict | None = None,
) -> dict:
    """
    Rendert ein beliebiges <input> Feld.

    Arguments:
    ---------
        tag_id (str): Eine optionale, eindeutige ID für JavaScript.
        name (str): Wird für eine <form> benötigt, als Name des Request-Parameters.
        input_type (str): Der Type des Input-Feldes bspw.: "text", "password", "date", etc..
        placeholder (str): Ein platzhalter Text.
        value (str): Der Wert des Input-Feldes (Bei type="checkbox", siehe 'checked').
        minimum (int): Bestimmt den minimalen Wert der Eingabe.
        maximum (int): Bestimmt den maximalen Wert der Eingabe.
        min_length (int): Bestimmt die minimale Anzahl an Zeichen in einem Textfeld.
        max_length (int): Bestimmt die maximale Anzahl an Zeichen in einem Textfeld.
        checked (bool): 'True', wenn type="checkbox" und die Checkbox ausgewählt sein soll.
        required (bool): 'True' wenn das Feld ausgefüllt werden muss.
        disabled (bool): 'True', wenn das Feld deaktiviert sein soll, andernfalls 'False'.
        label (str): Ein Label-Text welcher über dem Input-Feld angezeigt wird.
        config (dict[str, Any]): Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    if config is not None:
        tag_id = config.get("tag_id", tag_id)
        name = config.get("name", name)
        input_type = config.get("input_type", input_type)
        placeholder = config.get("placeholder", placeholder)
        value = config.get("value", value)
        minimum = config.get("minimum", minimum)
        maximum = config.get("maximum", maximum)
        min_length = config.get("min_length", min_length)
        max_length = config.get("max_length", max_length)
        label = config.get("label", label)
        checked = config.get("checked", checked)
        required = config.get("required", required)
        disabled = config.get("disabled", disabled)

    return {
        "tag_id": tag_id,
        "name": name,
        "input_type": input_type,
        "placeholder": placeholder,
        "value": value,
        "minimum": minimum,
        "maximum": maximum,
        "min_length": min_length,
        "max_length": max_length,
        "label": label,
        "checked": checked,
        "required": required,
        "disabled": disabled,
    }


@register.inclusion_tag("insight_ui/components/textarea.html")
def textarea(  # noqa: PLR0913 (too many arguments)
    tag_id: str | None = None,
    name: str | None = None,
    placeholder: str | None = None,
    value: str | None = None,
    rows: int | None = None,
    cols: int | None = None,
    required: bool | None = None,
    disabled: bool | None = None,
    label: str | None = None,
    config: dict | None = None,
) -> dict:
    """
    Rendert ein <textarea> Feld.

    Arguments:
    ---------
        tag_id (str): Eine optionale, eindeutige ID für JavaScript.
        name (str): Wird für eine <form> benötigt, als Name des Request-Parameters.
        placeholder (str): Ein platzhalter Text.
        value (str): Der Wert des Text-Feldes.
        rows (int): Bestimmt die Anzahl an Zeilen.
        cols (int): Bestimmt die Anzahl an Zeichen in einer Zeile.
        required (bool): 'True' wenn das Feld ausgefüllt werden muss.
        disabled (bool): 'True', wenn das Feld deaktiviert sein soll, andernfalls 'False'.
        label (str): Ein Label-Text welcher über dem Input-Feld angezeigt wird.
        config (dict[str, Any]): Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    if config is not None:
        tag_id = config.get("tag_id", tag_id)
        name = config.get("name", name)
        placeholder = config.get("placeholder", placeholder)
        value = config.get("value", value)
        rows = config.get("rows", rows)
        cols = config.get("cols", cols)
        label = config.get("label", label)
        required = config.get("required", required)
        disabled = config.get("disabled", disabled)

    return {
        "tag_id": tag_id,
        "name": name,
        "placeholder": placeholder,
        "value": value,
        "rows": rows,
        "cols": cols,
        "label": label,
        "required": required,
        "disabled": disabled,
    }


@register.inclusion_tag("insight_ui/components/dropdown.html")
def dropdown(config: dict) -> dict:
    """
    Rendert ein Dropdown Menü.

    Arguments:
    ---------
        config (dict): Ein Dictionary welches das Dropdown Menü beschreibt:
        config = {
            "tag_id": "user-menu",
            "title": _("User"),
            "show_arrow": True,
            "items": [
                {
                    "text": _("Profile"),
                    "view_name": "user_profile_view",
                    "icon": {"name": "user", "size": "small"},
                },
                ...
            ],
        }

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return config


@register.inclusion_tag("insight_ui/components/checkbox.html")
def checkbox(  # noqa: PLR0913 (too many arguments)
    tag_id: str | None = None,
    name: str | None = None,
    value: str | None = None,
    label: str | None = None,
    checked: bool | None = None,
    disabled: bool | None = None,
    config: dict | None = None,
) -> dict:
    """
    Rendert eine Checkbox mit einem Label-Text.

    Arguments:
    ---------
        tag_id (str): Eine optionale, eindeutige ID für JavaScript.
        name (str): Wird für eine <form> benötigt, als Name des Request-Parameters.
        value (str): Der Wert der Checkbox (Das ist nicht der Zustand, siehe dafür 'checked').
        label (str): Ein Label-Text welcher über der Checkbox angezeigt wird.
        checked (bool): 'True', wenn die Checkbox ausgewählt sein soll, andernfalls 'False'.
        disabled (bool): 'True', wenn die Checkbox deaktiviert sein soll, andernfalls 'False'.
        config (dict[str, Any]): Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    if config is not None:
        tag_id = config.get("tag_id", tag_id)
        name = config.get("name", name)
        value = config.get("value", value)
        label = config.get("label", label)
        checked = config.get("checked", checked)
        disabled = config.get("disabled", disabled)

    return {"tag_id": tag_id, "name": name, "value": value, "label": label, "checked": checked, "disabled": disabled}


@register.inclusion_tag("insight_ui/components/checkbox_group.html")
def checkbox_group(config: dict) -> dict:
    """
    Rendert eine Gruppe von Checkbox-Elementen.

    Arguments:
    ---------
        config (dict): Beschreibt die Checkbox-Gruppen Komponente.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"config": config}


@register.inclusion_tag("insight_ui/components/radio_group.html")
def radio_group(config: dict, current_value: str) -> dict:
    """
    Rendert eine Gruppe von Radio-Buttons.

    Arguments:
    ---------
        config (dict): Beschreibt die Radio Komponente und deren Items.
        current_value (str): Der Name des aktuell ausgewählten Radio-Buttons.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {
        "name": config.get("name"),
        "label": config.get("label"),
        "as_row": config.get("as_row"),
        "items": config.get("items"),
        "current_value": current_value,
    }


@register.inclusion_tag("insight_ui/components/radio_block.html")
def radio_block(  # noqa: PLR0913 (too many arguments)
    config: dict,
    current_value: str,
    name: str = "",
    view_name: str = "",
    query_params: str = "",
    hx_target_id: str = "",
    hx_swap_method: str = "",
    method: str = "",
    integrated: bool = False,
) -> dict:
    """
    Rendert ein Gruppe von Radio-Buttons.

    Arguments:
    ---------
        config (dict): Beschreibt die Radio Komponente und deren Items.
        current_value (str): Der Name des aktuell ausgewählten Radio-Buttons.
        name (str): Der Name des gesamten Radio-Blocks, benötigt zur Referenzierung im JavaScript Code.
        view_name (str): Der Name der View an welchen der Request beim wechseln, gesendet werden soll.
        query_params (str): Ein String von Query-Parametern
        hx_target_id (str): Die ID des HTML-Tags, welches bei wechseln des Wertes ausgetauscht werden soll.
        hx_swap_method (str): Die Art wie das Target ausgetauscht werden soll (siehe: https://htmx.org/attributes/hx-swap/).
        method (str): Der Name der JavaScript Methode welche ausgeführt werden soll.
        integrated (bool): 'False' wenn die Komponente ihr eigenes <form> Element haben soll.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    if config is not None:
        name = config.get("name", name)

    return {
        "name": name,
        "label": config.get("label"),
        "items": config.get("items"),
        "current_value": current_value,
        "view_name": view_name,
        "query_params": query_params,
        "hx_target_id": hx_target_id,
        "hx_swap_method": hx_swap_method,
        "method": method,
        "integrated": integrated,
    }


@register.inclusion_tag("insight_ui/components/toggle_button.html")
def toggle(  # noqa: PLR0913 (too many arguments)
    tag_id: str | None = None,
    name: str | None = None,
    value: str | None = None,
    label: str | None = None,
    icon: dict[str, str] | None = None,
    checked: bool | None = None,
    disabled: bool | None = None,
    switch: bool | None = None,
    config: dict | None = None,
    method: str = "",
) -> dict:
    """
    Rendert ein Toggle-Button.

    Arguments:
    ---------
        tag_id (str): Eine eindeutige ID für die Verknüpfung von <input> und <label>, sowie JavaScript.
        name (str): Wird für eine <form> benötigt, als Name des Request-Parameters.
        value (str): Der Wert des Toggles (Das ist nicht der Zustand, siehe dafür 'checked').
        label (str): Ein Label-Text welcher über dem Toggle angezeigt wird.
        icon (dict[str, str]): Ein Icon welches neben dem Text angezeigt wird.
        checked (bool): 'True', wenn der Toggle ausgewählt sein soll, andernfalls 'False'.
        disabled (bool): 'True', wenn der Toggle deaktiviert sein soll, andernfalls 'False'.
        switch (bool): 'True', wenn der Toggle-Button wie ein typischer Switch-Select aussehen soll.
        config (dict[str, Any]): Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.
        method (str): Der Name der JavaScript Methode welche ausgeführt werden soll.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    if config is not None:
        tag_id = config.get("tag_id", tag_id)
        name = config.get("name", name)
        value = config.get("value", value)
        label = config.get("label", label)
        icon = config.get("icon", icon)
        checked = config.get("checked", checked)
        disabled = config.get("disabled", disabled)
        switch = config.get("switch", switch)

    return {
        "tag_id": tag_id,
        "name": name,
        "value": value,
        "label": label,
        "icon": icon,
        "checked": checked,
        "disabled": disabled,
        "switch": switch,
        "method": method,
    }


@register.inclusion_tag("insight_ui/components/range_slider.html")
def slider(  # noqa: PLR0913 (too many arguments)
    tag_id: str | None = None,
    name: str | None = None,
    value: int | None = None,
    minimum: int | None = None,
    maximum: int | None = None,
    step_size: int | None = None,
    label: str | None = None,
    disabled: bool | None = None,
    items: list[str] | None = None,
    config: dict | None = None,
) -> dict:
    """
    Rendert ein Range-Slider.

    Arguments:
    ---------
        tag_id (str): Eine eindeutige ID für die Verknüpfung von <input> und <label>, sowie JavaScript.
        name (str): Wird für eine <form> benötigt, als Name des Request-Parameters.
        value (int): Der Wert des Sliders.
        minimum (int): Der kleinste Wert des Sliders.
        maximum (int): Der größte Wert des Sliders.
        step_size (int): Die Größe der Schritte des Sliders.
        label (str): Ein Label-Text welcher über dem Toggle angezeigt wird.
        disabled (bool): 'True', wenn der Toggle deaktiviert sein soll, andernfalls 'False'.
        items (list[str]): Eine Liste von Texten, welche als Legende unter dem Slider angezeigt werden.
        config (dict[str, Any]): Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    if config is not None:
        tag_id = config.get("tag_id", tag_id)
        name = config.get("name", name)
        value = config.get("value", value)
        minimum = config.get("minimum", minimum)
        maximum = config.get("maximum", maximum)
        step_size = config.get("step_size", step_size)
        label = config.get("label", label)
        disabled = config.get("disabled", disabled)
        items = config.get("items", items)

    return {
        "tag_id": tag_id,
        "name": name,
        "value": value,
        "minimum": minimum,
        "maximum": maximum,
        "step_size": step_size,
        "label": label,
        "disabled": disabled,
        "items": items,
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


@register.inclusion_tag("insight_ui/components/pagination.html")
def pagination(current_page: Page, surrounding_pages: list[int], ipp_config: dict[str, Any] = {}) -> dict:
    """
    Rendert eine Pagination.

    Arguments:
    ---------
        current_page (Page): Ein von Django erzeugtes Pagination-Objekt der aktuellen Seite.
        surrounding_pages (list[int]): Eine liste der benachbarten Seiten.
            Siehe: from insight_ui.utils.pagination import get_page
        ipp_config (dict[str, Any]): Konfiguration eines "Items per Page" Selects (select Komponente).

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"current_page": current_page, "surrounding_pages": surrounding_pages, "ipp_config": ipp_config}


@register.inclusion_tag("insight_ui/components/generic_filter.html")
def generic_filter(  # noqa: PLR0913 (too many arguments)
    filters: list,
    view_name: str,
    hx_target: str = "",
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
    Rendert eine Filterung mit welcher sich eine eigene Suchanfrage zusammenbauen lässt. Angelehnt an eine SQL-Query.

    Arguments:
    ---------
        model_fields (list): Eine Liste der Modell Felder mit möglichen Operatoren, etc.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"model_fields": model_fields}


@register.inclusion_tag("insight_ui/components/toggle_view.html")
def toggle_view(tag_id: str, data: list, view_radio_config: dict, current_view: str) -> dict:
    """
    Rendert eine Ansicht von Daten, welche auf verschiedene Arten dargestellt werden kann.

    Arguments:
    ---------
        tag_id (str): Eine einzigartige ID für die Komponente. (Wird für den wechsel der Ansicht benötigt).
        data (list): Die Daten, welche angezeigt werden sollen.
        view_radio_config (dict): Die Konfiguration der Radio-Group, zum wechseln der Ansichtsart.
        current_view (str): Der name der aktuellen Ansichtsart.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"tag_id": tag_id, "data": data, "view_radio_config": view_radio_config, "current_view": current_view}


@register.inclusion_tag("insight_ui/components/live_content.html")
def live_content(tag_id: str = "", url: str = "", interval: int = 10, initial_content: str = "") -> dict[str, Any]:
    """
    Rendert einen Container für Live-Updates via HTMX.

    Args:
    ----
        tag_id (str): Eine optionale, eindeutige ID für JavaScript.
        url (str): Die URL an welche der Request für das updaten des Inhalts gesendet werden soll.
        interval (int): Das Intervall für automatische Updates in Sekunden.
        initial_content (str): Optionaler, initialer Inhalt.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    htmx_config = {"url": url, "trigger": f"load, every {interval}s", "swap": "innerHTML"}

    return {"tag_id": tag_id, "initial_content": initial_content, "htmx": htmx_config}


@register.inclusion_tag("insight_ui/components/websocket.html")
def insight_websocket(tag_id: str = "", url: str = "", initial_content: str = "") -> dict[str, Any]:
    """
    Rendert eine WebSocket-Komponente als Wrapper für die htmx v2 ws-Extension.

    Args:
    ----
        tag_id: Die ID des WebSocket-Containers.
        url: Die WebSocket-URL (z.B. ws://localhost:8765).
        initial_content: Initialer Inhalt.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"tag_id": tag_id, "url": url, "initial_content": initial_content}


@register.inclusion_tag("insight_ui/components/infinite_scroll.html")
def infinite_scroll(  # noqa: PLR0913 (Too many arguments)
    tag_id: str = "",
    view_name: str = "",
    items: Sequence[Any] | None = None,
    page: int = 1,
    has_next: bool = True,
    auto_fetch: bool = True,
    threshold: int = 100,
) -> dict[str, Any]:
    """
    Rendert einen Container für Infinite Scroll.

    Args:
    ----
        tag_id (str): Optionale, eindeutige Tag-ID für die identification des Elements im JavaScript.
        view_name (str): Name der View für das Laden weiterer Elemente.
        items (list): Liste der bereits geladenen Elemente.
        page (int): Die Nummer der aktuellen "Seite", welche geladen werden soll.
        has_next (bool): 'True' wenn noch weitere Elemente verfügbar sind.
        auto_fetch (bool): 'False' wenn der Nutzer aktiv weitere Elemente per Button anfordern soll.
        threshold (int): Der Pixel-Schwellenwert für das Laden weiterer Elemente.
        **kwargs: Zusätzliche Optionen ('id' = Tag-ID).

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {
        "tag_id": tag_id,
        "items": items,
        "view_name": view_name,
        "page": page,
        "has_next": has_next,
        "auto_fetch": auto_fetch,
        "threshold": threshold,
    }


@register.inclusion_tag("insight_ui/components/alert.html")
def alert(tag_id: str = "", message: str = "", type: str = "info", dismissible: bool = True) -> dict[str, Any]:  # noqa: A002
    """
    Rendert eine barrierefreie Benachrichtigung.

    Args:
    ----
        tag_id (str): Optionale, eindeutige Tag-ID für die identification des Elements im JavaScript.
        message: Die Hauptnachricht der Benachrichtigung.
        type: Der Typ der Benachrichtigung ('info', 'success', 'warning', 'error').
        dismissible: True wenn die Benachrichtigung schließbar sein soll.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"tage_id": tag_id, "message": message, "type": type, "dismissible": dismissible}


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
        Dict mit Kontext-Variablen für das Template.

    """
    resolved_sidebar = _resolve_view_urls(dict(sidebar_data)) if sidebar_data else {}

    return {
        "sidebar_data": resolved_sidebar,
        "side": side,
        "static": static,
        "auto_close": auto_close,
        "navbar_fixed": get_config("navbar_fixed"),
    }


@register.inclusion_tag("insight_ui/components/breadcrumbs.html")
def breadcrumbs(items: Sequence[Mapping[str, Any]] | None = None) -> dict[str, Any]:
    """
    Rendert eine Breadcrumb-Navigation.

    Args:
    ----
        items (list): Eine Liste von Dictionaries mit den Breadcrumb-Elementen.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    resolved_items = [dict(item) for item in items] if items is not None else []
    return {"items": resolved_items}


@register.inclusion_tag("insight_ui/components/table.html")
def table(data: dict) -> dict[str, Any]:
    """
    Rendert eine einfache Tabelle.

    Args:
    ----
        data (dict): Ein Dictionary mit den Headern, den Rows und einer Überschrift.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {
        "caption": data.get("caption"),
        "empty_msg": data.get("empty_msg"),
        "headers": data.get("headers"),
        "rows": data.get("rows"),
    }


@register.inclusion_tag("insight_ui/components/modal.html")
def modal(  # noqa: PLR0913 (too many args)
    tag_id: str,
    title: str,
    description: str = "",
    additional_content: str = "",
    actions: Sequence[Mapping[str, str]] = [],
) -> dict[str, Any]:
    """
    Rendert ein barrierefreies Modal-Dialog.

    Args:
    ----
        tag_id (str): Eine eindeutige ID für das Modal.
        title (str): Der Titel des Modals.
        description (str): Eine optionale Beschreibung des Modals.
        additional_content (str): Der Inhalt des Modals.
        actions (list): Eine Liste von Aktion-Buttons.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {
        "tag_id": tag_id,
        "title": title,
        "description": description,
        "additional_content": additional_content,
        "actions": [dict(action) for action in actions] if actions is not None else [],
    }


@register.inclusion_tag("insight_ui/components/carousels/card_carousel.html")
def carousel(  # noqa: PLR0913 (too many args)
    carousel_items: Sequence[Mapping[str, Any]] = [],
    autoplay: bool = False,
    show_dots: bool = True,
    show_index: bool = False,
    items_per_slide: int = 1,
) -> dict[str, Any]:
    """
    Rendert ein Karten-Karussell.

    Args:
    ----
        carousel_items (list): Darzustellender Inhalt (Karten)
        autoplay (bool): Wechsle automatisch nach einer bestimmten Zeit (5s) zur nächsten Seite
        show_dots (bool): Zeige Pagination Dots unter dem Inhalt
        show_index (bool): Zeige Anzahl und aktuelle Seite in der unteren rechten Ecke
        items_per_slide (int): Anzahl der Items pro Seite

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {
        "carousel_items": carousel_items,
        "autoplay": autoplay,
        "show_dots": show_dots,
        "show_index": show_index,
        "slides_count": range(math.ceil(len(carousel_items) / items_per_slide)),
        "items_per_slide": items_per_slide,
    }


@register.inclusion_tag("insight_ui/components/carousels/image_carousel.html")
def image_carousel(  # noqa: PLR0913 (too many args)
    images: Sequence[Mapping[str, Any]] = [],
    autoplay: bool = False,
    show_dots: bool = True,
    show_index: bool = False,
    items_per_slide: int = 1,
) -> dict[str, Any]:
    """
    Rendert ein Bilder-Karussell.

    Args:
    ----
        images (list): Bilder welche innerhalb des Karussell angezeigt werden sollen.
        autoplay (bool): Wechsle automatisch nach einer bestimmten Zeit (5s) zur nächsten Seite
        show_dots (bool): Zeige Pagination Dots unter dem Inhalt
        show_index (bool): 'True', wenn in der unteren rechten Ecke die aktuelle Seite angezeigt werden soll.
        items_per_slide (int): Anzahl der Items pro Seite

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {
        "carousel_items": images,
        "autoplay": autoplay,
        "show_dots": show_dots,
        "show_index": show_index,
        "slides_count": range(math.ceil(len(images) / items_per_slide)),
        "items_per_slide": items_per_slide,
    }


@register.inclusion_tag("insight_ui/components/cards/card.html")
def card(
    title: str, content: str, subtitle: str = "", image: dict[str, str] = {}, actions: list[dict[str, str]] = []
) -> dict[str, Any]:
    """
    Rendert eine Karte mit dem Seitenverhältnis 16:9, dies entspricht ca. dem einer Visitenkarte.

    Args:
    ----
        title (str): Der Title der Karte.
        content (str): Der Hauptinhalt der Karte.
        subtitle (str): Ein optionaler Untertitel der Karte.
        image (dict[url: str, alt: str]): Informationen über das Bild der Karte.
        actions (list[dict[text: str, url: str, type: str]]): Eine Liste von Aktionbuttons.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"title": title, "subtitle": subtitle, "content": content, "image": image, "actions": actions}


@register.inclusion_tag("insight_ui/components/cards/app_card.html")
def card_app(  # noqa: PLR0913
    title: str,
    content: str,
    tags: list[str] = [],
    url: str = "",
    image: dict[str, str] = {},
    actions: list[dict[str, str]] = [],
) -> dict[str, Any]:
    """
    Rendert eine vertikal ausgerichtete Karte.

    Die Karte beginnt mit einem quadratischen Bild. Darunter befindet sich der Titel und der Content,
    sowie wenn angegeben, eine Liste von Tags. Am Ende werden, sofern vorhanden die Aktionbuttons
    übereinander dargestellt.

    Args:
    ----
        title (str): Der Title der Karte.
        content (str): Der Hauptinhalt der Karte.
        tags (list[str]): Eine Liste von Buttons.
        url (str): Eine URL welche aufgerufen wird, wenn der Nutzer auf den Title klickt.
        image (dict[url: str, alt: str]): Informationen über das Bild der Karte.
        actions (list[dict[text: str, url: str, type: str]]): Eine Liste von Aktionbuttons.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

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
    Rendert eine Karte, welche sich um 180° drehen kann und auf der Rückseite weitere Informationen enthält.

    Args:
    ----
        title (str): Der Title der Karte.
        content (str): Der Hauptinhalt der Karte.
        tags (list[str]): Eine Liste von Buttons.
        url (str): Eine URL welche aufgerufen wird, wenn der Nutzer auf den Title klickt.
        image (dict[url: str, alt: str]): Informationen über das Bild der Karte.
        actions (list[dict[text: str, url: str, type: str]]): Eine Liste von Aktionbuttons.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {"title": title, "content": content, "tags": tags, "url": url, "image": image, "actions": actions}


@register.inclusion_tag("insight_ui/components/form.html")
def form(  # noqa: PLR0913 (too many args)
    tag_id: str = "",
    title: str = "",
    description: str = "",
    fields: Sequence[Mapping[str, Any]] | None = [],
    show_reset_button: bool = False,
    view_name: str = "",
    htmx_config: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Rendert ein Formular mit HTMX-Unterstützung.

    Args:
    ----
        tag_id (str): Optionale, eindeutige ID zur Identifizierung.
        title (str): Der Titel des Formulars.
        description (str): Eine optionale Beschreibung.
        fields (list): Eine Liste von Formularfeldern.
        show_reset_button (bool): Zeigt neben dem "Absenden" Button ein "Zurücksetzen" Button an.
        view_name (str): Die Name des Endpunktes für die Formular-Übermittlung.
        htmx_config (dict): HTMX Konfiguration für AJAX-Requests.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    return {
        "tag_id": tag_id,
        "title": title,
        "description": description,
        "fields": fields,
        "show_reset_button": show_reset_button,
        "view_name": view_name,
        "htmx": htmx_config,
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
    return {
        "description": data.get("description"),
        "links": data.get("links"),
        "contact": data.get("contact"),
        "copyright": data.get("copyright"),
    }


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
        Dict mit Kontext-Variablen für das Template.

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
        Dict mit Kontext-Variablen für das Template.

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
        Dict mit Kontext-Variablen für das Template.

    """
    return {
        "id": tag_id,
        "velocity": velocity,
        "tilt": tilt,
        "face_camera": face_camera,
        "carousel_items": carousel_items,
    }


@register.inclusion_tag("insight_ui/components/select.html")
def select(
    name: str | None = None,
    label: str | None = None,
    options: list[str] | dict[str, str] | None = None,
    selected_option: str | None = None,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Rendert eine Auswahlbox.

    Args:
    ----
        name (str): Der Name des <select> Elements.
        label (str): Ein kurzer Titel, welche rüber dem Select angezeigt wird.
        options (list[str] or dict[str, str]): Alle Werte welche ausgewählt werden können.
        selected_option (str): Ein bereits ausgewählter Wert.
        config (dict[str, Any]): Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    if config is not None:
        name = config.get("name", name)
        label = config.get("label", label)
        options = config.get("options", options)
        selected_option = config.get("selected_option", selected_option)

    if isinstance(options, list):
        options = dict(zip(options, options))

    return {"name": name, "label": label, "options": options, "selected_option": selected_option}


@register.inclusion_tag("insight_ui/components/multiselect.html")
def multiselect(  # noqa: PLR0913 (too many arguments)
    name: str | None = None,
    label: str | None = None,
    maximum: int | None = None,
    show_buttons: bool | None = None,
    options: list[str] | dict[str, str] | None = None,
    selected_options: list[str] | None = None,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Rendert eine Auswahlbox, welche mehrere ausgewählte Werte zulässt und eine integrierte Suchzeile hat.

    Args:
    ----
        name (str): Der Name des Multiselect Elements.
        label (str): Ein kurzer Titel, welche rüber dem Multiselect angezeigt wird.
        maximum (int): Gibt an wie viele Werte maximal ausgewählt sein dürfen.
        show_buttons (bool): 'True' zeigt zusätzlich "Alle Auswählen" und "Alle Abwählen" Buttons an.
        options (list[str] or dict[str, str]): Alle Werte welche ausgewählt werden können.
        selected_options (list[str]): Alle Werte welche bereits ausgewählt sein sollen.
        config (dict[str, Any]): Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template.

    """
    if config is not None:
        name = config.get("name", name)
        label = config.get("label", label)
        maximum = config.get("maximum", maximum)
        show_buttons = config.get("show_buttons", show_buttons)
        options = config.get("options", options)
        selected_options = config.get("selected_options", selected_options)

    if isinstance(options, list):
        options = dict(zip(options, options))

    return {
        "name": name,
        "label": label,
        "maximum": maximum,
        "show_buttons": show_buttons,
        "options": options,
        "selected_options": selected_options,
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
        Dict mit Kontext-Variablen für das Template.

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
        Dict mit Kontext-Variablen für das Template.

    """
    return {"chart_id": chart_id, "chart": chart, "chart_height": chart_height}
