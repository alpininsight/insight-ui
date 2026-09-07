"""Component enumeration and configuration mapping."""

from enum import Enum
from pathlib import Path
from typing import Any

from django.utils.translation import gettext_lazy as _
from insight_ui.configs import (
    AccordionConfig,
    AlertConfig,
    AppCardConfig,
    ArticleConfig,
    BadgeConfig,
    BrandMarkConfig,
    BulletPointListConfig,
    ButtonConfig,
    CardCarouselConfig,
    CardConfig,
    ChartConfig,
    ChatConfig,
    CheckboxConfig,
    CheckboxGroupConfig,
    CornerRibbonConfig,
    DividerConfig,
    DropdownConfig,
    FlipCardConfig,
    FooterConfig,
    FormConfig,
    GenericFilterConfig,
    GeoMapConfig,
    GridConfig,
    HBoxConfig,
    HeroConfig,
    ImageCarouselConfig,
    InfiniteScrollConfig,
    InfoboxConfig,
    InputFieldConfig,
    LegalNoticeConfig,
    ListConfig,
    LiveContentConfig,
    LogoConfig,
    MinimalStepperConfig,
    ModalConfig,
    MultiselectConfig,
    NavbarConfig,
    PageConfig,
    PageHeaderConfig,
    PaginationConfig,
    ProgressBarConfig,
    QueryBuilderConfig,
    RadioBlockConfig,
    RadioGroupConfig,
    SearchBarConfig,
    SectionConfig,
    SelectConfig,
    SidebarConfig,
    SliderConfig,
    SpacerConfig,
    StatusScreenConfig,
    StepperConfig,
    SurfaceConfig,
    TableConfig,
    TabsConfig,
    TextareaConfig,
    ThreeDCarouselConfig,
    ToggleConfig,
    ToggleViewConfig,
    VBoxConfig,
    WebSocketConfig,
)


class ComponentCategory(Enum):
    """Enum of all available component categories."""

    LAYOUT = ("layout", _("Layout"))
    NAVIGATION = ("navigation", _("Navigation"))
    INPUT = ("input", _("Input"))
    POPUP = ("popup", _("Popup"))
    UTIL = ("util", _("Utilities"))
    LIST = ("list", _("Lists"))
    FILTER = ("filter", _("Filters"))
    CARD = ("card", _("Cards"))
    FORM = ("form", _("Forms"))

    def __new__(cls, value: str, formatted_name: str):  # noqa: ANN204
        """Create new ComponentCategory entry."""
        obj = object.__new__(cls)
        obj._value_ = value
        obj.formatted_name = formatted_name
        return obj


