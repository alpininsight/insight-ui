from django.urls import reverse
from django.utils.translation import gettext as _

from insight_ui.component_details.component_context import register_component
from insight_ui.component_details.components import Component

# =============================================================
#
#   Layout Tags
#
# =============================================================


@register_component(Component.PAGE_HEADER)
def get_page_header_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the page header component."""
    return {
        "a11y": [
            _("The title is rendered as a semantic `<h1>` element."),
            _("The description uses `<p>` elements with sufficient color contrast."),
            _("The decorative background graphic is hidden with `aria-hidden='true'`."),
            _("CTA buttons are implemented as link elements with clear text labels."),
        ]
    }


@register_component(Component.ARTICLE)
def get_article_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the article component."""
    return {
        "a11y": [
            _("The article uses the semantic `<article>` element."),
            _("The column structure is purely visual and does not influence the reading order for screen readers."),
            _("The column separation is visually represented with column-rule."),
        ]
    }


@register_component(Component.HERO)
def get_hero_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the hero component."""
    return {
        "a11y": [
            _("The title is rendered as a semantic `<h1>` element."),
            _("CTA buttons are implemented as link elements with clear labels."),
            _("Background images are denoted with `aria-hidden`."),
        ]
    }


@register_component(Component.PAGE)
def get_page_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the page layout tag."""
    return {
        "a11y": [
            _("The page container is a semantic `<div>` with no specific ARIA role."),
            _("Content within should use appropriate semantic HTML elements."),
            _("Consider wrapping main content in a `<main>` element for landmark navigation."),
        ]
    }


@register_component(Component.HBOX)
def get_hbox_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the hbox layout tag."""
    return {
        "a11y": [
            _("The flex container is rendered as a `<div>` element."),
            _("Visual layout does not affect the reading order for screen readers."),
            _("Ensure content order in the source matches the intended reading order."),
        ]
    }


@register_component(Component.VBOX)
def get_vbox_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the vbox layout tag."""
    return {
        "a11y": [
            _("The flex container is rendered as a `<div>` element."),
            _("Content order in the DOM matches the visual order (top to bottom)."),
            _("Screen readers will announce items in their source order."),
        ]
    }


@register_component(Component.GRID)
def get_grid_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the grid layout tag."""
    return {
        "a11y": [
            _("The grid container is rendered as a `<div>` element with CSS Grid."),
            _("Content order in the DOM matches the visual reading order."),
            _("Screen readers will announce items in their source order, regardless of visual layout."),
        ]
    }


@register_component(Component.SPACER)
def get_spacer_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the spacer layout tag."""
    return {
        "a11y": [
            _("The spacer is a purely presentational empty element."),
            _("Screen readers will skip over the spacer element."),
            _("Use CSS margins/padding instead when possible to avoid extra DOM elements."),
        ]
    }


@register_component(Component.DIVIDER)
def get_divider_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the divider layout tag."""
    return {
        "a11y": [
            _("The divider is a purely visual element with no semantic meaning."),
            _("Screen readers will skip over the divider element."),
            _("Consider using `<hr>` with `role='separator'` for semantic section breaks."),
        ]
    }


# =============================================================
#
#   Navigation Tags
#
# =============================================================


@register_component(Component.NAVBAR)
def get_navbar_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the navbar component."""
    return {
        "a11y": [
            _("A skip link before the navigation allows keyboard users to jump directly to the main content."),
            _("The `<nav>` element has `role='navigation'` and `aria-label` for landmark identification."),
            _("The mobile menu toggle has `aria-expanded`, `aria-controls`, and `aria-label` attributes."),
            _("Active navigation links use `aria-current='page'`."),
            _("External links include `rel='noopener'` for security."),
            _("The brand link uses `aria-label` for accessible naming when configured."),
        ]
    }


