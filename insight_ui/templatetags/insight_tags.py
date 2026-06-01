"""Template-Tags for Insight UI-Components."""

from __future__ import annotations

import math
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import asdict, fields, is_dataclass, replace
from difflib import HtmlDiff, ndiff, unified_diff
from typing import Any, Final, Literal

from django import template
from django.core.paginator import Page
from django.templatetags.static import static
from django.utils.functional import Promise
from django.utils.safestring import SafeString, mark_safe
from django.utils.translation import gettext as _
from markdown import markdown

from insight_ui.config import get_config
from insight_ui.configs import (
    AlertConfig,
    AppCardConfig,
    ArticleConfig,
    BreadcrumbItemConfig,
    BulletPointItemConfig,
    CardCarouselConfig,
    CardConfig,
    ChartConfig,
    CheckboxConfig,
    CheckboxGroupConfig,
    CopyrightNoticeConfig,
    CornerRibbonConfig,
    DropdownConfig,
    FlipCardConfig,
    FooterConfig,
    FormConfig,
    FormFieldConfig,
    GenericFilterConfig,
    GeoMapConfig,
    HeadingDecorationConfig,
    HeroConfig,
    IconConfig,
    ImageCarouselConfig,
    InfiniteScrollConfig,
    InputFieldConfig,
    LiveContentConfig,
    LogoConfig,
    MinimalStepBarConfig,
    ModalConfig,
    MultiselectConfig,
    NavbarConfig,
    PageHeaderConfig,
    PaginationIppConfig,
    RadioBlockConfig,
    RadioGroupConfig,
    RadioItemConfig,
    SearchBarConfig,
    SelectConfig,
    SidebarConfig,
    SliderConfig,
    StepBarItemConfig,
    TableConfig,
    TabsConfig,
    TextareaConfig,
    ThreeDCarouselConfig,
    ToggleConfig,
    ToggleViewConfig,
    WebSocketConfig,
)
from insight_ui.configs.base import ActionConfig, HtmxConfig, ImageConfig
from insight_ui.configs.filter import QueryBuilderFieldConfig
from insight_ui.configs.layout import BadgeConfig
from insight_ui.configs.navigation import AccordionConfig, SidebarDataConfig
from insight_ui.configs.utils import GeoMapDatasetConfig, InfoboxConfig
from insight_ui.utils.diff import file_template, styles

register = template.Library()

JsonPrimitive = str | int | float | bool | None
type JsonMapping = dict[str, "JsonValue"]
type JsonSequence = list["JsonValue"]
type JsonValue = JsonPrimitive | JsonMapping | JsonSequence


class _Unset:
    def __repr__(self) -> Literal["UNSET"]:
        return "UNSET"


UNSET: Final = _Unset()


def _resolve_asset_url(value: object) -> str:
    """Resolve static asset paths while preserving absolute, root-relative, and data URLs."""
    if not value:
        return ""

    url = str(value)
    if url.startswith(("http://", "https://", "/", "data:")):
        return url

    return static(url)


def _to_dict(obj: Any) -> dict[str, Any]:  # noqa: ANN401
    """Convert dataclass or dict to dict."""
    if is_dataclass(obj) and not isinstance(obj, type):
        return asdict(obj)
    if isinstance(obj, Mapping):
        return dict(obj)
    return obj


def _to_dict_list(items: Sequence[Any]) -> list[dict[str, Any]]:
    """Convert a sequence of dataclasses or dicts to list of dicts."""
    return [_to_dict(item) for item in items]


@register.filter
def markdownify(value: str) -> SafeString:
    """Convert markdown to html."""
    html = markdown(value)

    # Assign "inline-tag" class to <code> elements
    html = html.replace("<code>", '<span class="inline-tag">')
    html = html.replace("</code>", "</span>")

    # Assign text style to <a> elements
    html = html.replace("<a", '<a class="text-link"')

    return mark_safe(html)  # nosec  # noqa: S308


@register.filter
def get_item(dictionary: dict, key: str) -> Any:  # noqa: ANN401
    """Get the specified item of a dictionary."""
    return dictionary.get(key)


def ensure_list(value: str | Iterable[str] | None) -> list[str]:
    """Take a string or a list of strings and return in both cases a list of strings."""
    if value is None:
        return []

    if isinstance(value, (str, Promise)):
        return [value]

    return list(value)


def merge_config(config: Any, **overrides) -> Any:  # noqa: ANN401
    """Take a component config Dataclass and overwrite the respective member with the kwargs."""
    if config is None:
        return config.__class__(**overrides)

    values = {}
    for field in fields(config):
        override = overrides.get(field.name)
        if override:
            values[field.name] = override
        else:
            values[field.name] = getattr(config, field.name)

    return replace(config, **values)


@register.inclusion_tag("insight_ui/components/icons.html")
def icon(config: IconConfig | None = None, *, name: str = "", size: str = "m") -> dict[str, Any]:
    """
    Render specified icon with given size.

    Args:
    ----
        config: IconConfig dataclass with all parameters.
        name: Name of the icon from the Insight UI icon set.
        size: Size of the icon ('xs', 's', 'm', 'l', 'xl').

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is not None:
        name = config.name or name
        size = config.size or size

    return {"icon_config": IconConfig(name, size)}


# =============================================================
#
#   Layout Tags
#
# =============================================================


@register.inclusion_tag("insight_ui/components/page_header.html")
def page_header(
    config: PageHeaderConfig | None = None,
    *,
    title: str | _Unset = UNSET,
    description: str | list[str] | _Unset = UNSET,
) -> dict[str, Any]:
    """
    Render a page header in the base template.

    Args:
    ----
        config: PageHeaderConfig dataclass with all parameters.
        title: The title of the page.
        description: An optional description below the title.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is not None:
        page_header_conf: PageHeaderConfig = merge_config(config, title=title, description=description)
    else:
        if title is UNSET:
            raise ValueError("'title' is required for 'page_header' component")  # noqa: TRY003
        page_header_conf = PageHeaderConfig(title=title, description=description if description is not UNSET else [])

    page_header_conf.description = ensure_list(page_header_conf.description)

    return {"page_header_config": page_header_conf}


