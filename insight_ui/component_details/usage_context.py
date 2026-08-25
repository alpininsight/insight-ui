"""Usage example context for UI components."""

from django.utils.translation import gettext as _

from insight_ui.component_details.component_context import register_component
from insight_ui.component_details.components import Component

# =============================================================
#
#   Layout Tags
#
# =============================================================


@register_component(Component.PAGE_HEADER)
def get_page_header_usage_context() -> dict[str, str]:
    """Serve usage documentation for the page header component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% block heading %}
            {# With chapter for hierarchical titles #}
            {% page_header chapter="My App" title="Dashboard" description="Welcome to your personal dashboard." %}

            {# Without chapter for standalone pages #}
            {% page_header title="About Us" description="Learn more about our company." %}
        {% endblock heading %}
        """
    }


@register_component(Component.ARTICLE)
def get_article_usage_context() -> dict[str, str]:
    """Serve usage documentation for the article component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% article config=article_config %}

        <!-- or -->

        {% article title="News" columns=3 content="<p>First paragraph...</p><p>Second paragraph...</p>" %}
        """
    }


@register_component(Component.HERO)
def get_hero_usage_context() -> dict[str, str]:
    """Serve usage documentation for the hero component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% hero config=hero_config %}

        <!-- or -->

        {% hero title="Insight UI" subtitle="A Django Component Framework" description="A modern UI library." cta_primary=cta_primary badge=badge %}
        """
    }


@register_component(Component.STATUS_SCREEN)
def get_status_screen_usage_context() -> dict[str, str]:
    """Serve usage documentation for the status screen component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% status_screen
            title="Sign-in failed"
            description="The SSO process could not be completed."
            status="error"
            notice_title="What happened?"
            notice="Please try again or contact support if the issue persists."
            primary_action=retry_button
            secondary_action=support_button
        %}
        """
    }


@register_component(Component.PAGE)
def get_page_usage_context() -> dict[str, str]:
    """Serve usage documentation for the page layout tag."""
    return {
        "usage": """
        {% load layout_tags %}

        {% page padding="l" %}
            <h1>Page Title</h1>
            <p>Page content goes here.</p>
        {% endpage %}

        <!-- Full viewport height with centered content -->
        {% page height="full" %}
            {% vbox v_align="center" full_height=True %}
                <main>Vertically centered content</main>
            {% endvbox %}
        {% endpage %}

        <!-- Peek: shows next section is coming -->
        {% page height="peek" %}
            <h1>Hero Section</h1>
        {% endpage %}
        """
    }


@register_component(Component.HBOX)
def get_hbox_usage_context() -> dict[str, str]:
    """Serve usage documentation for the hbox layout tag."""
    return {
        "usage": """
        {% load layout_tags %}

        {% hbox gap="s" v_align="center" h_align="between" %}
            <span>Left</span>
            <span>Right</span>
        {% endhbox %}

        <!-- Fill parent height - useful inside page with height="full" -->
        {% hbox full_height=True %}
            {% vbox %}Column 1{% endvbox %}
            {% vbox %}Column 2{% endvbox %}
        {% endhbox %}

        <!-- With wrapping enabled -->
        {% hbox gap="m" wrap=True %}
            <div>Item 1</div>
            <div>Item 2</div>
            <div>Item 3</div>
        {% endhbox %}
        """
    }


@register_component(Component.VBOX)
def get_vbox_usage_context() -> dict[str, str]:
    """Serve usage documentation for the vbox layout tag."""
    return {
        "usage": """
        {% load layout_tags %}

        {% vbox gap="m" %}
            <div>Top</div>
            <div>Middle</div>
            <div>Bottom</div>
        {% endvbox %}

        <!-- Fill parent height and center content vertically -->
        {% vbox full_height=True v_align="center" %}
            <div>Vertically centered</div>
        {% endvbox %}

        <!-- Full-height layout with vertical distribution -->
        {% vbox full_height=True h_align="center" v_align="between" %}
            <header>Header</header>
            <main>Content</main>
            <footer>Footer</footer>
        {% endvbox %}
        """
    }


