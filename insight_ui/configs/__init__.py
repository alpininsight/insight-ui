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
    FlipCardConfig,
    ImageCarouselConfig,
    ImageCarouselItemConfig,
    ThreeDCarouselConfig,
    ToggleViewConfig,
)
from insight_ui.configs.filter import FilterConfig, GenericFilterConfig, QueryBuilderFieldConfig, SearchBarConfig
from insight_ui.configs.forms import FormConfig, FormFieldConfig
from insight_ui.configs.input import (
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
from insight_ui.configs.layout import ArticleConfig, HeadingDecorationConfig, HeroConfig, PageHeaderConfig
from insight_ui.configs.list import InfiniteScrollConfig, PaginationIppConfig, TableConfig
from insight_ui.configs.navigation import (
    AccordionConfig,
    AccordionItemConfig,
    BreadcrumbItemConfig,
    BulletPointItemConfig,
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
    StepBarItemConfig,
    TabConfig,
    TabsConfig,
)
from insight_ui.configs.popup import AlertConfig, ModalConfig
from insight_ui.configs.utils import (
    ChartConfig,
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
    # Controls
    "CheckboxConfig",
    "CheckboxGroupConfig",
    "CheckboxItemConfig",
    "DropdownConfig",
    "DropdownItemConfig",
    "MultiselectConfig",
    "RadioBlockConfig",
    "RadioGroupConfig",
    "RadioItemConfig",
    "SelectConfig",
    "SliderConfig",
    "ToggleConfig",
    # Forms
    "FormConfig",
    "FormFieldConfig",
    "InputFieldConfig",
    "TextareaConfig",
    # Layout
    "AccordionConfig",
    "AccordionItemConfig",
    "AlertConfig",
    "AppCardConfig",
    "CardConfig",
    "CornerRibbonConfig",
    "FlipCardConfig",
    "InfoboxConfig",
    "ModalConfig",
    "TabConfig",
    "TabsConfig",
    "TableConfig",
    # Navigation
    "BreadcrumbItemConfig",
    "CopyrightNoticeConfig",
    "FooterConfig",
    "FooterContactConfig",
    "FooterDescriptionConfig",
    "LogoConfig",
    "NavbarBrandConfig",
    "NavbarConfig",
    "NavbarLinkConfig",
    "SidebarCategoryConfig",
    "SidebarConfig",
    "SidebarItemConfig",
    "SidebarDataConfig",
    # Content
    "ArticleConfig",
    "HeadingDecorationConfig",
    "HeroConfig",
    "PageHeaderConfig",
    # Data
    "FilterConfig",
    "GenericFilterConfig",
    "InfiniteScrollConfig",
    "LiveContentConfig",
    "PaginationIppConfig",
    "QueryBuilderFieldConfig",
    "SearchBarConfig",
    "ToggleViewConfig",
    "WebSocketConfig",
    # Media
    "CardCarouselConfig",
    "ChartConfig",
    "GeoMapConfig",
    "GeoMapDatasetConfig",
    "ImageCarouselConfig",
    "ImageCarouselItemConfig",
    "ThreeDCarouselConfig",
    # Progress
    "BulletPointItemConfig",
    "MinimalStepBarConfig",
    "StepBarItemConfig",
]