def _coerce_heading_decoration_height(value: object, default: int = 90) -> int:
    """Return a positive integer height for the heading decoration."""
    try:
        height = int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return default

    return max(height, 1)


@register.inclusion_tag("insight_ui/components/heading_decoration.html")
def heading_decoration(
    config: HeadingDecorationConfig | None = None,
    *,
    style: str | None = None,
    color: str | None = None,
    image_url: str | None = None,
    height: int | str | None = None,
) -> dict[str, Any]:
    """
    Render a decorative transition between the heading and content area.

    Args:
    ----
        config: HeadingDecorationConfig dataclass with all parameters.
        style: One of 'waves', 'image', 'gradient', or 'none'.
        color: Optional CSS color override.
        image_url: Optional background image URL for 'image' style.
        height: Decoration height in px.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is not None:
        style = config.style
        color = config.color
        image_url = config.image_url
        height = config.height

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
def article(
    config: ArticleConfig | None = None,
    *,
    content: str | _Unset = UNSET,
    columns: int = 2,
    column_gap: str = "2rem",
    title: str = "",
) -> dict[str, Any]:
    """
    Render an article in newspaper style with a multi-column layout.

    Args:
    ----
        config: ArticleConfig dataclass with all parameters.
        content: The text content of the article (may contain HTML).
        columns: The number of columns.
        column_gap: The distance between columns.
        title: An optional title above the article.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is not None:
        article_config: ArticleConfig = merge_config(
            config, title=title, content=content, columns=columns, column_gap=column_gap
        )
    else:
        if content is UNSET:
            raise ValueError("'content' is required for 'article' component!")  # noqa: TRY003
        article_config = ArticleConfig(title=title, content=content, columns=columns, column_gap=column_gap)

    return {"article_config": article_config}


@register.inclusion_tag("insight_ui/components/hero.html")
def hero(
    config: HeroConfig | None = None,
    *,
    title: str = "",
    subtitle: str = "",
    description: str = "",
    cta_primary: ActionConfig | None = None,
    cta_secondary: ActionConfig | None = None,
    background_image_url: str = "",
    badge: BadgeConfig | None = None,
) -> dict[str, Any]:
    """
    Render a hero section with optional background image.

    Args:
    ----
        config: HeroConfig dataclass with all parameters.
        title: Title of the hero section.
        subtitle: Subtitle displayed under the title.
        description: Description displayed under the subtitle.
        cta_primary: Primary call-to-action button.
        cta_secondary: Secondary call-to-action button.
        background_image_url: URL of the background image.
        badge: A badge with an icon and text.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is not None:
        hero_config: HeroConfig = merge_config(
            config,
            title=title,
            subtitle=subtitle,
            description=description,
            cta_primary=cta_primary,
            cta_secondary=cta_secondary,
            background_image_url=background_image_url,
            badge=badge,
        )
    else:
        hero_config = HeroConfig(
            title=title,
            subtitle=subtitle,
            description=description,
            cta_primary=cta_primary,
            cta_secondary=cta_secondary,
            background_image_url=background_image_url,
            badge=badge,
        )

    return {"hero_config": hero_config}


# =============================================================
#
#   Navigation Tags
#
# =============================================================


@register.inclusion_tag("insight_ui/components/navbar.html")
def navbar(config: NavbarConfig, **kwargs: JsonValue) -> dict[str, Any]:
    """
    Render a configurable navigation bar.

    Args:
    ----
        config: NavbarConfig dataclass with all configuration.
        **kwargs: Additional options for the navigation bar.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"navbar_config": config, "fixed": get_config("navbar_fixed"), "options": {**kwargs}}


@register.inclusion_tag("insight_ui/components/sidebar.html")
def sidebar(
    config: SidebarConfig | None = None,
    *,
    sidebar_data: SidebarDataConfig | None = None,
    side: str = "right",
    static: bool = True,
    auto_close: bool = False,
    mobile_hidden: bool = False,
) -> dict[str, Any]:
    """
    Render a configurable page navigation.

    Args:
    ----
        config: SidebarConfig dataclass with all parameters.
        sidebar_data: The content of the sidebar.
        side: Specifies on which side the sidebar should be displayed.
        static: True if the sidebar should not be collapsible.
        auto_close: True if the sidebar should close when the cursor leaves.
        mobile_hidden: True if a static sidebar should be hidden on mobile.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = SidebarConfig(
            sidebar_data=sidebar_data, side=side, static=static, auto_close=auto_close, mobile_hidden=mobile_hidden
        )

    return {"sidebar_config": config, "navbar_fixed": get_config("navbar_fixed")}


@register.inclusion_tag("insight_ui/components/footer.html")
def footer(config: FooterConfig) -> dict[str, Any]:
    """
    Render a footer with optional description, links, and a copyright line.

    Args:
    ----
        config: FooterConfig dataclass with all parameters.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"footer_config": config}


@register.inclusion_tag("insight_ui/components/breadcrumbs.html")
def breadcrumbs(items: list[BreadcrumbItemConfig]) -> dict[str, Any]:
    """
    Render breadcrumb navigation.

    Args:
    ----
        items: List of breadcrumb item configurations.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"items": items}


@register.inclusion_tag("insight_ui/components/step_bar.html")
def step_bar(items: list[StepBarItemConfig]) -> dict[str, Any]:
    """
    Render a graphical representation of process steps.

    Args:
    ----
        items: A list of step configurations.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"items": items}


