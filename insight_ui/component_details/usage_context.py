from insight_ui.component_details.component_context import register_component
from insight_ui.component_details.components import Component


@register_component(Component.PAGE_HEADER)
def get_page_header_usage_context() -> dict[str, str]:
    """Serve usage documentation for the page header component."""
    return {
        "usage": """
        {% block heading %}
        {% page_header title="Base Template" description="Beschreibung der Seite." %}
        {% endblock heading %}
        """
    }


@register_component(Component.ARTICLE)
def get_article_usage_context() -> dict[str, str]:
    """Serve usage documentation for the article component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% article title="Aktuelles" columns=3 content="<p>Erster Absatz...</p><p>Zweiter Absatz...</p>" %}
        """
    }


@register_component(Component.HERO)
def get_hero_usage_context() -> dict[str, str]:
    """Serve usage documentation for the hero component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% hero title="Insight UI" subtitle="A Django Component Framework" description="A modern UI library." cta_primary=cta_primary badge=badge %}
        """
    }


@register_component(Component.NAVBAR)
def get_navbar_usage_context() -> dict[str, str]:
    """Serve usage documentation for the navbar component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% block navbar %}
            {% navbar config=nav_config user=user user_dropdown_links=user_dropdown_links show_login=True %}
        {% endblock navbar %}
        """
    }


@register_component(Component.SIDEBAR)
def get_sidebar_usage_context() -> dict[str, str]:
    """Serve usage documentation for the sidebar component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% block drawers %}
            {% sidebar sidebar_data=right_sidebar side="right" auto_close=False %}
        {% endblock drawers %}
        """
    }


@register_component(Component.FOOTER)
def get_footer_usage_context() -> dict[str, str]:
    """Serve usage documentation for the footer component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% block footer %}
            {% footer data=footer_data %}
        {% endblock footer %}
        """
    }


@register_component(Component.BREADCRUMBS)
def get_breadcrumb_usage_context() -> dict[str, str]:
    """Serve usage documentation for the breadcrumbs component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% breadcrumbs items=breadcrumb_items %}
        """
    }


@register_component(Component.STEP_BAR)
def get_step_bar_usage_context() -> dict[str, str]:
    """Serve usage documentation for the step bar component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% step_bar items=step_bar_items %}
        """
    }


@register_component(Component.MINIMAL_STEP_BAR)
def get_minimal_step_bar_usage_context() -> dict[str, str]:
    """Serve usage documentation for the minimal step bar component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% minimal_step_bar config=min_step_bar_config %}
        """
    }


@register_component(Component.BULLET_POINT_LIST)
def get_bullet_point_list_usage_context() -> dict[str, str]:
    """Serve usage documentation for the bullet point list component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% bullet_point_list items=bulletpoints %}
        """
    }


@register_component(Component.ACCORDION)
def get_accordion_usage_context() -> dict[str, str]:
    """Serve usage documentation for the accordion component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% accordion id="faq-exclusive" items=accordion_items exclusive=True %}
        """
    }


@register_component(Component.TABS)
def get_tabs_usage_context() -> dict[str, str]:
    """Serve usage documentation for the tabs component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% tabs config=tabs_config %}
        """
    }


@register_component(Component.BUTTON)
def get_button_usage_context() -> dict[str, str]:
    """Serve usage documentation for the button component."""
    return {
        "usage": """
        <button class="btn btn-primary">{% trans "Primary" %}</button>
        <button class="btn btn-secondary">{% trans "Secondary" %}</button>
        <button class="btn btn-success">{% trans "Success" %}</button>
        <button class="btn btn-warning">{% trans "Warning" %}</button>
        <button class="btn btn-danger">{% trans "Danger" %}</button>
        <button class="btn btn-info">{% trans "Info" %}</button>
        <button disabled class="btn btn-disabled">{% trans "Disabled" %}</button>
        <button aria-label="{% trans 'Close' %}" class="btn btn-close">{% icon name="x-mark" size="xs" %}</button>
        <a href="#" class="btn-link">{% trans "Link" %}</a>

        <button class="btn btn-outline-primary">{% trans "Primary" %}</button>
        <button class="btn btn-outline-secondary">{% trans "Secondary" %}</button>
        <button class="btn btn-outline-success">{% trans "Success" %}</button>
        <button class="btn btn-outline-warning">{% trans "Warning" %}</button>
        <button class="btn btn-outline-danger">{% trans "Danger" %}</button>
        <button class="btn btn-outline-info">{% trans "Info" %}</button>
        <button disabled class="btn btn-outline-disabled">{% trans "Disabled" %}</button>

        <button class="btn btn-primary btn-large">{% trans "Click me!" %}</button>
        <button class="btn btn-primary">{% trans "Click me!" %}</button>
        <button class="btn btn-primary btn-sm">{% trans "Click me!" %}</button>
        <button class="btn btn-primary btn-xs">{% trans "Click me!" %}</button>
        """
    }


@register_component(Component.INPUT_FIELD)
def get_input_field_usage_context() -> dict[str, str]:
    """Serve usage documentation for the input field component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% input_field tag_id="expiration-date" name="expiration_date" input_type="date" value="expiration_date" label="Choose expiration date:" %}

        <!-- or -->

        {% input_field config=input_config %}
        """
    }


