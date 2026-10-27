# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Template-Tags for Insight UI-Components."""

from __future__ import annotations

import json
from dataclasses import MISSING, fields, is_dataclass, replace
from difflib import HtmlDiff, ndiff, unified_diff
from typing import TYPE_CHECKING, Any, Final, Literal, TypeVar, cast
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from django import template
from django.conf import settings
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import NoReverseMatch, reverse

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Sequence

    from django.core.paginator import Page
from django.utils.functional import Promise
from django.utils.html import format_html_join
from django.utils.safestring import SafeString, mark_safe
from django.utils.translation import gettext as _
from markdown import markdown

from insight_ui.brand import get_navbar_brand_defaults
from insight_ui.config import get_config
from insight_ui.configs import (
    AccordionConfig,
    AlertConfig,
    AppCardConfig,
    ArticleConfig,
    BadgeConfig,
    BadgeListConfig,
    BrandMarkConfig,
    BreadcrumbItemConfig,
    BreadcrumbsConfig,
    BulletPointItemConfig,
    BulletPointListConfig,
    ButtonColor,
    ButtonConfig,
    ButtonVariant,
    CardConfig,
    CarouselConfig,
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
    FilterConfig,
    FlipCardConfig,
    FooterConfig,
    FormConfig,
    FormField,
    GenericFilterConfig,
    GeoMapConfig,
    GeoMapDatasetConfig,
    HeadingLevel,
    HeroConfig,
    HtmlButtonType,
    HtmxConfig,
    HttpMethod,
    IconColor,
    IconConfig,
    ImageConfig,
    InfiniteScrollConfig,
    InfoboxConfig,
    InputFieldConfig,
    LegalNoticeConfig,
    LiveContentConfig,
    LogoConfig,
    MessageDialogConfig,
    MinimalStepperConfig,
    MultiselectConfig,
    NavbarConfig,
    PageHeaderConfig,
    PaginationConfig,
    PaginationIppConfig,
    QueryBuilderConfig,
    QueryBuilderFieldConfig,
    QueryBuilderFilterConfig,
    RadioBlockConfig,
    RadioGroupConfig,
    RadioItemConfig,
    SearchBarConfig,
    SelectConfig,
    Severity,
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
from insight_ui.utils import query_builder as query_builder_utils
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
        TypeError: If config is neither None nor a dataclass instance.
        ValueError: If required fields are missing when creating a new instance.

    """
    overrides = {key: value for key, value in kwargs.items() if value is not UNSET}

    if config is not None:
        if not is_dataclass(config) or isinstance(config, type):
            raise TypeError(  # noqa: TRY003
                f"config for {cls.__name__} must be a dataclass instance, got {type(config).__name__}."
            )
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


@register.simple_tag
def data_attributes(attrs: Iterable[DataAttrConfig], prefix: str = "data") -> SafeString:
    """Render DataAttrConfig entries as data-* (or aria-*/hx-*) HTML attributes.

    Usage: ``<input {% data_attributes config.data_attrs %}>``, ``{% data_attributes attrs prefix="aria" %}``

    Raises:
        ValueError: If the prefix is not data, aria or hx.

    """
    if prefix not in {"data", "aria", "hx"}:
        raise ValueError(f"Invalid attribute prefix {prefix!r}: use 'data', 'aria' or 'hx'.")  # noqa: TRY003
    return format_html_join(" ", '{}-{}="{}"', ((prefix, attr.name, attr.value) for attr in attrs))


def _collect_data_attrs(
    tag_name: str,
    config: object,
    data_attrs: list[DataAttrConfig] | _Unset,
    kwargs: dict[str, Any],
) -> list[DataAttrConfig] | _Unset:
    """Append the data_* keyword arguments of a tag to its data attributes.

    ``{% input_field name="title" data_inspector_label="" %}`` renders ``data-inspector-label=""``.
    Attributes from ``data_attrs`` (or else from the config) are kept.

    Raises:
        ValueError: If a keyword argument does not start with ``data_``.

    """
    unknown = [key for key in kwargs if not key.startswith("data_")]
    if unknown:
        raise ValueError(  # noqa: TRY003
            f"Unknown parameter '{unknown[0]}' in {{% {tag_name} %}}. "
            "Only data_* attributes are allowed as extra arguments."
        )
    if not kwargs:
        return data_attrs
    existing = data_attrs if isinstance(data_attrs, list) else getattr(config, "data_attrs", [])
    return [
        *existing,
        *(DataAttrConfig(name=key[5:].replace("_", "-"), value=str(value)) for key, value in kwargs.items()),
    ]


@register.simple_tag
def htmx_attributes(
    htmx: HtmxConfig | None,
    *,
    request_url: str = "",
    method: HttpMethod | None = None,
    target: str = "",
    swap: str = "",
    trigger: str = "",
    indicator: str = "",
    push_url: bool | None = None,
    swap_modifiers: str = "",
    global_indicator: bool = True,
) -> SafeString:
    """Render the HTMX attributes of an HtmxConfig in one consistent way.

    Components pass values they fix or derive themselves; these take precedence over the config.
    Attributes without a value are left out.

    Args:
        htmx: The request options. Renders nothing if None.
        request_url: URL of the component, e.g. of a breadcrumb item, used instead of htmx.request_url.
        method: HTTP method the component needs, used instead of htmx.method.
        target: Target the component needs, e.g. its own response container, used instead of htmx.target.
        swap: Swap method the component needs, used instead of htmx.swap_method.
        trigger: hx-trigger of the component. Empty keeps the HTMX default of the element.
        indicator: hx-indicator of the component, used instead of htmx.loading_indicator_id.
        push_url: Forces hx-push-url on or off. None uses htmx.push_url.
        swap_modifiers: Appended to hx-swap, e.g. "show:window:top".
        global_indicator: Whether the component shows the global loading bar when
            htmx.show_global_loading_indicator is None; background requests like polling pass False.

    Returns:
        The attributes, separated by spaces.

    """
    attributes: list[tuple[str, str]] = []
    if htmx is None:
        return format_html_join(" ", '{}="{}"', attributes)
    url = request_url or htmx.request_url
    if url:
        attributes.append((f"hx-{method or htmx.method}", url))
    if target or htmx.target:
        attributes.append(("hx-target", target or htmx.target))
    settle = f"settle:{htmx.swap_settle}" if htmx.swap_settle else ""
    attributes.append(
        ("hx-swap", " ".join(part for part in (swap or htmx.swap_method, settle, swap_modifiers) if part))
    )
    if trigger:
        attributes.append(("hx-trigger", trigger))
    if htmx.push_url if push_url is None else push_url:
        attributes.append(("hx-push-url", "true"))
    if indicator or htmx.loading_indicator_id:
        attributes.append(("hx-indicator", indicator or htmx.loading_indicator_id))
    if htmx.confirm:
        attributes.append(("hx-confirm", htmx.confirm))
    if htmx.vals:
        attributes.append(("hx-vals", json_attribute(htmx.vals)))
    show_global = htmx.show_global_loading_indicator
    if not (global_indicator if show_global is None else show_global):
        attributes.append(("data-insight-global-indicator", "false"))
    return format_html_join(" ", '{}="{}"', attributes)


@register.inclusion_tag("insight_ui/components/icons.html")
def icon(
    config: IconConfig | None = None,
    *,
    name: str | _Unset = UNSET,
    size: Size | _Unset = UNSET,
    color: IconColor | _Unset = UNSET,
    mirror_rtl: bool | _Unset | None = UNSET,
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
    badge: BadgeConfig | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a hero section with optional background image."""
    config = build_config(HeroConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"hero_config": config}


STATUS_SCREEN_ICON_BY_SEVERITY = {
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
    severity: Severity | _Unset = UNSET,
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
        "status_screen_icon": STATUS_SCREEN_ICON_BY_SEVERITY[config.severity],
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
def navbar(context: dict[str, Any], config: NavbarConfig | None = None, **kwargs: JsonValue) -> dict[str, Any]:
    """Render a configurable navigation bar.

    Without a ``config``, the navbar shows the brand from ``INSIGHT_UI["brand"]``
    (see :func:`insight_ui.brand.get_navbar_brand_defaults`) and no links. An
    explicit Config is rendered as supplied.
    """
    if config is None:
        config = NavbarConfig(brand=get_navbar_brand_defaults())
    config = build_config(NavbarConfig, config)
    return {
        "user": context.get("user"),
        "navbar_config": config,
        "align_to_content": get_config("align_navbar_footer_to_content"),
        "login_url": _resolve_url(getattr(settings, "LOGIN_URL", "login")),
        "register_url": _resolve_url(str(get_config("register_url") or "")),
        "redirect_to": context.get("redirect_to", ""),
        "options": {**kwargs},
    }


@register.inclusion_tag("insight_ui/components/toggle_theme.html")
def theme_toggle() -> dict[str, Any]:
    """Render the light/dark theme toggle button outside the navbar.

    Uses the same template and ``data-insight-theme-toggle`` behavior as
    ``NavbarConfig(show_theme_toggle=True)``.
    """
    return {}


@register.inclusion_tag("insight_ui/components/footer.html")
def footer(config: FooterConfig) -> dict[str, Any]:
    """Render a footer with optional description, links, and a legal notice line."""
    config = build_config(FooterConfig, config)
    return {"footer_config": config, "align_to_content": get_config("align_navbar_footer_to_content")}


@register.inclusion_tag("insight_ui/components/breadcrumbs.html")
def breadcrumbs(
    config: BreadcrumbsConfig | None = None,
    *,
    items: list[BreadcrumbItemConfig] | _Unset = UNSET,
    htmx: HtmxConfig | _Unset | None = UNSET,
) -> dict[str, Any]:
    """Render breadcrumb navigation."""
    config = build_config(BreadcrumbsConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"items": config.items, "htmx": config.htmx}


@register.inclusion_tag("insight_ui/components/stepper.html")
def stepper(config: StepperConfig | None = None, *, items: list[StepperItemConfig] | _Unset = UNSET) -> dict[str, Any]:
    """Render a graphical representation of process steps."""
    config = build_config(StepperConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"items": config.items}


@register.inclusion_tag("insight_ui/components/minimal_stepper.html")
def minimal_stepper(
    config: MinimalStepperConfig | None = None,
    *,
    steps: list[StepStatus] | _Unset = UNSET,
    step_count: int | _Unset = UNSET,
    current_step: int | _Unset = UNSET,
    current_step_status: StepStatus | _Unset = UNSET,
    icon_size: Size | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a compact graphical representation of process steps."""
    config = build_config(MinimalStepperConfig, config, **{k: v for k, v in locals().items() if k != "config"})

    # Generate steps from step_count if not provided
    if not config.steps and config.step_count > 0:
        config.steps = []
        for step in range(config.step_count):
            if step < config.current_step:
                config.steps.append("completed")
            elif step == config.current_step:
                config.steps.append(config.current_step_status)
            else:
                config.steps.append("pending")

    return {"steps": config.steps, "icon_size": config.icon_size}


@register.inclusion_tag("insight_ui/components/bullet_point_list.html")
def bullet_point_list(
    config: BulletPointListConfig | None = None,
    *,
    items: list[BulletPointItemConfig] | _Unset = UNSET,
    htmx: HtmxConfig | _Unset | None = UNSET,
) -> dict[str, Any]:
    """Render a graphical representation of a bullet point list."""
    config = build_config(BulletPointListConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"items": config.items, "htmx": config.htmx}


@register.inclusion_tag("insight_ui/components/accordion.html")
def accordion(config: AccordionConfig) -> dict[str, Any]:
    """Render an accordion that can have one or more sections open."""
    config = build_config(AccordionConfig, config)
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
    external: bool | _Unset = UNSET,
    on_click: str | _Unset = UNSET,
    icon_name: str | _Unset = UNSET,
    icon_size: str | _Unset = UNSET,
    icon_mirror_rtl: bool | _Unset | None = UNSET,
    icon_end: bool | _Unset = UNSET,
    icon_only: bool | _Unset = UNSET,
    color: ButtonColor | _Unset = UNSET,
    variant: ButtonVariant | _Unset = UNSET,
    size: Size | _Unset = UNSET,
    round: bool | _Unset = UNSET,  # noqa: A002
    tooltip: str | _Unset = UNSET,
    htmx: HtmxConfig | _Unset = UNSET,
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
        icon = (
            IconConfig(
                icon_name,
                icon_size if icon_size is not UNSET else "m",
                mirror_rtl=None if icon_mirror_rtl is UNSET else icon_mirror_rtl,
            )
            if icon_name
            else None
        )

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
        external=external,
        on_click=on_click,
        icon=icon,
        icon_end=icon_end,
        icon_only=icon_only,
        color=color,
        variant=variant,
        size=size,
        round=round,
        tooltip=tooltip,
        htmx=htmx,
        hidden=hidden,
        disabled=disabled,
        disabled_reason=disabled_reason,
        button_type=button_type,
        extra_classes=extra_classes,
        data_attrs=data_attrs,
        aria_attrs=aria_attrs,
        hx_attrs=hx_attrs,
    )
    # Solid is the default look of .btn, so it needs no class of its own.
    variant_class = "" if config.variant == "solid" else f" btn-{config.variant}"
    return {"button_config": config, "variant_class": variant_class}


@register.inclusion_tag("insight_ui/components/input.html")
def input_field(
    config: InputFieldConfig | None = None,
    *,
    tag_id: str | _Unset | None = UNSET,
    name: str | _Unset = UNSET,
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
    help_text: str | _Unset = UNSET,
    error_text: str | _Unset = UNSET,
    data_attrs: list[DataAttrConfig] | _Unset = UNSET,
    **kwargs: Any,  # noqa: ANN401
) -> dict[str, Any]:
    """Render any <input> field."""
    data_attrs = _collect_data_attrs("input_field", config, data_attrs, kwargs)
    config = build_config(
        InputFieldConfig, config, **{k: v for k, v in locals().items() if k not in ("config", "kwargs")}
    )
    return {"input_config": config}


@register.inclusion_tag("insight_ui/components/textarea.html")
def textarea(
    config: TextareaConfig | None = None,
    *,
    tag_id: str | _Unset | None = UNSET,
    name: str | _Unset = UNSET,
    placeholder: str | _Unset = UNSET,
    value: str | _Unset = UNSET,
    rows: int | _Unset = UNSET,
    cols: int | _Unset | None = UNSET,
    required: bool | _Unset = UNSET,
    disabled: bool | _Unset = UNSET,
    disabled_reason: str | _Unset | None = UNSET,
    label: str | _Unset | None = UNSET,
    help_text: str | _Unset = UNSET,
    error_text: str | _Unset = UNSET,
    data_attrs: list[DataAttrConfig] | _Unset = UNSET,
    **kwargs: Any,  # noqa: ANN401
) -> dict[str, Any]:
    """Render a <textarea> field."""
    data_attrs = _collect_data_attrs("textarea", config, data_attrs, kwargs)
    config = build_config(
        TextareaConfig, config, **{k: v for k, v in locals().items() if k not in ("config", "kwargs")}
    )
    return {"textarea_config": config}


@register.inclusion_tag("insight_ui/components/checkbox.html")
def checkbox(
    config: CheckboxConfig | None = None,
    *,
    tag_id: str | _Unset | None = UNSET,
    name: str | _Unset = UNSET,
    value: str | _Unset = UNSET,
    label: str | _Unset | None = UNSET,
    checked: bool | _Unset = UNSET,
    required: bool | _Unset = UNSET,
    disabled: bool | _Unset = UNSET,
    disabled_reason: str | _Unset = UNSET,
    help_text: str | _Unset = UNSET,
    error_text: str | _Unset = UNSET,
    data_attrs: list[DataAttrConfig] | _Unset = UNSET,
    **kwargs: Any,  # noqa: ANN401
) -> dict[str, Any]:
    """Render a checkbox with label text."""
    data_attrs = _collect_data_attrs("checkbox", config, data_attrs, kwargs)
    config = build_config(
        CheckboxConfig, config, **{k: v for k, v in locals().items() if k not in ("config", "kwargs")}
    )
    return {"checkbox_config": config}


@register.inclusion_tag("insight_ui/components/checkbox_group.html")
def checkbox_group(config: CheckboxGroupConfig) -> dict[str, Any]:
    """Render a group of checkbox elements."""
    config = build_config(CheckboxGroupConfig, config)
    return {"checkbox_group_config": config}


@register.inclusion_tag("insight_ui/components/dropdown.html")
def dropdown(config: DropdownConfig) -> dict[str, Any]:
    """Render a dropdown menu."""
    config = build_config(DropdownConfig, config)
    return {"dropdown_config": config}


@register.inclusion_tag("insight_ui/components/radio_group.html")
def radio_group(
    config: RadioGroupConfig | None = None,
    *,
    name: str | _Unset = UNSET,
    label: str | _Unset = UNSET,
    items: list[RadioItemConfig] | _Unset = UNSET,
    as_row: bool | _Unset = UNSET,
    current_value: str | _Unset = UNSET,
    help_text: str | _Unset = UNSET,
    error_text: str | _Unset = UNSET,
    data_attrs: list[DataAttrConfig] | _Unset = UNSET,
    **kwargs: Any,  # noqa: ANN401
) -> dict[str, Any]:
    """Render a group of radio buttons."""
    data_attrs = _collect_data_attrs("radio_group", config, data_attrs, kwargs)
    config = build_config(
        RadioGroupConfig, config, **{k: v for k, v in locals().items() if k not in ("config", "kwargs")}
    )
    return {"radio_group_config": config}


@register.inclusion_tag("insight_ui/components/radio_block.html")
def radio_block(
    config: RadioBlockConfig | None = None,
    *,
    name: str | _Unset = UNSET,
    label: str | _Unset = UNSET,
    items: list[RadioItemConfig] | _Unset = UNSET,
    integrated: bool | _Unset = UNSET,
    as_row: bool | _Unset = UNSET,
    request_url: str | _Unset = UNSET,
    htmx: HtmxConfig | _Unset | None = UNSET,
    method: str | _Unset = UNSET,
    current_value: str | _Unset = UNSET,
    help_text: str | _Unset = UNSET,
    error_text: str | _Unset = UNSET,
    data_attrs: list[DataAttrConfig] | _Unset = UNSET,
    **kwargs: Any,  # noqa: ANN401
) -> dict[str, Any]:
    """Render a group of radio buttons as a block."""
    data_attrs = _collect_data_attrs("radio_block", config, data_attrs, kwargs)
    config = build_config(
        RadioBlockConfig, config, **{k: v for k, v in locals().items() if k not in ("config", "kwargs")}
    )
    return {"radio_block_config": config}


@register.inclusion_tag("insight_ui/components/range_slider.html")
def slider(
    config: SliderConfig | None = None,
    *,
    tag_id: str | _Unset | None = UNSET,
    name: str | _Unset = UNSET,
    value: int | _Unset | None = UNSET,
    minimum: int | _Unset = UNSET,
    maximum: int | _Unset = UNSET,
    step_size: int | _Unset = UNSET,
    label: str | _Unset | None = UNSET,
    disabled: bool | _Unset = UNSET,
    disabled_reason: str | _Unset | None = UNSET,
    items: list[str] | _Unset = UNSET,
    legend_mode: str | _Unset = UNSET,
    dual: bool | _Unset = UNSET,
    value_min: int | _Unset | None = UNSET,
    value_max: int | _Unset | None = UNSET,
    help_text: str | _Unset = UNSET,
    error_text: str | _Unset = UNSET,
    data_attrs: list[DataAttrConfig] | _Unset = UNSET,
    **kwargs: Any,  # noqa: ANN401
) -> dict[str, Any]:
    """Render a range slider."""
    data_attrs = _collect_data_attrs("slider", config, data_attrs, kwargs)
    config = build_config(SliderConfig, config, **{k: v for k, v in locals().items() if k not in ("config", "kwargs")})
    # Each legend item sits at the share of the track where the thumb stands for its value (0 = start, 1 = end).
    last = max(len(config.items) - 1, 1)
    legend = [{"text": item, "position": f"{index / last:.4f}"} for index, item in enumerate(config.items)]
    return {"slider_config": config, "legend": legend}


@register.inclusion_tag("insight_ui/components/toggle_button.html")
def toggle(
    config: ToggleConfig | None = None,
    *,
    tag_id: str | _Unset | None = UNSET,
    name: str | _Unset = UNSET,
    value: str | _Unset = UNSET,
    label: str | _Unset | None = UNSET,
    icon: IconConfig | _Unset | None = UNSET,
    checked: bool | _Unset = UNSET,
    required: bool | _Unset = UNSET,
    disabled: bool | _Unset = UNSET,
    disabled_reason: str | _Unset | None = UNSET,
    switch: bool | _Unset = UNSET,
    method: str | _Unset = UNSET,
    help_text: str | _Unset = UNSET,
    error_text: str | _Unset = UNSET,
    data_attrs: list[DataAttrConfig] | _Unset = UNSET,
    **kwargs: Any,  # noqa: ANN401
) -> dict[str, Any]:
    """Render a toggle button."""
    data_attrs = _collect_data_attrs("toggle", config, data_attrs, kwargs)
    config = build_config(ToggleConfig, config, **{k: v for k, v in locals().items() if k not in ("config", "kwargs")})
    return {"toggle_config": config}


@register.inclusion_tag("insight_ui/components/select.html")
def select(
    config: SelectConfig | None = None,
    *,
    tag_id: str | _Unset | None = UNSET,
    name: str | _Unset = UNSET,
    label: str | _Unset | None = UNSET,
    required: bool | _Unset = UNSET,
    disabled: bool | _Unset = UNSET,
    disabled_reason: str | _Unset | None = UNSET,
    options: list[str] | dict[str, str] | _Unset = UNSET,
    selected_option: str | _Unset = UNSET,
    help_text: str | _Unset = UNSET,
    error_text: str | _Unset = UNSET,
    data_attrs: list[DataAttrConfig] | _Unset = UNSET,
    **kwargs: Any,  # noqa: ANN401
) -> dict[str, Any]:
    """Render a selection box."""
    data_attrs = _collect_data_attrs("select", config, data_attrs, kwargs)
    config = build_config(SelectConfig, config, **{k: v for k, v in locals().items() if k not in ("config", "kwargs")})
    return {"select_config": config}


@register.inclusion_tag("insight_ui/components/multiselect.html")
def multiselect(
    config: MultiselectConfig | None = None,
    *,
    name: str | _Unset = UNSET,
    label: str | _Unset | None = UNSET,
    maximum: int | _Unset | None = UNSET,
    show_buttons: bool | _Unset = UNSET,
    disabled: bool | _Unset = UNSET,
    disabled_reason: str | _Unset | None = UNSET,
    options: list[str] | dict[str, str] | _Unset = UNSET,
    selected_options: list[str] | _Unset = UNSET,
    help_text: str | _Unset = UNSET,
    error_text: str | _Unset = UNSET,
    data_attrs: list[DataAttrConfig] | _Unset = UNSET,
    **kwargs: Any,  # noqa: ANN401
) -> dict[str, Any]:
    """Render a selection box that allows multiple values."""
    data_attrs = _collect_data_attrs("multiselect", config, data_attrs, kwargs)
    config = build_config(
        MultiselectConfig, config, **{k: v for k, v in locals().items() if k not in ("config", "kwargs")}
    )
    return {"multiselect_config": config}


@register.inclusion_tag("insight_ui/components/chat.html")
def chat(
    config: ChatConfig | None = None,
    *,
    request_url: str | _Unset = UNSET,
    tag_id: str | _Unset = UNSET,
    htmx: HtmxConfig | _Unset | None = UNSET,
) -> dict[str, Any]:
    """Render a chat with an input line and a place for the response."""
    config = build_config(ChatConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"chat_config": config, "htmx": config.htmx or HtmxConfig(), "response_target": f"#{config.tag_id}-response"}


# =============================================================
#
#   Popup Tags
#
# =============================================================


@register.inclusion_tag("insight_ui/components/message_dialog.html")
def message_dialog(
    config: MessageDialogConfig | None = None,
    *,
    id: str | _Unset = UNSET,  # noqa: A002 - matches the modal block tag
    title: str | _Unset = UNSET,
    width: int | _Unset = UNSET,
    show_close: bool | _Unset = UNSET,
    message: str | list[str] | _Unset = UNSET,
    actions: list[ButtonConfig] | _Unset = UNSET,
    alert: bool | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a modal dialog with a predefined message and action buttons."""
    config = build_config(MessageDialogConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {
        # Context of the shared modal shell (layout/modal.html), which message_dialog.html extends.
        "modal_id": config.id,
        "title": config.title,
        "width": config.width,
        "show_close": config.show_close,
        "role": "alertdialog" if config.alert else "dialog",
        "describedby": f"{config.id}-message",
        # Extra classes of the {% modal %} layout tag; a message dialog has none.
        "wrapper_class": "",
        "paragraphs": [config.message] if isinstance(config.message, str) else config.message,
        "actions": config.actions,
    }


@register.inclusion_tag("insight_ui/components/alert.html")
def alert(
    config: AlertConfig | None = None,
    *,
    tag_id: str | _Unset = UNSET,
    message: str | _Unset = UNSET,
    severity: Severity | _Unset = UNSET,
    dismissible: bool | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a closable notification."""
    config = build_config(AlertConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"alert_config": config}


# =============================================================
#
#   Util Tags
#
# =============================================================


@register.inclusion_tag("insight_ui/components/infobox.html")
def infobox(
    config: InfoboxConfig | None = None,
    *,
    severity: Severity | _Unset = UNSET,
    message: str | _Unset = UNSET,
    **kwargs: str,
) -> dict[str, Any]:
    """Render a small box of information."""
    config = build_config(InfoboxConfig, config, severity=severity, message=message)

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
    year: int | str | _Unset = UNSET,
    holder: str | _Unset = UNSET,
    source_label: str | _Unset = UNSET,
    license_text: str | _Unset = UNSET,
    license_url: str | _Unset = UNSET,
    separator: str | _Unset = UNSET,
    rights_text: str | _Unset = UNSET,
    version: str | _Unset = UNSET,
    holder_url: str | _Unset = UNSET,
    holder_logo: LogoConfig | _Unset | None = UNSET,
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
    foreground_color: ColorType | str | _Unset = UNSET,
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
    dataset: ChartDatasetConfig | _Unset = UNSET,
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
    dataset: ChartDatasetConfig | _Unset = UNSET,
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
    htmx: HtmxConfig | _Unset | None = UNSET,
) -> dict[str, Any]:
    """Render a container for live updates via HTMX."""
    config = build_config(LiveContentConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {
        "live_content_config": config,
        "htmx": config.htmx or HtmxConfig(),
        "trigger": f"load, every {config.interval}s",
    }


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
    icon_mirror_rtl: bool | _Unset | None = UNSET,
    icon_end: bool | _Unset = UNSET,
    color: ColorType | _Unset = UNSET,
    size: Size | _Unset = UNSET,
    disabled: bool | _Unset = UNSET,
    tooltip: str | _Unset = UNSET,
    remove_htmx: HtmxConfig | _Unset | None = UNSET,
    remove_label: str | _Unset = UNSET,
) -> dict[str, Any]:
    """Render the badge component."""
    icon: IconConfig | _Unset | None = UNSET
    if icon_name is not UNSET:
        icon = (
            IconConfig(
                icon_name,
                icon_size if icon_size is not UNSET else "m",
                mirror_rtl=None if icon_mirror_rtl is UNSET else icon_mirror_rtl,
            )
            if icon_name
            else None
        )

    config = build_config(
        BadgeConfig,
        config,
        label=label,
        icon=icon,
        icon_end=icon_end,
        color=color,
        size=size,
        disabled=disabled,
        tooltip=tooltip,
        remove_htmx=remove_htmx,
        remove_label=remove_label,
    )
    remove_button = None
    if config.remove_htmx:
        remove_button = ButtonConfig(
            label=f"{config.remove_label or _('Remove')}: {config.label}",
            icon=IconConfig("x-mark", "xs"),
            icon_only=True,
            # Same color as the badge; a neutral badge has no button color, so its button uses the text color.
            color="secondary" if config.color == "neutral" else cast("ButtonColor", config.color),
            variant="plain" if config.color == "neutral" else "subtle",
            disabled=config.disabled,
            disabled_reason="",
            round=True,
            size="xs",
            button_type="button",
            htmx=config.remove_htmx,
            data_attrs=[DataAttrConfig(name="insight-badge-remove")],
            # Compensate the button padding and border, so the badge keeps its height.
            extra_classes="-my-1.5 -me-2",
        )
    return {"badge_config": config, "remove_button": remove_button}


@register.inclusion_tag("insight_ui/components/badge_list.html")
def badge_list(
    config: BadgeListConfig | None = None,
    *,
    tag_id: str | _Unset = UNSET,
    label: str | _Unset = UNSET,
    items: list[BadgeConfig] | _Unset = UNSET,
    clear_all_htmx: HtmxConfig | _Unset | None = UNSET,
    clear_all_label: str | _Unset = UNSET,
) -> dict[str, Any]:
    """Render badges as a labelled list that keeps the keyboard focus when a badge is removed."""
    config = build_config(BadgeListConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    clear_all_button = None
    if config.clear_all_htmx and config.items:
        clear_all_button = ButtonConfig(
            label=config.clear_all_label or _("Remove all"),
            color="secondary",
            variant="subtle",
            size="s",
            button_type="button",
            htmx=config.clear_all_htmx,
            data_attrs=[DataAttrConfig(name="insight-badge-clear-all")],
        )
    return {"badge_list_config": config, "clear_all_button": clear_all_button}


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
    items: Sequence[Any] | _Unset = UNSET,
    page: int | _Unset = UNSET,
    has_next: bool | _Unset = UNSET,
    auto_fetch: bool | _Unset = UNSET,
    threshold: int | _Unset = UNSET,
    heading_level: HeadingLevel | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a container for infinite scroll."""
    config = build_config(InfiniteScrollConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"infinite_scroll_config": config}


def _url_with_query(url: str, query: list[tuple[str, str]]) -> str:
    """Return the URL with its query string replaced by the given parameters."""
    return urlunsplit(urlsplit(url)._replace(query=urlencode(query)))


@register.inclusion_tag("insight_ui/components/pagination.html")
def pagination(
    config: PaginationConfig | None = None,
    *,
    request_url: str | _Unset = UNSET,
    current_page: Page | _Unset = UNSET,
    tag_id: str | _Unset = UNSET,
    htmx: HtmxConfig | _Unset | None = UNSET,
    include: str | _Unset = UNSET,
    page_param: str | _Unset = UNSET,
    on_each_side: int | _Unset = UNSET,
    on_ends: int | _Unset = UNSET,
    items_per_page: PaginationIppConfig | _Unset | None = UNSET,
) -> dict[str, Any]:
    """Render pagination with items per page selection."""
    config = build_config(PaginationConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    page = config.current_page
    paginator = page.paginator

    # Keep the other query parameters of request_url (filters, search) and only set the page number.
    query = parse_qsl(urlsplit(config.request_url).query, keep_blank_values=True)
    base_params = [(key, value) for key, value in query if key != config.page_param]

    def page_url(number: int) -> str:
        return _url_with_query(config.request_url, [*base_params, (config.page_param, str(number))])

    pages = [
        {"ellipsis": True}
        if number == paginator.ELLIPSIS
        else {
            "number": number,
            "url": page_url(int(number)),
            "current": number == page.number,
            "label": _("Page %(number)s") % {"number": number},
            # Stable ids let HTMX put the focus back after the swap: the link of page 3 and,
            # after navigating, the current-page marker of page 3 share the same id.
            "id": f"{config.tag_id}-page-{number}",
        }
        for number in paginator.get_elided_page_range(
            page.number, on_each_side=config.on_each_side, on_ends=config.on_ends
        )
    ]

    ipp_select = None
    ipp_hidden_params: list[tuple[str, str]] = []
    if config.items_per_page:
        ipp = config.items_per_page
        ipp_select = SelectConfig(
            name=ipp.name,
            tag_id=f"{config.tag_id}-ipp-select",
            label=str(ipp.label),
            options={str(option): str(option) for option in ipp.options},
            selected_option=str(ipp.selected_option),
        )
        # A GET form drops the query string of its action, so the other parameters travel as hidden fields.
        # The page number is left out: a new page size starts at page 1.
        ipp_hidden_params = [(key, value) for key, value in base_params if key != ipp.name]

    include = ", ".join(
        selector for selector in (f"#{config.tag_id}-ipp" if config.items_per_page else "", config.include) if selector
    )
    return {
        "pagination_config": config,
        "pages": pages,
        "previous_url": page_url(page.previous_page_number()) if page.has_previous() else "",
        "next_url": page_url(page.next_page_number()) if page.has_next() else "",
        "include": include,
        "ipp_select": ipp_select,
        "ipp_action": _url_with_query(config.request_url, []),
        "ipp_hidden_params": ipp_hidden_params,
    }


@register.inclusion_tag("insight_ui/components/table.html")
def table(config: TableConfig) -> dict[str, Any]:
    """Render a simple table."""
    config = build_config(TableConfig, config)
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
    htmx: HtmxConfig | _Unset | None = UNSET,
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
    filters: list[FilterConfig] | _Unset = UNSET,
    request_url: str | _Unset = UNSET,
    vertical: bool | _Unset = UNSET,
    htmx: HtmxConfig | _Unset | None = UNSET,
) -> dict[str, Any]:
    """Render a generic filter consisting of one or more <select> fields."""
    config = build_config(GenericFilterConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"generic_filter_config": config}


@register.inclusion_tag("insight_ui/components/query_builder.html")
def query_builder(
    config: QueryBuilderConfig | None = None,
    *,
    tag_id: str | _Unset = UNSET,
    fields: list[QueryBuilderFieldConfig] | _Unset = UNSET,
    filters: list[QueryBuilderFilterConfig] | _Unset = UNSET,
    request_url: str | _Unset = UNSET,
    param_name: str | _Unset = UNSET,
    max_filters: int | _Unset = UNSET,
    htmx: HtmxConfig | _Unset | None = UNSET,
    show_summary: bool | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a form to combine filters on model fields."""
    config = build_config(QueryBuilderConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    by_name = {field.field: field for field in config.fields}
    rows = []
    active: list[QueryBuilderFilterConfig | None] = list(config.filters) or [None]
    for item in active:
        field = by_name.get(item.field) if item else None
        definition = query_builder_utils.field_definition(field) if field else {}
        rows.append(
            {
                "filter": item,
                "operations": definition.get("operations", {}),
                "choices": definition.get("choices", {}),
                "input_type": definition.get("input_type", "text"),
                "value": query_builder_utils.format_value(item.value) if item else "",
            }
        )
    return {
        "query_builder_config": config,
        "field_definitions": [query_builder_utils.field_definition(field) for field in config.fields],
        "rows": rows,
        "summary": query_builder_utils.describe_filters(config.filters, config.fields) if config.show_summary else "",
        # Reset loads the request URL without filters; with HTMX it also resets the browser URL.
        "reset_url": config.request_url or "?",
        "reset_htmx": replace(config.htmx, push_url=True) if config.htmx else None,
    }


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
    actions: list[ButtonConfig] | _Unset = UNSET,
    heading_level: HeadingLevel | _Unset = UNSET,
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
    tags: list[BadgeConfig] | _Unset = UNSET,
    request_url: str | _Unset = UNSET,
    image: ImageConfig | _Unset | None = UNSET,
    actions: list[ButtonConfig] | _Unset = UNSET,
    heading_level: HeadingLevel | _Unset = UNSET,
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
    tags: list[BadgeConfig] | _Unset = UNSET,
    request_url: str | _Unset = UNSET,
    image: ImageConfig | _Unset | None = UNSET,
    actions: list[ButtonConfig] | _Unset = UNSET,
    back_title: str | _Unset = UNSET,
    back_content: str | _Unset = UNSET,
    back_actions: list[ButtonConfig] | _Unset = UNSET,
    heading_level: HeadingLevel | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a card that can be rotated 180°."""
    config = build_config(FlipCardConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"flip_card_config": config}


@register.inclusion_tag("insight_ui/components/carousel.html", takes_context=True)
def carousel(
    context: template.Context,
    config: CarouselConfig | None = None,
    *,
    items: Sequence[Any] | _Unset = UNSET,
    item_template: str | _Unset = UNSET,
    tag_id: str | _Unset = UNSET,
    label: str | _Unset = UNSET,
    autoplay: bool | _Unset = UNSET,
    show_dots: bool | _Unset = UNSET,
    show_index: bool | _Unset = UNSET,
    items_per_slide: int | _Unset = UNSET,
    min_item_width: str | _Unset = UNSET,
) -> dict[str, Any]:
    """Render any items as browsable pages; each item is rendered with the item template.

    The item template sees the page context (request, user, csrf_token) besides item.
    """
    config = build_config(
        CarouselConfig, config, **{k: v for k, v in locals().items() if k not in ("config", "context")}
    )
    page_context = cast("dict[str, Any]", context.flatten())
    return {**page_context, "carousel_config": config, "item_count": len(config.items)}


@register.inclusion_tag("insight_ui/components/carousels/3D_carousel.html")
def three_d_carousel(
    config: ThreeDCarouselConfig | None = None,
    *,
    tag_id: str | _Unset = UNSET,
    velocity: int | _Unset = UNSET,
    tilt: int | _Unset = UNSET,
    face_camera: bool | _Unset = UNSET,
    carousel_items: Sequence[CarouselItemConfig] | _Unset = UNSET,
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
    table: TableConfig | _Unset = UNSET,
    view_switch: RadioBlockConfig | _Unset | None = UNSET,
) -> dict[str, Any]:
    """Render a view of data that can be displayed in various ways."""
    config = build_config(ToggleViewConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    switch = config.view_switch
    # Switching the view reloads the whole component, so the radio block targets it and replaces it.
    if switch is not None and switch.request_url:
        htmx = replace(switch.htmx or HtmxConfig(), target=f"#{config.tag_id}", swap_method="outerHTML")
        switch = replace(switch, htmx=htmx)
    return {"toggle_view_config": config, "view_switch": switch}


# =============================================================
#
#   Form Tags
#
# =============================================================


# Tag and template that render each field config supported by the form component.
_FORM_FIELD_RENDERERS: dict[type, tuple[Callable[..., dict[str, Any]], str]] = {
    InputFieldConfig: (input_field, "insight_ui/components/input.html"),
    TextareaConfig: (textarea, "insight_ui/components/textarea.html"),
    SelectConfig: (select, "insight_ui/components/select.html"),
    MultiselectConfig: (multiselect, "insight_ui/components/multiselect.html"),
    CheckboxConfig: (checkbox, "insight_ui/components/checkbox.html"),
    CheckboxGroupConfig: (checkbox_group, "insight_ui/components/checkbox_group.html"),
    RadioGroupConfig: (radio_group, "insight_ui/components/radio_group.html"),
    RadioBlockConfig: (radio_block, "insight_ui/components/radio_block.html"),
    SliderConfig: (slider, "insight_ui/components/range_slider.html"),
    ToggleConfig: (toggle, "insight_ui/components/toggle_button.html"),
}


def _render_form_field(form_field: FormField) -> SafeString:
    """Render a single form field with the template tag of its config type.

    Args:
        form_field: The field config to render.

    Returns:
        The rendered field HTML.

    Raises:
        TypeError: If the config is not one of the supported field configs or a subclass of one.

    """
    if isinstance(form_field, RadioBlockConfig):
        # A standalone radio block renders its own <form>, which must not be nested.
        form_field = replace(form_field, integrated=True)
    # isinstance, like FormConfig's validation, so subclasses of supported configs render too.
    for config_type, (tag, template_name) in _FORM_FIELD_RENDERERS.items():
        if isinstance(form_field, config_type):
            return render_to_string(template_name, tag(form_field))
    raise TypeError(f"Unsupported form field: {type(form_field).__name__}")  # noqa: TRY003


@register.inclusion_tag("insight_ui/components/form.html")
def form(
    config: FormConfig | None = None,
    *,
    tag_id: str | _Unset = UNSET,
    title: str | _Unset = UNSET,
    description: str | _Unset = UNSET,
    fields: Sequence[FormField] | _Unset = UNSET,
    show_reset_button: bool | _Unset = UNSET,
    submit_label: str | _Unset = UNSET,
    reset_label: str | _Unset = UNSET,
    request_url: str | _Unset = UNSET,
    method: str | _Unset = UNSET,
    htmx: HtmxConfig | _Unset | None = UNSET,
    show_loading_indicator: bool | _Unset = UNSET,
) -> dict[str, Any]:
    """Render a form with HTMX support."""
    config = build_config(FormConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {
        "form_config": config,
        "rendered_fields": [_render_form_field(field) for field in config.fields],
        # "find" keeps the indicator to this form; a plain class selector would show every indicator on the page.
        "form_indicator": "find .htmx-indicator" if config.show_loading_indicator else "",
    }