@register_component(Component.SIDEBAR)
def get_sidebar_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the sidebar component."""
    return {
        "a11y": [
            _("The sidebar uses an `<aside>` element with `role='complementary'` for landmark navigation."),
            _("The sidebar has an `aria-label` describing its purpose ('Side navigation')."),
            _("Open and close buttons have descriptive `aria-label` attributes."),
            _("Navigation uses semantic `<nav>` and nested `<ul>`/`<li>` structure."),
            _("The drawer variant has a close button to be accessible via keyboard."),
            _("Focus trapping is implemented when the drawer is open."),
            _("**TODO: Add Escape key handler to close the drawer.**"),
            _("**TODO: Return focus to the trigger element when drawer closes.**"),
        ]
    }


@register_component(Component.FOOTER)
def get_footer_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the footer component."""
    return {
        "a11y": [
            _("The footer uses the semantic `<footer>` element."),
            _("The headings of the columns use `<h4>` tags so that a screen reader can navigate between them."),
            _("The listing of the links uses a semantically correct `<ul>` tag with corresponding `<li>` tags."),
            _("**TODO: Add `role='contentinfo'` to the footer element for landmark navigation.**"),
        ]
    }


@register_component(Component.BREADCRUMBS)
def get_breadcrumb_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the breadcrumbs component."""
    return {
        "a11y": [
            _("The component uses a `<nav>` tag with the corresponding `aria-label='Breadcrumb'`."),
            _("The active element has the attribute `aria-current='page'`."),
            _("The breadcrumb items are structured as a semantic list (`<ul>`, `<li>`)."),
            _("**TODO: The separator chevron icons should have `aria-hidden='true'` since they are decorative.**"),
        ]
    }


@register_component(Component.STEPPER)
def get_stepper_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the step bar component."""
    return {
        "a11y": [
            _("The component uses a semantic `<ol>` element for the ordered step list."),
            _("Step numbers are displayed as text and readable by screen readers."),
            _("The separator SVG arrows are hidden with `aria-hidden='true'`."),
            _("Step status (success, failed, current) is communicated through text labels."),
            _("**TODO: Add `aria-current='step'` to the current step.**"),
            _("**TODO: The decorative status icons should have `aria-hidden='true'`.**"),
        ]
    }


@register_component(Component.MINIMAL_STEPPER)
def get_minimal_stepper_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the minimal step bar component."""
    return {
        "a11y": [
            _("The status icons (tick, danger, gear) convey step state visually."),
            _("**TODO: Add `aria-label` to each step to describe its state (e.g., 'Step 1: Completed').**"),
            _("**TODO: Add `role='progressbar'` or `role='list'` with `aria-current='step'` for the active step.**"),
            _("**TODO: The decorative icons should have `aria-hidden='true'`.**"),
        ]
    }


@register_component(Component.BULLET_POINT_LIST)
def get_bullet_point_list_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the bullet point list component."""
    return {
        "a11y": [
            _("The component uses a semantic `<ol>` element for the ordered list structure."),
            _("The current step is marked with `aria-current='step'`."),
            _("The connecting lines between items are hidden from screen readers using `aria-hidden='true'`."),
            _("**TODO: The decorative bullet icons and graphical elements should have `aria-hidden='true'`.**"),
        ]
    }


@register_component(Component.ACCORDION)
def get_accordion_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the accordion component."""
    return {
        "a11y": [
            _("The currently active element is labeled with `aria-expanded='true'`."),
            _("The header row is equipped with `aria-controls`, establishing the relationship to the container below."),
            _("The container additionally has the attribute `aria-labelledby`."),
            _("The container has the `role='region'` for ease of navigation."),
            _("Full keyboard navigation: Arrow Up/Down to move between headers, Home/End to jump to first/last."),
            _("Focus is moved programmatically when navigating with arrow keys."),
            _("A visible focus indicator (`focus-visible:ring`) is provided for keyboard navigation."),
            _("**TODO: The decorative chevron icon should have `aria-hidden='true'`.**"),
        ]
    }


@register_component(Component.TABS)
def get_tabs_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the tabs component."""
    return {
        "a11y": [
            _("Full ARIA tabs pattern: `role='tablist'`, `role='tab'`, `role='tabpanel'`."),
            _("The tablist has an `aria-label` describing its purpose."),
            _("Tabs use `aria-controls` to associate with their panels."),
            _("The tabpanel has `aria-label` for accessible naming."),
            _("Full keyboard navigation: Arrow Left/Right to move between tabs, Home/End to jump to first/last."),
            _("`aria-selected` is dynamically updated to indicate the active tab."),
            _("Focus is moved programmatically when navigating with arrow keys."),
            _("**TODO: Add `tabindex` management (`0` for active, `-1` for inactive tabs).**"),
        ]
    }