@register_component(Component.CHECKBOX)
def get_checkbox_usage_context() -> dict[str, str]:
    """Serve usage documentation for the checkbox component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% checkbox tag_id="agb-box" name="accept_agb" value="accept_agb" checked=False disabled=False label="Accept AGBs" %}

        <!-- or -->

        {% checkbox config=checkbox_config %}
        """
    }


@register_component(Component.CHECKBOX_GROUP)
def get_checkbox_group_usage_context() -> dict[str, str]:
    """Serve usage documentation for the checkbox group component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% checkbox_group config=checkbox_config %}
        """
    }


@register_component(Component.DROPDOWN)
def get_dropdown_usage_context() -> dict[str, str]:
    """Serve usage documentation for the dropdown component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% dropdown dropdown_menu=user_dropdown %}
        """
    }


@register_component(Component.RADIO_GROUP)
def get_radio_group_usage_context() -> dict[str, str]:
    """Serve usage documentation for the radio_group component."""
    return {
        "usage": """
        {% load insight_tags %}

        <!-- Radio Group -->
        {% radio_group config=example_radio %}
        """
    }


@register_component(Component.RADIO_BLOCK)
def get_radio_group_usage_context() -> dict[str, str]:
    """Serve usage documentation for the radio_block component."""
    return {
        "usage": """
        {% load insight_tags %}

        <!-- Radio Block -->
        {% radio_block config=view_radio_config current_value=current_view view_name="toggle_view" target_id=target_id %}
        """
    }


@register_component(Component.RANGE_SLIDER)
def get_rangle_slider_usage_context() -> dict[str, str]:
    """Serve usage documentation for the range slider component."""
    return {
        "usage": """
        {% load insight-tags %}

        {% slider tag_id="cpu-cores" name="cpu_core_count" value=4 minimum=2 maximum=8 step_size=2 disabled=False label="Choose amount of CPU-Cores:" items=labels %}

        <!-- or -->

        {% slider config=slider_config %}
        """
    }


@register_component(Component.TOGGLE)
def get_toggle_usage_context() -> dict[str, str]:
    """Serve usage documentation for the toggle component."""
    return {
        "usage": """
        {% load insight-tags %}

        {% toggle tag_id="theme-toggle" name="toggle_theme" value="toggle_theme" checked=False disabled=False label="Dark" method="changeTheme" switch=True %}

        <!-- or -->

        {% toggle config=toggle_config method="changeTheme" %}
        """
    }


@register_component(Component.SELECT)
def get_select_usage_context() -> dict[str, str]:
    """Serve usage documentation for the select component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% select name="test" label="Test" options=["A", "B", "C"] %}

        <!-- Oder -->

        {% select config=select_config %}
        """
    }


@register_component(Component.MULTISELECT)
def get_multiselect_usage_context() -> dict[str, str]:
    """Serve usage documentation for the multiselect component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% multiselect name="test" label="Test" maximum=0 show_buttons=True options=["A", "B", "C"] %}

        <!-- Oder -->

        {% multiselect config=multiselect_config %}
        """
    }


@register_component(Component.CHAT)
def get_chat_usage_context() -> dict[str, str]:
    """Serve usage documentation for the chat component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% chat view_name=view_name %}
        """
    }


@register_component(Component.ALERT)
def get_alert_usage_context() -> dict[str, str]:
    """Serve usage documentation for the alert component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% alert message="Ihre Änderungen wurden gespeichert." type="success" dismissible=True %}
        """
    }


@register_component(Component.MODAL)
def get_modal_usage_context() -> dict[str, str]:
    """Serve usage documentation for the modal component."""
    return {
        "usage": """
        {% load insight_tags %}

        <button class="btn btn-primary" data-insight-toggle="modal" data-insight-target="demo-modal">
            {% trans "Open Modal" %}
        </button>
        {% modal tag_id="demo-modal" title=_("Demo Modal") description=_("Dies ist ein Beispiel-Modal mit Standard-Styling!") %}
        """
    }


@register_component(Component.POPOVER)
def get_popover_usage_context() -> dict[str, str]:
    """Serve usage documentation for the popover component."""
    return {
        "usage": """
        <button data-popover="demo-popover" data-show-arrow="true" data-position="top" class="btn btn-primary">Hover me!</button>
        <div id="demo-popover" class="bg-white dark:bg-gray-500 w-64 border border-gray-300 dark:border-0 rounded-sm shadow">
            <!-- Content -->
        </div>
        """
    }


@register_component(Component.TOOLTIP)
def get_tooltip_usage_context() -> dict[str, str]:
    """Serve usage documentation for the tooltip component."""
    return {
        "usage": """
        <button
            data-tooltip="This is a tooltip."
            data-show-arrow="true"
            data-position="bottom"
            class="btn btn-primary"
        >
            Click me!
        </button>
        """
    }


@register_component(Component.CODE_BLOCK)
def get_code_block_usage_context() -> dict[str, str]:
    """Serve usage documentation for the code block component."""
    return {
        "usage": """
        <div id="code" data-insight-code-block="javascript">
            function greet(name) {
                return `Hello, ${name}!`;
            }
        </div>
        """
    }


