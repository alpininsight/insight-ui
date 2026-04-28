"""Template-Tags for Insight UI-Components."""

import math
from collections.abc import Iterable, Mapping, Sequence
from copy import deepcopy
from difflib import HtmlDiff, ndiff, unified_diff
from typing import Any

from django import template
from django.core.paginator import Page
from django.templatetags.static import static
from django.urls import reverse
from django.utils.functional import Promise
from django.utils.safestring import SafeString, mark_safe
from django.utils.translation import gettext as _
from markdown import markdown

from insight_ui.config import get_config
from insight_ui.utils.diff import file_template, styles

register = template.Library()

JsonPrimitive = str | int | float | bool | None
type JsonMapping = dict[str, "JsonValue"]
type JsonSequence = list["JsonValue"]
type JsonValue = JsonPrimitive | JsonMapping | JsonSequence


@register.filter
def markdownify(value: str) -> SafeString:
    """Convert markdown to html."""
    html = markdown(value)

    html = html.replace("<code>", '<span class="inline-tag">')
    html = html.replace("</code>", "</span>")

    return mark_safe(html)  # nosec  # noqa: S308


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


def _resolve_asset_url(value: object) -> str:
    """Resolve static asset paths while preserving absolute, root-relative, and data URLs."""
    if not value:
        return ""

    url = str(value)
    if url.startswith(("http://", "https://", "/", "data:")):
        return url

    return static(url)