@register.inclusion_tag("insight_ui/components/minimal_step_bar.html")
def minimal_step_bar(
    config: MinimalStepBarConfig | None = None,
    *,
    items: list[Literal["active", "success", "failed", ""]] | None = None,
    step_count: int = 0,
    current_step: int = 0,
    current_step_status: Literal["active", "success", "failed"] = "active",
    icon_size: Literal["xs", "s", "m", "l", "xl"] = "xs",
) -> dict[str, Any]:
    """
    Render a compact graphical representation of process steps.

    Args:
    ----
        config: MinimalStepBarConfig dataclass with all parameters.
        items: List of step statuses ('success', 'failed', 'active', '').
        step_count: Total number of steps (used if items is empty).
        current_step: Current step index (0-based, used if items is empty).
        current_step_status: Status for current step.
        icon_size: Icon size for step indicators.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is not None:
        items = config.items if config.items else []
        step_count = config.step_count
        current_step = config.current_step
        current_step_status = config.current_step_status
        icon_size = config.icon_size

    if items is None:
        items = []

    # Generate items from step_count if not provided
    if not items and step_count > 0:
        items = []
        for step in range(step_count):
            if step < current_step:
                items.append("success")
            elif step == current_step:
                items.append(current_step_status)
            else:
                items.append("")

    return {"items": items, "icon_size": icon_size}


@register.inclusion_tag("insight_ui/components/bullet_point_list.html")
def bullet_point_list(items: list[BulletPointItemConfig]) -> dict[str, Any]:
    """
    Render a graphical representation of a bullet point list.

    Args:
    ----
        items: A list of bullet point configurations.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"items": items}


@register.inclusion_tag("insight_ui/components/accordion.html")
def accordion(config: AccordionConfig) -> dict[str, Any]:
    """
    Render an accordion that can have one or more sections open.

    Args:
    ----
        config: AccordionConfig dataclass with all parameters.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"accordion_config": config}


@register.inclusion_tag("insight_ui/components/tabs.html")
def tabs(config: TabsConfig) -> dict[str, Any]:
    """
    Render a group of tabs and a container for the content of each tab.

    Args:
    ----
        config: TabsConfig dataclass with tab configuration.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"config": config}


# =============================================================
#
#   Input Tags
#
# =============================================================


@register.inclusion_tag("insight_ui/components/input.html")
def input_field(
    config: InputFieldConfig | None = None,
    *,
    tag_id: str | None = None,
    name: str | None = None,
    input_type: str = "text",
    placeholder: str = "",
    value: str | int | float | None = None,
    minimum: int | None = None,
    maximum: int | None = None,
    min_length: int | None = None,
    max_length: int | None = None,
    checked: bool = False,
    required: bool = False,
    disabled: bool = False,
    label: str | None = None,
) -> dict[str, Any]:
    """
    Render any <input> field.

    Args:
    ----
        config: InputFieldConfig dataclass with all parameters.
        tag_id: An optional, unique ID for JavaScript.
        name: Required for a <form> as the name of the request parameter.
        input_type: The type of input field (text, password, email, etc.).
        placeholder: Placeholder text.
        value: The value of the input field.
        minimum: Minimum value for number inputs.
        maximum: Maximum value for number inputs.
        min_length: Minimum character length.
        max_length: Maximum character length.
        checked: True if checkbox should be selected.
        required: True if the field must be filled in.
        disabled: True if the field should be disabled.
        label: Label text displayed above the input field.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = InputFieldConfig(
            tag_id=tag_id,
            name=name,
            input_type=input_type,
            placeholder=placeholder,
            value=value,
            minimum=minimum,
            maximum=maximum,
            min_length=min_length,
            max_length=max_length,
            checked=checked,
            required=required,
            disabled=disabled,
            label=label,
        )

    return {"input_config": config}


@register.inclusion_tag("insight_ui/components/textarea.html")
def textarea(
    config: TextareaConfig | None = None,
    *,
    tag_id: str | None = None,
    name: str | None = None,
    placeholder: str = "",
    value: str = "",
    rows: int = 3,
    cols: int | None = None,
    required: bool = False,
    disabled: bool = False,
    label: str | None = None,
) -> dict[str, Any]:
    """
    Render a <textarea> field.

    Args:
    ----
        config: TextareaConfig dataclass with all parameters.
        tag_id: An optional, unique ID for JavaScript.
        name: Required for a <form> as the name of the request parameter.
        placeholder: Placeholder text.
        value: The value of the text field.
        rows: Number of visible text lines.
        cols: Visible width in characters.
        required: True if the field must be filled in.
        disabled: True if the field should be disabled.
        label: Label text displayed above the text field.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = TextareaConfig(
            tag_id=tag_id,
            name=name,
            placeholder=placeholder,
            value=value,
            rows=rows,
            cols=cols,
            required=required,
            disabled=disabled,
            label=label,
        )

    return {"textarea_config": config}


