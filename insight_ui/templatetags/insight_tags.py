"""Template-Tags for Insight UI-Components."""

from __future__ import annotations

import json
import math
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import MISSING, fields, is_dataclass, replace
from difflib import HtmlDiff, ndiff, unified_diff
from types import UnionType
from typing import TYPE_CHECKING, Any, Final, Literal, TypeVar, get_args, get_origin, get_type_hints

from django import template
from django.conf import settings
from django.templatetags.static import static
from django.urls import NoReverseMatch, reverse

if TYPE_CHECKING:
    from django.core.paginator import Page
from django.utils.functional import Promise
from django.utils.safestring import SafeString, mark_safe
from django.utils.translation import gettext as _
from markdown import markdown

from insight_ui.config import get_config
from insight_ui.configs import (
    AccordionConfig,
    AlertConfig,
    AlertType,
    AppCardConfig,
    ArticleConfig,
    BadgeConfig,
    BadgeType,
    BrandMarkConfig,
    BreadcrumbItemConfig,
    BreadcrumbsConfig,
    BulletPointItemConfig,
    BulletPointListConfig,
    ButtonConfig,
    ButtonType,
    CardCarouselConfig,
    CardConfig,
    CarouselItemConfig,
    ChartConfig,
    ChartDatasetConfig,
    ChatConfig,
    CheckboxConfig,
    CheckboxGroupConfig,
    ColorType,
    CornerPosition,
    CornerRibbonConfig,
    DataAttrConfig,
    DropdownConfig,
    FlipCardConfig,
    FooterConfig,
    FormConfig,
    FormFieldConfig,
    GenericFilterConfig,
    GeoMapConfig,
    GeoMapDatasetConfig,
    HeroConfig,
    HtmlButtonType,
    HtmxConfig,
    IconColor,
    IconConfig,
    ImageCarouselConfig,
    ImageCarouselItemConfig,
    ImageConfig,
    InfiniteScrollConfig,
    InfoboxConfig,
    InputFieldConfig,
    LegalNoticeConfig,
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
    Size,
    SliderConfig,
    StatusScreenConfig,
    StepperConfig,
    StepperItemConfig,
    StepStatus,
    TableConfig,
    TextareaConfig,
    ThreeDCarouselConfig,
    ToggleConfig,
    ToggleViewConfig,
    WebSocketConfig,
)
from insight_ui.configs.utils import ProgressBarConfig
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
    """Resolve static asset paths while preserving absolute, root-relative, and data URLs.

    Args:
        value: The asset path or URL to resolve.

    Returns:
        The resolved URL, or empty string if value is falsy.

    """
    if not value:
        return ""

    url = str(value)
    if url.startswith(("http://", "https://", "/", "data:")):
        return url

    return static(url)


def ensure_list(value: str | Iterable[str] | None) -> list[str]:
    """Take a string or a list of strings and return in both cases a list of strings.

    Args:
        value: A string, iterable of strings, or None.

    Returns:
        A list of strings, empty list if value is None.

    """
    if value is None:
        return []

    if isinstance(value, (str, Promise)):
        return [value]

    return list(value)


def _is_dataclass_type(annotation: object) -> bool:
    """Return whether a type annotation directly describes a dataclass config.

    Args:
        annotation: The type annotation to check.

    Returns:
        True if annotation is a dataclass type, False otherwise.

    """
    return isinstance(annotation, type) and is_dataclass(annotation)


def _coerce_mapping_to_config[T](cls: type[T], value: Mapping[str, Any]) -> T:
    """Create a dataclass config from a mapping, including nested config values.

    Args:
        cls: The dataclass type to instantiate.
        value: The mapping of field names to values.

    Returns:
        An instance of the dataclass with coerced values.

    """
    type_hints = get_type_hints(cls)
    coerced_values = {key: _coerce_config_value(item, type_hints.get(key, Any)) for key, item in value.items()}
    return cls(**coerced_values)


def _coerce_sequence_to_config(value: Sequence[Any], annotation: object) -> list[Any]:
    """Convert list-like config values according to their annotated item type.

    Args:
        value: The sequence to convert.
        annotation: The type annotation describing the expected item type.

    Returns:
        A list with items coerced to the annotated type.

    """
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
    """Return whether an annotation expects a list-like config value.

    Args:
        annotation: The type annotation to check.

    Returns:
        True if annotation expects a sequence, False otherwise.

    """
    origin = get_origin(annotation)
    if origin in (list, Sequence):
        return True

    if origin is UnionType:
        return any(_expects_sequence_config(option) for option in get_args(annotation))

    return False