# =============================================================
#
#   Input Tags
#
# =============================================================


@register_component(Component.BUTTON)
def get_button_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the button component."""
    return {
        "a11y": [
            _("Buttons that only have an icon and no text should have a descriptive `aria-label`."),
            _("A button should, like the rest of the website, always be operable and usable via keyboard."),
            _(
                "For correct semantic compliance, a `<button>` is always preferable to an interactive `<div>` container."
            ),
        ]
    }


@register_component(Component.INPUT_FIELD)
def get_input_field_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the input field component."""
    return {
        "a11y": [
            _("The `<label>` and its associated `<input>` are linked using `for` / `id`."),
            _("Required fields display an asterisk with `aria-label='Required'` for screen reader context."),
            _("The `required` and `disabled` attributes are properly set on the input element."),
            _("Explanation tooltips provide additional context via `data-insight-tooltip`."),
        ]
    }


@register_component(Component.TEXTAREA)
def get_textarea_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the textarea component."""
    return {
        "a11y": [
            _("The `<label>` and its associated `<textarea>` are linked using `for` / `id`."),
            _("Required fields display an asterisk with `aria-label='Required'` for screen reader context."),
            _("The `required` and `disabled` attributes are properly set on the textarea element."),
            _("Explanation tooltips provide additional context via `data-insight-tooltip`."),
        ]
    }


@register_component(Component.CHECKBOX)
def get_checkbox_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the checkbox component."""
    return {
        "a11y": [
            _("The `<label>` wraps the `<input>` element, creating an implicit association (label-wrapping pattern)."),
            _("The checkbox supports `disabled` state which is properly communicated to assistive technologies."),
        ]
    }


@register_component(Component.CHECKBOX_GROUP)
def get_checkbox_group_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the checkbox group component."""
    checkbox_url = reverse("component_detail_page_view", args=[Component.CHECKBOX.value])
    return {
        "a11y": [
            _("See [Checkbox](%(url)s).") % {"url": checkbox_url},
            _("The group label is rendered as visible text above the checkboxes."),
            _(
                "**TODO: Use `role='group'` with `aria-labelledby` or `<fieldset>`/`<legend>` for better group semantics.**"
            ),
            _("**TODO: Announce constraint violations (min/max reached) to screen readers.**"),
        ]
    }


@register_component(Component.DROPDOWN)
def get_dropdown_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the dropdown component."""
    return {
        "a11y": [
            _("Icons displayed in links or menu items are decorative."),
            _("The dropdown closes when clicking outside."),
            _("**TODO: Add `aria-expanded` to the trigger button.**"),
            _("**TODO: Add `aria-haspopup='menu'` and `role='menu'` to the dropdown container.**"),
            _("**TODO: Add `role='menuitem'` to dropdown items.**"),
            _("**TODO: Add keyboard navigation with Arrow Up/Down keys.**"),
            _("**TODO: Add Escape key handler to close the dropdown.**"),
            _("**TODO: The chevron icon should have `aria-hidden='true'`.**"),
        ]
    }