@register.inclusion_tag("insight_ui/components/checkbox.html")
def checkbox(
    config: CheckboxConfig | None = None,
    *,
    tag_id: str | None = None,
    name: str | None = None,
    value: str = "",
    label: str | None = None,
    checked: bool = False,
    disabled: bool = False,
) -> dict[str, Any]:
    """
    Render a checkbox with label text.

    Args:
    ----
        config: CheckboxConfig dataclass with all parameters.
        tag_id: An optional, unique ID for JavaScript.
        name: Required for a <form> as the name of the request parameter.
        value: The value of the checkbox (not the state).
        label: Label text displayed next to the checkbox.
        checked: True if the checkbox should be selected.
        disabled: True if the checkbox should be disabled.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = CheckboxConfig(tag_id=tag_id, name=name, value=value, label=label, checked=checked, disabled=disabled)

    return {"checkbox_config": config}


@register.inclusion_tag("insight_ui/components/checkbox_group.html")
def checkbox_group(config: CheckboxGroupConfig) -> dict[str, Any]:
    """
    Render a group of checkbox elements.

    Args:
    ----
        config: CheckboxGroupConfig dataclass describing the checkbox group.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"checkbox_group_config": config}


@register.inclusion_tag("insight_ui/components/dropdown.html")
def dropdown(config: DropdownConfig) -> dict[str, Any]:
    """
    Render a dropdown menu.

    Args:
    ----
        config: DropdownConfig dataclass describing the dropdown menu.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"dropdown_config": config}


@register.inclusion_tag("insight_ui/components/radio_group.html")
def radio_group(
    config: RadioGroupConfig | None = None,
    *,
    name: str = "",
    label: str = "",
    items: list[RadioItemConfig | dict[str, Any]] | None = None,
    as_row: bool = True,
    current_value: str = "",
) -> dict[str, Any]:
    """
    Render a group of radio buttons.

    Args:
    ----
        config: RadioGroupConfig dataclass with all parameters.
        name: The name of the radio group.
        label: Label text displayed above the radio buttons.
        items: A list of radio-button configurations.
        as_row: False if the elements should be arranged in a column.
        current_value: The currently selected value.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = RadioGroupConfig(name, label, items, as_row, current_value)

    return {"radio_group_config": config}


@register.inclusion_tag("insight_ui/components/radio_block.html")
def radio_block(
    config: RadioBlockConfig | None = None,
    *,
    name: str = "",
    label: str = "",
    items: list[RadioItemConfig] | None = None,
    integrated: bool = False,
    as_row: bool = True,
    request_url: str = "",
    hx_target_id: str = "",
    hx_swap_method: str = "outerHTML",
    method: str = "",
    current_value: str = "",
) -> dict[str, Any]:
    """
    Render a group of radio buttons as a block.

    Args:
    ----
        config: RadioBlockConfig dataclass with all parameters.
        name: The name of the radio block.
        label: Label text displayed above the radio buttons.
        items: A list of radio-button configurations.
        integrated: False if the component should have its own <form> element.
        as_row: False if the elements should be arranged in a column.
        request_url: Url for the request on change.
        hx_target_id: The ID of the target element for HTMX.
        hx_swap_method: The HTMX swap method.
        method: JavaScript method to execute on change.
        current_value: The currently selected value.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = RadioBlockConfig(
            name, label, items, integrated, as_row, request_url, hx_target_id, hx_swap_method, method, current_value
        )

    return {"radio_block_config": config}


@register.inclusion_tag("insight_ui/components/range_slider.html")
def slider(
    config: SliderConfig | None = None,
    *,
    tag_id: str | None = None,
    name: str | None = None,
    value: int | None = None,
    minimum: int = 0,
    maximum: int = 100,
    step_size: int = 1,
    label: str | None = None,
    disabled: bool = False,
    items: list[str] | None = None,
    legend_mode: str = "static",
    dual: bool = False,
    value_min: int | None = None,
    value_max: int | None = None,
) -> dict[str, Any]:
    """
    Render a range slider.

    Args:
    ----
        config: SliderConfig dataclass with all parameters.
        tag_id: A unique ID for linking <input> and <label>.
        name: Required for a <form> as the name of the request parameter.
        value: The value of the slider (single-thumb mode).
        minimum: The smallest value of the slider.
        maximum: The largest value of the slider.
        step_size: The size of the slider's steps.
        label: Label text displayed above the slider.
        disabled: True if the slider should be disabled.
        items: Legend labels displayed below the slider.
        legend_mode: Responsive legend behavior ('static', 'skip', 'rotate').
        dual: Enable dual-thumb mode for range selection.
        value_min: The minimum value in dual-thumb mode.
        value_max: The maximum value in dual-thumb mode.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = SliderConfig(
            tag_id,
            name,
            label,
            disabled,
            False,
            value,
            minimum,
            maximum,
            step_size,
            items,
            legend_mode,
            dual,
            value_min,
            value_max,
        )

    return {"slider_config": config}


@register.inclusion_tag("insight_ui/components/toggle_button.html")
def toggle(
    config: ToggleConfig | None = None,
    *,
    tag_id: str | None = None,
    name: str | None = None,
    value: str = "",
    label: str | None = None,
    icon: IconConfig | None = None,
    checked: bool = False,
    disabled: bool = False,
    switch: bool = False,
    method: str = "",
) -> dict[str, Any]:
    """
    Render a toggle button.

    Args:
    ----
        config: ToggleConfig dataclass with all parameters.
        tag_id: A unique ID for linking <input> and <label>.
        name: Required for a <form> as the name of the request parameter.
        value: The value of the toggle (not the state).
        label: Label text displayed above the toggle.
        icon: An icon displayed next to the text.
        checked: True if the toggle should be selected.
        disabled: True if the toggle should be disabled.
        switch: True if the toggle should look like a switch.
        method: JavaScript method to execute on change.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = ToggleConfig(tag_id, name, label, disabled, False, value, icon, checked, switch, method)

    return {"toggle_config": config}


@register.inclusion_tag("insight_ui/components/select.html")
def select(
    config: SelectConfig | None = None,
    *,
    tag_id: str | None = None,
    name: str | None = None,
    label: str | None = None,
    required: bool = False,
    explanation: str = "",
    options: list[str] | dict[str, str] | None = None,
    selected_option: str = "",
) -> dict[str, Any]:
    """
    Render a selection box.

    Args:
    ----
        config: SelectConfig dataclass with all parameters.
        tag_id: A unique ID for linking <input> and <label>.
        name: The name of the select element.
        required: True if an option must be selected.
        label: A short title that appears above the select box.
        explanation: A brief description that appears in a tooltip.
        options: All values that can be selected.
        selected_option: A value that has already been selected.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        if isinstance(options, list):
            options = dict(zip(options, options))

        config = SelectConfig(tag_id, name, label, False, required, explanation, options, selected_option)
    elif isinstance(config.options, list):
        config.options = dict(zip(config.options, config.options))

    return {"select_config": config}


