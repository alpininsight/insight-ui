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

    PAGE_HEADER = ("page_header", ComponentCategory.LAYOUT, True, False, False)
    HEADING_DECORATION = ("heading_decoration", ComponentCategory.LAYOUT, False, False, True)
    ARTICLE = ("article", ComponentCategory.LAYOUT)
    HERO = ("hero", ComponentCategory.LAYOUT)
    NAVBAR = ("navbar", ComponentCategory.NAVIGATION, True, False, False)
    SIDEBAR = ("sidebar", ComponentCategory.NAVIGATION, True, False, False)
    FOOTER = ("footer", ComponentCategory.NAVIGATION, True, False, False)
    BREADCRUMBS = ("breadcrumbs", ComponentCategory.NAVIGATION)
    STEP_BAR = ("step_bar", ComponentCategory.NAVIGATION)
    MINIMAL_STEP_BAR = ("minimal_step_bar", ComponentCategory.NAVIGATION)
    BULLET_POINT_LIST = ("bullet_point_list", ComponentCategory.NAVIGATION)
    ACCORDION = ("accordion", ComponentCategory.NAVIGATION)
    TABS = ("tabs", ComponentCategory.NAVIGATION, False, True, False)
    BUTTON = ("button", ComponentCategory.INPUT)
    INPUT_FIELD = ("input_field", ComponentCategory.INPUT)
    TEXTAREA = ("textarea", ComponentCategory.INPUT)
    CHECKBOX = ("checkbox", ComponentCategory.INPUT)
    CHECKBOX_GROUP = ("checkbox_group", ComponentCategory.INPUT)
    DROPDOWN = ("dropdown", ComponentCategory.INPUT)
    RADIO_GROUP = ("radio_group", ComponentCategory.INPUT)
    RADIO_BLOCK = ("radio_block", ComponentCategory.INPUT)
    RANGE_SLIDER = ("range_slider", ComponentCategory.INPUT)
    TOGGLE = ("toggle", ComponentCategory.INPUT)
    SELECT = ("select", ComponentCategory.INPUT)
    MULTISELECT = ("multiselect", ComponentCategory.INPUT)
    CHAT = ("chat", ComponentCategory.INPUT, False, True, False)
    ALERT = ("alert", ComponentCategory.POPUP)
    MODAL = ("modal", ComponentCategory.POPUP)
    POPOVER = ("popover", ComponentCategory.POPUP)
    TOOLTIP = ("tooltip", ComponentCategory.POPUP)
    INFOBOX = ("infobox", ComponentCategory.UTIL)
    CODE_BLOCK = ("code_block", ComponentCategory.UTIL)
    COPYRIGHT_NOTICE = ("copyright_notice", ComponentCategory.UTIL)
    DIFFERENTIATOR = ("differentiator", ComponentCategory.UTIL)
    LOGO = ("logo", ComponentCategory.UTIL)
    CORNER_RIBBON = ("corner_ribbon", ComponentCategory.UTIL)
    PROGRESS_BAR = ("progress_bar", ComponentCategory.UTIL, False, False, True)
    GEO_MAP = ("geo_map", ComponentCategory.UTIL)
    CHART = ("chart", ComponentCategory.UTIL)
    LIVE_CONTENT = ("live_content", ComponentCategory.UTIL, False, True, False)
    WEB_SOCKET = ("web_socket", ComponentCategory.UTIL, False, True, True)
    INFINITE_SCROLL = ("infinite_scroll", ComponentCategory.LIST, False, True, False)
    PAGINATION = ("pagination", ComponentCategory.LIST, False, True, False)
    TABLE = ("table", ComponentCategory.LIST)
    GENERIC_FILTER = ("generic_filter", ComponentCategory.FILTER)
    SEARCH_BAR = ("search_bar", ComponentCategory.FILTER)
    QUERY_BUILDER = ("query_builder", ComponentCategory.FILTER, False, True, False)
    CARD = ("card", ComponentCategory.CARD)
    APP_CARD = ("app_card", ComponentCategory.CARD)
    FLIP_CARD = ("flip_card", ComponentCategory.CARD)
    CARD_CAROUSEL = ("card_carousel", ComponentCategory.CARD)
    IMAGE_CAROUSEL = ("image_carousel", ComponentCategory.CARD)
    THREE_D_CAROUSEL = ("3d_carousel", ComponentCategory.CARD, False, True, False)
    TOGGLE_VIEW = ("toggle_view", ComponentCategory.CARD, False, True, False)
    FORM = ("form", ComponentCategory.FORM)

    def __new__(  # noqa: ANN204
        cls,
        value: str,
        group: ComponentCategory,
        no_padding: bool = False,
        allow_requests: bool = False,
        in_development: bool = False,
    ):
        """
        Create new Component entry where 'value' is the value.

        Arguments:
            value (str): The name of the component.
            group (ComponentCategory): The category of the component.
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
        obj.no_padding = no_padding
        obj.allow_requests = allow_requests
        obj.in_development = in_development
        return obj