@register_component(Component.RADIO_GROUP)
def get_radio_group_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the radio_group component."""
    return {
        "a11y": [
            _("The `<label>` wraps the `<input>` element, creating an implicit association."),
            _("The group label is rendered as visible text above the radio buttons."),
            _("The component supports keyboard navigation using the arrow keys (up/down, right/left)."),
            _(
                "**TODO: Use `role='radiogroup'` with `aria-labelledby` or `<fieldset>`/`<legend>` for better group semantics.**"
            ),
        ]
    }


@register_component(Component.RADIO_BLOCK)
def get_radio_block_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the radio_block component."""
    return {
        "a11y": [
            _("Radio inputs use `sr-only` to hide the native control while keeping it accessible."),
            _("The `<label>` and `<input>` are linked using `for` / `id`."),
            _("Labels can use `aria-label` when in screen-reader-only mode."),
            _("The component supports keyboard navigation using the arrow keys (up/down, right/left)."),
            _("Visible focus indicators are provided via `peer-focus:outline`."),
        ]
    }


@register_component(Component.RANGE_SLIDER)
def get_rangle_slider_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the range slider component."""
    return {
        "a11y": [
            _("The `<label>` and its associated `<input>` are linked using `for` / `id`."),
            _("The component supports keyboard navigation using the arrow keys (up/down, right/left)."),
            _(
                "ARIA attributes `aria-valuemin`, `aria-valuemax`, and `aria-valuenow` are set on each input "
                "and updated dynamically for screen reader announcements."
            ),
            _(
                "In dual-thumb mode, both inputs have descriptive `aria-label` attributes (e.g., 'Label - Minimum', 'Label - Maximum') "
                'and are grouped using `role="group"` with `aria-labelledby`.'
            ),
            _("Visible focus indicators are provided for keyboard navigation (`focus-visible` ring)."),
            _('Decorative elements (track, legend) are hidden from assistive technologies using `aria-hidden="true"`.'),
        ]
    }


@register_component(Component.TOGGLE)
def get_toggle_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the toggle component."""
    return {
        "a11y": [
            _("The checkbox input uses `sr-only` to hide the native control while keeping it accessible."),
            _("The `<label>` and its associated `<input>` are linked using `for` / `id`."),
            _("The visual toggle track uses CSS `peer-checked` states to indicate selection."),
            _("Visible focus indicators are provided via `peer-focus:outline`."),
            _("The `disabled` attribute is properly set and communicated to assistive technologies."),
        ]
    }


@register_component(Component.SELECT)
def get_select_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the select component."""
    return {
        "a11y": [
            _("The `<label>` and its associated `<select>` are linked using `for` / `id`."),
            _(
                "Uses the native `<select>` element which has built-in keyboard support and screen reader compatibility."
            ),
            _("Required fields display an asterisk with `aria-label='Required'` for screen reader context."),
            _(
                "Disabled options use the `disabled` attribute which is properly communicated to assistive technologies."
            ),
            _("Explanation tooltips provide additional context via `data-insight-tooltip`."),
        ]
    }


@register_component(Component.MULTISELECT)
def get_multiselect_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the multiselect component."""
    return {
        "a11y": [
            _("The label is linked to the combobox via `aria-labelledby`."),
            _(
                "Full ARIA combobox pattern: `role='combobox'`, `aria-haspopup='listbox'`, `aria-expanded`, `aria-owns`, `aria-activedescendant`."
            ),
            _("Options use `role='option'` with `aria-selected` and unique IDs."),
            _("A live region (`aria-live='polite'`) announces selection changes to screen readers."),
            _("The search input has an accessible label for filtering options."),
            _(
                "Full keyboard navigation: Arrow Up/Down to navigate options, Enter to select, Backspace to remove last selection."
            ),
            _("Escape and Tab keys close the dropdown."),
            _("Focus is maintained in the search input after selection changes."),
            _("`aria-activedescendant` is updated to indicate the currently focused option."),
        ]
    }


@register_component(Component.CHAT)
def get_chat_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the chat component."""
    return {
        "a11y": [
            _("The `<label>` and its associated `<input>` are linked using `for` / `id`."),
            _("The submit button has a descriptive text label."),
            _("**TODO: The response container should have `aria-live='polite'` to announce new messages.**"),
        ]
    }


# =============================================================
#
#   Popup Tags
#
# =============================================================


@register_component(Component.ALERT)
def get_alert_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the alert component."""
    return {
        "a11y": [
            _("The alert box has the attribute `role='alert'` to support screen readers."),
            _("The close button is accessible via keyboard and has a corresponding `aria-label`."),
            _(
                "**TODO: The type icons (info, warning, error, success) should have `aria-hidden='true'` since they are decorative.**"
            ),
        ]
    }