@register.inclusion_tag("insight_ui/components/multiselect.html")
def multiselect(
    config: MultiselectConfig | None = None,
    *,
    name: str | None = None,
    label: str | None = None,
    maximum: int | None = None,
    show_buttons: bool = False,
    options: list[str] | dict[str, str] | None = None,
    selected_options: list[str] | None = None,
) -> dict[str, Any]:
    """
    Render a selection box that allows multiple values.

    Args:
    ----
        config: MultiselectConfig dataclass with all parameters.
        name: The name of the multiselect element.
        label: A short title that appears above the multiselect.
        maximum: Maximum number of values that may be selected.
        show_buttons: Display "Select All" and "Deselect All" buttons.
        options: All values that can be selected.
        selected_options: All values that should already be selected.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        if isinstance(options, list):
            options = dict(zip(options, options))
        config = MultiselectConfig("", name, label, False, False, maximum, show_buttons, options, selected_options)
    elif isinstance(config.options, list):
        config.options = dict(zip(config.options, config.options))

    return {"multiselect_config": config}


@register.inclusion_tag("insight_ui/components/chat.html")
def chat(request_url: str) -> dict[str, Any]:
    """
    Render a chat with an input line and a place for the response.

    Args:
    ----
        request_url: The URL to which the request should be sent.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"request_url": request_url}


# =============================================================
#
#   Popup Tags
#
# =============================================================


@register.inclusion_tag("insight_ui/components/alert.html")
def alert(
    config: AlertConfig | None = None,
    *,
    tag_id: str = "",
    message: str = "",
    type: str = "info",  # noqa: A002
    dismissible: bool = True,
) -> dict[str, Any]:
    """
    Render a closable notification.

    Args:
    ----
        config: AlertConfig dataclass with all parameters.
        tag_id: An optional, unique ID for JavaScript.
        message: The message of the notification.
        type: The type of notification ('info', 'success', 'warning', 'error').
        dismissible: True if the notification should be closable.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = AlertConfig(tag_id, message, type, dismissible)

    return {"alert_config": config}


@register.inclusion_tag("insight_ui/components/modal.html")
def modal(
    config: ModalConfig | None = None,
    *,
    tag_id: str = "",
    title: str = "",
    description: str | list[str] = "",
    actions: Sequence[ActionConfig] | None = None,
    width: int = 32,
) -> dict[str, Any]:
    """
    Render an accessible modal dialog.

    Args:
    ----
        config: ModalConfig dataclass with all parameters.
        tag_id: A unique ID for the modal.
        title: The title of the modal.
        description: Text description of the modal.
        actions: A list of action buttons.
        width: The maximum width of the dialog box in 'rem'.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = ModalConfig(tag_id, title, description, actions, width)

    config.description = ensure_list(config.description)

    return {"modal_config": config}


# =============================================================
#
#   Util Tags
#
# =============================================================


@register.inclusion_tag("insight_ui/components/infobox.html")
def infobox(config: InfoboxConfig | None = None, *, info_type: str = "", message: str = "", **kwargs) -> dict[str, Any]:
    """
    Render a small box of information.

    Args:
    ----
        config: InfoConfig dataclass with all parameters.
        info_type: Importance level of the message ('info', 'warn', 'danger').
        message: Descriptive message.
        kwargs: Variables inserted into the message using 'format'.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = InfoboxConfig(message, info_type)

    if kwargs:
        try:
            config.message = config.message.format(**kwargs)
        except (KeyError, ValueError):
            config.message = config.message

    return {"info_config": config}


@register.inclusion_tag("insight_ui/components/copyright_notice.html")
def copyright_notice(
    config: CopyrightNoticeConfig | None = None,
    *,
    year: int | str | None = None,
    holder: str | None = None,
    source_label: str | None = None,
    license_text: str | None = None,
    license_url: str | None = None,
    separator: str | None = None,
    rights_text: str | None = None,
) -> dict[str, Any]:
    """
    Render a reusable copyright and legal notice line.

    Args:
    ----
        config: CopyrightNoticeConfig dataclass with all parameters.
        year: Optional copyright year.
        holder: Copyright holder name.
        source_label: Optional source/distribution label.
        license_text: Optional license label.
        license_url: Optional URL for the license label.
        separator: Separator between legal metadata parts.
        rights_text: Optional rights statement.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = CopyrightNoticeConfig(year, holder, source_label, license_text, license_url, separator, rights_text)

    metadata = [
        {"text": config.source_label or "", "url": ""},
        {"text": config.license_text or "", "url": config.license_url or ""},
        {"text": config.rights_text or _("All rights reserved."), "url": ""},
    ]

    return {"copyright_config": config, "metadata": [item for item in metadata if item["text"]]}


