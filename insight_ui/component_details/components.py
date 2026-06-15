from enum import Enum
from typing import Any

from insight_ui.configs import (
    AccordionConfig,
    AlertConfig,
    AppCardConfig,
    ArticleConfig,
    BrandLockupConfig,
    BulletPointListConfig,
    CardCarouselConfig,
    CardConfig,
    ChartConfig,
    ChatConfig,
    CheckboxConfig,
    CheckboxGroupConfig,
    CopyrightNoticeConfig,
    CornerRibbonConfig,
    DropdownConfig,
    FlipCardConfig,
    FooterConfig,
    FormConfig,
    GenericFilterConfig,
    GeoMapConfig,
    HeroConfig,
    ImageCarouselConfig,
    InfiniteScrollConfig,
    InfoboxConfig,
    InputFieldConfig,
    LiveContentConfig,
    LogoConfig,
    MinimalStepBarConfig,
    ModalConfig,
    MultiselectConfig,
    NavbarConfig,
    PageHeaderConfig,
    PaginationConfig,
    QueryBuilderConfig,
    RadioBlockConfig,
    RadioGroupConfig,
    SearchBarConfig,
    SelectConfig,
    SidebarConfig,
    SliderConfig,
    StepBarConfig,
    TableConfig,
    TabsConfig,
    TextareaConfig,
    ThreeDCarouselConfig,
    ToggleConfig,
    ToggleViewConfig,
    WebSocketConfig,
)


class ComponentCategory(Enum):
    """Enum of all available component categories."""

    LAYOUT = "layout"
    NAVIGATION = "navigation"
    INPUT = "input"
    POPUP = "popup"
    UTIL = "util"
    LIST = "list"
    FILTER = "filter"
    CARD = "card"
    FORM = "form"

    def __new__(cls, value: str):  # noqa: ANN204
        """Create new ComponentCategory entry."""
        obj = object.__new__(cls)
        obj._value_ = value
        obj.formatted_name = value.replace("_", " ").title()
        return obj