@register_component(Component.MODAL)
def get_modal_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the modal component."""
    return {
        "a11y": [
            _("Full ARIA dialog pattern: `role='dialog'`, `aria-modal='true'`, `tabindex='-1'`."),
            _("The title is linked via `aria-labelledby` pointing to the `<h2>` element."),
            _("The description is linked via `aria-describedby` when provided."),
            _("The close button has a descriptive `aria-label` ('Close')."),
            _("The backdrop is clickable to dismiss the modal."),
            _("Action buttons have descriptive text labels."),
            _("Focus trapping is implemented to keep keyboard focus within the modal."),
            _("Page scroll is blocked while the modal is open."),
            _("**TODO: Add Escape key handler to close the modal.**"),
            _("**TODO: Return focus to the trigger element when modal closes.**"),
        ]
    }


@register_component(Component.POPOVER)
def get_popover_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the popover component."""
    return {
        "a11y": [
            _("The popover closes when clicking outside (for click-triggered popovers with `auto-close`)."),
            _("Position updates on scroll to remain visible."),
            _("**TODO: Add `role='dialog'` or appropriate ARIA role to the popover.**"),
            _("**TODO: Add `aria-expanded` on the trigger button.**"),
            _("**TODO: Add `aria-controls` on the trigger pointing to the popover ID.**"),
            _("**TODO: Add keyboard support - toggle on Enter/Space, close on Escape.**"),
            _("**TODO: Implement focus trapping when popover contains interactive elements.**"),
        ]
    }


@register_component(Component.TOOLTIP)
def get_tooltip_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the tooltip component."""
    return {
        "a11y": [
            _("Tooltip content is readable text."),
            _("The tooltip uses `role='tooltip'` for proper screen reader identification."),
            _("The tooltip closes when clicking outside (for click-triggered tooltips)."),
            _("Position updates on scroll to remain visible."),
            _("**TODO: Add `aria-describedby` on the trigger element pointing to the tooltip ID.**"),
            _("**TODO: Add keyboard support - show tooltip on focus, hide on blur.**"),
            _("**TODO: Add Escape key to dismiss the tooltip.**"),
        ]
    }


# =============================================================
#
#   Util Tags
#
# =============================================================


@register_component(Component.INFOBOX)
def get_infobox_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the infobox component."""
    return {
        "a11y": [
            _(
                "The info type (Info, Warning, Error, Success) is rendered as bold text and announced by screen readers."
            ),
            _("The message content supports Markdown formatting."),
            _("**TODO: Add `role='note'` for informational boxes or `role='alert'` for warnings/errors.**"),
        ]
    }


@register_component(Component.CODE_BLOCK)
def get_code_block_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the code block component."""
    return {
        "a11y": [
            _("The component is accessible via keyboard."),
            _("The copy button includes descriptive text ('Copy') alongside the icon."),
            _("The copy icon SVG has `aria-hidden='true'` since it is decorative."),
            _("Visual feedback is provided after copying ('copied' text appears temporarily)."),
        ]
    }


@register_component(Component.COPYRIGHT_NOTICE)
def get_copyright_notice_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the copyright notice component."""
    return {
        "a11y": [
            _("The legal notice is rendered as text so it remains readable by screen readers."),
            _("Decorative separators are marked with `aria-hidden='true'`."),
            _("A license URL is rendered as a normal accessible link when provided."),
        ]
    }


@register_component(Component.DIFFERENTIATOR)
def get_differentiator_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the differentiator component."""
    return {"a11y": [_("**TODO: Determine if this component requires accessibility documentation.**")]}


@register_component(Component.LOGO)
def get_logo_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the logo component."""
    return {
        "a11y": [
            _("Image and SVG logos use the provided `alt` text. Empty `alt` values make them decorative."),
            _("Icon logos receive `role='img'` and an accessible label when `alt` is provided."),
        ]
    }