@register.filter
def diff(a: str, b: str, simple: bool = True) -> str:
    """
    Generate a visualization of the differences between two texts.

    Args:
    ----
        a: The original version of the text.
        b: The modified version of the text.
        simple: 'True' for a simplified display.

    Returns:
    -------
        The HTML code for the graphical representation of the differences.

    """
    if not simple:
        differentiator = HtmlDiff()
        differentiator._file_template = file_template
        differentiator._styles = styles
        diff_result = unified_diff(a.splitlines(), b.splitlines(), lineterm="")
        return "\n".join(list(diff_result))

    diff_result = ndiff(a.split(), b.split())
    html = ""

    for word in diff_result:
        if word.startswith("  "):
            html += f"{word[2:]} "
        elif word.startswith("- "):
            html += f"<span class='del'>{word[2:]}</span> "
        elif word.startswith("+ "):
            html += f"<span class='ins'>{word[2:]}</span> "

    return f"""
        <style>
            .del {{ background-color: #ffbbbb; color: #721c24; text-decoration: line-through; }}
            .ins {{ background-color: #bbffbb; color: #155724; }}
        </style>
        <p class='text-primary'>{html}</p>
    """


@register.inclusion_tag("insight_ui/components/logo.html")
def logo(
    config: LogoConfig | None = None,
    *,
    url: str | None = None,
    url_dark: str | None = None,
    alt: str | None = None,
    icon_name: str | None = None,
    icon_size: str | None = None,
    height: str | None = None,
    width: str | None = None,
) -> dict[str, Any]:
    """
    Render a brand logo as an image, SVG asset, or Insight UI icon.

    Args:
    ----
        config: LogoConfig dataclass with all parameters.
        url: Static, absolute, root-relative, or data URL for image/svg logos.
        url_dark: Optional dark-theme URL for image/svg logos.
        alt: Accessible text. Empty values mark image/svg logos as decorative.
        icon_name: Insight UI icon name (alternative to icon config).
        icon_size: Insight UI icon size (alternative to icon config).
        height: CSS height for image/svg logos.
        width: Optional CSS width for image/svg logos.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        icon = IconConfig(icon_name, icon_size) if icon_name else None
        config = LogoConfig(url, url_dark, alt, icon, "", "", height, width)

    config.url = _resolve_asset_url(config.url)
    config.url_dark = _resolve_asset_url(config.url_dark)

    return {
        "logo_config": config,
        "type": "icon" if config.icon else "svg" if str(config.url or "").lower().endswith(".svg") else "image",
        "has_dark_variant": bool(config.url_dark and config.url_dark != config.url),
    }


@register.inclusion_tag("insight_ui/components/corner_ribbon.html")
def corner_ribbon(
    config: CornerRibbonConfig | None = None, *, text: str = "", position: str = "top-right", color: str = "primary"
) -> dict[str, Any]:
    """
    Render a corner ribbon positioned in any browser corner.

    Args:
    ----
        config: CornerRibbonConfig dataclass with all parameters.
        text: The text displayed in the ribbon.
        position: Corner position.
        color: Color variant.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = CornerRibbonConfig(text, position, color)

    return {"corner_ribbon_config": config}


@register.inclusion_tag("insight_ui/components/geo_map.html")
def geo_map(
    config: GeoMapConfig | None = None,
    *,
    initial_coords: list[float] = [],
    initial_zoom: int = 8,
    map_height: int = 36,
    datasets: list[GeoMapDatasetConfig] = [],
) -> dict[str, Any]:
    """
    Render an integrated geographic map.

    Args:
    ----
        config: GeoMapConfig dataclass with all parameters.
        initial_coords: Starting map center [lat, lon].
        initial_zoom: Starting zoom level.
        map_height: The height of the map in 'rem'.
        datasets: List of data layers to display.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = GeoMapConfig(datasets, initial_coords, initial_zoom, map_height)

    return {"map_config": config}


@register.inclusion_tag("insight_ui/components/charts/bar_chart.html")
def bar_chart(chart_id: str, chart: ChartConfig, chart_height: int = 24) -> dict[str, Any]:
    """
    Render a bar chart with Apache ECharts.

    Args:
    ----
        chart_id: A unique ID for the chart.
        chart: Contains the information and data for the chart.
        chart_height: The height of the chart in 'rem'.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"chart_id": chart_id, "chart": _to_dict(chart), "chart_height": chart_height}


@register.inclusion_tag("insight_ui/components/charts/line_chart.html")
def line_chart(chart_id: str, chart: ChartConfig | dict, chart_height: int = 24) -> dict[str, Any]:
    """
    Render a line chart with Apache ECharts.

    Args:
    ----
        chart_id: A unique ID for the chart.
        chart: Contains the information and data for the chart.
        chart_height: The height of the chart in 'rem'.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"chart_id": chart_id, "chart": _to_dict(chart), "chart_height": chart_height}


@register.inclusion_tag("insight_ui/components/live_content.html")
def live_content(
    config: LiveContentConfig | None = None,
    *,
    tag_id: str = "",
    request_url: str = "",
    interval: int = 10,
    initial_content: str = "",
) -> dict[str, Any]:
    """
    Render a container for live updates via HTMX.

    Args:
    ----
        config: LiveContentConfig dataclass with all parameters.
        tag_id: An optional, unique ID for JavaScript.
        request_url: The URL for content updates.
        interval: The interval for automatic updates in seconds.
        initial_content: Optional initial content.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = LiveContentConfig(tag_id, request_url, interval, initial_content)

    htmx_config = {"request_url": request_url, "trigger": f"load, every {interval}s", "swap": "innerHTML"}

    return {"live_content_config": config, "htmx_config": htmx_config}


