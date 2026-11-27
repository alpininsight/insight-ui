# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Template-Tags for Insight UI-Components."""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass, replace
from typing import TYPE_CHECKING, Any, Literal, cast
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from django import template
from django.conf import settings
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import NoReverseMatch, reverse
from django.utils.encoding import force_str

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Sequence

    from django.core.paginator import Page
from django.utils.functional import Promise
from django.utils.html import format_html_join
from django.utils.safestring import SafeData, SafeString, mark_safe
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
    ChartConfig,
    ChartDatasetConfig,
    ChatConfig,
    CheckboxConfig,
    CheckboxGroupConfig,
    CodeDiffConfig,
    ColorType,
    ControlVariant,
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
    RingCarouselConfig,
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
    TextDiffConfig,
    ToggleConfig,
    ToggleViewConfig,
    TurnstileConfig,
    WebSocketConfig,
)
from insight_ui.configs.building import UNSET, Unset, build_config
from insight_ui.configs.utils import ProgressBarConfig
from insight_ui.utils import query_builder as query_builder_utils
from insight_ui.utils.diff import text_parts, unified_diff
from insight_ui.utils.safe_markdown import render_untrusted

register = template.Library()

JsonPrimitive = str | int | float | bool | None
type JsonMapping = dict[str, "JsonValue"]
type JsonSequence = list["JsonValue"]
type JsonValue = JsonPrimitive | JsonMapping | JsonSequence


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