@register_component(Component.DIFFERENTIATOR)
def get_differentiator_usage_context() -> dict[str, str]:
    """Serve usage documentation for the differentiator component."""
    return {
        "usage": """
        {% load insight_tags %}

        {{ textA|diff:textB|safe }}
        """
    }


@register_component(Component.PROGRESS_BAR)
def get_progress_bar_usage_context() -> dict[str, str]:
    """Serve usage documentation for the progress bar component."""
    return {
        "usage": """
        {% include "insight_ui/components/progress_bar.html" %}
        """
    }


@register_component(Component.GEO_MAP)
def get_geo_map_usage_context() -> dict[str, str]:
    """Serve usage documentation for the geo map component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% geo_map data=geo_map_data %}
        """
    }


@register_component(Component.CHART)
def get_charts_usage_context() -> dict[str, str]:
    """Serve usage documentation for the charts component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% bar_chart chart_id="bar_chart_example" chart=chart_data %}
        {% line_chart chart_id="line_chart_example" chart=chart_data %}
        """
    }


@register_component(Component.LIVE_CONTENT)
def get_live_content_usage_context() -> dict[str, str]:
    """Serve usage documentation for the live content component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% live_content url="/api/live-data/" interval=10 id="live-content" %}
        """
    }


@register_component(Component.WEB_SOCKET)
def get_web_socket_usage_context() -> dict[str, str]:
    """Serve usage documentation for the web socket component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% insight_websocket tag_id="demo-websocket" url="ws://localhost:8765" initial_content="Connect to Web-Socket…" %}
        """
    }


@register_component(Component.INFINITE_SCROLL)
def get_infinite_scroll_usage_context() -> dict[str, str]:
    """Serve usage documentation for the infinite scroll component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% infinite_scroll items=scroll_items view_name="more_items" auto_fetch=False %}
        """
    }


@register_component(Component.PAGINATION)
def get_pagination_usage_context() -> dict[str, str]:
    """Serve usage documentation for the pagination component."""
    return {
        "usage": """
        {% load insight_tags %}

        <div id="list-container">
            {% pagination with current_page=start_page surrounding_pages=surrounding_pages %}
        </div>
        """
    }


@register_component(Component.TABLE)
def get_table_usage_context() -> dict[str, str]:
    """Serve usage documentation for the table component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% table data=user_data %}
        """
    }


@register_component(Component.GENERIC_FILTER)
def get_generic_filter_usage_context() -> dict[str, str]:
    """Serve usage documentation for the generic filter component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% generic_filter filters=filters view_name=filter_view_name hx_target="#data" hx_push_url="true" vertical=False query_params=request.GET %}
        """
    }


@register_component(Component.SEARCH_BAR)
def get_search_bar_usage_context() -> dict[str, str]:
    """Serve usage documentation for the search bar component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% search_bar request_view="index_view" simple=True search_query="Test 123" %}
        """
    }


@register_component(Component.QUERY_BUILDER)
def get_query_builder_usage_context() -> dict[str, str]:
    """Serve usage documentation for the query builder component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% sq_builder model_fields=model_fields %}
        """
    }


@register_component(Component.CARD)
def get_card_usage_context() -> dict[str, str]:
    """Serve usage documentation for the card component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% card title=card.title subtitle=card.subtitle content=card.content actions=card.actions %}
        {% card_app title=card.title content=card.content tags=card.tags url=card.url image=card.image actions=card.actions %}
        {% card_flip title=card.title content=card.content tags=card.tags url=card.url image=card.image actions=card.actions %}
        """
    }


@register_component(Component.CARD_CAROUSEL)
def get_card_carousel_usage_context() -> dict[str, str]:
    """Serve usage documentation for the card carousel component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% carousel carousel_items=carousel_items show_index=True items_per_slide=2 %}
        """
    }


@register_component(Component.IMAGE_CAROUSEL)
def get_image_carousel_usage_context() -> dict[str, str]:
    """Serve usage documentation for the image carousel component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% image_carousel images=image_carousel_items show_dots=True show_index=True items_per_slide=1 %}
        """
    }


@register_component(Component.THREE_D_CAROUSEL)
def get_3d_carousel_usage_context() -> dict[str, str]:
    """Serve usage documentation for the 3D carousel component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% three_d_carousel tag_id="threeD_carousel" velocity=300 face_camera=True carousel_items=items %}
        """
    }


@register_component(Component.TOGGLE_VIEW)
def get_toggle_view_usage_context() -> dict[str, str]:
    """Serve usage documentation for the toggle view component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% toggle_view tag_id="test" data=toggle_data view_radio_config=view_radio_config current_view=toggle_start_view %}
        """
    }


@register_component(Component.FORM)
def get_form_usage_context() -> dict[str, str]:
    """Serve usage documentation for the form component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% form tag_id="htmx-form" title="Contact Form" description="Please fill out the form" fields=form_fields show_reset_button=True view_name="form_submit" htmx_config_params=htmx_config %}
        """
    }