class Component(Enum):
    """Enum of all available components with an additional member called 'group' to categorize components."""

    PAGE_HEADER = ("page_header", ComponentCategory.LAYOUT, PageHeaderConfig, True, False, False)
    HEADING_DECORATION = ("heading_decoration", ComponentCategory.LAYOUT, None, False, False, True)
    ARTICLE = ("article", ComponentCategory.LAYOUT, ArticleConfig)
    HERO = ("hero", ComponentCategory.LAYOUT, HeroConfig, False, False, False)
    NAVBAR = ("navbar", ComponentCategory.NAVIGATION, NavbarConfig, True, False, False)
    SIDEBAR = ("sidebar", ComponentCategory.NAVIGATION, SidebarConfig, True, False, False)
    FOOTER = ("footer", ComponentCategory.NAVIGATION, FooterConfig, True, False, False)
    BREADCRUMBS = ("breadcrumbs", ComponentCategory.NAVIGATION)
    STEP_BAR = ("step_bar", ComponentCategory.NAVIGATION, StepBarConfig)
    MINIMAL_STEP_BAR = ("minimal_step_bar", ComponentCategory.NAVIGATION, MinimalStepBarConfig)
    BULLET_POINT_LIST = ("bullet_point_list", ComponentCategory.NAVIGATION, BulletPointListConfig)
    ACCORDION = ("accordion", ComponentCategory.NAVIGATION, AccordionConfig)
    TABS = ("tabs", ComponentCategory.NAVIGATION, TabsConfig, False, True, False)
    BUTTON = ("button", ComponentCategory.INPUT, None, False, False, True)
    INPUT_FIELD = ("input_field", ComponentCategory.INPUT, InputFieldConfig)
    TEXTAREA = ("textarea", ComponentCategory.INPUT, TextareaConfig)
    CHECKBOX = ("checkbox", ComponentCategory.INPUT, CheckboxConfig)
    CHECKBOX_GROUP = ("checkbox_group", ComponentCategory.INPUT, CheckboxGroupConfig)
    DROPDOWN = ("dropdown", ComponentCategory.INPUT, DropdownConfig)
    RADIO_GROUP = ("radio_group", ComponentCategory.INPUT, RadioGroupConfig)
    RADIO_BLOCK = ("radio_block", ComponentCategory.INPUT, RadioBlockConfig)
    RANGE_SLIDER = ("range_slider", ComponentCategory.INPUT, SliderConfig)
    TOGGLE = ("toggle", ComponentCategory.INPUT, ToggleConfig)
    SELECT = ("select", ComponentCategory.INPUT, SelectConfig)
    MULTISELECT = ("multiselect", ComponentCategory.INPUT, MultiselectConfig)
    CHAT = ("chat", ComponentCategory.INPUT, ChatConfig, False, True, False)
    ALERT = ("alert", ComponentCategory.POPUP, AlertConfig)
    MODAL = ("modal", ComponentCategory.POPUP, ModalConfig)
    POPOVER = ("popover", ComponentCategory.POPUP)
    TOOLTIP = ("tooltip", ComponentCategory.POPUP)
    INFOBOX = ("infobox", ComponentCategory.UTIL, InfoboxConfig)
    CODE_BLOCK = ("code_block", ComponentCategory.UTIL)
    COPYRIGHT_NOTICE = ("copyright_notice", ComponentCategory.UTIL, CopyrightNoticeConfig)
    DIFFERENTIATOR = ("differentiator", ComponentCategory.UTIL)
    LOGO = ("logo", ComponentCategory.UTIL, LogoConfig)
    BRAND_LOCKUP = ("brand_lockup", ComponentCategory.UTIL, BrandLockupConfig)
    CORNER_RIBBON = ("corner_ribbon", ComponentCategory.UTIL, CornerRibbonConfig)
    PROGRESS_BAR = ("progress_bar", ComponentCategory.UTIL, None, False, False, True)
    GEO_MAP = ("geo_map", ComponentCategory.UTIL, GeoMapConfig)
    CHART = ("chart", ComponentCategory.UTIL, ChartConfig)
    LIVE_CONTENT = ("live_content", ComponentCategory.UTIL, LiveContentConfig, False, True, False)
    WEB_SOCKET = ("web_socket", ComponentCategory.UTIL, WebSocketConfig, False, True, True)
    INFINITE_SCROLL = ("infinite_scroll", ComponentCategory.LIST, InfiniteScrollConfig, False, True, False)
    PAGINATION = ("pagination", ComponentCategory.LIST, PaginationConfig, False, True, False)
    TABLE = ("table", ComponentCategory.LIST, TableConfig)
    SEARCH_BAR = ("search_bar", ComponentCategory.FILTER, SearchBarConfig)
    GENERIC_FILTER = ("generic_filter", ComponentCategory.FILTER, GenericFilterConfig)
    QUERY_BUILDER = ("query_builder", ComponentCategory.FILTER, QueryBuilderConfig, False, True, False)
    CARD = ("card", ComponentCategory.CARD, CardConfig)
    APP_CARD = ("app_card", ComponentCategory.CARD, AppCardConfig)
    FLIP_CARD = ("flip_card", ComponentCategory.CARD, FlipCardConfig)
    CARD_CAROUSEL = ("card_carousel", ComponentCategory.CARD, CardCarouselConfig)
    IMAGE_CAROUSEL = ("image_carousel", ComponentCategory.CARD, ImageCarouselConfig)
    THREE_D_CAROUSEL = ("3d_carousel", ComponentCategory.CARD, ThreeDCarouselConfig, False, True, False)
    TOGGLE_VIEW = ("toggle_view", ComponentCategory.CARD, ToggleViewConfig, False, True, False)
    FORM = ("form", ComponentCategory.FORM, FormConfig)

    def __new__(  # noqa: ANN204, PLR0913
        cls,
        value: str,
        group: ComponentCategory,
        config_class: Any = None,  # noqa: ANN401
        no_padding: bool = False,
        allow_requests: bool = False,
        in_development: bool = False,
    ):
        """
        Create new Component entry where 'value' is the value.

        Arguments:
            value (str): The name of the component.
            group (ComponentCategory): The category of the component.
            config_class (Any): Configuration Dataclass of the component.
            no_padding (bool): 'True' if the component have to touch the edge of the demo container (just for demonstration).
            allow_requests (bool): 'True' if the component is allowed to do requests in the demo (just for demonstration).
            in_development (bool): 'True' if the component is not finished yet (shows a hint on the detailpage and in the nav-list).

        Returns:
            component: The newly created component object.

        """
        obj = object.__new__(cls)
        obj._value_ = value
        obj.formatted_name = value.replace("_", " ").title()
        obj.group = group
        obj.config_class = config_class
        obj.no_padding = no_padding
        obj.allow_requests = allow_requests
        obj.in_development = in_development
        return obj
