"""
Dataclass configurations for Insight UI components.

This module provides type-safe configuration classes for all Insight UI template tags.
Using these dataclasses instead of plain dictionaries gives you:

- IDE autocompletion when creating configurations
- Static type checking with mypy
- Runtime validation via __post_init__
- Clear documentation of required and optional fields
- Reusable base classes for common patterns

Example usage:
    from insight_ui.configs import InputFieldConfig, SliderConfig

    # IDE shows all available fields with types
    email_field = InputFieldConfig(
        name="email",
        input_type="email",
        label="E-Mail Address",
        required=True,
    )

    price_slider = SliderConfig(
        name="price",
        label="Price Range",
        minimum=0,
        maximum=1000,
        dual=True,
    )
"""

from insight_ui.configs.base import ActionConfig, HtmxConfig, IconConfig, ImageConfig
from insight_ui.configs.card import (
    AppCardConfig,
    CardCarouselConfig,
    CardConfig,
    CarouselItemConfig,
    FlipCardConfig,
    ImageCarouselConfig,
    ImageCarouselItemConfig,
    ThreeDCarouselConfig,
    ToggleViewConfig,
)
from insight_ui.configs.filter import (
    FilterConfig,
    GenericFilterConfig,
    QueryBuilderConfig,
    QueryBuilderFieldConfig,
    SearchBarConfig,
)
from insight_ui.configs.forms import FormConfig, FormFieldConfig
from insight_ui.configs.input import (
    ChatConfig,
    CheckboxConfig,
    CheckboxGroupConfig,
    CheckboxItemConfig,
    DropdownConfig,
    DropdownItemConfig,
    InputFieldConfig,
    MultiselectConfig,
    RadioBlockConfig,
    RadioGroupConfig,
    RadioItemConfig,
    SelectConfig,
    SliderConfig,
    TextareaConfig,
    ToggleConfig,
)
from insight_ui.configs.layout import ArticleConfig, BadgeConfig, HeadingDecorationConfig, HeroConfig, PageHeaderConfig
from insight_ui.configs.list import InfiniteScrollConfig, PaginationConfig, PaginationIppConfig, TableConfig
from insight_ui.configs.navigation import (
    AccordionConfig,
    AccordionItemConfig,
    BreadcrumbItemConfig,
    BreadcrumbsConfig,
    BulletPointItemConfig,
    BulletPointListConfig,
    FooterConfig,
    FooterContactConfig,
    FooterDescriptionConfig,
    MinimalStepBarConfig,
    NavbarBrandConfig,
    NavbarConfig,
    NavbarLinkConfig,
    SidebarCategoryConfig,
    SidebarConfig,
    SidebarDataConfig,
    SidebarItemConfig,
    StepBarConfig,
    StepBarItemConfig,
    TabConfig,
    TabsConfig,
)
from insight_ui.configs.popup import AlertConfig, ModalConfig
from insight_ui.configs.utils import (
    BrandLockupConfig,
    ChartConfig,
    ChartDatasetConfig,
    CopyrightNoticeConfig,
    CornerRibbonConfig,
    GeoMapConfig,
    GeoMapDatasetConfig,
    InfoboxConfig,
    LiveContentConfig,
    LogoConfig,
    WebSocketConfig,
)

__all__ = [
    # Base
    "ActionConfig",
    "HtmxConfig",
    "IconConfig",
    "ImageConfig",
    # Cards
    "AppCardConfig",
    "CardCarouselConfig",
    "CardConfig",
    "CarouselItemConfig",
    "FlipCardConfig",
    "ImageCarouselConfig",
    "ImageCarouselItemConfig",
    "ThreeDCarouselConfig",
    "ToggleViewConfig",
    # Filters
    "FilterConfig",
    "GenericFilterConfig",
    "QueryBuilderConfig",
    "QueryBuilderFieldConfig",
    "SearchBarConfig",
    # Forms
    "FormConfig",
    "FormFieldConfig",
    # Inputs
    "ChatConfig",
    "CheckboxConfig",
    "CheckboxGroupConfig",
    "CheckboxItemConfig",
    "DropdownConfig",
    "DropdownItemConfig",
    "InputFieldConfig",
    "MultiselectConfig",
    "RadioBlockConfig",
    "RadioGroupConfig",
    "RadioItemConfig",
    "SelectConfig",
    "SliderConfig",
    "TextareaConfig",
    "ToggleConfig",
    # Layout
    "ArticleConfig",
    "BadgeConfig",
    "HeadingDecorationConfig",
    "HeroConfig",
    "PageHeaderConfig",
    # Lists
    "InfiniteScrollConfig",
    "PaginationConfig",
    "PaginationIppConfig",
    "TableConfig",
    # Navigation
    "AccordionConfig",
    "AccordionItemConfig",
    "BreadcrumbItemConfig",
    "BreadcrumbsConfig",
    "BulletPointItemConfig",
    "BulletPointListConfig",
    "FooterConfig",
    "FooterContactConfig",
    "FooterDescriptionConfig",
    "MinimalStepBarConfig",
    "NavbarBrandConfig",
    "NavbarConfig",
    "NavbarLinkConfig",
    "SidebarCategoryConfig",
    "SidebarConfig",
    "SidebarDataConfig",
    "SidebarItemConfig",
    "StepBarConfig",
    "StepBarItemConfig",
    "TabConfig",
    "TabsConfig",
    # Popups
    "AlertConfig",
    "ModalConfig",
    # Utils
    "BrandLockupConfig",
    "ChartConfig",
    "ChartDatasetConfig",
    "CopyrightNoticeConfig",
    "CornerRibbonConfig",
    "GeoMapConfig",
    "GeoMapDatasetConfig",
    "InfoboxConfig",
    "LiveContentConfig",
    "LogoConfig",
    "WebSocketConfig",
]