@register.inclusion_tag("insight_ui/components/logo.html")
def logo(  # noqa: PLR0913 (too many arguments)
    logo_type: str | None = None,
    url: str | None = None,
    url_dark: str | None = None,
    alt: str | None = None,
    icon_name: str | None = None,
    icon_size: str | None = None,
    height: str | None = None,
    width: str | None = None,
    css_class: str | None = None,
    config: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Render a brand logo as an image, SVG asset, or Insight UI icon.

    Args:
    ----
        logo_type (str): One of 'image', 'svg', or 'icon'. In config dictionaries, 'type' is also supported.
        url (str): Static, absolute, root-relative, or data URL for image/svg logos.
        url_dark (str): Optional dark-theme URL for image/svg logos.
        alt (str): Accessible text. Empty values mark image/svg logos as decorative.
        icon_name (str): Insight UI icon name when logo_type is 'icon'.
        icon_size (str): Insight UI icon size when logo_type is 'icon'.
        height (str): CSS height for image/svg logos.
        width (str): Optional CSS width for image/svg logos.
        css_class (str): Extra classes for the rendered logo root.
        config (dict[str, Any]): Alternative configuration with keys corresponding to the previous parameters.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is not None:
        logo_type = config.get("type", config.get("logo_type", logo_type))
        url = config.get("url", config.get("src", url))
        url_dark = config.get("url_dark", config.get("src_dark", url_dark))
        alt = config.get("alt", alt)
        icon_size = config.get("icon_size", icon_size)
        height = config.get("height", height)
        width = config.get("width", width)
        css_class = config.get("class", config.get("css_class", css_class))

        icon_config = config.get("icon")
        if isinstance(icon_config, Mapping):
            icon_name = icon_config.get("name", icon_name)
            icon_size = icon_config.get("size", icon_size)
        elif isinstance(icon_config, str):
            icon_name = icon_config

        icon_name = config.get("icon_name", icon_name)

    inferred_type = logo_type or (
        "icon" if icon_name else "svg" if str(url or "").lower().endswith(".svg") else "image"
    )
    normalized_type = str(inferred_type).strip().lower()
    if normalized_type not in {"image", "svg", "icon"}:
        normalized_type = "image"

    src = _resolve_asset_url(url)
    dark_src = _resolve_asset_url(url_dark)

    return {
        "type": normalized_type,
        "src": src,
        "dark_src": dark_src,
        "has_dark_variant": bool(dark_src and dark_src != src),
        "alt": alt or "",
        "icon": {"name": icon_name or "", "size": icon_size or "m"},
        "height": height or "2rem",
        "width": width or "",
        "css_class": css_class or "",
    }


@register.inclusion_tag("insight_ui/components/copyright_notice.html")
def copyright_notice(  # noqa: PLR0913
    year: int | str | None = None,
    holder: str | None = None,
    app_name: str | None = None,
    source_label: str | None = None,
    license_text: str | None = None,
    license_url: str | None = None,
    separator: str | None = None,
    rights_text: str | None = None,
    css_class: str | None = None,
    config: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Render a reusable copyright and legal notice line.

    Args:
    ----
        year: Optional copyright year.
        holder: Copyright holder name.
        app_name: Backwards-compatible fallback for the holder name.
        source_label: Optional source/distribution label, for example "Open Source".
        license_text: Optional license label.
        license_url: Optional URL for the license label.
        separator: Separator between legal metadata parts. Defaults to a middle dot.
        rights_text: Optional rights statement.
        css_class: Additional CSS classes for the rendered notice.
        config: Alternative dictionary-based configuration for all parameters.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is not None:
        year = config.get("year", year)
        holder = config.get("holder", holder)
        app_name = config.get("app_name", app_name)
        source_label = config.get("source_label", source_label)
        license_text = config.get("license_text", license_text)
        license_url = config.get("license_url", license_url)
        separator = config.get("separator", separator)
        rights_text = config.get("rights_text", rights_text)
        css_class = config.get("class", config.get("css_class", css_class))

    notice_holder = holder or app_name or ""
    metadata = [
        {"text": source_label or "", "url": ""},
        {"text": license_text or "", "url": license_url or ""},
        {"text": rights_text or _("All rights reserved."), "url": ""},
    ]

    return {
        "year": year or "",
        "holder": notice_holder,
        "metadata": [item for item in metadata if item["text"]],
        "separator": separator or "\u00b7",
        "css_class": css_class or "",
    }


@register.filter
def diff(a: str, b: str, simple: bool = True) -> str:
    """
    Generate a visualization of the differences between to texts.

    Arguments:
    ---------
        a (str): The original version of the text.
        b (str): The modified version of the text.
        simple (bool): 'True' for a simplified display.

    Returns:
    -------
        diff (str): The HTML code for the graphical representation of the differences.

    """
    if not simple:
        differentiator = HtmlDiff()
        differentiator._file_template = file_template
        differentiator._styles = styles
        diff = unified_diff(a.splitlines(), b.splitlines(), lineterm="")
        return "\n".join(list(diff))

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
    Render a configurable navigation bar.

    Args:
    ----
        config (dict): Navbar configuration.
        **kwargs: Additional options for the navigation bar.

    Returns:
    -------
        A dict with context variables for the template.

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


@register.inclusion_tag("insight_ui/components/step_bar.html")
def step_bar(items: list) -> dict:
    """
    Render a graphical representation of process steps.

    Arguments:
    ---------
        items (list): A list of the individual steps.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"items": items}


@register.inclusion_tag("insight_ui/components/minimal_step_bar.html")
def minimal_step_bar(config: dict) -> dict:
    """
    Render a graphical representation of process steps.

    Arguments:
    ---------
        config (dict): Configuration of the individual steps of the Step Bar.

    Returns:
    -------
        A dict with context variables for the template.

    """
    items = config.get("items", [])
    if items == []:
        for step in range(0, config.get("step_count")):
            if step < config.get("current_step"):
                items.append("success")
            elif step == config.get("current_step"):
                items.append(config.get("current_step_status", "active"))
            else:
                items.append("")

    return {"items": items, "icon_size": config.get("icon_size", "xs")}


@register.inclusion_tag("insight_ui/components/bullet_point_list.html")
def bullet_point_list(items: list = []) -> dict:
    """
    Render a graphical representation of a bullet point list.

    Arguments:
    ---------
        items (list): A list of the individual bullet points.

    Returns:
    -------
        A dict with context variables for the template.

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
    Render any <input> field.

    Arguments:
    ---------
        tag_id (str): An optional, unique ID for JavaScript.
        name (str): Required for a <form> as the name of the request parameter.
        input_type (str): The type of input field, e.g. "text", "password", "date" etc..
        placeholder (str): Placeholder text.
        value (str): The value of the input field (for type="checkbox", see 'checked').
        minimum (int): Determines the minimum value of the input.
        maximum (int): Determines the minimum value of the input.
        min_length (int): Determines the minimum number of characters in a text field.
        max_length (int): Determines the minimum number of characters in a text field.
        checked (bool): 'True' if type="checkbox" and the checkbox should be selected.
        required (bool): 'True' if the field must be filled in.
        disabled (bool): 'True' if the field should be disabled, otherwise 'False'.
        label (str): A label text that is displayed above the input field.
        config (dict[str, Any]): An alternative configuration with keys corresponding to the previous parameters.

    Returns:
    -------
        A dict with context variables for the template.

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
    Render a <textarea> field.

    Arguments:
    ---------
        tag_id (str): An optional, unique ID for JavaScript.
        name (str): Required for a <form> as the name of the request parameter.
        placeholder (str): Placeholder text.
        value (str): The value of the text field.
        rows (int): Determines the number of lines.
        cols (int): Determines the number of characters in a line.
        required (bool): 'True' if the field must be filled in.
        disabled (bool): 'True' if the field should be disabled, otherwise 'False'.
        label (str): A label text that is displayed above the text field.
        config (dict[str, Any]): An alternative configuration with keys corresponding to the previous parameters.

    Returns:
    -------
        A dict with context variables for the template.

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
    Render a dropdown menu.

    Arguments:
    ---------
        config (dict): A dictionary that describes the dropdown menu.

    Returns:
    -------
        A dict with context variables for the template.

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
    Render a checkbox with label text.

    Arguments:
    ---------
        tag_id (str): An optional, unique ID for JavaScript.
        name (str): Required for a <form> as the name of the request parameter.
        value (str): The value of the checkbox (this is not the state, see 'checked' for that).
        label (str): A label text that is displayed above the checkbox.
        checked (bool): 'True' if the checkbox should be selected, otherwise 'False'.
        disabled (bool): 'True' if the checkbox should be disabled, otherwise 'False'.
        config (dict[str, Any]): An alternative configuration with keys corresponding to the previous parameters.

    Returns:
    -------
        A dict with context variables for the template.

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
    Render a group of checkbox elements.

    Arguments:
    ---------
        config (dict): Describes the checkbox groups component.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"config": config}


@register.inclusion_tag("insight_ui/components/radio_group.html")
def radio_group(  # noqa: PLR0913 (too many arguments)
    name: str = "",
    label: str = "",
    items: list[dict[str, Any]] = [],
    as_row: bool = True,
    current_value: str = "",
    config: dict[str, Any] = {},
) -> dict:
    """
    Render a group of radio buttons.

    Arguments:
    ---------
        name (str): The name of the radio group, required for identification in requests etc.
        label (str): A label text that is displayed above the radio buttons.
        items (list[dict[str, Any]]): A list of radio-button configurations.
        as_row (bool): 'False' if the elements are to be arranged in a column.
        current_value (str): The name of the currently selected radio button.
        config (dict[str, Any]): An alternative configuration with keys corresponding to the previous parameters.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is not None:
        name = config.get("name", name)
        label = config.get("label", label)
        items = config.get("items", items)
        as_row = config.get("as_row", as_row)
        current_value = config.get("current_value", current_value)

    return {"name": name, "label": label, "items": items, "as_row": as_row, "current_value": current_value}


@register.inclusion_tag("insight_ui/components/radio_block.html")
def radio_block(  # noqa: PLR0913 (too many arguments)
    name: str = "",
    label: str = "",
    items: list[dict[str, Any]] = [],
    integrated: bool = False,
    as_row: bool = True,
    view_name: str = "",
    query_params: str = "",
    hx_target_id: str = "",
    hx_swap_method: str = "outerHTML",
    method: str = "",
    current_value: str = "",
    config: dict[str, Any] = {},
) -> dict:
    """
    Render a group of radio buttons.

    Arguments:
    ---------
        name (str): The name of the entire radio block, required for referencing in JavaScript code.
        label (str): A label text that is displayed above the radio buttons.
        items (list[dict[str, Any]]): A list of radio-button configurations.
        integrated (bool): 'False' if the component should have its own <form> element.
        as_row (bool): 'False' if the elements are to be arranged in a column.
        view_name (str): The name of the view to which the request should be sent when switching.
        query_params (str): A string of query parameters.
        hx_target_id (str): The ID of the HTML tag that should be replaced when the value changes.
        hx_swap_method (str): The way in which the target is to be replaced (see: https://htmx.org/attributes/hx-swap/).
        method (str): The name of the JavaScript method to be executed.
        current_value (str): The name of the currently selected radio button.
        config (dict[str, Any]): An alternative configuration with keys corresponding to the previous parameters.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is not None:
        name = config.get("name", name)
        label = config.get("label", label)
        items = config.get("items", items)
        integrated = config.get("integrated", integrated)
        as_row = config.get("as_row", as_row)
        view_name = config.get("view_name", view_name)
        query_params = config.get("query_params", query_params)
        hx_target_id = config.get("hx_target_id", hx_target_id)
        hx_swap_method = config.get("hx_swap_method", hx_swap_method)
        method = config.get("method", method)
        current_value = config.get("current_value", current_value)

    return {
        "name": name,
        "label": label,
        "items": items,
        "current_value": current_value,
        "view_name": view_name,
        "query_params": query_params,
        "hx_target_id": hx_target_id,
        "hx_swap_method": hx_swap_method,
        "method": method,
        "integrated": integrated,
        "as_row": as_row,
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
    Render a toggle button.

    Arguments:
    ---------
        tag_id (str): A unique ID for linking <input> and <label>, as well as JavaScript.
        name (str): Required for a <form> as the name of the request parameter.
        value (str): The value of the toggle (this is not the state, see 'checked' for that).
        label (str): A label text that is displayed above the toggle.
        icon (dict[str, str]): An icon displayed next to the text.
        checked (bool): 'True' if the toggle should be selected, otherwise 'False'.
        disabled (bool): 'True' if the toggle should be disabled, otherwise 'False'.
        switch (bool): 'True' if the toggle button should look like a typical switch select.
        config (dict[str, Any]): An alternative configuration with keys corresponding to the previous parameters.
        method (str): The name of the JavaScript method to be executed.

    Returns:
    -------
        A dict with context variables for the template.

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
    Render a range slider.

    Arguments:
    ---------
        tag_id (str): A unique ID for linking <input> and <label>, as well as JavaScript.
        name (str): Required for a <form> as the name of the request parameter.
        value (int): The value of the slider.
        minimum (int): The smallest value of the slider.
        maximum (int): The largest value of the slider.
        step_size (int): The size of the slider's steps.
        label (str): A label text that is displayed above the slider.
        disabled (bool): 'True' if the slider should be disabled, otherwise 'False'.
        items (list[str]): A list of texts that are displayed as captions below the slider.
        config (dict[str, Any]): An alternative configuration with keys corresponding to the previous parameters.

    Returns:
    -------
        A dict with context variables for the template.

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
def chat(request_url: str) -> dict:
    """
    Render a chat with an input line and a place for the response.

    Arguments:
    ---------
        request_url (str): The URL to which the request should be sent.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"request_url": request_url}


@register.inclusion_tag("insight_ui/components/geo_map.html")
def geo_map(data: dict = {}, map_height: int = 36) -> dict:
    """
    Render an integrated geographic map.

    Arguments:
    ---------
        data (dict): Settings for the map and data to be displayed on the map.
        map_height (int): The height of the map in 'rem'.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"data": data, "map_height": map_height}


@register.inclusion_tag("insight_ui/components/pagination.html")
def pagination(current_page: Page, surrounding_pages: list[int], ipp_config: dict[str, Any] = {}) -> dict:
    """
    Render pagination with items per page selection and display of adjacent pages.

    Arguments:
    ---------
        current_page (Page): A pagination object generated by Django for the current page.
        surrounding_pages (list[int]): A list of neighboring pages.
            See: from insight_ui.utils.pagination import get_page
        ipp_config (dict[str, Any]): Configuration an "Items per Page" select (select component).

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"current_page": current_page, "surrounding_pages": surrounding_pages, "ipp_config": ipp_config}


@register.inclusion_tag("insight_ui/components/generic_filter.html")
def generic_filter(  # noqa: PLR0913 (too many arguments)
    filters: list = [],
    request_url: str = "",
    vertical: bool = False,
    htmx_config: Mapping[str, Any] | None = None,
    query_params: dict[str, str] = {},
) -> dict:
    """
    Render a generic filter consisting of one or more <select> fields.

    Arguments:
    ---------
        filters (list): A list of individual filters (<select> fields).
        request_url (str): The URL to which the request should be sent.
        vertical (bool): 'True' if the filters should be arranged one above the other.
        htmx_config ([str, str]): HTMX configuration for AJAX requests.
        query_params (dict[str, str]): A dictionary to set the values of the filters.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {
        "filters": filters,
        "request_url": request_url,
        "vertical": vertical,
        "htmx": htmx_config,
        "query_params": query_params,
    }


@register.inclusion_tag("insight_ui/components/search_bar.html")
def search_bar(request_view: str, simple: bool = False, search_query: str = "") -> dict:
    """
    Render text input with a button for a search function.

    Arguments:
    ---------
        request_view (str): The name of the view to which the request should be sent.
        simple (bool): 'True' if the search bar should be displayed without buttons and smaller.
        search_query (str): An optional value that appears automatically in the text field.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"request_view": request_view, "simple": simple, "search_query": search_query}


@register.inclusion_tag("insight_ui/components/search_query_builder/sq_builder.html")
def query_builder(model_fields: list[dict[str, Any]]) -> dict:
    """
    Render a filter that can be used to construct your own search query. Based on an SQL query.

    Arguments:
    ---------
        model_fields (list[dict[str, Any]]): A list of model fields with possible operators.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"model_fields": model_fields}


@register.inclusion_tag("insight_ui/components/toggle_view.html")
def toggle_view(tag_id: str, data: list, view_radio_config: dict, current_view: str) -> dict:
    """
    Render a view of data that can be displayed in various ways.

    Arguments:
    ---------
        tag_id (str): A unique ID for the component. (Required for changing the view).
        data (list): The data to be displayed.
        view_radio_config (dict): The configuration of the radio group for changing the view type.
        current_view (str): The name of the current view type.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"tag_id": tag_id, "data": data, "view_radio_config": view_radio_config, "current_view": current_view}


@register.inclusion_tag("insight_ui/components/live_content.html")
def live_content(tag_id: str = "", url: str = "", interval: int = 10, initial_content: str = "") -> dict[str, Any]:
    """
    Render a container for live updates via HTMX.

    Args:
    ----
        tag_id (str): An optional, unique ID for JavaScript.
        url (str): The URL to which the request for updating the content should be sent.
        interval (int): The interval for automatic updates in seconds.
        initial_content (str): Optional initial content.

    Returns:
    -------
        A dict with context variables for the template.

    """
    htmx_config = {"url": url, "trigger": f"load, every {interval}s", "swap": "innerHTML"}

    return {"tag_id": tag_id, "initial_content": initial_content, "htmx": htmx_config}


@register.inclusion_tag("insight_ui/components/websocket.html")
def insight_websocket(tag_id: str = "", url: str = "", initial_content: str = "") -> dict[str, Any]:
    """
    Render a WebSocket component as a thin wrapper for the HTMX ws extension.

    Args:
    ----
        tag_id: The ID of the WebSocket container.
        url: The WebSocket endpoint URL (for example `/runtime/stream/`).
        initial_content: Initial content.

    Returns:
    -------
        A dict with context variables for the template.

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
    Render a container for infinite scroll with an optional 'Fetch more' button.

    Args:
    ----
        tag_id (str): An optional, unique ID for JavaScript.
        view_name (str): Name of the view for loading additional elements.
        items (list): List of items already loaded.
        page (int): The number of the current "page" to be loaded.
        has_next (bool): 'True' if further elements are available.
        auto_fetch (bool): 'False' if the user should actively request additional elements via a button.
        threshold (int): The pixel threshold for loading additional elements.

    Returns:
    -------
        A dict with context variables for the template.

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
    Render a closable notification.

    Args:
    ----
        tag_id (str): An optional, unique ID for JavaScript.
        message: The message of the notification.
        type: The type of notification ('info', 'success', 'warning', 'error').
        dismissible: 'True' if the notification should be closable.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"tag_id": tag_id, "message": message, "type": type, "dismissible": dismissible}