@register_component(Component.GRID)
def get_grid_usage_context() -> dict[str, str]:
    """Serve usage documentation for the grid layout tag."""
    return {
        "usage": """
        {% load layout_tags %}

        <!-- Auto-fit mode: items wrap based on available space -->
        {% grid gap="l" %}
            <div>Item 1</div>
            <div>Item 2</div>
            <div>Item 3</div>
            <div>Item 4</div>
        {% endgrid %}

        <!-- Auto-fit with custom minimum width (supports px, rem, em, etc.) -->
        {% grid min="15rem" gap="m" %}
            <div>Card 1</div>
            <div>Card 2</div>
        {% endgrid %}

        <!-- Fixed columns with responsive breakpoints (adapts to container width) -->
        {% grid cols=3 gap="l" %}
            <div>Column 1</div>
            <div>Column 2</div>
            <div>Column 3</div>
        {% endgrid %}

        <!-- Fixed columns without responsive behavior (always 4 columns) -->
        {% grid cols=4 fixed=True %}
            <div>Always 4 columns</div>
        {% endgrid %}
        """
    }


@register_component(Component.SPACER)
def get_spacer_usage_context() -> dict[str, str]:
    """Serve usage documentation for the spacer layout tag."""
    return {
        "usage": """
        {% load layout_tags %}

        {% hbox gap="xs" v_align="center" %}
            <span>Left</span>
            {% spacer size="xl" %}
            <span>Right</span>
        {% endhbox %}

        <!-- Using default size (m) -->
        {% vbox %}
            <div>Above</div>
            {% spacer %}
            <div>Below</div>
        {% endvbox %}
        """
    }


@register_component(Component.DIVIDER)
def get_divider_usage_context() -> dict[str, str]:
    """Serve usage documentation for the divider layout tag."""
    return {
        "usage": """
        {% load layout_tags %}

        {% vbox gap="m" %}
            <p>Content above</p>
            {% divider %}
            <p>Content below</p>
        {% endvbox %}

        <!-- Vertical divider -->
        {% hbox gap="m" v_align="stretch" %}
            <div>Left</div>
            {% divider direction="vertical" %}
            <div>Right</div>
        {% endhbox %}

        <!-- With custom margin spacing -->
        {% divider spacing="xl" %}
        """
    }


@register_component(Component.SECTION)
def get_section_usage_context() -> dict[str, str]:
    """Serve usage documentation for the section layout tag."""
    return {
        "usage": """
        {% load layout_tags %}

        <!-- Basic section with anchor ID -->
        {% section id="installation" gap="m" %}
            <h2>Installation</h2>
            <p>Follow these steps to install the package.</p>
            <pre><code>pip install insight-ui</code></pre>
        {% endsection %}

        <!-- Section without ID (no scroll offset) -->
        {% section gap="s" %}
            <h3>Quick Start</h3>
            <p>Get started in minutes.</p>
        {% endsection %}

        <!-- With accessibility label -->
        {% section id="features" aria_label="Product features and capabilities" %}
            <h2>Features</h2>
            <ul>
                <li>Feature 1</li>
                <li>Feature 2</li>
            </ul>
        {% endsection %}

        <!-- Section labeled by its heading -->
        {% section id="faq" aria_labelledby="faq-heading" %}
            <h2 id="faq-heading">Frequently Asked Questions</h2>
            <p>Common questions answered.</p>
        {% endsection %}
        """
    }


@register_component(Component.SURFACE)
def get_surface_usage_context() -> dict[str, str]:
    """Serve usage documentation for the surface layout tag."""
    return {
        "usage": """
        {% load layout_tags %}

        <!-- Static container (renders as <div>) -->
        {% surface variant="surface" padding="l" %}
            <h3>Card Title</h3>
            <p>This is a basic surface container.</p>
        {% endsurface %}

        <!-- Raised variant with shadow -->
        {% surface variant="raised" padding="m" radius="l" %}
            <h4>Elevated Content</h4>
            <p>Content with visual prominence.</p>
        {% endsurface %}

        <!-- Outline variant (border only) -->
        {% surface variant="outline" padding="s" %}
            <span>Minimal container</span>
        {% endsurface %}

        <!-- Clickable surface (renders as <a>) -->
        {% surface href="/components" padding="m" %}
            {% hbox gap="s" v_align="center" %}
                <span class="group-hover:text-insight-primary">Browse Components</span>
            {% endhbox %}
        {% endsurface %}

        <!-- External link with new tab -->
        {% surface href="https://github.com/example/repo" external=True padding="m" %}
            <span>View on GitHub</span>
        {% endsurface %}
        """
    }


