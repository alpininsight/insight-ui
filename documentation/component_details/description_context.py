"""Component description documentation context."""

from django.urls import reverse
from django.utils.translation import gettext as _

from documentation.component_details.component_context import register_component
from documentation.component_details.components import Component

# =============================================================
#
#   Layout Tags
#
# =============================================================


@register_component(Component.PAGE_HEADER)
def get_page_header_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the page header component."""
    return {
        "description": [
            _(
                "The `page_header` component displays a prominent header section with geometric decorations, "
                "a title, optional description, and action buttons. The header uses the primary color to stand out from the page content."
            )
        ],
        "features": [
            _("**Geometric decorations**: Distinctive visual patterns for branding."),
            _("**Title and description**: Headline with optional supporting text."),
            _("**Action buttons**: Configurable buttons for primary actions."),
            _("**Primary color theming**: Uses the brand's primary color for visual impact."),
        ],
    }


@register_component(Component.ARTICLE)
def get_article_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the article component."""
    return {
        "description": [
            _(
                "The `article` component renders text content in newspaper style with multi-column CSS columns. "
                "The text flows automatically from one column to the next. "
                "Uses CSS Container Queries to adapt the column count based on available width, "
                "ensuring readable text regardless of where the component is placed."
            )
        ],
        "features": [
            _("**Multi-column layout**: Automatic text flow across columns."),
            _("**Responsive columns**: Column count adjusts to available width."),
            _("**Gap control**: Configurable spacing between columns."),
        ],
    }


@register_component(Component.HERO)
def get_hero_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the hero component."""
    return {
        "description": [
            _(
                "The `hero` component renders a prominent banner section for landing pages. "
                "It combines a title, subtitle, description text, and call-to-action buttons."
            )
        ],
        "features": [
            _("**Title and subtitle**: Primary headline with optional secondary text."),
            _("**Description**: Supporting paragraph text."),
            _("**Call-to-action buttons**: Primary and secondary action buttons."),
            _("**Badge**: Optional badge for highlighting features or announcements."),
        ],
    }


@register_component(Component.STATUS_SCREEN)
def get_status_screen_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the status screen component."""
    return {
        "description": [
            _(
                "The `status_screen` component renders a reusable full-page status view. "
                "It combines brand, surface, status icon, title, description, notice and actions for common application states."
            ),
            _(
                "It is intentionally generic. Use it for authentication failures, expired sessions, "
                "access states, deployment states, empty starts or workflow results without coupling the component to auth logic."
            ),
        ],
        "features": [
            _("**Semantic status**: Supports `info`, `success`, `warning` and `danger`."),
            _("**Reusable actions**: Uses the standard `button` component and `ButtonConfig`."),
            _("**Token-based surface**: Uses Insight UI surface, border, radius and shadow tokens."),
            _("**Optional brand**: Can show a `brand_mark` above the status card."),
        ],
    }


@register_component(Component.PAGE)
def get_page_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the page layout tag."""
    return {
        "description": [
            _(
                "The `page` block tag provides a full-width page container with consistent padding. "
                "Use it as the outermost wrapper for page content to ensure uniform spacing across your application."
            ),
            _("For advanced layout control (max-width, alignment), use a `vbox` inside the page container."),
        ],
        "features": [
            _("**padding**: Configurable inner padding using the spacing scale (xs/s/m/l/xl)."),
            _(
                "**height**: Height behavior - `auto` (fits content), `full` (viewport height), or `peek` (shows next section). When set to `full` or `peek`, the page becomes a flex-col container so children can use `full_height=True` to fill available space."
            ),
        ],
    }


@register_component(Component.HBOX)
def get_hbox_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the hbox layout tag."""
    return {
        "description": [
            _(
                "The `hbox` block tag creates a horizontal flex container (row direction). "
                "Child elements are arranged horizontally with configurable gap, alignment, and justification."
            )
        ],
        "features": [
            _("**gap**: Consistent spacing between children (xs/s/m/l/xl)."),
            _("**padding**: Inner padding (xs/s/m/l/xl). Optional."),
            _("**max_width**: Maximum container width (xs/s/m/l/xl/fit/full)."),
            _("**full_height**: Fill available height in parent container."),
            _("**h_align**: Horizontal/main-axis alignment (start/center/end/between/around/evenly)."),
            _("**v_align**: Vertical/cross-axis alignment (start/center/end/stretch/baseline)."),
            _("**wrap**: Optional flex-wrap for responsive layouts."),
        ],
    }