@register.inclusion_tag("insight_ui/components/sidebar.html")
def sidebar(
    sidebar_data: Mapping[str, Any] | None = None,
    side: str = "right",
    static: bool = True,
    auto_close: bool = False,
    mobile_hidden: bool = False,
) -> dict[str, Any]:
    """
    Render a configurable page navigation.

    Args:
    ----
        sidebar_data (dict): The content of the sidebar (title and navigation elements).
        side (str): Specifies on which side the sidebar should be displayed.
        static (bool): 'True' if the sidebar should not be collapsible.
        auto_close (bool): 'True' if the sidebar should close automatically when the cursor leaves it.
        mobile_hidden (bool): 'True' if a static sidebar should be hidden on smaller viewports.

    Returns:
    -------
        A dict with context variables for the template.

    """
    resolved_sidebar = _resolve_view_urls(dict(sidebar_data)) if sidebar_data else {}

    return {
        "sidebar_data": resolved_sidebar,
        "side": side,
        "static": static,
        "auto_close": auto_close,
        "mobile_hidden": mobile_hidden,
        "navbar_fixed": get_config("navbar_fixed"),
    }


@register.inclusion_tag("insight_ui/components/breadcrumbs.html")
def breadcrumbs(items: Sequence[Mapping[str, Any]] | None = None) -> dict[str, Any]:
    """
    Render breadcrumb navigation.

    Args:
    ----
        items (list): List of dictionaries containing the breadcrumb elements.

    Returns:
    -------
        A dict with context variables for the template.

    """
    resolved_items = [dict(item) for item in items] if items is not None else []
    return {"items": resolved_items}


