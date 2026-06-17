"""Template-Tags for Insight UI-Components."""

from __future__ import annotations

import math
import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import MISSING, fields, is_dataclass, replace
from difflib import HtmlDiff, ndiff, unified_diff
from types import UnionType
from typing import Any, Final, Literal, TypeVar, get_args, get_origin, get_type_hints

from django import template
from django.core.paginator import Page
from django.templatetags.static import static
from django.utils.functional import Promise
from django.utils.safestring import SafeString, mark_safe
from django.utils.translation import gettext as _
from markdown import markdown

from insight_ui.config import get_config
from insight_ui.configs import (
    AccordionConfig,
    ActionConfig,
    AlertConfig,
    AppCardConfig,
    ArticleConfig,
    BadgeConfig,
    BrandLockupConfig,
    BreadcrumbItemConfig,
    BreadcrumbsConfig,
    BulletPointItemConfig,
    BulletPointListConfig,
    ButtonConfig,
    CardCarouselConfig,
    CardConfig,
    CarouselItemConfig,
    ChartConfig,
    ChartDatasetConfig,
    ChatConfig,
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
    GeoMapDatasetConfig,
    HeroConfig,
    HtmxConfig,
    IconConfig,
    ImageCarouselConfig,
    ImageCarouselItemConfig,
    ImageConfig,
    InfiniteScrollConfig,
    InfoboxConfig,
    InputFieldConfig,
    LiveContentConfig,
    LogoConfig,
    MinimalStepperConfig,
    ModalConfig,
    MultiselectConfig,
    NavbarConfig,
    PageHeaderConfig,
    PaginationConfig,
    PaginationIppConfig,
    QueryBuilderConfig,
    QueryBuilderFieldConfig,
    RadioBlockConfig,
    RadioGroupConfig,
    RadioItemConfig,
    SearchBarConfig,
    SelectConfig,
    SidebarConfig,
    SidebarDataConfig,
    SliderConfig,
    StepperConfig,
    StepperItemConfig,
    TableConfig,
    TabsConfig,
    TextareaConfig,
    ThreeDCarouselConfig,
    ToggleConfig,
    ToggleViewConfig,
    WebSocketConfig,
)
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
T = TypeVar("T")


def _resolve_asset_url(value: object) -> str:
    """Resolve static asset paths while preserving absolute, root-relative, and data URLs."""
    if not value:
        return ""

    url = str(value)
    if url.startswith(("http://", "https://", "/", "data:")):
        return url

    return static(url)


def ensure_list(value: str | Iterable[str] | None) -> list[str]:
    """Take a string or a list of strings and return in both cases a list of strings."""
    if value is None:
        return []

    if isinstance(value, (str, Promise)):
        return [value]

    return list(value)


def _is_dataclass_type(annotation: object) -> bool:
    """Return whether a type annotation directly describes a dataclass config."""
    return isinstance(annotation, type) and is_dataclass(annotation)


def _coerce_mapping_to_config[T](cls: type[T], value: Mapping[str, Any]) -> T:
    """Create a dataclass config from a mapping, including nested config values."""
    type_hints = get_type_hints(cls)
    coerced_values = {key: _coerce_config_value(item, type_hints.get(key, Any)) for key, item in value.items()}
    return cls(**coerced_values)


def _coerce_sequence_to_config(value: Sequence[Any], annotation: object) -> list[Any]:
    """Convert list-like config values according to their annotated item type."""
    origin = get_origin(annotation)
    if origin in (list, Sequence):
        args = get_args(annotation)
        item_annotation = args[0] if args else Any
        return [_coerce_config_value(item, item_annotation) for item in value]

    if origin is UnionType:
        for option in get_args(annotation):
            option_origin = get_origin(option)
            if option_origin in (list, Sequence):
                return _coerce_sequence_to_config(value, option)

    return list(value)


def _expects_sequence_config(annotation: object) -> bool:
    """Return whether an annotation expects a list-like config value."""
    origin = get_origin(annotation)
    if origin in (list, Sequence):
        return True

    if origin is UnionType:
        return any(_expects_sequence_config(option) for option in get_args(annotation))

    return False


def _coerce_config_value(value: Any, annotation: object) -> Any:  # noqa: ANN401
    """Coerce mapping and sequence values into annotated dataclass config types."""
    origin = get_origin(annotation)

    if isinstance(value, Mapping):
        if _is_dataclass_type(annotation):
            return _coerce_mapping_to_config(annotation, value)

        if origin is UnionType:
            for option in get_args(annotation):
                if _is_dataclass_type(option):
                    return _coerce_mapping_to_config(option, value)

    if (
        isinstance(value, Sequence)
        and not isinstance(value, (str, bytes, bytearray))
        and _expects_sequence_config(annotation)
    ):
        return _coerce_sequence_to_config(value, annotation)

    return value