@register_component(Component.VBOX)
def get_vbox_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the vbox layout tag."""
    return {
        "description": [
            _(
                "The `vbox` block tag creates a vertical flex container (column direction). "
                "Child elements are stacked vertically with configurable gap, alignment, and justification."
            )
        ],
        "features": [
            _("**gap**: Consistent spacing between children (xs/s/m/l/xl)."),
            _("**padding**: Inner padding (xs/s/m/l/xl). Optional."),
            _("**max_width**: Maximum container width (xs/s/m/l/xl/fit/full)."),
            _("**full_height**: Fill available height in parent container."),
            _("**h_align**: Horizontal/cross-axis alignment (start/center/end/stretch/baseline)."),
            _("**v_align**: Vertical/main-axis alignment (start/center/end/between/around/evenly)."),
        ],
    }


@register_component(Component.GRID)
def get_grid_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the grid layout tag."""
    return {
        "description": [
            _(
                "The `grid` block tag creates a CSS Grid container for arranging items in columns. "
                "It supports two modes: **auto-fit** (items wrap automatically based on available space) "
                "and **fixed columns** (specific number of columns with responsive breakpoints)."
            ),
            _(
                "The grid uses CSS Container Queries, so breakpoints are based on the container width "
                "rather than the viewport. This means the grid adapts correctly regardless of where "
                "it's placed (sidebar, modal, card, etc.)."
            ),
        ],
        "features": [
            _(
                "**Auto-fit mode**: Items wrap based on available space. Set `min` for minimum item width (any CSS unit: px, rem, em)."
            ),
            _("**Fixed columns**: Set `cols` (1-6) for specific column count with container-based breakpoints."),
            _("**gap**: Consistent spacing between items (xs/s/m/l/xl)."),
            _("**fixed**: Disable responsive breakpoints to always use the exact column count."),
        ],
    }


@register_component(Component.SPACER)
def get_spacer_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the spacer layout tag."""
    return {
        "description": [
            _(
                "The `spacer` tag inserts a fixed-size spacer element. "
                "Use it to add explicit spacing between elements in flex or block layouts."
            )
        ],
        "features": [
            _("**size**: Spacer size using the spacing scale (xs/s/m/l/xl)."),
            _("**Flex-shrink**: Does not shrink in flex containers."),
        ],
    }


@register_component(Component.DIVIDER)
def get_divider_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the divider layout tag."""
    return {
        "description": [
            _("The `divider` tag inserts a visual divider line. Use it to separate content sections visually.")
        ],
        "features": [
            _("**direction**: Orientation of the divider (horizontal/vertical)."),
            _("**spacing**: Margin around the divider using the spacing scale (xs/s/m/l/xl)."),
            _("**weight**: Line thickness (thin/medium/thick)."),
            _("**style**: Line style (solid/dashed/dotted)."),
            _("**label**: Optional text displayed in the center of the divider."),
        ],
    }


@register_component(Component.SECTION)
def get_section_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the section layout tag."""
    return {
        "description": [
            _(
                "The `section` block tag creates a semantic HTML5 `<section>` element for content groupings. "
                "Unlike `vbox` which renders a `<div>`, `section` provides proper document semantics for accessibility and SEO."
            ),
            _(
                "Use `section` for thematic content groupings within a page, such as 'Installation', 'Features', or 'FAQ'. "
                "For pure layout purposes without semantic meaning, use `vbox` instead."
            ),
        ],
        "features": [
            _("**Semantic HTML**: Renders a `<section>` element for proper document structure."),
            _("**id**: Anchor ID for navigation links (automatically adds `scroll-mt-24` for fixed navbar offset)."),
            _("**gap**: Consistent spacing between children using the spacing scale (xs/s/m/l/xl)."),
        ],
    }


@register_component(Component.SURFACE)
def get_surface_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the surface layout tag."""
    return {
        "description": [
            _(
                "The `surface` block tag creates a styled container with background, border, and optional shadow. "
                "Use it to visually group content within a consistent design language."
            ),
            _(
                "When `href` is provided, the surface becomes clickable and renders as an `<a>` element with hover effects. "
                "This makes it ideal for navigation cards, feature links, or any clickable content block."
            ),
        ],
        "features": [
            _(
                "**variant**: Visual style - `surface` (light background), `raised` (with shadow), or `outline` (border only)."
            ),
            _("**padding**: Inner padding using the spacing scale (xs/s/m/l/xl)."),
            _("**radius**: Border radius from the design system (xs/s/m/l/xl/none)."),
            _("**href**: When set, renders as `<a>` with hover effects and `group` class for child styling."),
            _("**external**: Opens link in new tab with proper `rel` attributes (only when `href` is set)."),
        ],
    }


# =============================================================
#
#   Navigation Tags
#
# =============================================================


@register_component(Component.NAVBAR)
def get_navbar_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the navbar component."""
    return {
        "description": [
            _(
                "The `navbar` component provides a fixed navigation bar at the top of the page. "
                "It stays visible while scrolling and supports various navigation elements."
            )
        ],
        "features": [
            _("**Brand**: Logo and title on the left edge."),
            _("**Navigation links**: Main navigation items with optional icons and dropdowns."),
            _("**Search bar**: Optional search functionality with HTMX or Fuse.js support."),
            _("**User menu**: Optional dropdown menu for logged-in users or login button."),
            _("**Language selector**: Optional menu for switching display language."),
            _("**Theme toggle**: Optional button for switching between light and dark theme."),
        ],
    }


@register_component(Component.SIDEBAR)
def get_sidebar_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the sidebar component."""
    return {
        "description": [
            _(
                "The `sidebar` component provides a navigation panel at the window edge. "
                "It can be positioned left, right, or both sides and supports a collapsible drawer mode."
            )
        ],
        "features": [
            _("**Position**: Left, right, or both sides simultaneously."),
            _("**Drawer mode**: Collapsible with open/close functionality."),
            _("**Auto-close**: Optionally closes when the cursor leaves."),
            _("**Mobile support**: Can be hidden on smaller viewports."),
            _("**Categories**: Organizes navigation items into logical groups with icons and badges."),
        ],
    }