@register.inclusion_tag("insight_ui/components/table.html")
def table(data: dict) -> dict[str, Any]:
    """
    Render a simple table.

    Args:
    ----
        data (dict): Dictionary with headers, rows, a title and an empty message if not data is available.

    Returns:
    -------
        A dict with context variables for the template.

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
    description: str | list[str] = [],
    actions: Sequence[Mapping[str, str]] = [],
    width: int = 32,
) -> dict[str, Any]:
    """
    Render an accessible modal dialog.

    Args:
    ----
        tag_id (str): A unique ID for the modal.
        title (str): The title of the modal.
        description (list[str]): An optional text description of the modal.
        actions (list): A list of action buttons.
        width (int): The maximum width of the dialog box relative to the screen in 'rem'.

    Returns:
    -------
        A dict with context variables for the template.

    """
    # Convert a single string or a 'lazy translation objects' which is a Promise to a list.
    if isinstance(description, (str, Promise)) or not isinstance(description, Iterable):
        description = [description]

    return {
        "tag_id": tag_id,
        "title": title,
        "description": description,
        "actions": [dict(action) for action in actions] if actions is not None else [],
        "width": width,
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
    Render a card carousel.

    Args:
    ----
        carousel_items (list): Content to be displayed (cards).
        autoplay (bool): Automatically switch to the next page after a certain amount of time (5 seconds).
        show_dots (bool): Show pagination dots below the content.
        show_index (bool): Display number and current page in the lower right corner.
        items_per_slide (int): Number of items per page.

    Returns:
    -------
        A dict with context variables for the template.

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
    Render an image carousel.

    Args:
    ----
        images (list): Images to be displayed within the carousel.
        autoplay (bool): Automatically switch to the next page after a certain amount of time (5 seconds).
        show_dots (bool): Show pagination dots below the content.
        show_index (bool): Display number and current page in the lower right corner.
        items_per_slide (int): Number of items per page.

    Returns:
    -------
        A dict with context variables for the template.

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
    Render a card with an aspect ratio of 16:9, which is approximately the same as a business card.

    Args:
    ----
        title (str): The title of the card.
        content (str): The main content of the card.
        subtitle (str): An optional subtitle for the card.
        image (dict[url: str, alt: str]): Information about the image on the card.
        actions (list[dict[text: str, url: str, type: str]]): A list of action buttons.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"title": title, "subtitle": subtitle, "content": content, "image": image, "actions": actions}


@register.inclusion_tag("insight_ui/components/cards/app_card.html")
def app_card(  # noqa: PLR0913 (too many args)
    title: str,
    content: str,
    tags: list[str] = [],
    url: str = "",
    image: dict[str, str] = {},
    actions: list[dict[str, str]] = [],
) -> dict[str, Any]:
    """
    Render a vertically aligned card.

    The card starts with a square image. Below it is the title and content,
    as well as a list of tags, if specified. At the end, if available, the action buttons
    are displayed one above the other.

    Args:
    ----
        title (str): The title of the card.
        content (str): The main content of the card.
        tags (list[str]): A list of buttons.
        url (str): A URL that is called up when the user clicks on the title.
        image (dict[url: str, alt: str]): Information about the image on the card.
        actions (list[dict[text: str, url: str, type: str]]): A list of action buttons.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"title": title, "content": content, "tags": tags, "url": url, "image": image, "actions": actions}