# =============================================================
#
#   Navigation Tags
#
# =============================================================


@register_component(Component.NAVBAR)
def get_navbar_usage_context() -> dict[str, str]:
    """Serve usage documentation for the navbar component."""
    return {
        "usage_summary": _(
            "The navigation bar is integrated using the `navbar` tag. The _base template_ includes a block designated for the navigation bar, where it should be placed to ensure proper functionality."
        ),
        "usage": """
        {% load insight_tags %}

        {% block navbar %}
            {% navbar config=nav_config %}
        {% endblock navbar %}
        """,
    }


@register_component(Component.SIDEBAR)
def get_sidebar_usage_context() -> dict[str, str]:
    """Serve usage documentation for the sidebar component."""
    return {
        "usage_summary": _(
            "The sidebar is integrated using the `sidebar` layout tag from `layout_tags`. The _base template_ includes blocks designated for the sidebar, where it should be placed. There is one block for the right side and one for the left side. If the sidebar is collapsible, set `static=False` to create a drawer. If the component is used outside of these blocks, layout issues may occur."
        ),
        "usage": """
        {% load layout_tags %}

        {% block sidebar_left %}
            {% sidebar %}
                {% include "components/sidebar_nav.html" with sidebar_data=nav_data %}
            {% endsidebar %}
        {% endblock sidebar_left %}

        {% block sidebar_right %}
            {% sidebar width="wide" %}
                <h2>Table of Contents</h2>
                <div id="toc"></div>
            {% endsidebar %}
        {% endblock sidebar_right %}
        """,
    }


@register_component(Component.FOOTER)
def get_footer_usage_context() -> dict[str, str]:
    """Serve usage documentation for the footer component."""
    return {
        "usage_summary": _(
            "The footer is included using the `footer` tag. The _base template_ includes a block designated for the footer. To ensure that the footer always appears at the bottom of the webpage, it should be placed within this designated block."
        ),
        "usage": """
        {% load insight_tags %}

        {% block footer %}
            {% footer config=footer_config %}
        {% endblock footer %}
        """,
    }


@register_component(Component.BREADCRUMBS)
def get_breadcrumb_usage_context() -> dict[str, str]:
    """Serve usage documentation for the breadcrumbs component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% breadcrumbs config=breadcrumbs_config %}

        <!-- or -->

        {% breadcrumbs config=breadcrumbs_items %}
        """
    }


@register_component(Component.STEPPER)
def get_stepper_usage_context() -> dict[str, str]:
    """Serve usage documentation for the step bar component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% stepper config=stepper_config %}

        <!-- or -->

        {% stepper items=stepper_items %}
        """
    }


@register_component(Component.MINIMAL_STEPPER)
def get_minimal_stepper_usage_context() -> dict[str, str]:
    """Serve usage documentation for the minimal step bar component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% minimal_stepper config=min_stepper_config %}
        """
    }


@register_component(Component.BULLET_POINT_LIST)
def get_bullet_point_list_usage_context() -> dict[str, str]:
    """Serve usage documentation for the bullet point list component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% bullet_point_list config=bulletpoints_config %}

        <!-- or -->

        {% bullet_point_list items=bulletpoints %}
        """
    }


@register_component(Component.ACCORDION)
def get_accordion_usage_context() -> dict[str, str]:
    """Serve usage documentation for the accordion component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% accordion config=accordion_config %}

        <!-- or -->

        {% accordion tag_id="faq-exclusive" items=accordion_items exclusive=True %}
        """
    }


@register_component(Component.TABS)
def get_tabs_usage_context() -> dict[str, str]:
    """Serve usage documentation for the tabs component."""
    return {
        "usage": """
        {% load layout_tags %}

        {# Config mode (HTMX) #}
        {% tabs config=tabs_config %}{% endtabs %}

        {# Block mode (static content) #}
        {% tabs id="example" label="Example Tabs" %}
            {% tab id="first" label="First Tab" active=True %}
                <p>First tab content</p>
            {% endtab %}
            {% tab id="second" label="Second Tab" %}
                <p>Second tab content</p>
            {% endtab %}
        {% endtabs %}
        """
    }