@register_component(Component.FOOTER)
def get_footer_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the footer component."""
    return {
        "description": [
            _(
                "The `footer` component renders a three-column page footer with customizable content. "
                "It typically contains navigation links, contact information, legal notices, and copyright information."
            ),
            _("The footer composes the reusable `legal_notice` component for its legal notice line."),
        ],
        "features": [
            _("**Description column**: Application summary with optional logo."),
            _("**Navigation links**: Quick links to important pages."),
            _("**Contact information**: Email, imprint, and privacy policy links."),
            _("**Legal notice**: copyright, license and rights information."),
            _("**Version display**: Optional application version."),
        ],
    }


@register_component(Component.BREADCRUMBS)
def get_breadcrumb_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the breadcrumbs component."""
    return {
        "description": [
            _(
                "The `breadcrumbs` component provides secondary navigation showing the user's location "
                "within the site hierarchy. It is especially useful for websites with deep structure."
            ),
            _(
                "Breadcrumbs should be used consistently across all pages when implemented. "
                "Sites with only two levels (e.g., Overview → Details) typically don't need breadcrumbs."
            ),
        ],
        "features": [
            _("**Hierarchical navigation**: Shows path from home to current page."),
            _("**Optional icons**: Icons can be added to items (typically home icon for first item)."),
            _("**HTMX support**: Optional AJAX navigation for single-page application behavior."),
        ],
    }


@register_component(Component.STEPPER)
def get_stepper_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the step bar component."""
    return {
        "description": [
            _(
                "The `stepper` component displays progress through a multi-step process. "
                "Common use cases include checkout flows, registration wizards, or onboarding sequences."
            )
        ],
        "features": [
            _("**Step states**: Active, success, and failed states with visual indicators."),
            _("**Descriptions**: Optional description text below each step title."),
            _("**Clickable steps**: Steps can link to their respective pages."),
            _("**Current step highlight**: Visual emphasis on the active step."),
        ],
    }


@register_component(Component.MINIMAL_STEPPER)
def get_minimal_stepper_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the minimal step bar component."""
    return {
        "description": [
            _(
                "The `minimal_stepper` component displays a compact progress indicator for multi-step processes. "
                "It provides a simpler alternative to the full stepper component."
            )
        ],
        "features": [
            _("**Compact design**: Icon-based indicator without text labels."),
            _("**Step states**: Active, success, and failed states."),
            _("**Configurable size**: Icon size can be adjusted (xs/s/m/l/xl)."),
            _("**Two configuration modes**: Either provide step items or use step_count/current_step."),
        ],
    }


@register_component(Component.BULLET_POINT_LIST)
def get_bullet_point_list_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the bullet point list component."""
    return {
        "description": [
            _(
                "The `bullet_point_list` component displays a sequence of tasks, process steps, or similar items. "
                "Individual items can include links, descriptions, and completion states."
            )
        ],
        "features": [
            _("**Completion states**: Checkmark indicator for completed items."),
            _("**Current item highlight**: Visual emphasis on the active item."),
            _("**Clickable items**: Items can link to specific pages."),
            _("**Descriptions**: Optional description text below each title."),
            _("**HTMX support**: Optional AJAX navigation."),
        ],
    }


@register_component(Component.ACCORDION)
def get_accordion_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the accordion component."""
    return {
        "description": [
            _(
                "The `accordion` component displays expandable sections for organizing content. "
                "When a section is opened, a URL anchor is automatically set for deep linking."
            )
        ],
        "features": [
            _("**Exclusive mode**: Optionally allow only one section open at a time."),
            _("**URL anchors**: Sections can be expanded via URL hash on page load."),
            _("**Auto-scroll**: Automatically scrolls to expanded section."),
            _("**Initial state**: Sections can be configured as open by default."),
        ],
    }


@register_component(Component.TABS)
def get_tabs_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the tabs component."""
    return {
        "description": [
            _(
                "The `tabs` component organizes content into switchable panels. "
                "Tab content is loaded via HTMX requests, allowing page sections to switch without full page reloads."
            )
        ],
        "features": [
            _("**HTMX integration**: Content loaded asynchronously when tabs are clicked."),
            _("**Active state**: Visual indication of the currently selected tab."),
            _("**Keyboard navigation**: Tab switching via arrow keys."),
            _("**URL-based tabs**: Each tab can load content from a different URL."),
        ],
    }


# =============================================================
#
#   Input Tags
#
# =============================================================


@register_component(Component.BUTTON)
def get_button_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the button component."""
    return {
        "description": [
            _(
                "The `button` component provides customizable buttons in various styles and sizes. "
                "Buttons support icons, tooltips, and can function as links or form submit buttons."
            )
        ],
        "features": [
            _("**Types**: primary, secondary, neutral, info, success, warning, danger, disabled, and link."),
            _("**Sizes**: Five sizes (xs, s, m, l, xl) for different contexts."),
            _("**Design variants**: outline, subtle, and round for visual customization."),
            _("**Icons**: Optionally placed before or after the label, or icon-only mode."),
            _("**HTMX integration**: Native support for asynchronous requests."),
            _("**External links**: Opens in new tab with proper security attributes."),
        ],
    }