@register.inclusion_tag("insight_ui/components/cards/flip_card.html")
def flip_card(  # noqa: PLR0913 (too many args)
    title: str,
    content: str,
    tags: list[str] = [],
    url: str = "",
    image: dict[str, str] = {},
    actions: list[dict[str, str]] = [],
) -> dict[str, Any]:
    """
    Render a card that can be rotated 180° and contains additional information on the back.

    Args:
    ----
        title (str): The title of the card.
        content (str): The main content of the card.
        tags (list[str]): A list of buttons.
        url (str): A URL that is called up when the user clicks on the title.
        image (dict[url: str, alt: str]): Information about the image on the card.
        actions (list[dict[text: str, url: str, type: str]]): A list of action buttons.

    Returns:
    -------
        A dict with context variables for the template.

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
    Render a form with HTMX support.

    Args:
    ----
        tag_id (str): An optional, unique ID for JavaScript.
        title (str): The title of the form.
        description (str): An optional description.
        fields (list): A list of form fields.
        show_reset_button (bool): Displays a "Reset" button next to the "Submit" button.
        view_name (str): The name of the endpoint for form submission.
        htmx_config (dict): HTMX configuration for AJAX requests.

    Returns:
    -------
        A dict with context variables for the template.

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
    Render a footer with optional description, links, and a copyright line.

    Args:
    ----
        data (dict): The data that should be displayed in the footer.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {
        "description": data.get("description"),
        "links": data.get("links"),
        "contact": data.get("contact"),
        "copyright": data.get("copyright"),
        "version": data.get("version"),
    }


@register.inclusion_tag("insight_ui/components/accordion.html")
def accordion(items: list, tag_id: str = "accordion", exclusive: bool = True) -> dict:
    """
    Render an accordion that can have one or more sections open.

    Args:
    ----
        items (list): The individual sections with captions and content.
        tag_id (str): A unique ID for the accordion.
        exclusive (bool): 'True' if only one area may be open at a time.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"items": items, "tag_id": tag_id, "exclusive": exclusive}