@register.filter
def markdownify(value: str) -> SafeString:
    """Convert markdown to html.

    A plain string may come from users: its raw HTML is shown as text and links or images with a scheme outside
    the allowed URL schemes lose their URL. A safe string (``mark_safe``) is trusted and may contain HTML.
    """
    html = markdown(value) if isinstance(value, SafeData) else render_untrusted(str(value))

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
    data_attrs: list[DataAttrConfig] | Unset,
    kwargs: dict[str, Any],
) -> list[DataAttrConfig] | Unset:
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
    name: str | Unset = UNSET,
    size: Size | Unset = UNSET,
    color: IconColor | Unset = UNSET,
    mirror_rtl: bool | Unset | None = UNSET,
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
    title: str | Unset = UNSET,
    chapter: str | Unset = UNSET,
    description: str | list[str] | Unset = UNSET,
    badges: list[BadgeConfig] | Unset = UNSET,
    buttons: list[ButtonConfig] | Unset = UNSET,
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
    content: str | Unset = UNSET,
    max_columns: int | Unset = UNSET,
    column_gap: str | Unset = UNSET,
    title: str | Unset = UNSET,
    fixed: bool | Unset = UNSET,
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
    title: str | Unset = UNSET,
    subtitle: str | Unset = UNSET,
    description: str | Unset = UNSET,
    cta_primary: ButtonConfig | Unset = UNSET,
    cta_secondary: ButtonConfig | Unset = UNSET,
    background_image_url: str | Unset = UNSET,
    badge: BadgeConfig | Unset = UNSET,
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
    title: str | Unset = UNSET,
    description: str | list[str] | Unset = UNSET,
    severity: Severity | Unset = UNSET,
    brand: BrandMarkConfig | Unset | None = UNSET,
    notice_title: str | Unset = UNSET,
    notice: str | Unset = UNSET,
    primary_action: ButtonConfig | Unset = UNSET,
    secondary_action: ButtonConfig | Unset = UNSET,
    actions: list[ButtonConfig] | Unset = UNSET,
    css_class: str | Unset = UNSET,
    card_css_class: str | Unset = UNSET,
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
    items: list[BreadcrumbItemConfig] | Unset = UNSET,
    htmx: HtmxConfig | Unset | None = UNSET,
) -> dict[str, Any]:
    """Render breadcrumb navigation."""
    config = build_config(BreadcrumbsConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    config.validate_items(resolve_lazy=True)
    return {"items": config.items, "htmx": config.htmx}


@register.inclusion_tag("insight_ui/components/stepper.html")
def stepper(config: StepperConfig | None = None, *, items: list[StepperItemConfig] | Unset = UNSET) -> dict[str, Any]:
    """Render a graphical representation of process steps."""
    config = build_config(StepperConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"items": config.items}


@register.inclusion_tag("insight_ui/components/minimal_stepper.html")
def minimal_stepper(
    config: MinimalStepperConfig | None = None,
    *,
    steps: list[StepStatus] | Unset = UNSET,
    step_count: int | Unset = UNSET,
    current_step: int | Unset = UNSET,
    current_step_status: StepStatus | Unset = UNSET,
    icon_size: Size | Unset = UNSET,
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
    items: list[BulletPointItemConfig] | Unset = UNSET,
    htmx: HtmxConfig | Unset | None = UNSET,
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
    tag_id: str | Unset = UNSET,
    label: str | Unset = UNSET,
    request_url: str | Unset = UNSET,
    external: bool | Unset = UNSET,
    download: bool | str | Unset = UNSET,
    on_click: str | Unset = UNSET,
    icon_name: str | Unset = UNSET,
    icon_size: str | Unset = UNSET,
    icon_mirror_rtl: bool | Unset | None = UNSET,
    icon_end: bool | Unset = UNSET,
    icon_only: bool | Unset = UNSET,
    color: ButtonColor | Unset = UNSET,
    variant: ButtonVariant | Unset = UNSET,
    size: Size | Unset = UNSET,
    round: bool | Unset = UNSET,  # noqa: A002
    tooltip: str | Unset = UNSET,
    htmx: HtmxConfig | Unset = UNSET,
    hidden: bool | Unset = UNSET,
    disabled: bool | Unset = UNSET,
    disabled_reason: str | Unset = UNSET,
    button_type: HtmlButtonType | Unset = UNSET,
    extra_classes: str | Unset = UNSET,
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
    icon: IconConfig | Unset | None = UNSET
    if icon_name is not UNSET:
        icon = (
            IconConfig(
                name=icon_name,
                size=icon_size if icon_size is not UNSET else "m",
                mirror_rtl=None if icon_mirror_rtl is UNSET else icon_mirror_rtl,
            )
            if icon_name
            else None
        )

    # Collect data_* kwargs and convert to DataAttrConfig list
    data_attrs: list[DataAttrConfig] | Unset = UNSET
    data_kwargs = {k: v for k, v in kwargs.items() if k.startswith("data_")}
    if data_kwargs:
        data_attrs = [
            DataAttrConfig(name=key[5:].replace("_", "-"), value=str(value)) for key, value in data_kwargs.items()
        ]

    # Collect aria_* kwargs and convert to DataAttrConfig list
    aria_attrs: list[DataAttrConfig] | Unset = UNSET
    aria_kwargs = {k: v for k, v in kwargs.items() if k.startswith("aria_")}
    if aria_kwargs:
        aria_attrs = [
            DataAttrConfig(name=key[5:].replace("_", "-"), value=str(value)) for key, value in aria_kwargs.items()
        ]

    # Collect hx_* kwargs and convert to DataAttrConfig list
    hx_attrs: list[DataAttrConfig] | Unset = UNSET
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
        download=download,
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
    tag_id: str | Unset | None = UNSET,
    name: str | Unset = UNSET,
    input_type: str | Unset = UNSET,
    placeholder: str | Unset = UNSET,
    value: str | int | float | Unset | None = UNSET,
    minimum: int | Unset | None = UNSET,
    maximum: int | Unset | None = UNSET,
    min_length: int | Unset | None = UNSET,
    max_length: int | Unset | None = UNSET,
    checked: bool | Unset = UNSET,
    required: bool | Unset = UNSET,
    disabled: bool | Unset = UNSET,
    disabled_reason: str | Unset | None = UNSET,
    label: str | Unset | None = UNSET,
    help_text: str | Unset = UNSET,
    error_text: str | Unset = UNSET,
    data_attrs: list[DataAttrConfig] | Unset = UNSET,
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
    tag_id: str | Unset | None = UNSET,
    name: str | Unset = UNSET,
    placeholder: str | Unset = UNSET,
    value: str | Unset = UNSET,
    rows: int | Unset = UNSET,
    cols: int | Unset | None = UNSET,
    required: bool | Unset = UNSET,
    disabled: bool | Unset = UNSET,
    disabled_reason: str | Unset | None = UNSET,
    label: str | Unset | None = UNSET,
    help_text: str | Unset = UNSET,
    error_text: str | Unset = UNSET,
    data_attrs: list[DataAttrConfig] | Unset = UNSET,
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
    tag_id: str | Unset | None = UNSET,
    name: str | Unset = UNSET,
    value: str | Unset = UNSET,
    label: str | Unset | None = UNSET,
    checked: bool | Unset = UNSET,
    required: bool | Unset = UNSET,
    disabled: bool | Unset = UNSET,
    disabled_reason: str | Unset = UNSET,
    help_text: str | Unset = UNSET,
    error_text: str | Unset = UNSET,
    data_attrs: list[DataAttrConfig] | Unset = UNSET,
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
    name: str | Unset = UNSET,
    label: str | Unset = UNSET,
    items: list[RadioItemConfig] | Unset = UNSET,
    as_row: bool | Unset = UNSET,
    current_value: str | Unset = UNSET,
    help_text: str | Unset = UNSET,
    error_text: str | Unset = UNSET,
    data_attrs: list[DataAttrConfig] | Unset = UNSET,
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
    name: str | Unset = UNSET,
    label: str | Unset = UNSET,
    items: list[RadioItemConfig] | Unset = UNSET,
    integrated: bool | Unset = UNSET,
    as_row: bool | Unset = UNSET,
    request_url: str | Unset = UNSET,
    htmx: HtmxConfig | Unset | None = UNSET,
    method: str | Unset = UNSET,
    current_value: str | Unset = UNSET,
    variant: ControlVariant | Unset = UNSET,
    color: ButtonColor | Unset = UNSET,
    help_text: str | Unset = UNSET,
    error_text: str | Unset = UNSET,
    data_attrs: list[DataAttrConfig] | Unset = UNSET,
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
    tag_id: str | Unset | None = UNSET,
    name: str | Unset = UNSET,
    value: int | Unset | None = UNSET,
    minimum: int | Unset = UNSET,
    maximum: int | Unset = UNSET,
    step_size: int | Unset = UNSET,
    label: str | Unset | None = UNSET,
    disabled: bool | Unset = UNSET,
    disabled_reason: str | Unset | None = UNSET,
    items: list[str] | Unset = UNSET,
    legend_mode: str | Unset = UNSET,
    dual: bool | Unset = UNSET,
    value_min: int | Unset | None = UNSET,
    value_max: int | Unset | None = UNSET,
    color: ButtonColor | Unset = UNSET,
    help_text: str | Unset = UNSET,
    error_text: str | Unset = UNSET,
    data_attrs: list[DataAttrConfig] | Unset = UNSET,
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
    tag_id: str | Unset | None = UNSET,
    name: str | Unset = UNSET,
    value: str | Unset = UNSET,
    label: str | Unset | None = UNSET,
    icon: IconConfig | Unset | None = UNSET,
    icon_only: bool | Unset = UNSET,
    checked: bool | Unset = UNSET,
    required: bool | Unset = UNSET,
    disabled: bool | Unset = UNSET,
    disabled_reason: str | Unset | None = UNSET,
    switch: bool | Unset = UNSET,
    variant: ControlVariant | Unset = UNSET,
    color: ButtonColor | Unset = UNSET,
    method: str | Unset = UNSET,
    help_text: str | Unset = UNSET,
    error_text: str | Unset = UNSET,
    data_attrs: list[DataAttrConfig] | Unset = UNSET,
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
    tag_id: str | Unset | None = UNSET,
    name: str | Unset = UNSET,
    label: str | Unset | None = UNSET,
    required: bool | Unset = UNSET,
    disabled: bool | Unset = UNSET,
    disabled_reason: str | Unset | None = UNSET,
    options: list[str] | dict[str, str] | Unset = UNSET,
    selected_option: str | Unset = UNSET,
    help_text: str | Unset = UNSET,
    error_text: str | Unset = UNSET,
    data_attrs: list[DataAttrConfig] | Unset = UNSET,
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
    tag_id: str | Unset | None = UNSET,
    name: str | Unset = UNSET,
    label: str | Unset | None = UNSET,
    maximum: int | Unset | None = UNSET,
    show_buttons: bool | Unset = UNSET,
    disabled: bool | Unset = UNSET,
    disabled_reason: str | Unset | None = UNSET,
    options: list[str] | dict[str, str] | Unset = UNSET,
    selected_options: list[str] | Unset = UNSET,
    help_text: str | Unset = UNSET,
    error_text: str | Unset = UNSET,
    data_attrs: list[DataAttrConfig] | Unset = UNSET,
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
    request_url: str | Unset = UNSET,
    tag_id: str | Unset = UNSET,
    htmx: HtmxConfig | Unset | None = UNSET,
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
    id: str | Unset = UNSET,  # noqa: A002 - matches the modal block tag
    title: str | Unset = UNSET,
    width: int | Unset = UNSET,
    show_close: bool | Unset = UNSET,
    message: str | list[str] | Unset = UNSET,
    actions: list[ButtonConfig] | Unset = UNSET,
    alert: bool | Unset = UNSET,
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
    tag_id: str | Unset = UNSET,
    message: str | Unset = UNSET,
    severity: Severity | Unset = UNSET,
    dismissible: bool | Unset = UNSET,
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
    severity: Severity | Unset = UNSET,
    message: str | Unset = UNSET,
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
    year: int | str | Unset = UNSET,
    holder: str | Unset = UNSET,
    source_label: str | Unset = UNSET,
    license_text: str | Unset = UNSET,
    license_url: str | Unset = UNSET,
    separator: str | Unset = UNSET,
    rights_text: str | Unset = UNSET,
    version: str | Unset = UNSET,
    holder_url: str | Unset = UNSET,
    holder_logo: LogoConfig | Unset | None = UNSET,
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


@register.inclusion_tag("insight_ui/components/text_diff.html")
def text_diff(
    config: TextDiffConfig | None = None,
    *,
    before: str | Unset = UNSET,
    after: str | Unset = UNSET,
    show_legend: bool | Unset = UNSET,
) -> dict[str, Any]:
    """Render the changes between two texts with removed words struck through and added words underlined."""
    config = build_config(TextDiffConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"parts": text_parts(str(config.before), str(config.after)), "show_legend": config.show_legend}


@register.inclusion_tag("insight_ui/components/code_diff.html")
def code_diff(
    config: CodeDiffConfig | None = None,
    *,
    before: str | Unset = UNSET,
    after: str | Unset = UNSET,
    language: str | Unset = UNSET,
    filename: str | Unset = UNSET,
    tag_id: str | Unset = UNSET,
) -> dict[str, Any]:
    """Render the changes between two short code snippets as a unified diff in a code block."""
    config = build_config(CodeDiffConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    diff_text, marks = unified_diff(str(config.before), str(config.after))
    return {"code_diff_config": config, "diff_text": diff_text, "diff_marks": json_attribute(marks) if marks else ""}


@register.inclusion_tag("insight_ui/components/logo.html")
def logo(
    config: LogoConfig | None = None,
    *,
    url: str | Unset | None = UNSET,
    url_dark: str | Unset | None = UNSET,
    alt: str | Unset | None = UNSET,
    icon_name: str | Unset | None = UNSET,
    icon_size: str | Unset | None = UNSET,
    height: str | Unset | None = UNSET,
    width: str | Unset | None = UNSET,
) -> dict[str, Any]:
    """Render a brand logo as an image, SVG asset, or Insight UI icon."""
    # Only override icon if icon_name was explicitly provided
    icon: IconConfig | Unset | None = UNSET
    if icon_name is not UNSET:
        icon = IconConfig(name=icon_name, size=icon_size if icon_size is not UNSET else "m") if icon_name else None

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
    primary_text: str | Unset = UNSET,
    secondary_text: str | Unset = UNSET,
    primary_text_color: str | Unset = UNSET,
    secondary_text_color: str | Unset = UNSET,
    logo: LogoConfig | Unset = UNSET,
    logo_position: str | Unset = UNSET,
    css_class: str | Unset = UNSET,
) -> dict[str, Any]:
    """Render a public logo plus a two-tone wordmark.

    Next to a wordmark the logo is decorative, so a link around the mark is named by its text only.
    """
    config = build_config(BrandMarkConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    mark_logo = config.logo
    if mark_logo is not None and (config.primary_text or config.secondary_text):
        mark_logo = replace(mark_logo, alt="")
    return {"brand_mark_config": config, "mark_logo": mark_logo}


@register.inclusion_tag("insight_ui/components/corner_ribbon.html")
def corner_ribbon(
    config: CornerRibbonConfig | None = None,
    *,
    text: str | Unset = UNSET,
    position: CornerPosition | Unset = UNSET,
    color: ColorType | Unset = UNSET,
    request_url: str | Unset = UNSET,
) -> dict[str, Any]:
    """Render a corner ribbon positioned in any browser corner."""
    config = build_config(CornerRibbonConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"corner_ribbon_config": config}


@register.inclusion_tag("insight_ui/components/progress_bar.html")
def progress_bar(
    config: ProgressBarConfig | None = None,
    *,
    tag_id: str | Unset = UNSET,
    label: str | Unset = UNSET,
    request_url: str | Unset = UNSET,
    interval: int | Unset = UNSET,
    sse_url: str | Unset = UNSET,
    min_value: int | Unset = UNSET,
    max_value: int | Unset = UNSET,
    value: int | Unset = UNSET,
    show_value: bool | Unset = UNSET,
    hide_on_complete: bool | Unset = UNSET,
    complete_delay: int | Unset = UNSET,
    stop_on_error: bool | Unset = UNSET,
    show_cancel: bool | Unset = UNSET,
    cancel_label: str | Unset = UNSET,
    cancel_url: str | Unset = UNSET,
    show_retry: bool | Unset = UNSET,
    retry_label: str | Unset = UNSET,
) -> dict[str, Any]:
    """Render a simple progress bar."""
    config = build_config(ProgressBarConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"progress_bar_config": config}


@register.inclusion_tag("insight_ui/components/geo_map.html")
def geo_map(
    config: GeoMapConfig | None = None,
    *,
    initial_coords: list[float] | Unset = UNSET,
    initial_zoom: int | Unset = UNSET,
    map_height: int | Unset = UNSET,
    datasets: list[GeoMapDatasetConfig] | Unset = UNSET,
    aria_label: str | Unset = UNSET,
    tag_id: str | Unset = UNSET,
) -> dict[str, Any]:
    """Render an integrated geographic map.

    Everything the script needs goes through json_script, so marker texts can never end the script, and the
    datasets may be GeoMapDatasetConfig objects or plain dicts.
    """
    config = build_config(GeoMapConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    map_data = {
        "center": config.initial_coords,
        "zoom": config.initial_zoom,
        "datasets": _plain_data(config.datasets),
        "tiles": get_config("map_tiles"),
        "labels": {"zoom_in": _("Zoom in"), "zoom_out": _("Zoom out"), "layers": _("Map layers")},
    }
    return {"map_config": config, "map_data": map_data, "map_data_id": f"{config.tag_id}-data"}


def _plain_data(value: object) -> object:
    """Turn config objects inside lists and dicts into dicts, so json_script can serialize them."""
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    if isinstance(value, dict):
        return {key: _plain_data(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain_data(item) for item in value]
    return value


@register.inclusion_tag("insight_ui/components/charts/bar_chart.html")
def bar_chart(
    config: ChartConfig | None = None,
    *,
    tag_id: str | Unset = UNSET,
    dataset: ChartDatasetConfig | Unset = UNSET,
    chart_height: int | Unset = UNSET,
    aria_label: str | Unset = UNSET,
    show_decal: bool | Unset = UNSET,
) -> dict[str, Any]:
    """Render a bar chart with Apache ECharts."""
    config = build_config(ChartConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return _chart_context(config)


@register.inclusion_tag("insight_ui/components/charts/line_chart.html")
def line_chart(
    config: ChartConfig | None = None,
    *,
    tag_id: str | Unset = UNSET,
    dataset: ChartDatasetConfig | Unset = UNSET,
    chart_height: int | Unset = UNSET,
    aria_label: str | Unset = UNSET,
    show_decal: bool | Unset = UNSET,
) -> dict[str, Any]:
    """Render a line chart with Apache ECharts."""
    config = build_config(ChartConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return _chart_context(config)


def _chart_context(config: ChartConfig) -> dict[str, Any]:
    """Hand the chart data to the script through json_script, so titles and names can never end the script."""
    return {"chart_config": config, "chart_data": asdict(config.dataset), "chart_data_id": f"{config.tag_id}-data"}


@register.inclusion_tag("insight_ui/components/live_content.html")
def live_content(
    config: LiveContentConfig | None = None,
    *,
    tag_id: str | Unset = UNSET,
    request_url: str | Unset = UNSET,
    interval: int | Unset = UNSET,
    initial_content: str | Unset = UNSET,
    htmx: HtmxConfig | Unset | None = UNSET,
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
    tag_id: str | Unset = UNSET,
    request_url: str | Unset = UNSET,
    initial_content: str | Unset = UNSET,
) -> dict[str, Any]:
    """Render a WebSocket component as a thin wrapper for the HTMX ws extension."""
    config = build_config(WebSocketConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"websocket_config": config}


@register.inclusion_tag("insight_ui/components/badge.html")
def badge(
    config: BadgeConfig | None = None,
    *,
    label: str | Unset = UNSET,
    icon_name: str | Unset = UNSET,
    icon_size: str | Unset = UNSET,
    icon_mirror_rtl: bool | Unset | None = UNSET,
    icon_end: bool | Unset = UNSET,
    color: ColorType | Unset = UNSET,
    size: Size | Unset = UNSET,
    disabled: bool | Unset = UNSET,
    tooltip: str | Unset = UNSET,
    remove_htmx: HtmxConfig | Unset | None = UNSET,
    remove_label: str | Unset = UNSET,
) -> dict[str, Any]:
    """Render the badge component."""
    icon: IconConfig | Unset | None = UNSET
    if icon_name is not UNSET:
        icon = (
            IconConfig(
                name=icon_name,
                size=icon_size if icon_size is not UNSET else "m",
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
            icon=IconConfig(name="x-mark", size="xs"),
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
    tag_id: str | Unset = UNSET,
    label: str | Unset = UNSET,
    items: list[BadgeConfig] | Unset = UNSET,
    clear_all_htmx: HtmxConfig | Unset | None = UNSET,
    clear_all_label: str | Unset = UNSET,
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


@register.inclusion_tag("insight_ui/components/infinite_scroll.html", takes_context=True)
def infinite_scroll(
    context: template.Context,
    config: InfiniteScrollConfig | None = None,
    *,
    tag_id: str | Unset = UNSET,
    request_url: str | Unset = UNSET,
    current_page: Page | Unset = UNSET,
    page_param: str | Unset = UNSET,
    item_template: str | Unset = UNSET,
    auto_fetch: bool | Unset = UNSET,
    heading_level: HeadingLevel | Unset = UNSET,
    htmx: HtmxConfig | Unset | None = UNSET,
) -> dict[str, Any]:
    """Render a feed of the current page that loads the next pages."""
    config = build_config(
        InfiniteScrollConfig, config, **{k: v for k, v in locals().items() if k not in ("config", "context")}
    )
    return _infinite_scroll_context(context, config, next_page=False)


@register.inclusion_tag("insight_ui/components/infinite_scroll_items.html", takes_context=True)
def infinite_scroll_items(context: template.Context, config: InfiniteScrollConfig) -> dict[str, Any]:
    """Render the response to a request for the next page of an infinite_scroll feed."""
    config = build_config(InfiniteScrollConfig, config)
    return _infinite_scroll_context(context, config, next_page=True)


def _infinite_scroll_context(
    context: template.Context, config: InfiniteScrollConfig, *, next_page: bool
) -> dict[str, Any]:
    """Build the context shared by the feed and the responses for further pages.

    Args:
        context: The caller's page context, also available to custom item templates.
        config: The feed configuration with the page to render.
        next_page: True for a response that appends to an existing feed.

    Returns:
        The template context.

    """
    page = config.current_page
    load_more = None
    if page.has_next():
        options = config.htmx or HtmxConfig()
        number = page.next_page_number()
        next_url = _page_url(config.request_url, config.page_param, number)
        if options.method == "get":
            # HTMX appends vals to GET URLs. Keep the owned page value in vals exactly once.
            query = parse_qsl(urlsplit(next_url).query, keep_blank_values=True)
            next_url = _url_with_query(next_url, [(key, value) for key, value in query if key != config.page_param])
        # The control after the feed appends the next page to the feed and is replaced out of band.
        load_more = replace(
            options,
            request_url=next_url,
            vals={**(options.vals or {}), config.page_param: number},
            target=f"#{config.tag_id}",
            swap_method="beforeend",
            push_url=False,
            # Without an own indicator the control container shows its loading text.
            loading_indicator_id=(config.htmx and config.htmx.loading_indicator_id) or f"#{config.tag_id}-more",
        )
    return {
        **context.flatten(),
        "infinite_scroll_config": config,
        "items": [
            {"item": item, "position": page.start_index() + offset} for offset, item in enumerate(page.object_list)
        ],
        "set_size": page.paginator.count,
        "load_more": load_more,
        "next_page": next_page,
        # After "Load more" the focus moves to the first new item; on scroll it stays where it is.
        "focus_first": next_page and not config.auto_fetch,
    }


def _url_with_query(url: str, query: list[tuple[str, str]]) -> str:
    """Return the URL with its query string replaced by the given parameters."""
    return urlunsplit(urlsplit(force_str(url))._replace(query=urlencode(query)))


def _page_url(url: str, page_param: str, number: int) -> str:
    """Return the URL of a page: other query parameters (filters, search) stay, only the page number is set."""
    url = force_str(url)
    query = [(key, value) for key, value in parse_qsl(urlsplit(url).query, keep_blank_values=True) if key != page_param]
    return _url_with_query(url, [*query, (page_param, str(number))])


@register.inclusion_tag("insight_ui/components/pagination.html")
def pagination(
    config: PaginationConfig | None = None,
    *,
    request_url: str | Unset = UNSET,
    current_page: Page | Unset = UNSET,
    tag_id: str | Unset = UNSET,
    htmx: HtmxConfig | Unset | None = UNSET,
    include: str | Unset = UNSET,
    page_param: str | Unset = UNSET,
    on_each_side: int | Unset = UNSET,
    on_ends: int | Unset = UNSET,
    items_per_page: PaginationIppConfig | Unset | None = UNSET,
) -> dict[str, Any]:
    """Render pagination with items per page selection."""
    config = build_config(PaginationConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    page = config.current_page
    paginator = page.paginator

    # The other query parameters of request_url (filters, search) are kept; the page size form needs them too.
    resolved_url = force_str(config.request_url)
    query = parse_qsl(urlsplit(resolved_url).query, keep_blank_values=True)
    base_params = [(key, value) for key, value in query if key != config.page_param]

    def page_url(number: int) -> str:
        return _page_url(resolved_url, config.page_param, number)

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
        "ipp_action": _url_with_query(resolved_url, []),
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
    request_url: str | Unset = UNSET,
    tag_id: str | Unset = UNSET,
    name: str | Unset = UNSET,
    simple: bool | Unset = UNSET,
    search_query: str | Unset = UNSET,
    placeholder: str | Unset = UNSET,
    button_label: str | Unset = UNSET,
    htmx: HtmxConfig | Unset | None = UNSET,
    enable_search: bool | Unset = UNSET,
    search_index_url: str | Unset = UNSET,
) -> dict[str, Any]:
    """Render text input with a button for a search function."""
    config = build_config(SearchBarConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"search_bar_config": config}


@register.inclusion_tag("insight_ui/components/generic_filter.html")
def generic_filter(
    config: GenericFilterConfig | None = None,
    *,
    filters: list[FilterConfig] | Unset = UNSET,
    request_url: str | Unset = UNSET,
    vertical: bool | Unset = UNSET,
    htmx: HtmxConfig | Unset | None = UNSET,
) -> dict[str, Any]:
    """Render a generic filter consisting of one or more <select> fields."""
    config = build_config(GenericFilterConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"generic_filter_config": config}


@register.inclusion_tag("insight_ui/components/query_builder.html")
def query_builder(
    config: QueryBuilderConfig | None = None,
    *,
    tag_id: str | Unset = UNSET,
    fields: list[QueryBuilderFieldConfig] | Unset = UNSET,
    filters: list[QueryBuilderFilterConfig] | Unset = UNSET,
    request_url: str | Unset = UNSET,
    param_name: str | Unset = UNSET,
    max_filters: int | Unset = UNSET,
    htmx: HtmxConfig | Unset | None = UNSET,
    show_summary: bool | Unset = UNSET,
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
    title: str | Unset = UNSET,
    content: str | Unset = UNSET,
    subtitle: str | Unset = UNSET,
    image: ImageConfig | Unset | None = UNSET,
    actions: list[ButtonConfig] | Unset = UNSET,
    heading_level: HeadingLevel | Unset = UNSET,
) -> dict[str, Any]:
    """Render a card with an aspect ratio of 16:9."""
    config = build_config(CardConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"card_config": config}


@register.inclusion_tag("insight_ui/components/cards/app_card.html")
def app_card(
    config: AppCardConfig | None = None,
    *,
    title: str | Unset = UNSET,
    content: str | Unset = UNSET,
    tags: list[BadgeConfig] | Unset = UNSET,
    request_url: str | Unset = UNSET,
    image: ImageConfig | Unset | None = UNSET,
    actions: list[ButtonConfig] | Unset = UNSET,
    heading_level: HeadingLevel | Unset = UNSET,
) -> dict[str, Any]:
    """Render a vertically aligned card."""
    config = build_config(AppCardConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"app_card_config": config}


@register.inclusion_tag("insight_ui/components/cards/flip_card.html")
def flip_card(
    config: FlipCardConfig | None = None,
    *,
    title: str | Unset = UNSET,
    content: str | Unset = UNSET,
    tags: list[BadgeConfig] | Unset = UNSET,
    request_url: str | Unset = UNSET,
    image: ImageConfig | Unset | None = UNSET,
    actions: list[ButtonConfig] | Unset = UNSET,
    back_title: str | Unset = UNSET,
    back_content: str | Unset = UNSET,
    back_actions: list[ButtonConfig] | Unset = UNSET,
    heading_level: HeadingLevel | Unset = UNSET,
) -> dict[str, Any]:
    """Render a card that can be rotated 180°."""
    config = build_config(FlipCardConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"flip_card_config": config}


@register.inclusion_tag("insight_ui/components/carousel.html", takes_context=True)
def carousel(
    context: template.Context,
    config: CarouselConfig | None = None,
    *,
    items: Sequence[Any] | Unset = UNSET,
    item_template: str | Unset = UNSET,
    tag_id: str | Unset = UNSET,
    label: str | Unset = UNSET,
    autoplay: bool | Unset = UNSET,
    show_dots: bool | Unset = UNSET,
    show_index: bool | Unset = UNSET,
    items_per_slide: int | Unset = UNSET,
    min_item_width: str | Unset = UNSET,
) -> dict[str, Any]:
    """Render any items as browsable pages; each item is rendered with the item template.

    The item template sees the page context (request, user, csrf_token) besides item.
    """
    config = build_config(
        CarouselConfig, config, **{k: v for k, v in locals().items() if k not in ("config", "context")}
    )
    page_context = cast("dict[str, Any]", context.flatten())
    return {**page_context, "carousel_config": config, "item_count": len(config.items)}


@register.inclusion_tag("insight_ui/components/carousels/ring_carousel.html", takes_context=True)
def ring_carousel(
    context: template.Context,
    config: RingCarouselConfig | None = None,
    *,
    tag_id: str | Unset = UNSET,
    items: Sequence[Any] | Unset = UNSET,
    item_template: str | Unset = UNSET,
    label: str | Unset = UNSET,
    duration: int | Unset = UNSET,
    tilt: int | Unset = UNSET,
    face_camera: bool | Unset = UNSET,
) -> dict[str, Any]:
    """Render any items on a turning ring; each item is rendered with the item template.

    The item template sees the page context (request, user, csrf_token) besides item.
    """
    config = build_config(
        RingCarouselConfig, config, **{k: v for k, v in locals().items() if k not in ("config", "context")}
    )
    page_context = cast("dict[str, Any]", context.flatten())
    return {**page_context, "carousel_config": config, "item_count": len(config.items)}


@register.inclusion_tag("insight_ui/components/toggle_view.html", takes_context=True)
def toggle_view(
    context: template.Context,
    config: ToggleViewConfig | None = None,
    *,
    tag_id: str | Unset = UNSET,
    view_switch: RadioBlockConfig | Unset = UNSET,
    items: Sequence[Any] | Unset = UNSET,
    item_template: str | Unset = UNSET,
    table: TableConfig | Unset = UNSET,
    min_item_width: str | Unset = UNSET,
) -> dict[str, Any]:
    """Render the same data as a grid, a table or a carousel; the view switch picks the view.

    The item template sees the page context (request, user, csrf_token) besides item.
    """
    config = build_config(
        ToggleViewConfig, config, **{k: v for k, v in locals().items() if k not in ("config", "context")}
    )
    switch = config.view_switch
    # Switching the view reloads the whole component, so the radio block targets it and replaces it.
    if switch.request_url:
        htmx = replace(switch.htmx or HtmxConfig(), target=f"#{config.tag_id}", swap_method="outerHTML")
        switch = replace(switch, htmx=htmx)
    page_context = cast("dict[str, Any]", context.flatten())
    return {**page_context, "toggle_view_config": config, "view_switch": switch}


# =============================================================
#
#   Form Tags
#
# =============================================================


@register.inclusion_tag("insight_ui/components/turnstile.html")
def turnstile(
    config: TurnstileConfig | None = None,
    *,
    site_key: str | Unset = UNSET,
    theme: Literal["auto", "light", "dark"] | Unset = UNSET,
    size: Literal["normal", "flexible", "compact"] | Unset = UNSET,
    action: str | Unset = UNSET,
) -> dict[str, TurnstileConfig]:
    """Render the public Turnstile widget; the host must verify its token."""
    config = build_config(TurnstileConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {"turnstile_config": config}


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
    tag_id: str | Unset = UNSET,
    title: str | Unset = UNSET,
    description: str | Unset = UNSET,
    fields: Sequence[FormField] | Unset = UNSET,
    show_reset_button: bool | Unset = UNSET,
    submit_label: str | Unset = UNSET,
    reset_label: str | Unset = UNSET,
    request_url: str | Unset = UNSET,
    method: str | Unset = UNSET,
    htmx: HtmxConfig | Unset | None = UNSET,
    show_loading_indicator: bool | Unset = UNSET,
    turnstile: TurnstileConfig | Unset | None = UNSET,
) -> dict[str, Any]:
    """Render a form with HTMX support."""
    config = build_config(FormConfig, config, **{k: v for k, v in locals().items() if k != "config"})
    return {
        "form_config": config,
        "native_form_action": (config.htmx.request_url if config.htmx else "") or config.request_url,
        "rendered_fields": [_render_form_field(field) for field in config.fields],
        # "find" keeps the indicator to this form; a plain class selector would show every indicator on the page.
        "form_indicator": "find .htmx-indicator" if config.show_loading_indicator else "",
    }