# =============================================================
#
#   Input Tags
#
# =============================================================


@register_component(Component.BUTTON)
def get_button_usage_context() -> dict[str, str]:
    """Serve usage documentation for the button component."""
    return {
        "usage": """
        <!-- Standard / Filled -->
        {% button label=_("Primary") type="primary" %}

        <!-- Outline / Ghost -->
        {% button label=_("Primary") type="primary" outline=True %}

        <!-- Subtle -->
        {% button label=_("Primary") type="primary" subtle=True %}

        <!-- Size -->
        {% button label=_("Click me!") type="primary" size="xl" %}

        <!-- All together -->
        {% button label=_("Primary") type="success" subtle=True round=True size="s" %}

        <!-- Icons -->
        {% button label=_("With Icon") type="primary" icon_name="rocket-launch" %}
        {% button label=_("With Icon") type="primary" icon_name="rocket-launch" icon_end=True %}
        {% button label=_("Icon only") type="primary" icon_name="rocket-launch" icon_only=True %}
        {% button label=_("Icon only") type="primary" icon_name="rocket-launch" icon_only=True round=True %}

        <!-- Tooltip -->
        {% button label=_("With tooltip") type="primary" tooltip="This is a button." %}

        <!-- As hyperlink (creates <a> tag with href) -->
        {% button label=_("As hyperlink") type="primary" request_url="#" %}
        """
    }


@register_component(Component.INPUT_FIELD)
def get_input_field_usage_context() -> dict[str, str]:
    """Serve usage documentation for the input field component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% input_field config=input_config %}

        <!-- or -->

        {% input_field tag_id="expiration-date" name="expiration_date" input_type="date" value="expiration_date" label="Choose expiration date:" %}
        """
    }


@register_component(Component.TEXTAREA)
def get_textarea_usage_context() -> dict[str, str]:
    """Serve usage documentation for the textarea component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% textarea config=input_config %}

        <!-- or -->

        {% textarea tag_id="message" name="message" rows=4 label="Write a message:" placeholder="Write something..." %}
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

        {% dropdown config=user_dropdown_config %}
        """
    }


@register_component(Component.RADIO_GROUP)
def get_radio_group_usage_context() -> dict[str, str]:
    """Serve usage documentation for the radio_group component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% radio_group config=example_radio current_value=value %}

        <!-- or -->

        {% radio_group name="radio-example1" label="" items=items as_row=True %}
        """
    }


@register_component(Component.RADIO_BLOCK)
def get_radio_block_usage_context() -> dict[str, str]:
    """Serve usage documentation for the radio_block component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% radio_block config=example_radio current_value=value %}

        <!-- or -->

        {% radio_block config=view_radio_config current_value=current_view request_url="/switch_view/" hx_target_id=hx_target_id %}
        """
    }


@register_component(Component.RANGE_SLIDER)
def get_rangle_slider_usage_context() -> dict[str, str]:
    """Serve usage documentation for the range slider component."""
    return {
        "usage": """
        {% load insight_tags %}

        <!-- Single-thumb slider -->
        {% slider tag_id="cpu-cores" name="cpu_core_count" value=4 minimum=2 maximum=8 step_size=2 label="Choose amount of CPU-Cores:" items=labels %}

        <!-- With responsive legend (skip mode) -->
        {% slider tag_id="month" name="month" value=6 minimum=1 maximum=12 items=months legend_mode="skip" %}

        <!-- With responsive legend (rotate mode) -->
        {% slider tag_id="month" name="month" value=6 minimum=1 maximum=12 items=months legend_mode="rotate" %}

        <!-- Dual-thumb slider for range selection -->
        {% slider tag_id="price-range" name="price" dual=True value_min=200 value_max=800 minimum=0 maximum=1000 label="Price Range:" items=price_labels %}

        <!-- Using config dict -->
        {% slider config=slider_config %}
        """
    }


@register_component(Component.TOGGLE)
def get_toggle_usage_context() -> dict[str, str]:
    """Serve usage documentation for the toggle component."""
    return {
        "usage": """
        {% load insight-tags %}

        {% toggle config=toggle_config method="changeTheme" %}

        <!-- or -->

        {% toggle tag_id="theme-toggle" name="toggle_theme" value="toggle_theme" checked=False disabled=False label="Dark" method="changeTheme" switch=True %}
        """
    }