@register.inclusion_tag("insight_ui/components/tabs.html")
def tabs(config: dict) -> dict:
    """
    Render a group of tabs and a container for the content of each tab.

    Args:
    ----
        config (dict): Contains the individual tabs and some general information about the component.

    Returns:
    -------
        A dict with context variables for the template.

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
    Render a 3D version of the carousel component.

    Args:
    ----
        tag_id (str): A unique ID for the carousel.
        velocity (int): The speed at which the carousel should rotate.
        tilt (int): The inclination of the carousel toward the camera.
        face_camera (bool): 'True' if the cards should always be oriented toward the camera.
        carousel_items (list): Content to be displayed (card).

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {
        "id": tag_id,
        "velocity": velocity,
        "tilt": tilt,
        "face_camera": face_camera,
        "carousel_items": carousel_items,
    }


@register.inclusion_tag("insight_ui/components/select.html")
def select(  # noqa: PLR0913 (too many args)
    name: str | None = None,
    label: str | None = None,
    explanation: str = "",
    options: list[str] | dict[str, str] | None = None,
    selected_option: str | None = None,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Render a selection box.

    Args:
    ----
        name (str): The name of the select element.
        label (str): A short title that appears above the select box.
        explanation (str): A brief description of the filter that appears in a tooltip.
        options (list[str] or dict[str, str]): All values that can be selected.
        selected_option (str): A value that has already been selected.
        config (dict[str, Any]): An alternative configuration with keys corresponding to the previous parameters.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is not None:
        name = config.get("name", name)
        label = config.get("label", label)
        explanation = config.get("explanation", explanation)
        options = config.get("options", options)
        selected_option = config.get("selected_option", selected_option)

    if isinstance(options, list):
        options = dict(zip(options, options))

    return {
        "name": name,
        "label": label,
        "explanation": explanation,
        "options": options,
        "selected_option": selected_option,
    }


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
    Render a selection box that allows multiple selected values and has an integrated search bar.

    Args:
    ----
        name (str): The name of the multiselect element.
        label (str): A short title that appears above the multiselect.
        maximum (int): Specifies the maximum number of values that may be selected.
        show_buttons (bool): 'True' additionally displays "Select All" and "Deselect All" buttons.
        options (list[str] or dict[str, str]): All values that can be selected.
        selected_options (list[str]): All values that should already be selected.
        config (dict[str, Any]): An alternative configuration with keys corresponding to the previous parameters.

    Returns:
    -------
        A dict with context variables for the template.

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


@register.inclusion_tag("insight_ui/components/page_header.html")
def page_header(title: str = "", description: str | list[str] = []) -> dict[str, Any]:
    """
    Render a page header for the blue header in the base template.

    Args:
    ----
        title (str): The title of the page.
        description (str): An optional description below the title.

    Returns:
    -------
        A dict with context variables for the template.

    """
    # Convert a single string or a 'lazy translation objects' which is a Promise to a list.
    if isinstance(description, (str, Promise)) or not isinstance(description, Iterable):
        description = [description]

    return {"title": title, "description": description}


def _coerce_heading_decoration_height(value: object, default: int = 90) -> int:
    """Return a positive integer height for the heading decoration."""
    try:
        height = int(value)
    except (TypeError, ValueError):
        return default

    return max(height, 1)


@register.inclusion_tag("insight_ui/components/heading_decoration.html")
def heading_decoration(
    style: str | None = None,
    color: str | None = None,
    image_url: str | None = None,
    height: int | str | None = None,
    config: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Render a decorative transition between the base-template heading and content area.

    Args:
    ----
        style (str): One of 'waves', 'image', 'gradient', or 'none'. Defaults to 'waves'.
        color (str): Optional CSS color override. Defaults to --color-insight-primary.
        image_url (str): Optional background image URL used by the 'image' style.
        height (int): Decoration height in px. Defaults to 90.
        config (dict[str, Any]): Alternative configuration with keys corresponding to the previous parameters.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is not None:
        style = config.get("style", style)
        color = config.get("color", color)
        image_url = config.get("image_url", image_url)
        height = config.get("height", height)

    normalized_style = (style or "waves").strip().lower()
    if normalized_style not in {"waves", "image", "gradient", "none"}:
        normalized_style = "waves"

    height_px = _coerce_heading_decoration_height(height)
    color_value = color or "var(--color-insight-primary, #3b82f6)"

    return {
        "style": normalized_style,
        "color": color_value,
        "image_url": image_url or "",
        "height": height_px,
        "wave_back_y": max(height_px - 25, 0),
        "wave_middle_y": max(height_px - 10, 0),
        "wave_front_y": max(height_px - 55, 0),
    }


@register.inclusion_tag("insight_ui/components/article.html")
def article(content: str = "", columns: int = 2, column_gap: str = "2rem", title: str = "") -> dict[str, Any]:
    """
    Render an article in newspaper style with a multi-column layout.

    Args:
    ----
        content (str): The text content of the article (may contain HTML).
        columns (int): The number of columns (default: 2).
        column_gap (str): The distance between columns (default: '2rem').
        title (str): An optional title above the article.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"content": content, "columns": columns, "column_gap": column_gap, "title": title}