def build_config[T](cls: type[T], config: T | None = None, **kwargs: Any) -> T:  # noqa: ANN401
    """
    Create or update a dataclass instance.

    Parameters with value UNSET are ignored.

    If config is None:
        Creates a new instance and validates required fields.

    If config is given:
        Returns a copy with provided overrides applied.
    """
    overrides = {key: value for key, value in kwargs.items() if value is not UNSET}

    if isinstance(config, Mapping):
        return _coerce_mapping_to_config(cls, dict(config) | overrides)

    if config is not None and is_dataclass(config):
        return replace(config, **overrides)

    required_fields = [
        field.name for field in fields(cls) if field.default is MISSING and field.default_factory is MISSING
    ]

    missing = [field_name for field_name in required_fields if field_name not in overrides]

    if missing:
        raise ValueError(f"Missing required fields for {cls.__name__}: {', '.join(missing)}")  # noqa: TRY003

    return cls(**overrides)


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


@register.inclusion_tag("insight_ui/components/icons.html")
def icon(
    config: IconConfig | None = None,
    *,
    name: str | _Unset = UNSET,
    size: str | _Unset = UNSET,
    color: str | _Unset = UNSET,
) -> dict[str, Any]:
    """Render specified icon with given size."""
    config = build_config(IconConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"icon_config": config}


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
    """Render a page header in the base template."""
    config = build_config(PageHeaderConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    config.description = ensure_list(config.description)

    return {"page_header_config": config}


@register.inclusion_tag("insight_ui/components/article.html")
def article(
    config: ArticleConfig | None = None,
    *,
    content: str | _Unset = UNSET,
    columns: int | _Unset = UNSET,
    column_gap: str | _Unset = UNSET,
    title: str | _Unset = UNSET,
) -> dict[str, Any]:
    """Render an article in newspaper style with a multi-column layout."""
    config = build_config(ArticleConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"article_config": config}


@register.inclusion_tag("insight_ui/components/hero.html")
def hero(
    config: HeroConfig | None = None,
    *,
    title: str | _Unset = UNSET,
    subtitle: str | _Unset = UNSET,
    description: str | _Unset = UNSET,
    cta_primary: ActionConfig | _Unset = UNSET,
    cta_secondary: ActionConfig | _Unset = UNSET,
    background_image_url: str | _Unset = UNSET,
    badge_config: BadgeConfig | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a hero section with optional background image."""
    config = build_config(HeroConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"hero_config": config}


# =============================================================
#
#   Navigation Tags
#
# =============================================================


@register.inclusion_tag("insight_ui/components/navbar.html", takes_context=True)
def navbar(context: dict[str, Any], config: NavbarConfig, **kwargs: JsonValue) -> dict[str, Any]:
    """Render a configurable navigation bar."""
    return {
        "user": context.get("user"),
        "navbar_config": config,
        "fixed": get_config("navbar_fixed"),
        "options": {**kwargs},
    }


@register.inclusion_tag("insight_ui/components/sidebar.html")
def sidebar(
    config: SidebarConfig | None = None,
    *,
    sidebar_data: SidebarDataConfig | _Unset = UNSET,
    side: str | _Unset = UNSET,
    static: bool | _Unset = UNSET,
    auto_close: bool | _Unset = UNSET,
    mobile_hidden: bool | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a configurable page navigation."""
    config = build_config(SidebarConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {
        "sidebar_config": config,
        "sidebar_data": config.sidebar_data,
        "side": config.side,
        "static": config.static,
        "auto_close": config.auto_close,
        "mobile_hidden": config.mobile_hidden,
        "navbar_fixed": get_config("navbar_fixed"),
    }


@register.inclusion_tag("insight_ui/components/footer.html")
def footer(config: FooterConfig) -> dict[str, Any]:
    """Render a footer with optional description, links, and a copyright line."""
    return {"footer_config": config}


@register.inclusion_tag("insight_ui/components/breadcrumbs.html")
def breadcrumbs(
    config: BreadcrumbsConfig | None = None, *, items: list[BreadcrumbItemConfig] | None | _Unset = UNSET
) -> dict[str, Any]:
    """Render breadcrumb navigation."""
    config = build_config(BreadcrumbsConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"items": config.items, "htmx": config.htmx}


@register.inclusion_tag("insight_ui/components/stepper.html")
def stepper(
    config: StepperConfig | None = None, *, items: list[StepperItemConfig] | None | _Unset = UNSET
) -> dict[str, Any]:
    """Render a graphical representation of process steps."""
    config = build_config(StepperConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"items": config.items}


@register.inclusion_tag("insight_ui/components/minimal_stepper.html")
def minimal_stepper(
    config: MinimalStepperConfig | None = None,
    *,
    items: list[Literal["active", "success", "failed", ""]] | _Unset = UNSET,
    step_count: int | _Unset = UNSET,
    current_step: int | _Unset = UNSET,
    current_step_status: Literal["active", "success", "failed"] | _Unset = UNSET,
    icon_size: Literal["xs", "s", "m", "l", "xl"] | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a compact graphical representation of process steps."""
    config = build_config(MinimalStepperConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})

    # Generate items from step_count if not provided
    if not config.items and config.step_count > 0:
        config.items = []
        for step in range(config.step_count):
            if step < config.current_step:
                config.items.append("success")
            elif step == config.current_step:
                config.items.append(config.current_step_status)
            else:
                config.items.append("")

    return {"items": config.items, "icon_size": config.icon_size}


@register.inclusion_tag("insight_ui/components/bullet_point_list.html")
def bullet_point_list(
    config: BulletPointListConfig | None = None, *, items: list[BulletPointItemConfig] | None | _Unset = UNSET
) -> dict[str, Any]:
    """Render a graphical representation of a bullet point list."""
    config = build_config(BulletPointListConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"items": config.items, "htmx": config.htmx}


@register.inclusion_tag("insight_ui/components/accordion.html")
def accordion(config: AccordionConfig) -> dict[str, Any]:
    """Render an accordion that can have one or more sections open."""
    return {"accordion_config": config}


@register.inclusion_tag("insight_ui/components/tabs.html")
def tabs(config: TabsConfig) -> dict[str, Any]:
    """Render a group of tabs and a container for the content of each tab."""
    return {"config": config}


# =============================================================
#
#   Input Tags
#
# =============================================================


@register.inclusion_tag("insight_ui/components/button.html")
def button(
    config: ButtonConfig | None = None,
    *,
    tag_id: str | _Unset = UNSET,
    label: str | _Unset = UNSET,
    request_url: str | _Unset = UNSET,
    on_click: str | _Unset = UNSET,
    icon_name: str | _Unset = UNSET,
    icon_size: str | _Unset = UNSET,
    icon_end: bool | _Unset = UNSET,
    icon_only: bool | _Unset = UNSET,
    type: Literal["primary", "secondary", "info", "success", "warning", "danger", "disabled"] | _Unset = UNSET,  # noqa: A002
    size: Literal["xs", "s", "m", "l", "xl"] | _Unset = UNSET,
    outline: bool | _Unset = UNSET,
    subtil: bool | _Unset = UNSET,
    tooltip: str | _Unset = UNSET,
    htmx_config: HtmxConfig | _Unset = UNSET,
) -> dict[str, Any]:
    """Render the button component."""
    icon: IconConfig | None | _Unset = UNSET
    if icon_name is not UNSET:
        icon = IconConfig(icon_name, icon_size if icon_size is not UNSET else "m") if icon_name else None

    config = build_config(
        ButtonConfig,
        config,
        tag_id=tag_id,
        label=label,
        request_url=request_url,
        on_click=on_click,
        icon=icon,
        icon_end=icon_end,
        icon_only=icon_only,
        type=type,
        size=size,
        outline=outline,
        subtil=subtil,
        tooltip=tooltip,
        htmx_config=htmx_config,
    )
    return {"button_config": config}


@register.inclusion_tag("insight_ui/components/input.html")
def input_field(
    config: InputFieldConfig | None = None,
    *,
    tag_id: str | None | _Unset = UNSET,
    name: str | None | _Unset = UNSET,
    input_type: str | _Unset = UNSET,
    placeholder: str | _Unset = UNSET,
    value: str | int | float | None | _Unset = UNSET,
    minimum: int | None | _Unset = UNSET,
    maximum: int | None | _Unset = UNSET,
    min_length: int | None | _Unset = UNSET,
    max_length: int | None | _Unset = UNSET,
    checked: bool | _Unset = UNSET,
    required: bool | _Unset = UNSET,
    disabled: bool | _Unset = UNSET,
    label: str | None | _Unset = UNSET,
) -> dict[str, Any]:
    """Render any <input> field."""
    config = build_config(InputFieldConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"input_config": config}


@register.inclusion_tag("insight_ui/components/textarea.html")
def textarea(
    config: TextareaConfig | None = None,
    *,
    tag_id: str | None | _Unset = UNSET,
    name: str | None | _Unset = UNSET,
    placeholder: str | _Unset = UNSET,
    value: str | _Unset = UNSET,
    rows: int | _Unset = UNSET,
    cols: int | None | _Unset = UNSET,
    required: bool | _Unset = UNSET,
    disabled: bool | _Unset = UNSET,
    label: str | None | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a <textarea> field."""
    config = build_config(TextareaConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"textarea_config": config}


@register.inclusion_tag("insight_ui/components/checkbox.html")
def checkbox(
    config: CheckboxConfig | None = None,
    *,
    tag_id: str | None | _Unset = UNSET,
    name: str | None | _Unset = UNSET,
    value: str | _Unset = UNSET,
    label: str | None | _Unset = UNSET,
    checked: bool | _Unset = UNSET,
    disabled: bool | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a checkbox with label text."""
    config = build_config(CheckboxConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"checkbox_config": config}


@register.inclusion_tag("insight_ui/components/checkbox_group.html")
def checkbox_group(config: CheckboxGroupConfig) -> dict[str, Any]:
    """Render a group of checkbox elements."""
    return {"checkbox_group_config": config}


@register.inclusion_tag("insight_ui/components/dropdown.html")
def dropdown(config: DropdownConfig) -> dict[str, Any]:
    """Render a dropdown menu."""
    return {"dropdown_config": config}


@register.inclusion_tag("insight_ui/components/radio_group.html")
def radio_group(
    config: RadioGroupConfig | None = None,
    *,
    name: str | _Unset = UNSET,
    label: str | _Unset = UNSET,
    items: list[RadioItemConfig] | None | _Unset = UNSET,
    as_row: bool | _Unset = UNSET,
    current_value: str | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a group of radio buttons."""
    config = build_config(RadioGroupConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"radio_group_config": config}


@register.inclusion_tag("insight_ui/components/radio_block.html")
def radio_block(
    config: RadioBlockConfig | None = None,
    *,
    name: str | _Unset = UNSET,
    label: str | _Unset = UNSET,
    items: list[RadioItemConfig] | None | _Unset = UNSET,
    integrated: bool | _Unset = UNSET,
    as_row: bool | _Unset = UNSET,
    request_url: str | _Unset = UNSET,
    hx_target_id: str | _Unset = UNSET,
    hx_swap_method: str | _Unset = UNSET,
    method: str | _Unset = UNSET,
    current_value: str | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a group of radio buttons as a block."""
    config = build_config(RadioBlockConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"radio_block_config": config}


@register.inclusion_tag("insight_ui/components/range_slider.html")
def slider(
    config: SliderConfig | None = None,
    *,
    tag_id: str | None | _Unset = UNSET,
    name: str | None | _Unset = UNSET,
    value: int | None | _Unset = UNSET,
    minimum: int | _Unset = UNSET,
    maximum: int | _Unset = UNSET,
    step_size: int | _Unset = UNSET,
    label: str | None | _Unset = UNSET,
    disabled: bool | _Unset = UNSET,
    items: list[str] | None | _Unset = UNSET,
    legend_mode: str | _Unset = UNSET,
    dual: bool | _Unset = UNSET,
    value_min: int | None | _Unset = UNSET,
    value_max: int | None | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a range slider."""
    config = build_config(SliderConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"slider_config": config}


@register.inclusion_tag("insight_ui/components/toggle_button.html")
def toggle(
    config: ToggleConfig | None = None,
    *,
    tag_id: str | None | _Unset = UNSET,
    name: str | None | _Unset = UNSET,
    value: str | _Unset = UNSET,
    label: str | None | _Unset = UNSET,
    icon: IconConfig | None | _Unset = UNSET,
    checked: bool | _Unset = UNSET,
    disabled: bool | _Unset = UNSET,
    switch: bool | _Unset = UNSET,
    method: str | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a toggle button."""
    config = build_config(ToggleConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"toggle_config": config}


@register.inclusion_tag("insight_ui/components/select.html")
def select(
    config: SelectConfig | None = None,
    *,
    tag_id: str | None | _Unset = UNSET,
    name: str | None | _Unset = UNSET,
    label: str | None | _Unset = UNSET,
    required: bool | _Unset = UNSET,
    explanation: str | _Unset = UNSET,
    options: list[str] | dict[str, str] | None | _Unset = UNSET,
    selected_option: str | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a selection box."""
    if config is None:
        if isinstance(options, list):
            options = dict(zip(options, options))
    elif isinstance(config.options, list):
        config.options = dict(zip(config.options, config.options))

    config = build_config(SelectConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"select_config": config}


@register.inclusion_tag("insight_ui/components/multiselect.html")
def multiselect(
    config: MultiselectConfig | None = None,
    *,
    name: str | None | _Unset = UNSET,
    label: str | None | _Unset = UNSET,
    maximum: int | None | _Unset = UNSET,
    show_buttons: bool | _Unset = UNSET,
    options: list[str] | dict[str, str] | None | _Unset = UNSET,
    selected_options: list[str] | None | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a selection box that allows multiple values."""
    if config is None:
        if isinstance(options, list):
            options = dict(zip(options, options))
    elif isinstance(config.options, list):
        config.options = dict(zip(config.options, config.options))

    config = build_config(MultiselectConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"multiselect_config": config}


@register.inclusion_tag("insight_ui/components/chat.html")
def chat(config: ChatConfig | None = None, *, request_url: str | _Unset = UNSET) -> dict[str, Any]:
    """Render a chat with an input line and a place for the response."""
    config = build_config(ChatConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"request_url": config.request_url}


# =============================================================
#
#   Popup Tags
#
# =============================================================


@register.inclusion_tag("insight_ui/components/alert.html")
def alert(
    config: AlertConfig | None = None,
    *,
    tag_id: str | _Unset = UNSET,
    message: str | _Unset = UNSET,
    type: str | _Unset = UNSET,  # noqa: A002
    dismissible: bool | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a closable notification."""
    config = build_config(AlertConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"alert_config": config}


@register.inclusion_tag("insight_ui/components/modal.html")
def modal(
    config: ModalConfig | None = None,
    *,
    tag_id: str | _Unset = UNSET,
    title: str | _Unset = UNSET,
    description: str | list[str] | _Unset = UNSET,
    actions: Sequence[ActionConfig] | None | _Unset = UNSET,
    width: int | _Unset = UNSET,
) -> dict[str, Any]:
    """Render an accessible modal dialog."""
    config = build_config(ModalConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    config.description = ensure_list(config.description)
    return {"modal_config": config}


# =============================================================
#
#   Util Tags
#
# =============================================================


@register.inclusion_tag("insight_ui/components/infobox.html")
def infobox(
    config: InfoboxConfig | None = None, *, info_type: str | _Unset = UNSET, message: str | _Unset = UNSET, **kwargs
) -> dict[str, Any]:
    """Render a small box of information."""
    config = build_config(InfoboxConfig, config, info_type=info_type, message=message)

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
    year: int | str | None | _Unset = UNSET,
    holder: str | None | _Unset = UNSET,
    source_label: str | None | _Unset = UNSET,
    license_text: str | None | _Unset = UNSET,
    license_url: str | None | _Unset = UNSET,
    separator: str | None | _Unset = UNSET,
    rights_text: str | None | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a reusable copyright and legal notice line."""
    config = build_config(CopyrightNoticeConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
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
    url: str | None | _Unset = UNSET,
    url_dark: str | None | _Unset = UNSET,
    alt: str | None | _Unset = UNSET,
    icon_name: str | None | _Unset = UNSET,
    icon_size: str | None | _Unset = UNSET,
    height: str | None | _Unset = UNSET,
    width: str | None | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a brand logo as an image, SVG asset, or Insight UI icon."""
    # Only override icon if icon_name was explicitly provided
    icon: IconConfig | None | _Unset = UNSET
    if icon_name is not UNSET:
        icon = IconConfig(icon_name, icon_size if icon_size is not UNSET else "m") if icon_name else None

    config = build_config(
        LogoConfig,
        config,
        url=url,
        url_dark=url_dark,
        alt=alt,
        icon=icon,
        icon_name="",
        icon_size="",
        height=height,
        width=width,
    )

    config.url = _resolve_asset_url(config.url)
    config.url_dark = _resolve_asset_url(config.url_dark)

    return {
        "logo_config": config,
        "type": "icon" if config.icon else "svg" if str(config.url or "").lower().endswith(".svg") else "image",
        "has_dark_variant": bool(config.url_dark and config.url_dark != config.url),
    }


BRAND_LOCKUP_VARIANTS = ("main", "develop", "candidate")
BRAND_LOCKUP_ICON_BY_VARIANT = {"main": "app", "develop": "rocket", "candidate": "sparkles"}
CSS_SIZE_PATTERN = re.compile(r"^-?(?:\d+(?:\.\d+)?|\.\d+)(?:px|rem|em|vh|vw|vmin|vmax|%|ch|ex|lh|rlh)$")


def _looks_like_css_size(value: object) -> bool:
    """Return true when a positional value is intended as a CSS size."""
    normalized = str(value).strip().lower()
    return normalized in {"auto", "inherit", "initial", "revert", "unset"} or bool(CSS_SIZE_PATTERN.match(normalized))


def _normalize_brand_lockup_variant(value: object) -> str:
    """Normalize public variants and a small set of legacy aliases."""
    normalized = str(value).strip().lower()
    if normalized in BRAND_LOCKUP_VARIANTS:
        return normalized
    return "main"


@register.inclusion_tag("insight_ui/components/brand_lockup.html")
def brand_lockup(  # noqa: PLR0913
    primary_text: str = "Alpin Insight",
    secondary_text: str = "Solutions",
    logo_position: str = "start",
    height: str = "1.75rem",
    variant: str = "main",
    css_class: str | None = None,
    config: BrandLockupConfig | Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Render a public icon plus a two-tone wordmark."""
    if config is None:
        height_or_variant = str(height).strip().lower()
        variant_or_height = str(variant).strip().lower()
        if height_or_variant not in BRAND_LOCKUP_VARIANTS and not _looks_like_css_size(height):
            if variant != "main" and _looks_like_css_size(variant):
                height, variant = variant, height
            elif variant == "main":
                variant = height
                height = "1.75rem"
        elif variant == "main" and height_or_variant in BRAND_LOCKUP_VARIANTS:
            variant = height
            height = "1.75rem"
        elif variant != "main" and variant_or_height not in BRAND_LOCKUP_VARIANTS and _looks_like_css_size(variant):
            height, variant = variant, height

        config = BrandLockupConfig(
            primary_text=primary_text,
            secondary_text=secondary_text,
            logo_position="end" if str(logo_position).strip().lower() == "end" else "start",
            height=height,
            variant=_normalize_brand_lockup_variant(variant),
            css_class=css_class or "",
        )
    elif isinstance(config, Mapping):
        config = BrandLockupConfig(
            primary_text=str(config.get("primary_text", primary_text) or ""),
            secondary_text=str(config.get("secondary_text", secondary_text) or ""),
            logo_position=(
                "end" if str(config.get("logo_position", logo_position)).strip().lower() == "end" else "start"
            ),
            height=str(config.get("height", height) or "1.75rem"),
            variant=_normalize_brand_lockup_variant(config.get("variant", variant)),
            css_class=str(config.get("css_class", config.get("class", css_class or "")) or ""),
        )
    else:
        config = replace(
            config,
            logo_position="end" if str(config.logo_position).strip().lower() == "end" else "start",
            variant=_normalize_brand_lockup_variant(config.variant),
        )

    return {
        "primary_text": config.primary_text,
        "secondary_text": config.secondary_text,
        "logo_position": config.logo_position,
        "variant": config.variant,
        "icon_name": BRAND_LOCKUP_ICON_BY_VARIANT[config.variant],
        "icon_size": "l",
        "height": config.height,
        "css_class": config.css_class,
    }


@register.inclusion_tag("insight_ui/components/corner_ribbon.html")
def corner_ribbon(
    config: CornerRibbonConfig | None = None,
    *,
    text: str | _Unset = UNSET,
    position: str | _Unset = UNSET,
    color: str | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a corner ribbon positioned in any browser corner."""
    config = build_config(CornerRibbonConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"corner_ribbon_config": config}


@register.inclusion_tag("insight_ui/components/geo_map.html")
def geo_map(
    config: GeoMapConfig | None = None,
    *,
    initial_coords: list[float] | _Unset = UNSET,
    initial_zoom: int | _Unset = UNSET,
    map_height: int | _Unset = UNSET,
    datasets: list[GeoMapDatasetConfig] | _Unset = UNSET,
) -> dict[str, Any]:
    """Render an integrated geographic map."""
    config = build_config(GeoMapConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"map_config": config}


@register.inclusion_tag("insight_ui/components/charts/bar_chart.html")
def bar_chart(
    config: ChartConfig | None = None,
    *,
    tag_id: str | _Unset = UNSET,
    dataset: ChartDatasetConfig | None | _Unset = UNSET,
    chart_height: int | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a bar chart with Apache ECharts."""
    config = build_config(ChartConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"chart_config": config}


@register.inclusion_tag("insight_ui/components/charts/line_chart.html")
def line_chart(
    config: ChartConfig | None = None,
    *,
    tag_id: str | _Unset = UNSET,
    dataset: ChartDatasetConfig | None | _Unset = UNSET,
    chart_height: int | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a line chart with Apache ECharts."""
    config = build_config(ChartConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"chart_config": config}


@register.inclusion_tag("insight_ui/components/live_content.html")
def live_content(
    config: LiveContentConfig | None = None,
    *,
    tag_id: str | _Unset = UNSET,
    request_url: str | _Unset = UNSET,
    interval: int | _Unset = UNSET,
    initial_content: str | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a container for live updates via HTMX."""
    config = build_config(LiveContentConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    htmx_config = {"request_url": config.request_url, "trigger": f"load, every {config.interval}s", "swap": "innerHTML"}

    return {"live_content_config": config, "htmx_config": htmx_config}


@register.inclusion_tag("insight_ui/components/websocket.html")
def websocket(
    config: WebSocketConfig | None = None,
    *,
    tag_id: str | _Unset = UNSET,
    request_url: str | _Unset = UNSET,
    initial_content: str | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a WebSocket component as a thin wrapper for the HTMX ws extension."""
    config = build_config(WebSocketConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"websocket_config": config}


@register.inclusion_tag("insight_ui/components/badge.html")
def badge(
    config: BadgeConfig | None = None,
    *,
    label: str | _Unset = UNSET,
    icon_name: str | _Unset = UNSET,
    icon_size: str | _Unset = UNSET,
    icon_end: bool | _Unset = UNSET,
    type: Literal["primary", "secondary", "info", "success", "warning", "danger", "disabled"] | _Unset = UNSET,  # noqa: A002
    size: Literal["xs", "s", "m", "l", "xl"] | _Unset = UNSET,
) -> dict[str, Any]:
    """Render the badge component."""
    icon: IconConfig | None | _Unset = UNSET
    if icon_name is not UNSET:
        icon = IconConfig(icon_name, icon_size if icon_size is not UNSET else "m") if icon_name else None

    config = build_config(BadgeConfig, config, label=label, icon=icon, icon_end=icon_end, type=type, size=size)
    return {"badge_config": config}


# =============================================================
#
#   List Tags
#
# =============================================================


@register.inclusion_tag("insight_ui/components/infinite_scroll.html")
def infinite_scroll(
    config: InfiniteScrollConfig | None = None,
    *,
    tag_id: str | _Unset = UNSET,
    request_url: str | _Unset = UNSET,
    items: Sequence[Any] | None | _Unset = UNSET,
    page: int | _Unset = UNSET,
    has_next: bool | _Unset = UNSET,
    auto_fetch: bool | _Unset = UNSET,
    threshold: int | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a container for infinite scroll."""
    config = build_config(InfiniteScrollConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"infinite_scroll_config": config}


@register.inclusion_tag("insight_ui/components/pagination.html")
def pagination(
    config: PaginationConfig | None = None,
    *,
    request_url: str | _Unset = UNSET,
    current_page: Page | _Unset = UNSET,
    surrounding_pages: list[int] | _Unset = UNSET,
    ipp_config: PaginationIppConfig | None | _Unset = UNSET,
) -> dict[str, Any]:
    """Render pagination with items per page selection."""
    config = build_config(PaginationConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"pagination_config": config}


@register.inclusion_tag("insight_ui/components/table.html")
def table(config: TableConfig) -> dict[str, Any]:
    """Render a simple table."""
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
    request_url: str | _Unset = UNSET,
    simple: bool | _Unset = UNSET,
    search_query: str | _Unset = UNSET,
    htmx_config: HtmxConfig | None | _Unset = UNSET,
) -> dict[str, Any]:
    """Render text input with a button for a search function."""
    config = build_config(SearchBarConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"search_bar_config": config}


@register.inclusion_tag("insight_ui/components/generic_filter.html")
def generic_filter(
    config: GenericFilterConfig | None = None,
    *,
    filters: list | None | _Unset = UNSET,
    request_url: str | _Unset = UNSET,
    vertical: bool | _Unset = UNSET,
    htmx_config: HtmxConfig | None | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a generic filter consisting of one or more <select> fields."""
    config = build_config(GenericFilterConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"generic_filter_config": config}


@register.inclusion_tag("insight_ui/components/search_query_builder/sq_builder.html")
def query_builder(
    config: QueryBuilderConfig | None = None, *, model_fields: list[QueryBuilderFieldConfig] | None | _Unset = UNSET
) -> dict[str, Any]:
    """Render a filter for constructing custom search queries."""
    config = build_config(QueryBuilderConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"model_fields": config.model_fields}


# =============================================================
#
#   Card Tags
#
# =============================================================


@register.inclusion_tag("insight_ui/components/cards/card.html")
def card(
    config: CardConfig | None = None,
    *,
    title: str | _Unset = UNSET,
    content: str | _Unset = UNSET,
    subtitle: str | _Unset = UNSET,
    image: ImageConfig | None | _Unset = UNSET,
    actions: list[ActionConfig] | None | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a card with an aspect ratio of 16:9."""
    config = build_config(CardConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"card_config": config}


@register.inclusion_tag("insight_ui/components/cards/app_card.html")
def app_card(
    config: AppCardConfig | None = None,
    *,
    title: str | _Unset = UNSET,
    content: str | _Unset = UNSET,
    tags: list[str] | None | _Unset = UNSET,
    request_url: str | _Unset = UNSET,
    image: ImageConfig | None | _Unset = UNSET,
    actions: list[ActionConfig] | None | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a vertically aligned card."""
    config = build_config(AppCardConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"app_card_config": config}


@register.inclusion_tag("insight_ui/components/cards/flip_card.html")
def flip_card(
    config: FlipCardConfig | None = None,
    *,
    title: str | _Unset = UNSET,
    content: str | _Unset = UNSET,
    tags: list[str] | None | _Unset = UNSET,
    request_url: str | _Unset = UNSET,
    image: ImageConfig | None | _Unset = UNSET,
    actions: list[ActionConfig] | None | _Unset = UNSET,
    back_content: str | None | _Unset = UNSET,
    back_style: str | None | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a card that can be rotated 180°."""
    config = build_config(FlipCardConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"flip_card_config": config}


@register.inclusion_tag("insight_ui/components/carousels/card_carousel.html")
def carousel(
    config: CardCarouselConfig | None = None,
    *,
    carousel_items: Sequence[CardConfig] | None | _Unset = UNSET,
    autoplay: bool | _Unset = UNSET,
    show_dots: bool | _Unset = UNSET,
    show_index: bool | _Unset = UNSET,
    items_per_slide: int | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a card carousel."""
    config = build_config(CardCarouselConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
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
    carousel_items: Sequence[ImageCarouselItemConfig] | None | _Unset = UNSET,
    autoplay: bool | _Unset = UNSET,
    show_dots: bool | _Unset = UNSET,
    show_index: bool | _Unset = UNSET,
    items_per_slide: int | _Unset = UNSET,
) -> dict[str, Any]:
    """Render an image carousel."""
    config = build_config(ImageCarouselConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
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
    tag_id: str | _Unset = UNSET,
    velocity: int | _Unset = UNSET,
    tilt: int | _Unset = UNSET,
    face_camera: bool | _Unset = UNSET,
    carousel_items: Sequence[CarouselItemConfig] | None | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a 3D version of the carousel component."""
    config = build_config(ThreeDCarouselConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"carousel_config": config}


@register.inclusion_tag("insight_ui/components/toggle_view.html")
def toggle_view(
    config: ToggleViewConfig | None = None,
    *,
    tag_id: str | _Unset = UNSET,
    cards: list[CardConfig] | _Unset = UNSET,
    table_config: TableConfig | _Unset = UNSET,
    view_radio_config: RadioBlockConfig | None | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a view of data that can be displayed in various ways."""
    config = build_config(ToggleViewConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
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
    tag_id: str | _Unset = UNSET,
    title: str | _Unset = UNSET,
    description: str | _Unset = UNSET,
    fields: Sequence[FormFieldConfig] | None | _Unset = UNSET,
    show_reset_button: bool | _Unset = UNSET,
    request_url: str | _Unset = UNSET,
    htmx_config: HtmxConfig | None | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a form with HTMX support."""
    config = build_config(FormConfig, config, **{k: v for k, v in locals().items() if k not in {"config"}})
    return {"form_config": config}