@register.inclusion_tag("insight_ui/components/websocket.html")
def insight_websocket(
    config: WebSocketConfig | None = None, *, tag_id: str = "", request_url: str = "", initial_content: str = ""
) -> dict[str, Any]:
    """
    Render a WebSocket component as a thin wrapper for the HTMX ws extension.

    Args:
    ----
        config: WebSocketConfig dataclass with all parameters.
        tag_id: The ID of the WebSocket container.
        request_url: The WebSocket endpoint URL.
        initial_content: Initial content.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = WebSocketConfig(tag_id, request_url, initial_content)

    return {"websocket_config": config}


# =============================================================
#
#   List Tags
#
# =============================================================


@register.inclusion_tag("insight_ui/components/infinite_scroll.html")
def infinite_scroll(
    config: InfiniteScrollConfig | None = None,
    *,
    tag_id: str = "",
    request_url: str = "",
    items: Sequence[Any] | None = None,
    page: int = 1,
    has_next: bool = True,
    auto_fetch: bool = True,
    threshold: int = 100,
) -> dict[str, Any]:
    """
    Render a container for infinite scroll.

    Args:
    ----
        config: InfiniteScrollConfig dataclass with all parameters.
        tag_id: An optional, unique ID for JavaScript.
        request_url: Url for loading additional elements.
        items: List of items already loaded.
        page: The number of the current page.
        has_next: True if further elements are available.
        auto_fetch: False if the user should request elements via a button.
        threshold: The pixel threshold for loading additional elements.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = InfiniteScrollConfig(tag_id, request_url, items, page, has_next, auto_fetch, threshold)

    return {"infinite_scroll_config": config}


@register.inclusion_tag("insight_ui/components/pagination.html")
def pagination(
    current_page: Page, surrounding_pages: list[int], ipp_config: PaginationIppConfig | None = None
) -> dict[str, Any]:
    """
    Render pagination with items per page selection.

    Args:
    ----
        current_page: Django pagination Page object for the current page.
        surrounding_pages: A list of neighboring page numbers.
        ipp_config: Configuration for the items-per-page selector.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {
        "current_page": current_page,
        "surrounding_pages": surrounding_pages,
        "ipp_config": ipp_config if ipp_config else {},
    }


@register.inclusion_tag("insight_ui/components/table.html")
def table(config: TableConfig) -> dict[str, Any]:
    """
    Render a simple table.

    Args:
    ----
        config: TableConfig dataclass with table configuration.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"table_config": config}


# =============================================================
#
#   Filter Tags
#
# =============================================================


@register.inclusion_tag("insight_ui/components/search_bar.html")
def search_bar(
    config: SearchBarConfig | None = None,
    *,
    request_url: str = "",
    simple: bool = False,
    search_query: str = "",
    htmx_config: HtmxConfig | None = None,
) -> dict[str, Any]:
    """
    Render text input with a button for a search function.

    Args:
    ----
        config: SearchBarConfig dataclass with all parameters.
        request_url: Url for search requests.
        simple: If True, render compact/minimal style without 'send' button.
        search_query: Initial search query value.
        htmx_config: HTMX configuration for AJAX requests.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = SearchBarConfig(request_url, simple, search_query, htmx_config)

    return {"search_bar_config": config}


@register.inclusion_tag("insight_ui/components/generic_filter.html")
def generic_filter(
    config: GenericFilterConfig | None = None,
    *,
    filters: list | None = None,
    request_url: str = "",
    vertical: bool = False,
    htmx_config: HtmxConfig | None = None,
) -> dict[str, Any]:
    """
    Render a generic filter consisting of one or more <select> fields.

    Args:
    ----
        config: GenericFilterConfig dataclass with all parameters.
        filters: A list of individual filters.
        request_url: The URL to which the request should be sent.
        vertical: True if the filters should be arranged vertically.
        htmx_config: HTMX configuration for AJAX requests.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = GenericFilterConfig(filters, request_url, vertical, htmx_config)

    return {"generic_filter_config": config}


@register.inclusion_tag("insight_ui/components/search_query_builder/sq_builder.html")
def query_builder(model_fields: list[QueryBuilderFieldConfig]) -> dict[str, Any]:
    """
    Render a filter for constructing custom search queries.

    Args:
    ----
        model_fields: A list of model fields with possible operators.

    Returns:
    -------
        A dict with context variables for the template.

    """
    return {"model_fields": model_fields}


# =============================================================
#
#   Card Tags
#
# =============================================================


@register.inclusion_tag("insight_ui/components/cards/card.html")
def card(
    config: CardConfig | None = None,
    *,
    title: str = "",
    content: str = "",
    subtitle: str = "",
    image: ImageConfig | dict[str, str] | None = None,
    actions: list[ActionConfig | dict[str, str]] | None = None,
) -> dict[str, Any]:
    """
    Render a card with an aspect ratio of 16:9.

    Args:
    ----
        config: CardConfig dataclass with all parameters.
        title: The title of the card.
        content: The main content of the card.
        subtitle: An optional subtitle for the card.
        image: Information about the image on the card.
        actions: A list of action buttons.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = CardConfig(title, content, subtitle, image, actions)

    return {"card_config": config}


@register.inclusion_tag("insight_ui/components/cards/app_card.html")
def app_card(
    config: AppCardConfig | None = None,
    *,
    title: str = "",
    content: str = "",
    tags: list[str] | None = None,
    request_url: str = "",
    image: ImageConfig | dict[str, str] | None = None,
    actions: list[ActionConfig | dict[str, str]] | None = None,
) -> dict[str, Any]:
    """
    Render a vertically aligned card.

    Args:
    ----
        config: AppCardConfig dataclass with all parameters.
        title: The title of the card.
        content: The main content of the card.
        tags: A list of tag labels.
        request_url: A URL when the user clicks on the title.
        image: Information about the image on the card.
        actions: A list of action buttons.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = AppCardConfig(title, content, request_url, image, tags, actions)

    return {"app_card_config": config}