@register.inclusion_tag("insight_ui/components/hero.html")
def hero(  # noqa: PLR0913 (too many arguments)
    title: str = "",
    subtitle: str = "",
    description: str = "",
    cta_primary: dict = {},
    cta_secondary: dict = {},
    background_image_url: str = "",
    badge: dict = {},
) -> dict[str, Any]:
    """
    Render a hero section with optional background image.

    Args:
    ----
        title (str): Title of the hero section.
        subtitle (str): Subtitle of the hero section, which is displayed under the title.
        description (str): Description of the hero section, which is displayed under the title or subtitle.
        cta_primary (dict): Primary 'Call-to-Action' button.
        cta_secondary (dict): Secondary 'Call-to-Action' button.
        background_image_url (str): URL of the background image.
        badge (dict): A badge with an icon and text.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {
        "title": title,
        "subtitle": subtitle,
        "description": description,
        "cta_primary": cta_primary,
        "cta_secondary": cta_secondary,
        "background_image_url": background_image_url,
        "badge": badge,
    }


@register.inclusion_tag("insight_ui/components/infobox.html")
def infobox(info_type: str = "", message: str = "", **kwargs) -> dict[str, Any]:
    """
    Render a small box of information.

    Args:
    ----
        info_type (str): importance level of the message e.g 'info', 'warn' or 'danger'.
        message (str): Descriptive message.
        kwargs: A list of variables that are inserted into the message using 'format'.

    Returns:
    -------
        A dict with context variables for the template.

    """
    formatted_message = message
    if kwargs:
        try:
            formatted_message = message.format(**kwargs)
        except (KeyError, ValueError):
            formatted_message = message

    return {"type": info_type, "message": formatted_message}


@register.inclusion_tag("insight_ui/components/charts/bar_chart.html")
def bar_chart(chart_id: str, chart: dict, chart_height: int = 24) -> dict:
    """
    Render a bar chart with Apache ECharts.

    Args:
    ----
        chart_id (str): A unique ID for the chart.
        chart (dict): Contains the information and data from the chart.
        chart_height (int): The height of the chart in 'rem'.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"chart_id": chart_id, "chart": chart, "chart_height": chart_height}


@register.inclusion_tag("insight_ui/components/charts/line_chart.html")
def line_chart(chart_id: str, chart: dict, chart_height: int = 24) -> dict:
    """
    Render a line chart with Apache ECharts.

    Args:
    ----
        chart_id (str): A unique ID for the chart.
        chart (dict): Contains the information and data from the chart.
        chart_height (int): The height of the chart in 'rem'.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"chart_id": chart_id, "chart": chart, "chart_height": chart_height}