@register_component(Component.SELECT)
def get_select_usage_context() -> dict[str, str]:
    """Serve usage documentation for the select component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% select config=select_config %}

        <!-- or -->

        {% select name="test" label="Test" options=["A", "B", "C"] %}
        """
    }


@register_component(Component.MULTISELECT)
def get_multiselect_usage_context() -> dict[str, str]:
    """Serve usage documentation for the multiselect component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% multiselect config=multiselect_config %}

        <!-- or -->

        {% multiselect name="test" label="Test" maximum=0 show_buttons=True options=["A", "B", "C"] %}
        """
    }


@register_component(Component.CHAT)
def get_chat_usage_context() -> dict[str, str]:
    """Serve usage documentation for the chat component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% chat request_url="/api/chat-response/" %}
        """
    }


# =============================================================
#
#   Popup Tags
#
# =============================================================


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
        "usage_summary": _(
            "The component is included via the `modal` tag. Additionally you need a trigger that causes the dialog to appear when the user clicks on it. This trigger can be any HTML tag and must include the `data-insight-modal` attribute, whose value is the ID of the target element (the dialog)."
        ),
        "usage": """
        {% load insight_tags %}

        <button class="btn btn-primary" data-insight-modal="demo-modal">
            {% trans "Open Modal" %}
        </button>
        {% modal tag_id="demo-modal" title=_("Demo Modal") description=_("Dies ist ein Beispiel-Modal mit Standard-Styling!") %}
        """,
    }


@register_component(Component.POPOVER)
def get_popover_usage_context() -> dict[str, str]:
    """Serve usage documentation for the popover component."""
    return {
        "usage_summary": _(
            "To add a popover, you need a trigger that causes the popover to appear when the user hovers over it. This trigger can be any HTML tag and must include the `data-insight-popover` attribute, whose value is the ID of the target element (the popover). You can customize the popover entirely on your own; the only thing to keep in mind is the connection via the **tag ID**."
        ),
        "usage": """
        <button data-insight-popover="demo-popover" data-show-arrow="true" data-position="top" class="btn btn-primary">Hover me!</button>
        <div id="demo-popover" class="bg-white dark:bg-gray-500 w-64 border border-gray-300 dark:border-0 rounded-insight-overlay shadow-insight-overlay">
            <!-- Content -->
        </div>
        """,
    }


@register_component(Component.TOOLTIP)
def get_tooltip_usage_context() -> dict[str, str]:
    """Serve usage documentation for the tooltip component."""
    return {
        "usage_summary": _(
            "To add a tooltip to an element, simply add the `data-insight-tooltip` attribute, whose value is the text to be displayed in the tooltip."
        ),
        "usage": """
        <button
            data-insight-tooltip="This is a tooltip."
            data-show-arrow="true"
            data-position="bottom"
            class="btn btn-primary"
        >
            Click me!
        </button>
        """,
    }


# =============================================================
#
#   Util Tags
#
# =============================================================


@register_component(Component.INFOBOX)
def get_infobox_usage_context() -> dict[str, str]:
    """Serve usage documentation for the infobox component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% infobox info_type=note.type message=note.message %}
        """
    }


@register_component(Component.CODE_BLOCK)
def get_code_block_usage_context() -> dict[str, str]:
    """Serve usage documentation for the code block component."""
    return {
        "usage_summary": _(
            "To use the component, simply insert an HTML tag—preferably a `<div>`. The element must include the `data-insight-code-block` attribute, whose value should be the desired programming language. The tag should contain only the source code to be displayed."
        ),
        "usage": """
        <div id="code" data-insight-code-block="javascript">
            function greet(name) {
                return `Hello, ${name}!`;
            }
        </div>
        """,
    }