class Component(Enum):
    """Enum of all available components with an additional member called 'group' to categorize components."""

    # Layout Components
    PAGE_HEADER = ("page_header", ComponentCategory.LAYOUT, PageHeaderConfig)
    ARTICLE = ("article", ComponentCategory.LAYOUT, ArticleConfig)
    HERO = ("hero", ComponentCategory.LAYOUT, HeroConfig)
    STATUS_SCREEN = ("status_screen", ComponentCategory.LAYOUT, StatusScreenConfig)
    # Layout Block Tags (layout_tags.py)
    PAGE = ("page", ComponentCategory.LAYOUT, PageConfig)
    HBOX = ("hbox", ComponentCategory.LAYOUT, HBoxConfig)
    VBOX = ("vbox", ComponentCategory.LAYOUT, VBoxConfig)
    GRID = ("grid", ComponentCategory.LAYOUT, GridConfig)
    SPACER = ("spacer", ComponentCategory.LAYOUT, SpacerConfig)
    DIVIDER = ("divider", ComponentCategory.LAYOUT, DividerConfig)
    SECTION = ("section", ComponentCategory.LAYOUT, SectionConfig)
    SURFACE = ("surface", ComponentCategory.LAYOUT, SurfaceConfig)
    LIST = ("list", ComponentCategory.LAYOUT, ListConfig)
    # Navigation Components
    NAVBAR = ("navbar", ComponentCategory.NAVIGATION, NavbarConfig)
    SIDEBAR = ("sidebar", ComponentCategory.NAVIGATION, SidebarConfig)
    FOOTER = ("footer", ComponentCategory.NAVIGATION, FooterConfig)
    BREADCRUMBS = ("breadcrumbs", ComponentCategory.NAVIGATION)
    STEPPER = ("stepper", ComponentCategory.NAVIGATION, StepperConfig)
    MINIMAL_STEPPER = ("minimal_stepper", ComponentCategory.NAVIGATION, MinimalStepperConfig)
    BULLET_POINT_LIST = ("bullet_point_list", ComponentCategory.NAVIGATION, BulletPointListConfig)
    ACCORDION = ("accordion", ComponentCategory.NAVIGATION, AccordionConfig)
    TABS = ("tabs", ComponentCategory.NAVIGATION, TabsConfig)
    # Input Components
    BUTTON = ("button", ComponentCategory.INPUT, ButtonConfig)
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
    CHAT = ("chat", ComponentCategory.INPUT, ChatConfig)
    # Popup Components
    ALERT = ("alert", ComponentCategory.POPUP, AlertConfig)
    MODAL = ("modal", ComponentCategory.POPUP, ModalConfig)
    POPOVER = ("popover", ComponentCategory.POPUP)
    TOOLTIP = ("tooltip", ComponentCategory.POPUP)
    # Utility Components
    INFOBOX = ("infobox", ComponentCategory.UTIL, InfoboxConfig)
    CODE_BLOCK = ("code_block", ComponentCategory.UTIL)
    LEGAL_NOTICE = ("legal_notice", ComponentCategory.UTIL, LegalNoticeConfig)
    DIFFERENTIATOR = ("differentiator", ComponentCategory.UTIL)
    LOGO = ("logo", ComponentCategory.UTIL, LogoConfig)
    BRAND_MARK = ("brand_mark", ComponentCategory.UTIL, BrandMarkConfig)
    CORNER_RIBBON = ("corner_ribbon", ComponentCategory.UTIL, CornerRibbonConfig)
    PROGRESS_BAR = ("progress_bar", ComponentCategory.UTIL, ProgressBarConfig)
    GEO_MAP = ("geo_map", ComponentCategory.UTIL, GeoMapConfig)
    CHART = ("chart", ComponentCategory.UTIL, ChartConfig)
    LIVE_CONTENT = ("live_content", ComponentCategory.UTIL, LiveContentConfig)
    WEB_SOCKET = ("web_socket", ComponentCategory.UTIL, WebSocketConfig)
    BADGE = ("badge", ComponentCategory.UTIL, BadgeConfig)
    # List Components
    INFINITE_SCROLL = ("infinite_scroll", ComponentCategory.LIST, InfiniteScrollConfig)
    PAGINATION = ("pagination", ComponentCategory.LIST, PaginationConfig)
    TABLE = ("table", ComponentCategory.LIST, TableConfig)
    # Filter Components
    SEARCH_BAR = ("search_bar", ComponentCategory.FILTER, SearchBarConfig)
    GENERIC_FILTER = ("generic_filter", ComponentCategory.FILTER, GenericFilterConfig)
    QUERY_BUILDER = ("query_builder", ComponentCategory.FILTER, QueryBuilderConfig)
    # Card Components
    CARD = ("card", ComponentCategory.CARD, CardConfig)
    APP_CARD = ("app_card", ComponentCategory.CARD, AppCardConfig)
    FLIP_CARD = ("flip_card", ComponentCategory.CARD, FlipCardConfig)
    CARD_CAROUSEL = ("card_carousel", ComponentCategory.CARD, CardCarouselConfig)
    IMAGE_CAROUSEL = ("image_carousel", ComponentCategory.CARD, ImageCarouselConfig)
    THREE_D_CAROUSEL = ("3d_carousel", ComponentCategory.CARD, ThreeDCarouselConfig)
    TOGGLE_VIEW = ("toggle_view", ComponentCategory.CARD, ToggleViewConfig)
    # Form Components
    FORM = ("form", ComponentCategory.FORM, FormConfig)

    def __new__(  # noqa: ANN204
        cls,
        value: str,
        group: ComponentCategory,
        config_class: Any = None,  # noqa: ANN401
    ):
        """Create new Component entry where 'value' is the value.

        Args:
            value: The name of the component.
            group: The category of the component.
            config_class: Configuration Dataclass of the component.

        Returns:
            The newly created component object.

        """
        obj = object.__new__(cls)
        obj._value_ = value
        obj.formatted_name = value.replace("_", " ").title()
        obj.group = group
        obj.config_class = config_class
        return obj

    @property
    def no_padding(self) -> bool:
        """Check if this component's demo should touch the edge of the container."""
        return self in _NO_PADDING

    @property
    def allow_requests(self) -> bool:
        """Check if this component's demo is allowed to make server requests."""
        return self in _ALLOW_REQUESTS

    @property
    def in_development(self) -> bool:
        """Check if this component is still in development."""
        return self in _IN_DEVELOPMENT

    @property
    def requires_js(self) -> bool:
        """Check if this component has an associated JavaScript file."""
        js_name = self.value.replace("_", "-")
        js_path = Path(__file__).parent.parent / f"static/insight_ui/js/insight-ui-{js_name}.js"
        return js_path.exists()

    @property
    def external_dependency(self) -> str | None:
        """Return the name of an external library this component depends on, if any."""
        return _EXTERNAL_DEPENDENCIES.get(self)

    @property
    def is_new(self) -> bool:
        """Check if this component was recently added."""
        return self in _IS_NEW

    @property
    def is_block_tag(self) -> bool:
        """Check if this component is a block tag (requires closing tag)."""
        return self in _IS_BLOCK_TAG

    @property
    def uses_htmx(self) -> bool:
        """Check if this component uses HTMX for server interaction."""
        return self in _USES_HTMX