@register_component(Component.INPUT_FIELD)
def get_input_field_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the input field component."""
    return {
        "description": [
            _(
                "The `input_field` component provides form input fields with built-in validation styling. "
                "It supports various HTML input types and integrates with Django forms."
            )
        ],
        "features": [
            _("**Input types**: text, email, password, number, tel, url, date, time, color, file, and more."),
            _("**Validation constraints**: min/max values, min/max length attributes."),
            _("**Placeholder**: Hint text displayed when field is empty."),
            _("**States**: Disabled and required states."),
        ],
    }


@register_component(Component.TEXTAREA)
def get_textarea_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the textarea component."""
    return {
        "description": [
            _(
                "The `textarea` component provides a multi-line text input field for longer content. "
                "Use it for comments, descriptions, messages, or any free-form text entry."
            )
        ],
        "features": [
            _("**Configurable size**: Rows and columns can be adjusted."),
            _("**Placeholder**: Hint text displayed when field is empty."),
            _("**States**: Disabled and required states."),
        ],
    }


@register_component(Component.CHECKBOX)
def get_checkbox_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the checkbox component."""
    checkbox_group_url = reverse("component_detail_page_view", args=[Component.CHECKBOX_GROUP.value])
    return {
        "description": [
            _(
                "The `checkbox` component provides a single checkbox input with a label. "
                "For groups of related checkboxes, see [Checkbox Group](%(url)s)."
            )
            % {"url": checkbox_group_url}
        ],
        "features": [
            _("**Checked state**: Can be pre-selected via configuration."),
            _("**Custom value**: Configurable value attribute for form submission."),
            _("**States**: Disabled and required states."),
        ],
    }


@register_component(Component.CHECKBOX_GROUP)
def get_checkbox_group_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the checkbox group component."""
    return {
        "description": [
            _(
                "The `checkbox_group` component renders a group of related checkboxes with optional constraints. "
                "Use it when users need to select multiple options from a set."
            )
        ],
        "features": [
            _("**Minimum/maximum selection**: Enforce selection constraints."),
            _("**Layout options**: Display checkboxes in a row or column."),
            _("**Group label**: Text label displayed above the checkbox elements."),
            _("**Individual states**: Each checkbox can be disabled or pre-selected."),
        ],
    }


@register_component(Component.DROPDOWN)
def get_dropdown_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the dropdown component."""
    return {
        "description": [
            _(
                "The `dropdown` component displays a collapsible menu triggered by a button. "
                "Use it when space is limited or when grouping multiple related actions."
            ),
            _(
                "Dropdown menus should contain no more than seven elements. "
                "Nested dropdown menus (dropdowns within dropdowns) should be avoided."
            ),
        ],
        "features": [
            _("**Trigger button**: Customizable button with optional arrow indicator."),
            _("**Menu items**: Links with optional icons."),
            _("**Click-outside close**: Menu closes when clicking outside."),
        ],
    }


@register_component(Component.RADIO_GROUP)
def get_radio_group_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the radio_group component."""
    return {
        "description": [
            _(
                "The `radio_group` component renders a group of standard radio buttons. "
                "Use it when users must select exactly one option from a set."
            )
        ],
        "features": [
            _("**Layout options**: Display radio buttons in a row or column."),
            _("**Pre-selected option**: Set the initially selected value."),
            _("**Optional icons**: Icons can be added to individual options."),
            _("**Individual states**: Each radio button can be disabled."),
        ],
    }


@register_component(Component.RADIO_BLOCK)
def get_radio_block_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the radio_block component."""
    return {
        "description": [
            _(
                "The `radio_block` component renders radio buttons as a compact button group. "
                "Unlike standard radio buttons, it can trigger requests when the selection changes."
            )
        ],
        "features": [
            _("**Button-style display**: Compact block of connected buttons."),
            _("**HTMX integration**: Trigger requests on selection change."),
            _("**JavaScript callback**: Optional method call on selection change."),
            _("**Icon support**: Buttons can display icons instead of or with text."),
        ],
    }


@register_component(Component.RANGE_SLIDER)
def get_rangle_slider_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the range slider component."""
    return {
        "description": [
            _(
                "The `slider` component provides a range input for selecting numeric values within a defined interval. "
                "It supports both single-value and dual-thumb range selection."
            )
        ],
        "features": [
            _("**Dual-thumb mode**: Select a range with minimum and maximum values."),
            _("**Custom legend**: Text labels displayed below the slider."),
            _("**Legend modes**: `static`, `skip` (hides items when cramped), or `rotate` (vertical text)."),
            _("**Step size**: Configurable increment value."),
            _("**RTL support**: Adapts to right-to-left layouts."),
        ],
    }