@register_component(Component.BRAND_LOCKUP)
def get_brand_lockup_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the brand lockup component."""
    return {
        "a11y": [
            _("The wordmark is rendered as readable text so assistive technologies can announce the brand name."),
            _("The decorative public icon is hidden from assistive technologies with `aria-hidden='true'`."),
            _(
                "When used inside the navbar, provide `brand.aria_label` or `brand.title` so the surrounding link has a clear accessible name."
            ),
        ]
    }


@register_component(Component.CORNER_RIBBON)
def get_corner_ribbon_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the corner ribbon component."""
    return {
        "a11y": [
            _("The ribbon text is readable by screen readers."),
            _("The component uses `pointer-events-none` to prevent interaction interference."),
            _("**TODO: Consider adding `role='status'` or `aria-label` for better context.**"),
        ]
    }


@register_component(Component.PROGRESS_BAR)
def get_progress_bar_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the progress bar component."""
    return {
        "a11y": [
            _("**TODO: Add `role='progressbar'` to the progress element.**"),
            _("**TODO: Add `aria-valuenow`, `aria-valuemin`, and `aria-valuemax` attributes.**"),
            _("**TODO: Add `aria-label` or `aria-labelledby` to describe what is progressing.**"),
            _("**TODO: Use `aria-live='polite'` to announce progress updates.**"),
        ]
    }


@register_component(Component.GEO_MAP)
def get_geo_map_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the geo map component."""
    return {
        "a11y": [
            _("The map attribution link to OpenStreetMap is accessible."),
            _("Marker popups display title and description as readable text."),
            _("**TODO: Add `role='application'` or `role='img'` to the map container with `aria-label`.**"),
            _("**TODO: Enable Leaflet keyboard navigation for markers.**"),
            _("**TODO: Provide a text-based list of locations as an alternative for screen readers.**"),
            _("**TODO: Ensure map controls have accessible labels.**"),
        ]
    }


@register_component(Component.CHART)
def get_charts_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the charts component."""
    return {
        "a11y": [
            _("The chart title is set via ECharts configuration and rendered as part of the chart."),
            _("ECharts provides built-in tooltip support for data exploration."),
            _("**TODO: Enable ECharts `aria` option for automatic ARIA labels and descriptions.**"),
            _("**TODO: Add `role='img'` and `aria-label` to the chart container describing the data.**"),
            _("**TODO: Provide a data table alternative for screen reader users.**"),
            _("**TODO: Ensure sufficient color contrast and consider colorblind-friendly palettes.**"),
        ]
    }


@register_component(Component.LIVE_CONTENT)
def get_live_content_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the live content component."""
    return {
        "a11y": [
            _("The container has `aria-live='polite'` to announce content updates to screen readers."),
            _("The `aria-busy` attribute is dynamically updated during content loading."),
            _("The loading spinner has `role='status'` and the visual indicator is hidden with `aria-hidden='true'`."),
            _("The component uses `tabindex='-1'` to allow programmatic focus after updates."),
        ]
    }


@register_component(Component.WEB_SOCKET)
def get_web_socket_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the web socket component."""
    return {
        "a11y": [
            _("The connection status element has `role='status'` and `aria-live='polite'` to announce changes."),
            _(
                "Status messages are readable text that describe the connection state (Connected, Disconnected, Error, Connecting)."
            ),
            _(
                "Custom events are dispatched for status changes and messages, allowing host applications to implement accessible UI."
            ),
            _("**TODO: Add `aria-live` to the output container to announce new messages.**"),
            _("**TODO: Consider adding `role='log'` to the output container for message history.**"),
        ]
    }


@register_component(Component.BADGE)
def get_badge_a11y_context() -> dict[str, list[str]]:
    """Serve a11y context documentation for the badge component."""
    return {"a11y": []}


# =============================================================
#
#   List Tags
#
# =============================================================


@register_component(Component.INFINITE_SCROLL)
def get_infinite_scroll_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the infinite scroll component."""
    return {
        "a11y": [
            _("The 'Load more' button provides a manual alternative to automatic loading."),
            _("Content items use semantic `<h3>` headings for screen reader navigation."),
            _("**TODO: Add `aria-live='polite'` to announce when new content is loaded.**"),
            _("**TODO: Add `role='feed'` to the container for infinite scroll semantics.**"),
            _(
                "**TODO: The loading spinner should have `role='status'` with `aria-hidden='true'` on the visual element.**"
            ),
        ]
    }