def _coerce_config_value(value: Any, annotation: object) -> Any:  # noqa: ANN401
    """Coerce mapping and sequence values into annotated dataclass config types.

    Args:
        value: The value to coerce.
        annotation: The target type annotation.

    Returns:
        The coerced value, or unchanged if no coercion applies.

    """
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
    """Create or update a dataclass instance.

    Parameters with value UNSET are ignored. If config is None, creates a new
    instance and validates required fields. If config is given, returns a copy
    with provided overrides applied.

    Args:
        cls: The dataclass type to create or update.
        config: An existing config instance to update, or None to create new.
        **kwargs: Field values to set or override.

    Returns:
        A new or updated dataclass instance.

    Raises:
        ValueError: If required fields are missing when creating a new instance.

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
    html = html.replace("<a", '<a class="text-insight-link"')

    return mark_safe(html)  # nosec  # noqa: S308


@register.filter
def get_item(dictionary: dict, key: str) -> Any:  # noqa: ANN401
    """Get the specified item of a dictionary."""
    return dictionary.get(key)


@register.filter
def json_attribute(value: object) -> str:
    """Serialize a value as JSON for an HTML attribute.

    The returned string deliberately remains unsafe so Django's normal template
    auto-escaping protects the surrounding HTML attribute.
    """
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


@register.inclusion_tag("insight_ui/components/icons.html")
def icon(
    config: IconConfig | None = None,
    *,
    name: str | _Unset = UNSET,
    size: Size | _Unset = UNSET,
    color: IconColor | _Unset = UNSET,
) -> dict[str, Any]:
    """Render specified icon with given size and color."""
    config = build_config(IconConfig, config, **{k: v for k, v in locals().items() if k != "config"})
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
    chapter: str | _Unset = UNSET,
    description: str | list[str] | _Unset = UNSET,
    badges: list[BadgeConfig] | _Unset = UNSET,
    buttons: list[ButtonConfig] | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a page header in the base template."""
    config = build_config(PageHeaderConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    config.description = ensure_list(config.description)

    return {"page_header_config": config}


# Responsive column classes using container queries
_ARTICLE_COLUMN_CLASSES: dict[int, str] = {
    1: "columns-1",
    2: "columns-1 @sm:columns-2",
    3: "columns-1 @sm:columns-2 @md:columns-3",
    4: "columns-1 @sm:columns-2 @md:columns-3 @lg:columns-4",
}

# Fixed column classes (no container queries)
_ARTICLE_FIXED_CLASSES: dict[int, str] = {
    1: "columns-1",
    2: "columns-2",
    3: "columns-3",
    4: "columns-4",
}


@register.inclusion_tag("insight_ui/components/article.html")
def article(
    config: ArticleConfig | None = None,
    *,
    content: str | _Unset = UNSET,
    max_columns: int | _Unset = UNSET,
    column_gap: str | _Unset = UNSET,
    title: str | _Unset = UNSET,
    fixed: bool | _Unset = UNSET,
) -> dict[str, Any]:
    """Render an article in newspaper style with a multi-column layout.

    Uses CSS Container Queries to adapt the column count based on available width.
    """
    config = build_config(ArticleConfig, config, **{k: v for k, v in locals().items() if k != "config"})

    # Clamp columns to valid range
    cols = max(1, min(4, config.max_columns))

    # Select column classes based on mode
    if config.fixed:
        column_classes = _ARTICLE_FIXED_CLASSES[cols]
        needs_container = False
    else:
        column_classes = _ARTICLE_COLUMN_CLASSES[cols]
        needs_container = cols > 1

    return {
        "article_config": config,
        "column_classes": column_classes,
        "needs_container": needs_container,
    }


@register.inclusion_tag("insight_ui/components/hero.html")
def hero(
    config: HeroConfig | None = None,
    *,
    title: str | _Unset = UNSET,
    subtitle: str | _Unset = UNSET,
    description: str | _Unset = UNSET,
    cta_primary: ButtonConfig | _Unset = UNSET,
    cta_secondary: ButtonConfig | _Unset = UNSET,
    background_image_url: str | _Unset = UNSET,
    badge_config: BadgeConfig | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a hero section with optional background image."""
    config = build_config(HeroConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"hero_config": config}


STATUS_SCREEN_ICON_BY_STATUS = {
    "info": "information-circle",
    "success": "check",
    "warning": "exclamation-triangle",
    "error": "exclamation-circle",
}


@register.inclusion_tag("insight_ui/components/status_screen.html")
def status_screen(
    config: StatusScreenConfig | None = None,
    *,
    title: str | _Unset = UNSET,
    description: str | list[str] | _Unset = UNSET,
    status: AlertType | _Unset = UNSET,
    brand: BrandMarkConfig | _Unset | None = UNSET,
    notice_title: str | _Unset = UNSET,
    notice: str | _Unset = UNSET,
    primary_action: ButtonConfig | _Unset = UNSET,
    secondary_action: ButtonConfig | _Unset = UNSET,
    actions: list[ButtonConfig] | _Unset = UNSET,
    css_class: str | _Unset = UNSET,
    card_css_class: str | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a generic centered status screen."""
    config = build_config(StatusScreenConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    config.description = ensure_list(config.description)

    all_actions = [action for action in [config.primary_action, config.secondary_action, *config.actions] if action]
    config.actions = all_actions

    return {
        "status_screen_config": config,
        "status_screen_icon": STATUS_SCREEN_ICON_BY_STATUS[config.status],
    }


# =============================================================
#
#   Navigation Tags
#
# =============================================================


def _resolve_url(url_or_name: str) -> str:
    """Resolve a URL name to a URL, or return the URL if already a path.

    Args:
        url_or_name: Either a URL path (starting with /) or a URL name.

    Returns:
        The resolved URL path, or empty string if resolution fails.

    """
    if not url_or_name:
        return ""
    if url_or_name.startswith(("/", "http")):
        return url_or_name
    try:
        return reverse(url_or_name)
    except NoReverseMatch:
        return ""


@register.inclusion_tag("insight_ui/components/navbar.html", takes_context=True)
def navbar(context: dict[str, Any], config: NavbarConfig, **kwargs: JsonValue) -> dict[str, Any]:
    """Render a configurable navigation bar."""
    return {
        "user": context.get("user"),
        "navbar_config": config,
        "fixed": get_config("navbar_fixed"),
        "login_url": _resolve_url(getattr(settings, "LOGIN_URL", "login")),
        "register_url": _resolve_url(str(get_config("register_url") or "")),
        "options": {**kwargs},
    }


@register.inclusion_tag("insight_ui/components/footer.html")
def footer(config: FooterConfig) -> dict[str, Any]:
    """Render a footer with optional description, links, and a legal notice line."""
    return {"footer_config": config}


@register.inclusion_tag("insight_ui/components/breadcrumbs.html")
def breadcrumbs(
    config: BreadcrumbsConfig | None = None,
    *,
    items: list[BreadcrumbItemConfig] | _Unset | None = UNSET,
    htmx: HtmxConfig | _Unset | None = UNSET,
) -> dict[str, Any]:
    """Render breadcrumb navigation."""
    config = build_config(BreadcrumbsConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"items": config.items, "htmx": config.htmx}


@register.inclusion_tag("insight_ui/components/stepper.html")
def stepper(
    config: StepperConfig | None = None, *, items: list[StepperItemConfig] | _Unset | None = UNSET
) -> dict[str, Any]:
    """Render a graphical representation of process steps."""
    config = build_config(StepperConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"items": config.items}


@register.inclusion_tag("insight_ui/components/minimal_stepper.html")
def minimal_stepper(
    config: MinimalStepperConfig | None = None,
    *,
    items: list[StepStatus] | _Unset = UNSET,
    step_count: int | _Unset = UNSET,
    current_step: int | _Unset = UNSET,
    current_step_status: StepStatus | _Unset = UNSET,
    icon_size: Size | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a compact graphical representation of process steps."""
    config = build_config(MinimalStepperConfig, config, **{k: v for k, v in locals().items() if k != "config"})

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
    config: BulletPointListConfig | None = None, *, items: list[BulletPointItemConfig] | _Unset | None = UNSET
) -> dict[str, Any]:
    """Render a graphical representation of a bullet point list."""
    config = build_config(BulletPointListConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"items": config.items, "htmx": config.htmx}


@register.inclusion_tag("insight_ui/components/accordion.html")
def accordion(config: AccordionConfig) -> dict[str, Any]:
    """Render an accordion that can have one or more sections open."""
    return {"accordion_config": config}


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
    type: ButtonType | _Unset = UNSET,  # noqa: A002
    size: Size | _Unset = UNSET,
    outline: bool | _Unset = UNSET,
    subtle: bool | _Unset = UNSET,
    round: bool | _Unset = UNSET,  # noqa: A002
    tooltip: str | _Unset = UNSET,
    htmx_config: HtmxConfig | _Unset = UNSET,
    hidden: bool | _Unset = UNSET,
    disabled: bool | _Unset = UNSET,
    disabled_reason: str | _Unset = UNSET,
    button_type: HtmlButtonType | _Unset = UNSET,
    extra_classes: str | _Unset = UNSET,
    **kwargs: Any,  # noqa: ANN401
) -> dict[str, Any]:
    """Render the button component.

    Supports data_* kwargs for custom data attributes, e.g.:
        {% button label="Retry" data_progress_retry="" data_retry="retry-btn" %}
    becomes:
        <button data-progress-retry="" data-retry="retry-btn">Retry</button>

    Supports aria_* kwargs for ARIA attributes, e.g.:
        {% button label="Menu" aria_expanded="false" aria_controls="menu-id" %}
    becomes:
        <button aria-expanded="false" aria-controls="menu-id">Menu</button>

    Supports hx_* kwargs for HTMX attributes, e.g.:
        {% button label="Load" hx_get="/api/data" hx_swap="outerHTML" %}
    becomes:
        <button hx-get="/api/data" hx-swap="outerHTML">Load</button>
    """
    icon: IconConfig | _Unset | None = UNSET
    if icon_name is not UNSET:
        icon = IconConfig(icon_name, icon_size if icon_size is not UNSET else "m") if icon_name else None

    # Collect data_* kwargs and convert to DataAttrConfig list
    data_attrs: list[DataAttrConfig] | _Unset = UNSET
    data_kwargs = {k: v for k, v in kwargs.items() if k.startswith("data_")}
    if data_kwargs:
        data_attrs = [
            DataAttrConfig(name=key[5:].replace("_", "-"), value=str(value)) for key, value in data_kwargs.items()
        ]

    # Collect aria_* kwargs and convert to DataAttrConfig list
    aria_attrs: list[DataAttrConfig] | _Unset = UNSET
    aria_kwargs = {k: v for k, v in kwargs.items() if k.startswith("aria_")}
    if aria_kwargs:
        aria_attrs = [
            DataAttrConfig(name=key[5:].replace("_", "-"), value=str(value)) for key, value in aria_kwargs.items()
        ]

    # Collect hx_* kwargs and convert to DataAttrConfig list
    hx_attrs: list[DataAttrConfig] | _Unset = UNSET
    hx_kwargs = {k: v for k, v in kwargs.items() if k.startswith("hx_")}
    if hx_kwargs:
        hx_attrs = [
            DataAttrConfig(name=key[3:].replace("_", "-"), value=str(value)) for key, value in hx_kwargs.items()
        ]

    # Validate no unknown kwargs remain (must start with data_, aria_, or hx_)
    invalid_kwargs = [k for k in kwargs if not k.startswith(("data_", "aria_", "hx_"))]
    if invalid_kwargs:
        raise ValueError(  # noqa: TRY003
            f"Unknown parameter '{invalid_kwargs[0]}' in {{% button %}}. "
            "Only data_*, aria_*, hx_* dynamic attributes are allowed in **kwargs."
        )

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
        subtle=subtle,
        round=round,
        tooltip=tooltip,
        htmx_config=htmx_config,
        hidden=hidden,
        disabled=disabled,
        disabled_reason=disabled_reason,
        button_type=button_type,
        extra_classes=extra_classes,
        data_attrs=data_attrs,
        aria_attrs=aria_attrs,
        hx_attrs=hx_attrs,
    )
    return {"button_config": config}


@register.inclusion_tag("insight_ui/components/input.html")
def input_field(
    config: InputFieldConfig | None = None,
    *,
    tag_id: str | _Unset | None = UNSET,
    name: str | _Unset | None = UNSET,
    input_type: str | _Unset = UNSET,
    placeholder: str | _Unset = UNSET,
    value: str | int | float | _Unset | None = UNSET,
    minimum: int | _Unset | None = UNSET,
    maximum: int | _Unset | None = UNSET,
    min_length: int | _Unset | None = UNSET,
    max_length: int | _Unset | None = UNSET,
    checked: bool | _Unset = UNSET,
    required: bool | _Unset = UNSET,
    disabled: bool | _Unset = UNSET,
    disabled_reason: str | _Unset | None = UNSET,
    label: str | _Unset | None = UNSET,
) -> dict[str, Any]:
    """Render any <input> field."""
    config = build_config(InputFieldConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"input_config": config}


@register.inclusion_tag("insight_ui/components/textarea.html")
def textarea(
    config: TextareaConfig | None = None,
    *,
    tag_id: str | _Unset | None = UNSET,
    name: str | _Unset | None = UNSET,
    placeholder: str | _Unset = UNSET,
    value: str | _Unset = UNSET,
    rows: int | _Unset = UNSET,
    cols: int | _Unset | None = UNSET,
    required: bool | _Unset = UNSET,
    disabled: bool | _Unset = UNSET,
    disabled_reason: str | _Unset | None = UNSET,
    label: str | _Unset | None = UNSET,
) -> dict[str, Any]:
    """Render a <textarea> field."""
    config = build_config(TextareaConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"textarea_config": config}


@register.inclusion_tag("insight_ui/components/checkbox.html")
def checkbox(
    config: CheckboxConfig | None = None,
    *,
    tag_id: str | _Unset | None = UNSET,
    name: str | _Unset | None = UNSET,
    value: str | _Unset = UNSET,
    label: str | _Unset | None = UNSET,
    checked: bool | _Unset = UNSET,
    disabled: bool | _Unset = UNSET,
    disabled_reason: str | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a checkbox with label text."""
    config = build_config(CheckboxConfig, config, **{k: v for k, v in locals().items() if k != "config"})
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
    items: list[RadioItemConfig] | _Unset | None = UNSET,
    as_row: bool | _Unset = UNSET,
    current_value: str | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a group of radio buttons."""
    config = build_config(RadioGroupConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"radio_group_config": config}


@register.inclusion_tag("insight_ui/components/radio_block.html")
def radio_block(
    config: RadioBlockConfig | None = None,
    *,
    name: str | _Unset = UNSET,
    label: str | _Unset = UNSET,
    items: list[RadioItemConfig] | _Unset | None = UNSET,
    integrated: bool | _Unset = UNSET,
    as_row: bool | _Unset = UNSET,
    request_url: str | _Unset = UNSET,
    hx_target_id: str | _Unset = UNSET,
    hx_swap_method: str | _Unset = UNSET,
    method: str | _Unset = UNSET,
    current_value: str | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a group of radio buttons as a block."""
    config = build_config(RadioBlockConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"radio_block_config": config}


@register.inclusion_tag("insight_ui/components/range_slider.html")
def slider(
    config: SliderConfig | None = None,
    *,
    tag_id: str | _Unset | None = UNSET,
    name: str | _Unset | None = UNSET,
    value: int | _Unset | None = UNSET,
    minimum: int | _Unset = UNSET,
    maximum: int | _Unset = UNSET,
    step_size: int | _Unset = UNSET,
    label: str | _Unset | None = UNSET,
    disabled: bool | _Unset = UNSET,
    disabled_reason: str | _Unset | None = UNSET,
    items: list[str] | _Unset | None = UNSET,
    legend_mode: str | _Unset = UNSET,
    dual: bool | _Unset = UNSET,
    value_min: int | _Unset | None = UNSET,
    value_max: int | _Unset | None = UNSET,
) -> dict[str, Any]:
    """Render a range slider."""
    config = build_config(SliderConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"slider_config": config}


@register.inclusion_tag("insight_ui/components/toggle_button.html")
def toggle(
    config: ToggleConfig | None = None,
    *,
    tag_id: str | _Unset | None = UNSET,
    name: str | _Unset | None = UNSET,
    value: str | _Unset = UNSET,
    label: str | _Unset | None = UNSET,
    icon: IconConfig | _Unset | None = UNSET,
    checked: bool | _Unset = UNSET,
    disabled: bool | _Unset = UNSET,
    disabled_reason: str | _Unset | None = UNSET,
    switch: bool | _Unset = UNSET,
    method: str | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a toggle button."""
    config = build_config(ToggleConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"toggle_config": config}


@register.inclusion_tag("insight_ui/components/select.html")
def select(
    config: SelectConfig | None = None,
    *,
    tag_id: str | _Unset | None = UNSET,
    name: str | _Unset | None = UNSET,
    label: str | _Unset | None = UNSET,
    required: bool | _Unset = UNSET,
    disabled: bool | _Unset = UNSET,
    disabled_reason: str | _Unset | None = UNSET,
    explanation: str | _Unset = UNSET,
    options: list[str] | dict[str, str] | _Unset | None = UNSET,
    selected_option: str | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a selection box."""
    config = build_config(SelectConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"select_config": config}


@register.inclusion_tag("insight_ui/components/multiselect.html")
def multiselect(
    config: MultiselectConfig | None = None,
    *,
    name: str | _Unset | None = UNSET,
    label: str | _Unset | None = UNSET,
    maximum: int | _Unset | None = UNSET,
    show_buttons: bool | _Unset = UNSET,
    disabled: bool | _Unset = UNSET,
    disabled_reason: str | _Unset | None = UNSET,
    options: list[str] | dict[str, str] | _Unset | None = UNSET,
    selected_options: list[str] | _Unset | None = UNSET,
) -> dict[str, Any]:
    """Render a selection box that allows multiple values."""
    config = build_config(MultiselectConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"multiselect_config": config}


@register.inclusion_tag("insight_ui/components/chat.html")
def chat(config: ChatConfig | None = None, *, request_url: str | _Unset = UNSET) -> dict[str, Any]:
    """Render a chat with an input line and a place for the response."""
    config = build_config(ChatConfig, config, **{k: v for k, v in locals().items() if k != "config"})
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
    type: AlertType | _Unset = UNSET,  # noqa: A002
    dismissible: bool | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a closable notification."""
    config = build_config(AlertConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"alert_config": config}


@register.inclusion_tag("insight_ui/components/modal.html")
def modal(
    config: ModalConfig | None = None,
    *,
    tag_id: str | _Unset = UNSET,
    title: str | _Unset = UNSET,
    description: str | list[str] | _Unset = UNSET,
    actions: Sequence[ButtonConfig] | _Unset | None = UNSET,
    width: int | _Unset = UNSET,
) -> dict[str, Any]:
    """Render an accessible modal dialog."""
    config = build_config(ModalConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    config.description = ensure_list(config.description)
    return {"modal_config": config}


# =============================================================
#
#   Util Tags
#
# =============================================================


@register.inclusion_tag("insight_ui/components/infobox.html")
def infobox(
    config: InfoboxConfig | None = None,
    *,
    info_type: AlertType | _Unset = UNSET,
    message: str | _Unset = UNSET,
    **kwargs: str,
) -> dict[str, Any]:
    """Render a small box of information."""
    config = build_config(InfoboxConfig, config, info_type=info_type, message=message)

    if kwargs:
        try:
            config.message = config.message.format(**kwargs)
        except (KeyError, ValueError):
            config.message = config.message

    return {"info_config": config}


@register.inclusion_tag("insight_ui/components/legal_notice.html")
def legal_notice(
    config: LegalNoticeConfig | None = None,
    *,
    year: int | str | _Unset | None = UNSET,
    holder: str | _Unset | None = UNSET,
    source_label: str | _Unset | None = UNSET,
    license_text: str | _Unset | None = UNSET,
    license_url: str | _Unset | None = UNSET,
    separator: str | _Unset | None = UNSET,
    rights_text: str | _Unset | None = UNSET,
    version: str | _Unset | None = UNSET,
) -> dict[str, Any]:
    """Render a reusable legal notice line with copyright, license, and version."""
    config = build_config(LegalNoticeConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    metadata = [
        {"text": config.rights_text or _("All rights reserved."), "url": ""},
        {"text": config.source_label or "", "url": ""},
        {"text": config.license_text or "", "url": config.license_url or ""},
        {"text": config.version or "", "url": ""},
    ]

    return {"legal_config": config, "metadata": [item for item in metadata if item["text"]]}


@register.filter
def diff(a: str, b: str, simple: bool = True) -> str:
    """Generate a visualization of the differences between two texts.

    Args:
        a: The original version of the text.
        b: The modified version of the text.
        simple: 'True' for a simplified display.

    Returns:
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
        <p class='text-insight-headline'>{html}</p>
    """


@register.inclusion_tag("insight_ui/components/logo.html")
def logo(
    config: LogoConfig | None = None,
    *,
    url: str | _Unset | None = UNSET,
    url_dark: str | _Unset | None = UNSET,
    alt: str | _Unset | None = UNSET,
    icon_name: str | _Unset | None = UNSET,
    icon_size: str | _Unset | None = UNSET,
    height: str | _Unset | None = UNSET,
    width: str | _Unset | None = UNSET,
) -> dict[str, Any]:
    """Render a brand logo as an image, SVG asset, or Insight UI icon."""
    # Only override icon if icon_name was explicitly provided
    icon: IconConfig | _Unset | None = UNSET
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


@register.inclusion_tag("insight_ui/components/brand_mark.html")
def brand_mark(
    config: BrandMarkConfig | None = None,
    *,
    primary_text: str | _Unset = UNSET,
    secondary_text: str | _Unset = UNSET,
    logo: LogoConfig | _Unset = UNSET,
    logo_position: str | _Unset = UNSET,
    css_class: str | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a public logo plus a two-tone wordmark."""
    config = build_config(BrandMarkConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"brand_mark_config": config}


@register.inclusion_tag("insight_ui/components/corner_ribbon.html")
def corner_ribbon(
    config: CornerRibbonConfig | None = None,
    *,
    text: str | _Unset = UNSET,
    position: CornerPosition | _Unset = UNSET,
    color: ColorType | _Unset = UNSET,
    foreground_color: ColorType | _Unset = UNSET,
    request_url: str | _Unset = UNSET,
    aria_label: str | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a corner ribbon positioned in any browser corner."""
    config = build_config(CornerRibbonConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"corner_ribbon_config": config}


@register.inclusion_tag("insight_ui/components/progress_bar.html")
def progress_bar(
    config: ProgressBarConfig | None = None,
    *,
    tag_id: str | _Unset = UNSET,
    label: str | _Unset = UNSET,
    request_url: str | _Unset = UNSET,
    interval: int | _Unset = UNSET,
    sse_url: str | _Unset = UNSET,
    min_value: int | _Unset = UNSET,
    max_value: int | _Unset = UNSET,
    value: int | _Unset = UNSET,
    show_value: bool | _Unset = UNSET,
    hide_on_complete: bool | _Unset = UNSET,
    complete_delay: int | _Unset = UNSET,
    stop_on_error: bool | _Unset = UNSET,
    show_cancel: bool | _Unset = UNSET,
    cancel_label: str | _Unset = UNSET,
    cancel_url: str | _Unset = UNSET,
    show_retry: bool | _Unset = UNSET,
    retry_label: str | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a simple progress bar."""
    config = build_config(ProgressBarConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"progress_bar_config": config}


@register.inclusion_tag("insight_ui/components/geo_map.html")
def geo_map(
    config: GeoMapConfig | None = None,
    *,
    initial_coords: list[float] | _Unset = UNSET,
    initial_zoom: int | _Unset = UNSET,
    map_height: int | _Unset = UNSET,
    datasets: list[GeoMapDatasetConfig] | _Unset = UNSET,
    aria_label: str | _Unset = UNSET,
) -> dict[str, Any]:
    """Render an integrated geographic map."""
    config = build_config(GeoMapConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"map_config": config}


@register.inclusion_tag("insight_ui/components/charts/bar_chart.html")
def bar_chart(
    config: ChartConfig | None = None,
    *,
    tag_id: str | _Unset = UNSET,
    dataset: ChartDatasetConfig | _Unset | None = UNSET,
    chart_height: int | _Unset = UNSET,
    aria_label: str | _Unset = UNSET,
    show_decal: bool | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a bar chart with Apache ECharts."""
    config = build_config(ChartConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"chart_config": config}


@register.inclusion_tag("insight_ui/components/charts/line_chart.html")
def line_chart(
    config: ChartConfig | None = None,
    *,
    tag_id: str | _Unset = UNSET,
    dataset: ChartDatasetConfig | _Unset | None = UNSET,
    chart_height: int | _Unset = UNSET,
    aria_label: str | _Unset = UNSET,
    show_decal: bool | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a line chart with Apache ECharts."""
    config = build_config(ChartConfig, config, **{k: v for k, v in locals().items() if k != "config"})
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
    config = build_config(LiveContentConfig, config, **{k: v for k, v in locals().items() if k != "config"})
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
    config = build_config(WebSocketConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"websocket_config": config}


@register.inclusion_tag("insight_ui/components/badge.html")
def badge(
    config: BadgeConfig | None = None,
    *,
    label: str | _Unset = UNSET,
    icon_name: str | _Unset = UNSET,
    icon_size: str | _Unset = UNSET,
    icon_end: bool | _Unset = UNSET,
    type: BadgeType | _Unset = UNSET,  # noqa: A002
    size: Size | _Unset = UNSET,
    tooltip: str | _Unset = UNSET,
) -> dict[str, Any]:
    """Render the badge component."""
    icon: IconConfig | _Unset | None = UNSET
    if icon_name is not UNSET:
        icon = IconConfig(icon_name, icon_size if icon_size is not UNSET else "m") if icon_name else None

    config = build_config(
        BadgeConfig, config, label=label, icon=icon, icon_end=icon_end, type=type, size=size, tooltip=tooltip
    )
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
    items: Sequence[Any] | _Unset | None = UNSET,
    page: int | _Unset = UNSET,
    has_next: bool | _Unset = UNSET,
    auto_fetch: bool | _Unset = UNSET,
    threshold: int | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a container for infinite scroll."""
    config = build_config(InfiniteScrollConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"infinite_scroll_config": config}


@register.inclusion_tag("insight_ui/components/pagination.html")
def pagination(
    config: PaginationConfig | None = None,
    *,
    request_url: str | _Unset = UNSET,
    current_page: Page | _Unset = UNSET,
    surrounding_pages: list[int] | _Unset = UNSET,
    ipp_config: PaginationIppConfig | _Unset | None = UNSET,
) -> dict[str, Any]:
    """Render pagination with items per page selection."""
    config = build_config(PaginationConfig, config, **{k: v for k, v in locals().items() if k != "config"})
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
    htmx_config: HtmxConfig | _Unset | None = UNSET,
    enable_search: bool | _Unset = UNSET,
    search_index_url: str | _Unset = UNSET,
) -> dict[str, Any]:
    """Render text input with a button for a search function."""
    config = build_config(SearchBarConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"search_bar_config": config}


@register.inclusion_tag("insight_ui/components/generic_filter.html")
def generic_filter(
    config: GenericFilterConfig | None = None,
    *,
    filters: list | _Unset | None = UNSET,
    request_url: str | _Unset = UNSET,
    vertical: bool | _Unset = UNSET,
    htmx_config: HtmxConfig | _Unset | None = UNSET,
) -> dict[str, Any]:
    """Render a generic filter consisting of one or more <select> fields."""
    config = build_config(GenericFilterConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"generic_filter_config": config}


@register.inclusion_tag("insight_ui/components/search_query_builder/sq_builder.html")
def query_builder(
    config: QueryBuilderConfig | None = None, *, model_fields: list[QueryBuilderFieldConfig] | _Unset | None = UNSET
) -> dict[str, Any]:
    """Render a filter for constructing custom search queries."""
    config = build_config(QueryBuilderConfig, config, **{k: v for k, v in locals().items() if k != "config"})
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
    image: ImageConfig | _Unset | None = UNSET,
    actions: list[ButtonConfig] | _Unset | None = UNSET,
) -> dict[str, Any]:
    """Render a card with an aspect ratio of 16:9."""
    config = build_config(CardConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"card_config": config}


@register.inclusion_tag("insight_ui/components/cards/app_card.html")
def app_card(
    config: AppCardConfig | None = None,
    *,
    title: str | _Unset = UNSET,
    content: str | _Unset = UNSET,
    tags: list[str] | _Unset | None = UNSET,
    request_url: str | _Unset = UNSET,
    image: ImageConfig | _Unset | None = UNSET,
    actions: list[ButtonConfig] | _Unset | None = UNSET,
) -> dict[str, Any]:
    """Render a vertically aligned card."""
    config = build_config(AppCardConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"app_card_config": config}


@register.inclusion_tag("insight_ui/components/cards/flip_card.html")
def flip_card(
    config: FlipCardConfig | None = None,
    *,
    title: str | _Unset = UNSET,
    content: str | _Unset = UNSET,
    tags: list[str] | _Unset | None = UNSET,
    request_url: str | _Unset = UNSET,
    image: ImageConfig | _Unset | None = UNSET,
    actions: list[ButtonConfig] | _Unset | None = UNSET,
    back_content: str | _Unset | None = UNSET,
    back_style: str | _Unset | None = UNSET,
) -> dict[str, Any]:
    """Render a card that can be rotated 180°."""
    config = build_config(FlipCardConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"flip_card_config": config}


@register.inclusion_tag("insight_ui/components/carousels/card_carousel.html")
def carousel(
    config: CardCarouselConfig | None = None,
    *,
    carousel_items: Sequence[CardConfig] | _Unset | None = UNSET,
    autoplay: bool | _Unset = UNSET,
    show_dots: bool | _Unset = UNSET,
    show_index: bool | _Unset = UNSET,
    items_per_slide: int | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a card carousel."""
    config = build_config(CardCarouselConfig, config, **{k: v for k, v in locals().items() if k != "config"})
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
    carousel_items: Sequence[ImageCarouselItemConfig] | _Unset | None = UNSET,
    autoplay: bool | _Unset = UNSET,
    show_dots: bool | _Unset = UNSET,
    show_index: bool | _Unset = UNSET,
    items_per_slide: int | _Unset = UNSET,
) -> dict[str, Any]:
    """Render an image carousel."""
    config = build_config(ImageCarouselConfig, config, **{k: v for k, v in locals().items() if k != "config"})
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
    carousel_items: Sequence[CarouselItemConfig] | _Unset | None = UNSET,
) -> dict[str, Any]:
    """Render a 3D version of the carousel component."""
    config = build_config(ThreeDCarouselConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"carousel_config": config}


@register.inclusion_tag("insight_ui/components/toggle_view.html")
def toggle_view(
    config: ToggleViewConfig | None = None,
    *,
    tag_id: str | _Unset = UNSET,
    cards: list[CardConfig] | _Unset = UNSET,
    table_config: TableConfig | _Unset = UNSET,
    view_radio_config: RadioBlockConfig | _Unset | None = UNSET,
) -> dict[str, Any]:
    """Render a view of data that can be displayed in various ways."""
    config = build_config(ToggleViewConfig, config, **{k: v for k, v in locals().items() if k != "config"})
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
    fields: Sequence[FormFieldConfig] | _Unset | None = UNSET,
    show_reset_button: bool | _Unset = UNSET,
    request_url: str | _Unset = UNSET,
    htmx_config: HtmxConfig | _Unset | None = UNSET,
) -> dict[str, Any]:
    """Render a form with HTMX support."""
    config = build_config(FormConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"form_config": config}