@register_component(Component.TOGGLE)
def get_toggle_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the toggle component."""
    return {
        "description": [
            _(
                "The `toggle` component provides a toggle button or switch for binary choices. "
                "It functions like a single checkbox but with a different visual appearance."
            )
        ],
        "features": [
            _("**Switch style**: Optional iOS-style switch appearance."),
            _("**Icon support**: Optional icon displayed on the toggle."),
            _("**JavaScript callback**: Optional method call on state change."),
            _("**States**: Checked, disabled, and required states."),
        ],
    }


@register_component(Component.SELECT)
def get_select_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the select component."""
    return {
        "description": [
            _(
                "The `select` component provides a dropdown selection box for choosing a single value. "
                "It renders a native HTML select element with consistent styling."
            )
        ],
        "features": [
            _("**Options**: List or dictionary of selectable values."),
            _("**Pre-selected option**: Set the initially selected value."),
            _("**Tooltip**: Optional explanation text on hover."),
            _("**States**: Disabled and required states."),
        ],
    }


@register_component(Component.MULTISELECT)
def get_multiselect_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the multiselect component."""
    return {
        "description": [
            _(
                "The `multiselect` component provides a selection box that allows multiple values to be selected. "
                "It includes an integrated search bar for filtering options."
            )
        ],
        "features": [
            _("**Multiple selection**: Select multiple values from the list."),
            _("**Search filter**: Built-in search to find options quickly."),
            _("**Maximum selection**: Optionally limit the number of selections."),
            _("**Quick actions**: Optional 'Select All' and 'Deselect All' buttons."),
        ],
    }


@register_component(Component.CHAT)
def get_chat_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the chat component."""
    return {
        "description": [
            _(
                "The `chat` component provides a simple chat interface with a text input and message area. "
                "Messages are added via HTMX without requiring page reloads."
            )
        ],
        "features": [
            _("**Message input**: Text field with send button."),
            _("**Message area**: Scrollable container for chat history."),
            _("**HTMX integration**: Messages loaded asynchronously via POST requests."),
        ],
    }


# =============================================================
#
#   Popup Tags
#
# =============================================================


@register_component(Component.ALERT)
def get_alert_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the alert component."""
    return {
        "description": [
            _(
                "The `alert` component displays important messages, warnings, or notifications to users. "
                "It is more prominent than an infobox and typically used for system messages."
            )
        ],
        "features": [
            _("**Types**: info, success, warning, and error with appropriate colors."),
            _("**Dismissible**: Optional close button to dismiss the alert."),
            _("**Icon**: Automatic icon based on alert type."),
        ],
    }


@register_component(Component.MODAL)
def get_modal_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the modal component."""
    return {
        "description": [
            _(
                "The `modal` component displays customizable dialogs above the page content. "
                "Use it for confirmation prompts, forms, or displaying additional information."
            )
        ],
        "features": [
            _("**Configurable width**: Adjustable maximum width in rem units."),
            _("**Action buttons**: Customizable buttons at the bottom of the dialog."),
            _("**Title and description**: Header text with optional description."),
            _("**Backdrop click**: Closes modal when clicking outside (configurable)."),
        ],
    }


@register_component(Component.POPOVER)
def get_popover_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the popover component."""
    return {
        "description": [
            _(
                "The `popover` component displays additional content in a floating panel. "
                "Unlike tooltips, popovers remain open until explicitly closed and can contain interactive elements."
            ),
            _("For short explanatory text (1-2 words), use the tooltip component instead."),
        ],
        "features": [
            _("**Persistent display**: Stays open until closed, unlike tooltips."),
            _("**Interactive content**: Can contain buttons, links, and other elements."),
            _("**Positioning**: Appears near the trigger element without disrupting layout."),
        ],
    }


@register_component(Component.TOOLTIP)
def get_tooltip_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the tooltip component."""
    return {
        "description": [
            _(
                "The `tooltip` component displays brief explanatory text when hovering over an element. "
                "Use it to clarify button labels, icons, or other UI elements that might be ambiguous."
            ),
            _(
                "Tooltips should contain only short text (usually one word). "
                "For longer content or interactive elements, use the popover component instead."
            ),
        ],
        "features": [
            _("**Hover-triggered**: Appears on mouse hover, disappears on mouse leave."),
            _("**Non-blocking**: Floats above content without disrupting layout."),
            _("**Auto-positioning**: Positions itself to remain visible within viewport."),
        ],
    }


# =============================================================
#
#   Util Tags
#
# =============================================================