@register_component(Component.LEGAL_NOTICE)
def get_legal_notice_usage_context() -> dict[str, str]:
    """Serve usage documentation for the legal notice component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% legal_notice config=legal %}

        <!-- or -->

        {% legal_notice year=2026 holder="Alpin Insight Solutions GmbH & Co. KG" source_label="Open Source" license_text="AGPL-3.0" %}
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


@register_component(Component.LOGO)
def get_logo_usage_context() -> dict[str, str]:
    """Serve usage documentation for the logo component."""
    return {
        "usage": """
        {% load insight_tags %}

        {# SVG static asset #}
        {% logo config=logo_svg %}

        {# Bitmap image #}
        {% logo url="img/company-logo.png" alt="Company" height="3rem" %}

        {# Icon logo using the Insight UI icon set #}
        {% logo icon_name="sparkles" icon_size="xl" alt="Product mark" %}

        {# Theme-aware SVG asset #}
        {% logo url="svg/logo-light.svg" url_dark="svg/logo-dark.svg" alt="Company" %}
        """
    }


@register_component(Component.BRAND_MARK)
def get_brand_mark_usage_context() -> dict[str, str]:
    """Serve usage documentation for the brand mark component."""
    return {
        "usage": """
        {% load insight_tags %}

        {# Direct use with defaults #}
        {% brand_mark %}

        {# Deployment-lane variant #}
        {% brand_mark primary_text="Alpin Insight" secondary_text="Develop" variant="develop" %}

        {# Navbar brand mode #}
        {% navbar config=navbar_config %}
        """
    }


@register_component(Component.CORNER_RIBBON)
def get_corner_ribbon_usage_context() -> dict[str, str]:
    """Serve usage documentation for the corner ribbon component."""
    return {
        "usage": """
        {% load insight_tags %}

        {# Basic usage with default top-right position #}
        {% corner_ribbon text="New Feature" %}

        {# Different positions #}
        {% corner_ribbon text="Beta" position="top-left" %}
        {% corner_ribbon text="Sale" position="bottom-right" %}
        {% corner_ribbon text="Limited" position="bottom-left" %}

        {# Different colors #}
        {% corner_ribbon text="Success" color="success" %}
        {% corner_ribbon text="Warning" color="warning" %}
        {% corner_ribbon text="Error" color="danger" %}
        {% corner_ribbon text="Info" color="info" %}

        {# With custom ID for JavaScript #}
        {% corner_ribbon text="Click Me" tag_id="promo-ribbon" position="top-right" %}

        {# Using config dictionary from view context #}
        {% corner_ribbon config=ribbon_config %}
        """
    }


@register_component(Component.PROGRESS_BAR)
def get_progress_bar_usage_context() -> dict[str, str]:
    """Serve usage documentation for the progress bar component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% progress_bar config=progress_bar_config %}

        <!-- or -->

        {% progress_bar tag_id="download" value=66 %}
        """
    }


@register_component(Component.GEO_MAP)
def get_geo_map_usage_context() -> dict[str, str]:
    """Serve usage documentation for the geo map component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% geo_map config=geo_map_config %}
        """
    }


@register_component(Component.CHART)
def get_charts_usage_context() -> dict[str, str]:
    """Serve usage documentation for the charts component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% bar_chart config=chart_config %}

        <!-- or -->

        {% line_chart tag_id="line_chart_example" dataset=chart_data %}
        """
    }


@register_component(Component.LIVE_CONTENT)
def get_live_content_usage_context() -> dict[str, str]:
    """Serve usage documentation for the live content component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% live_content config=live_content_config %}

        <!-- or -->

        {% live_content tag_id="live-content" url="/api/live-data/" interval=10  %}
        """
    }


@register_component(Component.WEB_SOCKET)
def get_web_socket_usage_context() -> dict[str, str]:
    """Serve usage documentation for the web socket component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% websocket config=websocket_config %}

        <!-- or -->

        {% websocket tag_id="demo-websocket" request_url="/ws/ticker/" initial_content="<p>Connecting...</p>" %}
        """
    }


@register_component(Component.BADGE)
def get_badge_usage_context() -> dict[str, str]:
    """Serve usage context documentation for the badge component."""
    return {
        "usage": """
        {% load insight_tags %}

        <!-- Standard / Filled -->
        {% badge label=_("Primary") type="primary" %}

        <!-- Size -->
        {% badge label=_("New!") type="primary" size="xl" %}

        <!-- Icons -->
        {% badge label=_("New!") icon_name="sparkles" %}
        {% badge label=_("New!") icon_name="sparkles" icon_end=True %}
        """
    }


# =============================================================
#
#   List Tags
#
# =============================================================


@register_component(Component.INFINITE_SCROLL)
def get_infinite_scroll_usage_context() -> dict[str, str]:
    """Serve usage documentation for the infinite scroll component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% infinite_scroll config=infinite_scroll_config %}

        <!-- or -->

        {% infinite_scroll items=scroll_items request_url="/more_items/" auto_fetch=False %}
        """
    }


@register_component(Component.PAGINATION)
def get_pagination_usage_context() -> dict[str, str]:
    """Serve usage documentation for the pagination component."""
    return {
        "usage": """
        {% load insight_tags %}

        <div id="list-container">
            <!-- Actual list -->
            {% pagination config=pagination_config %}
        </div>

        <!-- or -->

        <div id="list-container">
            <!-- Actual list -->
            {% pagination current_page=start_page surrounding_pages=surrounding_pages %}
        </div>
        """
    }


@register_component(Component.TABLE)
def get_table_usage_context() -> dict[str, str]:
    """Serve usage documentation for the table component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% table config=table_config %}
        """
    }


# =============================================================
#
#   Filter Tags
#
# =============================================================


@register_component(Component.SEARCH_BAR)
def get_search_bar_usage_context() -> dict[str, str]:
    """Serve usage documentation for the search bar component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% search_bar request_url="/search/" simple=True search_query="Test 123" %}
        """
    }


@register_component(Component.GENERIC_FILTER)
def get_generic_filter_usage_context() -> dict[str, str]:
    """Serve usage documentation for the generic filter component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% generic_filter config=generic_filter_config %}
        """
    }


@register_component(Component.QUERY_BUILDER)
def get_query_builder_usage_context() -> dict[str, str]:
    """Serve usage documentation for the query builder component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% query_builder config=query_builder_config %}
        """
    }


# =============================================================
#
#   Card Tags
#
# =============================================================


@register_component(Component.CARD)
def get_card_usage_context() -> dict[str, str]:
    """Serve usage documentation for the card component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% card config=card_config %}

        <!-- or -->

        {% card title="My Card" subtitle="More than just a card." content="Ok, it's actually just a card." %}
        """
    }


@register_component(Component.APP_CARD)
def get_app_card_usage_context() -> dict[str, str]:
    """Serve usage documentation for the app card component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% app_card config=card_config %}

        <!-- or -->

        {% app_card title="Insight UI" content="Django UI Framework for ..." request_url="/insight-ui/" %}
        """
    }


@register_component(Component.FLIP_CARD)
def get_flip_card_usage_context() -> dict[str, str]:
    """Serve usage documentation for the flip card component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% flip_card config=card_config %}

        <!-- or with inline parameters -->

        {% flip_card title="Product" content="Short description" back_title="Details" back_content="Extended info" %}
        """
    }


@register_component(Component.CARD_CAROUSEL)
def get_card_carousel_usage_context() -> dict[str, str]:
    """Serve usage documentation for the card carousel component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% carousel config=carousel_config %}

        <!-- or -->

        {% carousel carousel_items=carousel_items show_index=True items_per_slide=2 %}
        """
    }


@register_component(Component.IMAGE_CAROUSEL)
def get_image_carousel_usage_context() -> dict[str, str]:
    """Serve usage documentation for the image carousel component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% image_carousel config=carousel_config %}

        <!-- or -->

        {% image_carousel images=image_carousel_items show_dots=True show_index=True items_per_slide=1 %}
        """
    }


@register_component(Component.THREE_D_CAROUSEL)
def get_3d_carousel_usage_context() -> dict[str, str]:
    """Serve usage documentation for the 3D carousel component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% three_d_carousel config=carousel_config %}

        <!-- or -->

        {% three_d_carousel tag_id="threeD_carousel" velocity=300 face_camera=True carousel_items=items %}
        """
    }


@register_component(Component.TOGGLE_VIEW)
def get_toggle_view_usage_context() -> dict[str, str]:
    """Serve usage documentation for the toggle view component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% toggle_view config=toggle_view_config %}
        """
    }


# =============================================================
#
#   Form Tags
#
# =============================================================


@register_component(Component.FORM)
def get_form_usage_context() -> dict[str, str]:
    """Serve usage documentation for the form component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% form config=form_config %}
        """
    }
