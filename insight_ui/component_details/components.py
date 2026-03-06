from enum import Enum


class Component(Enum):
    """Enum of all available components with an additional member called 'group' to categorize components."""

    PAGE_HEADER = ("page_header", "layout")
    ARTICLE = ("article", "layout")
    HERO = ("hero", "layout")
    NAVBAR = ("navbar", "navigation")
    SIDEBAR = ("sidebar", "navigation")
    FOOTER = ("footer", "navigation")
    BREADCRUMBS = ("breadcrumbs", "navigation")
    STEP_BAR = ("step_bar", "navigation")
    MINIMAL_STEP_BAR = ("minimal_Step_bar", "navigation")
    BULLET_POINT_LIST = ("bullet_point_list", "navigation")
    ACCORDION = ("accordion", "navigation")
    TABS = ("tabs", "navigation")
    BUTTON = ("button", "inputs")
    INPUT_FIELD = ("input_field", "inputs")
    CHECKBOX = ("checkbox", "inputs")
    CHECKBOX_GROUP = ("checkbox_group", "inputs")
    DROPDOWN = ("dropdown", "inputs")
    RADIO_GROUP = ("radio_group", "inputs")
    RADIO_BLOCK = ("radio_block", "inputs")
    RANGE_SLIDER = ("range_slider", "inputs")
    TOGGLE = ("toggle", "inputs")
    SELECT = ("select", "inputs")
    MULTISELECT = ("multiselect", "inputs")
    CHAT = ("chat", "inputs")
    ALERT = ("alert", "popups")
    MODAL = ("modal", "popups")
    POPOVER = ("popover", "popups")
    TOOLTIP = ("tooltip", "popups")
    CODE_BLOCK = ("code_block", "utils")
    DIFFERENTIATOR = ("differentiator", "utils")
    PROGRESS_BAR = ("progress_bar", "utils")
    GEO_MAP = ("geo_map", "utils")
    CHART = ("chart", "utils")
    LIVE_CONTENT = ("live_content", "utils")
    WEB_SOCKET = ("web_socket", "utils")
    INFINITE_SCROLL = ("infinite_scroll", "lists")
    PAGINATION = ("pagination", "lists")
    TABLE = ("table", "lists")
    GENERIC_FILTER = ("generic_filter", "filters")
    SEARCH_BAR = ("search_bar", "filters")
    QUERY_BUILDER = ("query_builder", "filters")
    CARD = ("card", "cards")
    CARD_CAROUSEL = ("card_carousel", "cards")
    IMAGE_CAROUSEL = ("image_carousel", "cards")
    THREE_D_CAROUSEL = ("3d_carousel", "cards")
    TOGGLE_VIEW = ("toggle_view", "cards")
    FORM = ("form", "forms")

    def __new__(cls, value: str, group: str):  # noqa: ANN204
        """Create new Component entry where 'value' is the value and 'group' is an additional member called group."""
        obj = object.__new__(cls)
        obj._value_ = value
        obj.group = group
        return obj
