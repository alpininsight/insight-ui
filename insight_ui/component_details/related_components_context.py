"""Related component mappings for cross-referencing documentation."""

from insight_ui.component_details.components import Component as C  # noqa: N817

RELATED_COMPONENTS = {
    # Layout
    C.PAGE_HEADER: [C.PAGE, C.HERO],
    C.ARTICLE: [],
    C.HERO: [C.PAGE, C.PAGE_HEADER, C.BADGE, C.BUTTON],
    C.STATUS_SCREEN: [C.BRAND_MARK, C.INFOBOX, C.CARD, C.BUTTON],
    C.PAGE: [C.VBOX, C.GRID, C.HERO, C.PAGE_HEADER],
    C.HBOX: [C.VBOX, C.GRID, C.SPACER],
    C.VBOX: [C.HBOX, C.GRID, C.PAGE, C.DIVIDER],
    C.GRID: [C.HBOX, C.VBOX, C.PAGE],
    C.SPACER: [C.DIVIDER, C.HBOX, C.VBOX],
    C.DIVIDER: [C.SPACER, C.HBOX, C.VBOX],
    # Navigation
    C.NAVBAR: [C.FOOTER, C.SIDEBAR, C.LOGO, C.BRAND_MARK],
    C.SIDEBAR: [C.NAVBAR, C.FOOTER, C.MODAL],
    C.FOOTER: [C.NAVBAR, C.SIDEBAR, C.LOGO, C.BRAND_MARK, C.COPYRIGHT_NOTICE],
    C.BREADCRUMBS: [],
    C.STEPPER: [C.MINIMAL_STEPPER, C.BULLET_POINT_LIST],
    C.MINIMAL_STEPPER: [C.STEPPER],
    C.BULLET_POINT_LIST: [],
    C.ACCORDION: [C.TABS],
    C.TABS: [C.ACCORDION],
    # Inputs
    C.BUTTON: [C.INPUT_FIELD, C.RADIO_GROUP, C.TOGGLE, C.CHECKBOX, C.BADGE],
    C.INPUT_FIELD: [C.TEXTAREA, C.CHECKBOX, C.CHECKBOX_GROUP, C.RADIO_GROUP, C.BUTTON, C.TOGGLE],
    C.TEXTAREA: [C.INPUT_FIELD],
    C.CHECKBOX: [C.CHECKBOX_GROUP, C.RADIO_GROUP, C.BUTTON, C.TOGGLE, C.INPUT_FIELD],
    C.CHECKBOX_GROUP: [C.CHECKBOX, C.RADIO_GROUP, C.BUTTON, C.TOGGLE, C.INPUT_FIELD],
    C.DROPDOWN: [],
    C.RADIO_GROUP: [C.CHECKBOX_GROUP, C.BUTTON, C.TOGGLE, C.INPUT_FIELD],
    C.RADIO_BLOCK: [C.CHECKBOX_GROUP, C.BUTTON, C.TOGGLE, C.INPUT_FIELD],
    C.RANGE_SLIDER: [C.INPUT_FIELD],
    C.TOGGLE: [C.CHECKBOX, C.BUTTON],
    C.SELECT: [C.MULTISELECT, C.GENERIC_FILTER, C.QUERY_BUILDER],
    C.MULTISELECT: [C.SELECT, C.GENERIC_FILTER, C.QUERY_BUILDER],
    C.CHAT: [C.SEARCH_BAR],
    # Popups
    C.ALERT: [C.INFOBOX],
    C.MODAL: [C.POPOVER],
    C.POPOVER: [C.MODAL, C.TOOLTIP],
    C.TOOLTIP: [C.POPOVER],
    # Utils
    C.INFOBOX: [C.ALERT],
    C.CODE_BLOCK: [],
    C.COPYRIGHT_NOTICE: [C.FOOTER],
    C.DIFFERENTIATOR: [],
    C.LOGO: [C.NAVBAR, C.FOOTER, C.BRAND_MARK],
    C.BRAND_MARK: [C.NAVBAR, C.LOGO, C.FOOTER, C.STATUS_SCREEN],
    C.CORNER_RIBBON: [],
    C.PROGRESS_BAR: [C.STEPPER],
    C.GEO_MAP: [],
    C.CHART: [],
    C.LIVE_CONTENT: [C.WEB_SOCKET],
    C.WEB_SOCKET: [C.LIVE_CONTENT],
    C.BADGE: [C.BUTTON, C.HERO],
    # Lists
    C.INFINITE_SCROLL: [C.PAGINATION],
    C.PAGINATION: [C.INFINITE_SCROLL],
    C.TABLE: [C.PAGINATION, C.TOGGLE_VIEW],
    # Filters
    C.SEARCH_BAR: [C.CHAT, C.SELECT, C.MULTISELECT],
    C.GENERIC_FILTER: [C.QUERY_BUILDER, C.SELECT, C.MULTISELECT],
    C.QUERY_BUILDER: [C.GENERIC_FILTER, C.SELECT, C.MULTISELECT],
    # Cards
    C.CARD: [C.APP_CARD, C.FLIP_CARD, C.CARD_CAROUSEL, C.TOGGLE_VIEW],
    C.APP_CARD: [C.CARD, C.FLIP_CARD, C.CARD_CAROUSEL, C.TOGGLE_VIEW],
    C.FLIP_CARD: [C.CARD, C.APP_CARD, C.CARD_CAROUSEL, C.TOGGLE_VIEW],
    C.CARD_CAROUSEL: [C.IMAGE_CAROUSEL, C.THREE_D_CAROUSEL],
    C.IMAGE_CAROUSEL: [C.CARD_CAROUSEL, C.THREE_D_CAROUSEL],
    C.THREE_D_CAROUSEL: [C.CARD_CAROUSEL, C.IMAGE_CAROUSEL],
    C.TOGGLE_VIEW: [C.TABLE, C.PAGINATION, C.CARD_CAROUSEL],
    # Forms
    C.FORM: [C.ALERT],
}


def get_related_components_context(component: C) -> list[dict[str, str]]:
    """Build context data for related component links.

    Looks up the component in ``RELATED_COMPONENTS`` and returns
    metadata for rendering cross-reference links in documentation.

    Args:
        component: The Component enum member to get related components for.

    Returns:
        A list of dictionaries, each containing ``component_name`` (the
        enum value) and ``formatted_name`` (human-readable display name).

    """
    return [
        {"component_name": related_component.value, "formatted_name": related_component.formatted_name}
        for related_component in RELATED_COMPONENTS[component]
    ]