@register_component(Component.INFOBOX)
def get_infobox_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the infobox component."""
    return {
        "description": [
            _(
                "The `infobox` component displays text in a bordered box with subtle emphasis. "
                "It is less prominent than an alert but more visible than plain text."
            )
        ],
        "features": [
            _("**Types**: info, success, warning, and error with appropriate styling."),
            _("**Bordered design**: Visual distinction without strong emphasis."),
        ],
    }


@register_component(Component.CODE_BLOCK)
def get_code_block_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the code block component."""
    return {
        "description": [
            _(
                "The `code_block` component displays source code with syntax highlighting. "
                "It supports virtually all common programming languages and includes a copy-to-clipboard button."
            )
        ],
        "features": [
            _("**Syntax highlighting**: Language-aware code coloring."),
            _("**Copy button**: One-click copy to clipboard."),
            _("**Language support**: Most common and many uncommon programming languages."),
            _("**Line numbers**: Optional line number display."),
        ],
    }


@register_component(Component.LEGAL_NOTICE)
def get_legal_notice_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the copyright notice component."""
    return {
        "description": [
            _("The `legal_notice` component renders a compact, reusable copyright and legal notice line."),
            _(
                "It can be used inside the footer or in other page shells where an application needs a consistent public legal notice."
            ),
        ],
        "features": [
            _("**Configurable parts**: Year, holder, source label, license text, and rights statement."),
            _("**License link**: Optional URL for the license."),
            _("**Custom separator**: Configurable separator between parts (defaults to middle dot)."),
        ],
    }


@register_component(Component.DIFFERENTIATOR)
def get_differentiator_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the differentiator component."""
    return {
        "description": [
            _(
                "The `differentiator` component displays a visual comparison between two text versions. "
                "It is especially helpful for longer texts with only small changes."
            )
        ],
        "features": [
            _("**Visual diff**: Highlights additions, deletions, and changes."),
            _("**Side-by-side view**: Compares original and modified text."),
        ],
    }


@register_component(Component.LOGO)
def get_logo_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the logo component."""
    return {
        "description": [
            _(
                "The `logo` component renders a brand mark from a consistent API. "
                "It supports image assets, SVG assets, and Insight UI icons."
            )
        ],
        "features": [
            _("**Multiple sources**: Image files, SVG files, or icon names."),
            _("**Dark mode variant**: Optional separate image for dark theme."),
            _("**Django static files**: Paths resolved through static file system."),
            _("**Configurable size**: Height and width attributes."),
        ],
    }


@register_component(Component.BRAND_MARK)
def get_brand_mark_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the brand mark component."""
    return {
        "description": [
            _(
                "The `brand_mark` component renders a logo combined with a two-tone wordmark. "
                "Use it when an application needs a recognizable brand identity."
            )
        ],
        "features": [
            _("**Two-tone wordmark**: Primary and secondary text with different colors."),
            _("**Logo integration**: Combines with the logo component."),
            _("**Logo position**: Logo can be placed at start or end."),
            _("**Design tokens**: Uses Insight UI brand color tokens."),
        ],
    }


@register_component(Component.CORNER_RIBBON)
def get_corner_ribbon_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the corner ribbon component."""
    return {
        "description": [
            _(
                "The `corner_ribbon` component displays a decorative diagonal text ribbon positioned in any of the four browser corners. "
                "It's ideal for highlighting new features, displaying status indicators, or adding promotional badges."
            ),
        ],
        "features": [
            _("**Position**: Any of the four browser corners."),
            _("**Color variants**: primary, secondary, info, success, warning, and danger."),
            _("**Non-blocking**: Elements behind the ribbon remain clickable."),
            _("**RTL support**: Adapts to right-to-left layouts."),
        ],
    }


@register_component(Component.PROGRESS_BAR)
def get_progress_bar_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the progress bar component."""
    return {
        "description": [
            _(
                "The `progress_bar` component visualizes the progress of background processes. "
                "It supports static values, polling updates, and server-sent events."
            )
        ],
        "features": [
            _("**Update modes**: Static, polling, or server-sent events (SSE)."),
            _("**Value display**: Optional percentage text."),
            _("**Auto-hide**: Optionally hide when complete."),
            _("**Cancel button**: Optional button to abort the process."),
            _("**Retry button**: Optional button shown on error."),
            _("**Dynamic label**: Label can be updated via JSON response."),
        ],
    }


@register_component(Component.GEO_MAP)
def get_geo_map_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the geo map component."""
    return {
        "description": [
            _(
                "The `geo_map` component displays an interactive geographic map using Leaflet. "
                "It supports markers, circles, and multiple data layers."
            )
        ],
        "features": [
            _("**Marker types**: Standard markers or scaled circles."),
            _("**Multiple datasets**: Display different data layers."),
            _("**Configurable view**: Initial coordinates and zoom level."),
            _("**Popup descriptions**: Optional descriptions on marker click."),
        ],
    }


@register_component(Component.CHART)
def get_charts_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the charts component."""
    return {
        "description": [
            _(
                "The `chart` component displays data visualizations using Apache ECharts. "
                "Charts are configured via Python without writing JavaScript."
            )
        ],
        "features": [
            _("**Chart types**: Line charts and stacked bar charts."),
            _("**Multiple series**: Display multiple data series with legend."),
            _("**Configurable height**: Chart height in rem units."),
            _("**Decal patterns**: Optional patterns for colorblind accessibility."),
        ],
    }