# =============================================================================
# Component metadata sets (defined after enum so we can use Component members)
# =============================================================================

# Remove padding around component, useful for layout components
_NO_PADDING: set[Component] = {
    Component.PAGE_HEADER,
    Component.PAGE,
    Component.NAVBAR,
    Component.SIDEBAR,
    Component.FOOTER,
}

# Allow the component to do requests in the demo
_ALLOW_REQUESTS: set[Component] = {
    Component.TABS,
    Component.CHAT,
    Component.LIVE_CONTENT,
    Component.WEB_SOCKET,
    Component.INFINITE_SCROLL,
    Component.PAGINATION,
    Component.QUERY_BUILDER,
    Component.THREE_D_CAROUSEL,
    Component.TOGGLE_VIEW,
}

# Shows a hint on the detail page and an icon in the left sidebar
_IN_DEVELOPMENT: set[Component] = {}

# Shows a badge on the detail page and in the left sidebar
_IS_NEW: set[Component] = {
    Component.FLIP_CARD,
    Component.SECTION,
    Component.SURFACE,
    Component.LIST,
}

# Shows a badge on the detail page
_IS_BLOCK_TAG: set[Component] = {
    Component.PAGE,
    Component.HBOX,
    Component.VBOX,
    Component.GRID,
    Component.SECTION,
    Component.SURFACE,
    Component.LIST,
    Component.SIDEBAR,
    Component.MODAL,
    Component.TABS,
}

# Shows a badge on the detail page
_USES_HTMX: set[Component] = {
    Component.NAVBAR,
    Component.BREADCRUMBS,
    Component.TABS,
    Component.BULLET_POINT_LIST,
    Component.BUTTON,
    Component.RADIO_BLOCK,
    Component.TOGGLE_VIEW,
    Component.DROPDOWN,
    Component.CHAT,
    Component.PAGINATION,
    Component.INFINITE_SCROLL,
    Component.SEARCH_BAR,
    Component.GENERIC_FILTER,
    Component.LIVE_CONTENT,
    Component.WEB_SOCKET,
    Component.FORM,
}

# Shows a badge on the detail page
_EXTERNAL_DEPENDENCIES: dict[Component, str] = {
    Component.CHART: "Chart.js",
    Component.GEO_MAP: "Leaflet",
}
