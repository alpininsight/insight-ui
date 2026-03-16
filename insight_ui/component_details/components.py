from enum import Enum


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

    PAGE_HEADER = ("page_header", ComponentCategory.LAYOUT)
    ARTICLE = ("article", ComponentCategory.LAYOUT)
    HERO = ("hero", ComponentCategory.LAYOUT)
    NAVBAR = ("navbar", ComponentCategory.NAVIGATION)
    SIDEBAR = ("sidebar", ComponentCategory.NAVIGATION)
    FOOTER = ("footer", ComponentCategory.NAVIGATION)
    BREADCRUMBS = ("breadcrumbs", ComponentCategory.NAVIGATION)
    STEP_BAR = ("step_bar", ComponentCategory.NAVIGATION)
    MINIMAL_STEP_BAR = ("minimal_step_bar", ComponentCategory.NAVIGATION)
    BULLET_POINT_LIST = ("bullet_point_list", ComponentCategory.NAVIGATION)
    ACCORDION = ("accordion", ComponentCategory.NAVIGATION)
    TABS = ("tabs", ComponentCategory.NAVIGATION)
    BUTTON = ("button", ComponentCategory.INPUT)
    INPUT_FIELD = ("input_field", ComponentCategory.INPUT)
    CHECKBOX = ("checkbox", ComponentCategory.INPUT)
    CHECKBOX_GROUP = ("checkbox_group", ComponentCategory.INPUT)
    DROPDOWN = ("dropdown", ComponentCategory.INPUT)
    RADIO_GROUP = ("radio_group", ComponentCategory.INPUT)
    RADIO_BLOCK = ("radio_block", ComponentCategory.INPUT)
    RANGE_SLIDER = ("range_slider", ComponentCategory.INPUT)
    TOGGLE = ("toggle", ComponentCategory.INPUT)
    SELECT = ("select", ComponentCategory.INPUT)
    MULTISELECT = ("multiselect", ComponentCategory.INPUT)
    CHAT = ("chat", ComponentCategory.INPUT)
    ALERT = ("alert", ComponentCategory.POPUP)
    MODAL = ("modal", ComponentCategory.POPUP)
    POPOVER = ("popover", ComponentCategory.POPUP)
    TOOLTIP = ("tooltip", ComponentCategory.POPUP)
    CODE_BLOCK = ("code_block", ComponentCategory.UTIL)
    DIFFERENTIATOR = ("differentiator", ComponentCategory.UTIL)
    PROGRESS_BAR = ("progress_bar", ComponentCategory.UTIL)
    GEO_MAP = ("geo_map", ComponentCategory.UTIL)
    CHART = ("chart", ComponentCategory.UTIL)
    LIVE_CONTENT = ("live_content", ComponentCategory.UTIL)
    WEB_SOCKET = ("web_socket", ComponentCategory.UTIL)
    INFINITE_SCROLL = ("infinite_scroll", ComponentCategory.LIST)
    PAGINATION = ("pagination", ComponentCategory.LIST)
    TABLE = ("table", ComponentCategory.LIST)
    GENERIC_FILTER = ("generic_filter", ComponentCategory.FILTER)
    SEARCH_BAR = ("search_bar", ComponentCategory.FILTER)
    QUERY_BUILDER = ("query_builder", ComponentCategory.FILTER)
    CARD = ("card", ComponentCategory.CARD)
    CARD_CAROUSEL = ("card_carousel", ComponentCategory.CARD)
    IMAGE_CAROUSEL = ("image_carousel", ComponentCategory.CARD)
    THREE_D_CAROUSEL = ("3d_carousel", ComponentCategory.CARD)
    TOGGLE_VIEW = ("toggle_view", ComponentCategory.CARD)
    FORM = ("form", ComponentCategory.FORM)

    def __new__(cls, value: str, group: ComponentCategory):  # noqa: ANN204
        """Create new Component entry where 'value' is the value and 'group' is an additional member called group."""
        obj = object.__new__(cls)
        obj._value_ = value
        obj.formatted_name = value.replace("_", " ").title()
        obj.group = group
        return obj