@register_component(Component.LIVE_CONTENT)
def get_live_content_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the live content component."""
    return {
        "description": [
            _(
                "The `live_content` component displays content that refreshes automatically via HTMX polling. "
                "Use it for dashboards, status views, or any content that needs periodic updates."
            )
        ],
        "features": [
            _("**Polling interval**: Configurable refresh interval in seconds."),
            _("**Initial content**: Content displayed before first update."),
            _("**HTMX integration**: Updates via asynchronous requests."),
        ],
    }


@register_component(Component.WEB_SOCKET)
def get_web_socket_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the web socket component."""
    return {
        "description": [
            _(
                "The `websocket` component provides real-time updates via WebSocket connections. "
                "It wraps the HTMX WebSocket extension for HTMX-managed DOM updates."
            ),
            _(
                "By default, the component expects HTML fragments that HTMX can swap into the DOM. "
                "Non-HTML frames are surfaced as browser events for custom handling."
            ),
        ],
        "features": [
            _("**Real-time updates**: Live content via WebSocket connection."),
            _("**HTMX integration**: DOM updates handled by HTMX swap mechanism."),
            _("**Initial content**: Content displayed while connecting."),
        ],
    }


@register_component(Component.BADGE)
def get_badge_description_context() -> dict[str, list[str]]:
    """Serve description context documentation for the badge component."""
    return {
        "description": [
            _(
                "The `badge` component displays compact status or category labels. "
                "Badges are ideal for tags, counters, or short status indicators."
            )
        ],
        "features": [
            _("**Types**: primary, secondary, neutral, info, success, warning, danger, and disabled."),
            _("**Sizes**: Five sizes (xs, s, m, l, xl) for different contexts."),
            _("**Icons**: Optionally placed before or after the label."),
            _("**Tooltips**: Optional hover text for additional context."),
        ],
    }


# =============================================================
#
#   List Tags
#
# =============================================================


@register_component(Component.INFINITE_SCROLL)
def get_infinite_scroll_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the infinite scroll component."""
    return {
        "description": [
            _(
                "The `infinite_scroll` component loads additional content as the user scrolls. "
                "It provides an alternative to traditional pagination for large data sets."
            )
        ],
        "features": [
            _("**Auto-fetch mode**: Automatically load more when scrolling near the bottom."),
            _("**Button mode**: Show a 'Load more' button instead of auto-loading."),
            _("**Scroll threshold**: Configurable pixel distance for triggering loads."),
            _("**HTMX integration**: Content loaded asynchronously."),
        ],
    }


@register_component(Component.PAGINATION)
def get_pagination_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the pagination component."""
    return {
        "description": [
            _(
                "The `pagination` component displays navigation controls for paged data. "
                "It integrates with Django's Paginator and supports items-per-page selection."
            )
        ],
        "features": [
            _("**Page navigation**: First, previous, next, and last page buttons."),
            _("**Page numbers**: Direct access to surrounding pages with ellipsis for gaps."),
            _("**Items per page**: Optional selector to change page size."),
            _("**Django integration**: Works with Django Paginator's Page objects."),
        ],
    }


@register_component(Component.TABLE)
def get_table_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the table component."""
    return {
        "description": [
            _(
                "The `table` component displays data in a clear tabular structure. "
                "It automatically shows a horizontal scrollbar when space is limited."
            )
        ],
        "features": [
            _("**Responsive**: Horizontal scrolling on narrow screens."),
            _("**Caption**: Optional table caption."),
            _("**Empty state**: Configurable message when no data is available."),
            _("**Consistent styling**: Design tokens from the Insight UI theme."),
        ],
    }


# =============================================================
#
#   Filter Tags
#
# =============================================================


@register_component(Component.SEARCH_BAR)
def get_search_bar_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the search bar component."""
    return {
        "description": [
            _(
                "The `search_bar` component provides a text input with a submit button for search queries. "
                "It supports both traditional form submission and HTMX-based search."
            )
        ],
        "features": [
            _("**HTMX integration**: Search results loaded without page reload."),
            _("**Client-side search**: Optional Fuse.js integration for documentation search."),
            _("**Compact mode**: Simplified styling for tight spaces."),
            _("**Pre-filled query**: Initial search term can be set."),
        ],
    }


@register_component(Component.GENERIC_FILTER)
def get_generic_filter_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the generic filter component."""
    return {
        "description": [
            _(
                "The `generic_filter` component renders a filter bar with multiple select dropdowns. "
                "Filters automatically update results via HTMX when changed."
            ),
            _("For more complex filtering needs, consider the Query Builder component."),
        ],
        "features": [
            _("**Multiple filters**: Combine several select dropdowns."),
            _("**HTMX integration**: Results update automatically on filter change."),
            _("**Layout options**: Horizontal or vertical arrangement."),
            _("**Tooltips**: Optional explanation text for each filter."),
        ],
    }


@register_component(Component.QUERY_BUILDER)
def get_query_builder_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the query builder component."""
    return {
        "description": [
            _(
                "The `query_builder` component provides a visual interface for constructing database queries. "
                "It offers more flexibility than simple filters but requires more configuration."
            ),
            _(
                "The query builder receives a list of model fields with allowed operations for each field. "
                "Users can build complex filters using field, operation, and value combinations."
            ),
        ],
        "features": [
            _("**Field types**: text, number, date, datetime, time, boolean, and choice."),
            _("**Operations**: Configurable operators per field (equals, contains, greater than, etc.)."),
            _("**Predefined values**: Optional dropdown values for choice fields."),
            _("**Dynamic conditions**: Add and remove filter conditions."),
        ],
    }