@register.inclusion_tag("insight_ui/components/cards/flip_card.html")
def flip_card(
    config: FlipCardConfig | None = None,
    *,
    title: str = "",
    content: str = "",
    tags: list[str] | None = None,
    request_url: str = "",
    image: ImageConfig | dict[str, str] | None = None,
    actions: list[ActionConfig | dict[str, str]] | None = None,
) -> dict[str, Any]:
    """
    Render a card that can be rotated 180°.

    Args:
    ----
        config: FlipCardConfig dataclass with all parameters.
        title: The title of the card.
        content: The main content of the card.
        tags: A list of tag labels.
        request_url: A URL when the user clicks on the title.
        image: Information about the image on the card.
        actions: A list of action buttons.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = FlipCardConfig(title, content, request_url, image, tags, actions)

    return {"flip_card_config": config}


@register.inclusion_tag("insight_ui/components/carousels/card_carousel.html")
def carousel(
    config: CardCarouselConfig | None = None,
    *,
    carousel_items: Sequence[Mapping[str, Any]] | None = None,
    autoplay: bool = False,
    show_dots: bool = True,
    show_index: bool = False,
    items_per_slide: int = 1,
) -> dict[str, Any]:
    """
    Render a card carousel.

    Args:
    ----
        config: CardCarouselConfig dataclass with all parameters.
        carousel_items: Content to be displayed (cards).
        autoplay: Automatically switch to the next page.
        show_dots: Show pagination dots below the content.
        show_index: Display number and current page.
        items_per_slide: Number of items per page.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = CardCarouselConfig(carousel_items, autoplay, show_dots, show_index, items_per_slide)

    return {
        "carousel_config": config,
        "slides_count": range(math.ceil(len(config.carousel_items) / config.items_per_slide))
        if config.carousel_items
        else range(0),
    }


@register.inclusion_tag("insight_ui/components/carousels/image_carousel.html")
def image_carousel(
    config: ImageCarouselConfig | None = None,
    *,
    carousel_items: Sequence[Mapping[str, Any]] | None = None,
    autoplay: bool = False,
    show_dots: bool = True,
    show_index: bool = False,
    items_per_slide: int = 1,
) -> dict[str, Any]:
    """
    Render an image carousel.

    Args:
    ----
        config: ImageCarouselConfig dataclass with all parameters.
        carousel_items: Images to be displayed within the carousel.
        autoplay: Automatically switch to the next page.
        show_dots: Show pagination dots below the content.
        show_index: Display number and current page.
        items_per_slide: Number of items per page.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = ImageCarouselConfig(carousel_items, autoplay, show_dots, show_index, items_per_slide)

    return {
        "carousel_config": config,
        "slides_count": range(math.ceil(len(config.carousel_items) / config.items_per_slide))
        if config.carousel_items
        else range(0),
    }


@register.inclusion_tag("insight_ui/components/carousels/3D_carousel.html")
def three_d_carousel(
    config: ThreeDCarouselConfig | None = None,
    *,
    tag_id: str = "",
    velocity: int = 1000,
    tilt: int = 0,
    face_camera: bool = False,
    carousel_items: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """
    Render a 3D version of the carousel component.

    Args:
    ----
        config: ThreeDCarouselConfig dataclass with all parameters.
        tag_id: A unique ID for the carousel.
        velocity: The speed at which the carousel should rotate.
        tilt: The inclination of the carousel toward the camera.
        face_camera: True if the cards should always face the camera.
        carousel_items: Content to be displayed (cards).

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = ThreeDCarouselConfig(tag_id, carousel_items, velocity, tilt, face_camera)

    return {"carousel_config": config}


@register.inclusion_tag("insight_ui/components/toggle_view.html")
def toggle_view(
    config: ToggleViewConfig | None = None,
    *,
    tag_id: str = "",
    cards: list[CardConfig] = [],
    table_config: TableConfig = None,
    view_radio_config: RadioBlockConfig | None = None,
) -> dict[str, Any]:
    """
    Render a view of data that can be displayed in various ways.

    Args:
    ----
        config: ToggleViewConfig dataclass with all parameters.
        tag_id: A unique ID for the component.
        cards: The cards to be displayed.
        table_config: Configuration of the table view.
        view_radio_config: Configuration of the radio group for view switching.
        current_view: The name of the current view type.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = ToggleViewConfig(tag_id, cards, table_config, view_radio_config)

    return {"toggle_view_config": config}


# =============================================================
#
#   Form Tags
#
# =============================================================


@register.inclusion_tag("insight_ui/components/form.html")
def form(
    config: FormConfig | None = None,
    *,
    tag_id: str = "",
    title: str = "",
    description: str = "",
    fields: Sequence[FormFieldConfig | Mapping[str, Any]] | None = None,
    show_reset_button: bool = False,
    request_url: str = "",
    htmx_config: HtmxConfig | Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Render a form with HTMX support.

    Args:
    ----
        config: FormConfig dataclass with all parameters.
        tag_id: An optional, unique ID for JavaScript.
        title: The title of the form.
        description: An optional description.
        fields: A list of form fields.
        show_reset_button: Display a "Reset" button.
        request_url: The Url of the endpoint for form submission.
        htmx_config: HTMX configuration for AJAX requests.

    Returns:
    -------
        A dict with context variables for the template.

    """
    if config is None:
        config = FormConfig(tag_id, title, description, fields, show_reset_button, request_url, htmx_config)

    return {"form_config": config}