@register_component(Component.PAGINATION)
def get_pagination_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the pagination component."""
    return {
        "a11y": [
            _("Navigation buttons use `sr-only` text to provide descriptive labels for screen readers."),
            _("Disabled buttons explain their state (e.g., 'Deactivated because there are no more previous pages')."),
            _("The current page information is displayed as text on mobile devices."),
            _("**TODO: Add `role='navigation'` and `aria-label='Pagination'` to the container.**"),
            _("**TODO: Mark the current page with `aria-current='page'`.**"),
            _("**TODO: Add support for arrow key navigation (right/left).**"),
        ]
    }


@register_component(Component.TABLE)
def get_table_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the table component."""
    return {
        "a11y": [
            _("Uses semantic `<table>`, `<thead>`, `<tbody>`, `<tfoot>`, `<th>`, `<td>` elements."),
            _("Header cells use `scope='col'` to associate with their columns."),
            _("An optional `<caption>` element describes the table's purpose."),
            _("Empty state message is displayed in a `<tfoot>` element."),
            _(
                "**TODO: For sortable columns, add `aria-sort` to indicate sort direction (ascending/descending/none).**"
            ),
            _("**TODO: The sort icons should have `aria-hidden='true'` since they are decorative.**"),
        ]
    }


# =============================================================
#
#   Filter Tags
#
# =============================================================


@register_component(Component.SEARCH_BAR)
def get_search_bar_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the search bar component."""
    return {
        "a11y": [
            _("The search input uses `type='search'` for semantic meaning and browser optimizations."),
            _("A visually hidden `<label>` with `sr-only` is linked to the input via `for`/`id`."),
            _("The search icon is decorative and hidden from assistive technologies."),
            _("The submit button has a descriptive text label when displayed."),
            _("**TODO: Add `role='search'` to the form element for landmark navigation.**"),
        ]
    }


@register_component(Component.GENERIC_FILTER)
def get_generic_filter_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the generic filter component."""
    return {
        "a11y": [
            _("The component uses a semantic `<form>` element."),
            _("Filter fields use the Select component with proper label associations."),
            _("**TODO: Add `role='search'` to the form element for better semantic meaning.**"),
        ]
    }


@register_component(Component.QUERY_BUILDER)
def get_query_builder_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the query builder component."""
    return {
        "a11y": [
            _("**TODO: Add ARIA labels to describe the query builder's purpose.**"),
            _("**TODO: Ensure all form controls have proper label associations.**"),
            _("**TODO: Add keyboard navigation for adding/removing query conditions.**"),
            _("**TODO: Use `aria-live` to announce query changes.**"),
        ]
    }


# =============================================================
#
#   Card Tags
#
# =============================================================


@register_component(Component.CARD)
def get_card_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the card component."""
    return {
        "a11y": [
            _("The card title uses a semantic `<h3>` heading for screen reader navigation."),
            _("Images include an `alt` attribute for screen reader descriptions."),
            _("External links use `rel='noopener'` for security."),
            _("Action buttons have descriptive text labels."),
            _("**TODO: Consider adding `role='article'` or wrapping in `<article>` element.**"),
        ]
    }