# =============================================================
#
#   Card Tags
#
# =============================================================


@register_component(Component.CARD)
def get_card_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the card component."""
    return {
        "description": [
            _(
                "The `card` component displays content in a 16:9 aspect ratio container. "
                "It combines a title, content, optional image, and action buttons."
            )
        ],
        "features": [
            _("**16:9 aspect ratio**: Business card-style layout."),
            _("**Optional subtitle**: Secondary heading below the title."),
            _("**Background image**: Optional image display."),
            _("**Action buttons**: Configurable buttons for card actions."),
        ],
    }


@register_component(Component.APP_CARD)
def get_app_card_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the app card component."""
    return {
        "description": [
            _(
                "The `app_card` component displays items in a vertically-oriented card layout. "
                "It is designed for overview pages featuring apps, products, demos, or similar items."
            )
        ],
        "features": [
            _("**Square image**: Large image at the top of the card."),
            _("**Tags**: Badge labels for categorization."),
            _("**Clickable title**: Optional link on the title."),
            _("**Action buttons**: Configurable buttons at the bottom."),
        ],
    }


@register_component(Component.FLIP_CARD)
def get_flip_card_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the flip card component."""
    return {
        "description": [
            _(
                "The `flip_card` component displays additional content on its back side. "
                "When the flip button is clicked, the card rotates 180° to reveal more information."
            )
        ],
        "features": [
            _("**3D flip animation**: Smooth rotation effect."),
            _("**Front and back content**: Separate title, content, and actions for each side."),
            _("**Tags**: Badge labels on the front side."),
            _("**Space-efficient**: Shows more content without taking extra space."),
        ],
    }


@register_component(Component.CARD_CAROUSEL)
def get_card_carousel_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the card carousel component."""
    return {
        "description": [
            _(
                "The `carousel` component displays a series of items in a swipeable carousel. "
                "It can show multiple items per slide and supports autoplay."
            )
        ],
        "features": [
            _("**Autoplay**: Optional automatic slide advancement."),
            _("**Navigation dots**: Pagination indicator dots."),
            _("**Slide index**: Optional current/total counter."),
            _("**Items per slide**: Configurable number of visible items."),
        ],
    }


@register_component(Component.IMAGE_CAROUSEL)
def get_image_carousel_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the image carousel component."""
    carousel_url = reverse("component_detail_page_view", args=[Component.CARD_CAROUSEL.value])
    return {
        "description": [
            _(
                "The `image_carousel` component displays images in a swipeable gallery. "
                "It is a variant of the card carousel optimized for image content."
            )
        ],
        "features": [
            _("**Image captions**: Optional description text for each image."),
            _("**Autoplay**: Optional automatic slide advancement."),
            _("**Navigation controls**: Dots, arrows, and optional index counter."),
        ],
        "description_notes_end": [
            {
                "type": "info",
                "message": _(
                    "This documentation applies only to the image carousel. For more information about the carousel in general, see [Card Carousel](%(url)s)."
                )
                % {"url": carousel_url},
            }
        ],
    }


@register_component(Component.THREE_D_CAROUSEL)
def get_3d_carousel_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the 3D carousel component."""
    return {
        "description": [
            _(
                "The `three_d_carousel` component displays items arranged in a 3D circular formation. "
                "It provides a unique visual presentation for showcasing content."
            )
        ],
        "features": [
            _("**3D arrangement**: Items positioned on a circular path."),
            _("**Rotation speed**: Configurable velocity."),
            _("**Camera tilt**: Adjustable viewing angle."),
            _("**Face camera**: Items can always face the viewer."),
        ],
    }


@register_component(Component.TOGGLE_VIEW)
def get_toggle_view_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the toggle view component."""
    return {
        "description": [
            _(
                "The `toggle_view` component allows users to switch between different data presentations. "
                "The same data can be displayed as cards, a table, or a carousel."
            )
        ],
        "features": [
            _("**View modes**: Card, table, and carousel views."),
            _("**View switcher**: Radio button block for switching views."),
            _("**Consistent data**: Same data rendered in different formats."),
        ],
    }


# =============================================================
#
#   Form Tags
#
# =============================================================


@register_component(Component.FORM)
def get_form_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the form component."""
    return {
        "description": [
            _(
                "The `form` component renders complete forms from configuration objects. "
                "It supports various field types and HTMX-based submission without page reloads."
            )
        ],
        "features": [
            _("**Field types**: text, email, password, number, tel, url, date, textarea, and select."),
            _("**Title and description**: Optional form header."),
            _("**Reset button**: Optional button to clear the form."),
            _("**HTMX integration**: Asynchronous form submission."),
        ],
    }
