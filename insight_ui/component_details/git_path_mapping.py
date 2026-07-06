"""GitHub URL mappings for component source files."""

# Base paths
GIT_BASE_FILE = "https://github.com/alpininsight/insight-ui/blob/develop/insight_ui/templates/insight_ui/components/"
GIT_BASE_DIR = "https://github.com/alpininsight/insight-ui/tree/develop/insight_ui/templates/insight_ui/components/"
GIT_BASE_SCRIPT_FILE = "https://github.com/alpininsight/insight-ui/blob/develop/insight_ui/static/insight_ui/js/"

# Mapping-Table between components and their respective template files
TEMPLATE_PATHS = {
    # Layout
    "page_header": GIT_BASE_FILE + "page_header.html",
    "article": GIT_BASE_FILE + "article.html",
    "hero": GIT_BASE_FILE + "hero.html",
    # Navigation
    "navbar": GIT_BASE_FILE + "navbar.html",
    "sidebar": GIT_BASE_FILE + "sidebar.html",
    "footer": GIT_BASE_FILE + "footer.html",
    "breadcrumbs": GIT_BASE_FILE + "breadcrumbs.html",
    "stepper": GIT_BASE_FILE + "stepper.html",
    "minimal_stepper": GIT_BASE_FILE + "minimal_stepper.html",
    "bullet_point_list": GIT_BASE_FILE + "bullet_point_list.html",
    "accordion": GIT_BASE_FILE + "accordion.html",
    "tabs": GIT_BASE_FILE + "tabs.html",
    # Inputs
    "button": GIT_BASE_FILE + "button.html",
    "input": GIT_BASE_FILE + "input.html",
    "textarea": GIT_BASE_FILE + "textarea.html",
    "checkbox": GIT_BASE_FILE + "checkbox.html",
    "checkbox_group": GIT_BASE_FILE + "checkbox_group.html",
    "dropdown": GIT_BASE_FILE + "dropdown.html",
    "radio_group": GIT_BASE_FILE + "radio_group.html",
    "radio_block": GIT_BASE_FILE + "radio_block.html",
    "range_slider": GIT_BASE_FILE + "range_slider.html",
    "toggle": GIT_BASE_FILE + "toggle_button.html",
    "select": GIT_BASE_FILE + "select.html",
    "multiselect": GIT_BASE_FILE + "multiselect.html",
    "chat": GIT_BASE_FILE + "chat.html",
    # Popups
    "alert": GIT_BASE_FILE + "alert.html",
    "modal": GIT_BASE_FILE + "modal.html",
    "tooltip": GIT_BASE_FILE + "tooltip.html",
    # Utils
    "infobox": GIT_BASE_FILE + "infobox.html",
    "copyright_notice": GIT_BASE_FILE + "copyright_notice.html",
    "logo": GIT_BASE_FILE + "logo.html",
    "brand_lockup": GIT_BASE_FILE + "brand_lockup.html",
    "corner_ribbon": GIT_BASE_FILE + "corner_ribbon.html",
    "progress_bar": GIT_BASE_FILE + "progress_bar.html",
    "geo_map": GIT_BASE_FILE + "geo_map.html",
    "bar_chart": GIT_BASE_FILE + "charts/bar_chart.html",
    "line_chart": GIT_BASE_FILE + "charts/line_chart.html",
    "live_content": GIT_BASE_FILE + "live_content.html",
    "web_socket": GIT_BASE_FILE + "websocket.html",
    "badge": GIT_BASE_FILE + "badge.html",
    # Lists
    "infinite_scroll": GIT_BASE_FILE + "infinite_scroll.html",
    "pagination": GIT_BASE_FILE + "pagination.html",
    "table": GIT_BASE_FILE + "table.html",
    # Filters
    "search_bar": GIT_BASE_FILE + "search_bar.html",
    "generic_filter": GIT_BASE_FILE + "generic_filter.html",
    "query_builder": GIT_BASE_DIR + "search_query_builder",
    # Cards
    "card": GIT_BASE_FILE + "cards/card.html",
    "app_card": GIT_BASE_FILE + "cards/app_card.html",
    "flip_card": GIT_BASE_FILE + "cards/flip_card.html",
    "carousel": GIT_BASE_FILE + "carousel.html",
    "card_carousel": GIT_BASE_FILE + "carousels/card_carousel.html",
    "image_carousel": GIT_BASE_FILE + "carousels/image_carousel.html",
    "3D_carousel": GIT_BASE_FILE + "carousels/3D_carousel.html",
    "toggle_view": GIT_BASE_FILE + "toggle_view.html",
    # Forms
    "form": GIT_BASE_FILE + "form.html",
}

# Mapping-Table between components and their respective script files
SCRIPT_PATHS = {
    # Layout
    # Navigation
    "sidebar": GIT_BASE_SCRIPT_FILE + "insight-ui-sidebar.js",
    "accordion": GIT_BASE_SCRIPT_FILE + "insight-ui-accordion.js",
    "tabs": GIT_BASE_SCRIPT_FILE + "insight-ui-tabs.js",
    # Inputs
    "checkbox_group": GIT_BASE_SCRIPT_FILE + "insight-ui-checkbox.js",
    "dropdown": GIT_BASE_SCRIPT_FILE + "insight-ui-dropdown.js",
    "multiselect": GIT_BASE_SCRIPT_FILE + "insight-ui-multiselect.js",
    # Popups
    "modal": GIT_BASE_SCRIPT_FILE + "insight-ui-modal.js",
    "popover": GIT_BASE_SCRIPT_FILE + "insight-ui-floater.js",
    "tooltip": GIT_BASE_SCRIPT_FILE + "insight-ui-floater.js",
    # Utils
    "code_block": GIT_BASE_SCRIPT_FILE + "insight-ui-code_block.js",
    "websocket": GIT_BASE_SCRIPT_FILE + "insight-ui-websocket.js",
    # Lists
    # Filters
    # Cards
    "carousel": GIT_BASE_SCRIPT_FILE + "insight-ui-carousel.js",
    "3D_carousel": GIT_BASE_SCRIPT_FILE + "insight-ui-3D-carousel.js",
    # Forms
}