@register_component(Component.APP_CARD)
def get_app_card_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the app card component."""
    return {
        "a11y": [
            _("Images include an `alt` attribute for screen reader descriptions."),
            _("Disabled actions use `aria-disabled='true'` to communicate their state."),
            _("External links use `rel='noopener'` for security."),
            _("**TODO: Use unique IDs instead of fixed `id='card-title'` to avoid duplicate IDs.**"),
            _("**TODO: Consider using semantic heading elements for the title.**"),
        ]
    }


@register_component(Component.FLIP_CARD)
def get_flip_card_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the flip card component."""
    return {
        "a11y": [
            _("Images include an `alt` attribute for screen reader descriptions."),
            _("Disabled actions use `aria-disabled='true'` to communicate their state."),
            _("External links use `rel='noopener'` for security."),
            _("**TODO: The flip animation may not be accessible via keyboard. Consider adding a button to flip.**"),
            _(
                "**TODO: The back content is hidden visually but may still be read by screen readers. Use `aria-hidden` on inactive side.**"
            ),
            _("**TODO: Use unique IDs instead of fixed `id='card-title'` to avoid duplicate IDs.**"),
        ]
    }


@register_component(Component.CARD_CAROUSEL)
def get_card_carousel_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the card carousel component."""
    return {
        "a11y": [
            _("Navigation buttons use `sr-only` text to provide descriptive labels for screen readers."),
            _("Pagination dots include `sr-only` text describing which page they navigate to."),
            _("The carousel is accessible via keyboard (navigation buttons)."),
            _("Touch gestures (swipe) are supported for mobile navigation."),
            _("**TODO: Add `role='region'` with `aria-roledescription='carousel'` to the container.**"),
            _("**TODO: Add `aria-label` to describe the carousel's purpose.**"),
            _("**TODO: Add keyboard navigation with Arrow Left/Right keys.**"),
            _("**TODO: Pause autoplay on hover/focus for users who need more time.**"),
        ]
    }


@register_component(Component.IMAGE_CAROUSEL)
def get_image_carousel_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the image carousel component."""
    carousel_url = reverse("component_detail_page_view", args=[Component.CARD_CAROUSEL.value])
    return {
        "a11y": [
            _("Inherits accessibility features from [Card Carousel](%(url)s).") % {"url": carousel_url},
            _("Images include `alt` attributes for screen reader descriptions."),
            _("Description overlays are rendered as readable text."),
            _("**TODO: Ensure all images have meaningful `alt` text describing the content.**"),
        ]
    }


@register_component(Component.THREE_D_CAROUSEL)
def get_3d_carousel_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the 3D carousel component."""
    return {
        "a11y": [
            _("Navigation buttons include descriptive text ('Back', 'Next') alongside icons."),
            _("The carousel is accessible via keyboard (navigation buttons)."),
            _("Responsive: animation distance adapts to screen size for better visibility."),
            _("**TODO: Add `role='region'` with `aria-roledescription='carousel'` to the container.**"),
            _("**TODO: Add `aria-label` to describe the carousel's purpose.**"),
            _("**TODO: Add keyboard navigation with Arrow Left/Right keys.**"),
            _("**TODO: Respect `prefers-reduced-motion` - 3D transforms may cause motion sickness.**"),
        ]
    }


@register_component(Component.TOGGLE_VIEW)
def get_toggle_view_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the toggle view component."""
    radio_block_url = reverse("component_detail_page_view", args=[Component.RADIO_BLOCK.value])
    return {
        "a11y": [
            _("The view switcher uses the [Radio Block](%(url)s) component which provides keyboard navigation.")
            % {"url": radio_block_url},
            _("The content area updates dynamically based on the selected view (carousel, card, table)."),
            _("**TODO: Add `aria-live='polite'` to announce view changes to screen readers.**"),
            _("**TODO: Move focus to the content area after view change for better UX.**"),
        ]
    }


# =============================================================
#
#   Form Tags
#
# =============================================================


@register_component(Component.FORM)
def get_form_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the form component."""
    return {
        "a11y": [
            _("The component uses the semantic `<form>` element."),
            _("Form fields use the corresponding input components with proper label associations."),
            _("Submit and reset buttons have descriptive text labels."),
            _("**TODO: The loading indicator should have `role='status'` and `aria-live='polite'`.**"),
            _("**TODO: The loading spinner SVG should have `aria-hidden='true'`.**"),
        ]
    }
