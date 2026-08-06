"""Accessibility documentation context for UI components."""

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


@register_component(Component.STATUS_SCREEN)
def get_status_screen_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the status screen component."""
    return {
        "a11y": [
            _("The status title is rendered as a semantic `<h1>` element."),
            _("The decorative status icon is hidden from assistive technologies with `aria-hidden`."),
            _("Error notices use `role='alert'`; all other notices use `role='status'`."),
            _("Actions are rendered through the standard button component with clear labels."),
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


@register_component(Component.SECTION)
def get_section_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the section layout tag."""
    return {
        "a11y": [
            _("The `<section>` element is a landmark region that screen readers announce."),
            _("Use `aria_label` or `aria_labelledby` to provide a descriptive name for the section."),
            _("Each section should ideally have a heading (`<h2>`-`<h6>`) as its first child."),
            _("Sections create a document outline that assistive technologies use for navigation."),
        ]
    }


@register_component(Component.SURFACE)
def get_surface_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the surface layout tag."""
    return {
        "a11y": [
            _("Static surfaces (`<div>`) are presentational and have no semantic meaning."),
            _("Clickable surfaces (`<a>`) are fully keyboard accessible via Tab and Enter."),
            _("When used as a link, ensure the surface contains descriptive text or an `aria-label`."),
            _("The `group-hover:` utility classes provide visual feedback on hover for clickable surfaces."),
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
            _("Pressing Escape closes the drawer."),
            _("Focus returns to the trigger element when the drawer closes."),
        ]
    }


@register_component(Component.FOOTER)
def get_footer_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the footer component."""
    return {
        "a11y": [
            _("The footer uses the semantic `<footer>` element with `role='contentinfo'` for landmark navigation."),
            _("The headings of the columns use `<h4>` tags so that a screen reader can navigate between them."),
            _("The listing of the links uses a semantically correct `<ul>` tag with corresponding `<li>` tags."),
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
            _("Separator chevron icons inherit `aria-hidden='true'` from the icon component."),
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
            _("Decorative status icons inherit `aria-hidden='true'` from the icon component."),
            _("The current step is marked with `aria-current='step'`."),
        ]
    }


@register_component(Component.MINIMAL_STEPPER)
def get_minimal_stepper_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the minimal step bar component."""
    return {
        "a11y": [
            _("The component has `role='group'` with `aria-label='Progress indicator'`."),
            _("Each step has an `aria-label` describing its position and state (e.g., 'Step 1: Completed')."),
            _("The active step is marked with `aria-current='step'`."),
            _("Decorative icons inherit `aria-hidden='true'` from the icon component."),
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
            _("Bullet icons inherit `aria-hidden='true'` from the icon component."),
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
            _("The decorative chevron icon inherits `aria-hidden='true'` from the icon component."),
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
            _("`tabindex` management: active tab has `0`, inactive tabs have `-1`."),
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
            _("The group uses `<fieldset>` with `<legend>` for proper grouping semantics."),
            _("The legend text is announced by screen readers as the group label."),
            _(
                "Constraint violations (min/max reached) are announced via `aria-live='assertive'` "
                "to inform screen reader users why their action was prevented."
            ),
        ]
    }


@register_component(Component.DROPDOWN)
def get_dropdown_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the dropdown component."""
    return {
        "a11y": [
            _("Icons displayed in links or menu items are decorative."),
            _("The dropdown closes when clicking outside."),
            _("Full keyboard navigation: Arrow Up/Down to navigate items, Home/End to jump to first/last."),
            _("Pressing Escape closes the dropdown and returns focus to the trigger."),
            _("The chevron icon inherits `aria-hidden='true'` from the icon component."),
            _("The trigger button has `aria-expanded`, `aria-haspopup='menu'`, and `aria-controls`."),
            _("The dropdown container has `role='menu'` and items have `role='menuitem'`."),
        ]
    }


@register_component(Component.RADIO_GROUP)
def get_radio_group_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the radio_group component."""
    return {
        "a11y": [
            _("The `<label>` wraps the `<input>` element, creating an implicit association."),
            _("The group uses `<fieldset>` with `<legend>` for proper grouping semantics."),
            _("The legend text is announced by screen readers as the group label."),
            _("The component supports keyboard navigation using the arrow keys (up/down, right/left)."),
        ]
    }


@register_component(Component.RADIO_BLOCK)
def get_radio_block_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the radio_block component."""
    return {
        "a11y": [
            _("The group uses `<fieldset>` with `<legend>` for proper grouping semantics."),
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
            _("The response container has `aria-live='polite'` to announce new messages to screen readers."),
            _(
                "The `aria-atomic='false'` attribute ensures only new messages are announced, "
                "not the entire chat history."
            ),
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
            _("Type icons (info, warning, error, success) inherit `aria-hidden='true'` from the icon component."),
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
            _("Pressing Escape closes the modal."),
            _("Focus returns to the trigger element when the modal closes."),
        ]
    }


@register_component(Component.POPOVER)
def get_popover_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the popover component."""
    return {
        "a11y": [
            _("The popover has `role='dialog'` for proper screen reader identification."),
            _("The trigger has `aria-expanded` and `aria-controls` for proper state communication."),
            _("The popover closes when clicking outside (for click-triggered popovers with `auto-close`)."),
            _("Position updates on scroll to remain visible."),
            _("Keyboard support: Enter/Space toggles click-triggered popovers, Escape closes."),
            _("Focus can move into the popover for interactive content (buttons, links)."),
        ]
    }


@register_component(Component.TOOLTIP)
def get_tooltip_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the tooltip component."""
    return {
        "a11y": [
            _("Tooltip content is readable text."),
            _("The tooltip uses `role='tooltip'` for proper screen reader identification."),
            _("The trigger element has `aria-describedby` pointing to the tooltip for association."),
            _("The tooltip closes when clicking outside (for click-triggered tooltips)."),
            _("Position updates on scroll to remain visible."),
            _("Keyboard support: tooltip shows on focus, hides on blur, Escape dismisses."),
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
            _("Error infoboxes use `role='alert'` for immediate screen reader announcement."),
            _("Info, warning, and success infoboxes use `role='note'` for less intrusive announcement."),
            _(
                "The info type (Info, Warning, Error, Success) is rendered as bold text and announced by screen readers."
            ),
            _("The message content supports Markdown formatting."),
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
    return {
        "a11y": [
            _("The diff output uses semantic markup to distinguish additions and deletions."),
            _("Text content is readable by screen readers in its natural order."),
            _("Color coding for additions (green) and deletions (red) meets WCAG contrast requirements."),
        ]
    }


@register_component(Component.LOGO)
def get_logo_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the logo component."""
    return {
        "a11y": [
            _("Image and SVG logos use the provided `alt` text. Empty `alt` values make them decorative."),
            _("Icon logos receive `role='img'` and an accessible label when `alt` is provided."),
        ]
    }


@register_component(Component.BRAND_MARK)
def get_brand_mark_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the brand mark component."""
    return {
        "a11y": [
            _("The wordmark is rendered as readable text so assistive technologies can announce the brand name."),
            _("The decorative public icon is hidden from assistive technologies with `aria-hidden='true'`."),
            _(
                "When used inside the navbar, provide `brand.aria_label` or `brand.mark.primary_text` so the surrounding link has a clear accessible name."
            ),
        ]
    }


@register_component(Component.CORNER_RIBBON)
def get_corner_ribbon_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the corner ribbon component."""
    return {
        "a11y": [
            _("The component has `role='status'` and `aria-label='Site status'` for context."),
            _("The ribbon text is readable by screen readers."),
            _("The component uses `pointer-events-none` to prevent interaction interference."),
        ]
    }


@register_component(Component.PROGRESS_BAR)
def get_progress_bar_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the progress bar component."""
    return {
        "a11y": [
            _(
                "The progress track has `role='progressbar'` with `aria-valuenow`, `aria-valuemin`, and `aria-valuemax`."
            ),
            _("The `aria-label` attribute describes what is progressing when a label is provided."),
            _("The `aria-valuetext` provides a human-readable progress description."),
            _("A live region with `aria-live='polite'` announces progress updates to screen readers."),
            _("Error messages use `role='alert'` for immediate announcement."),
        ]
    }


@register_component(Component.GEO_MAP)
def get_geo_map_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the geo map component."""
    return {
        "a11y": [
            _("The map container has `role='application'` with a descriptive `aria-label`."),
            _("A screen reader alternative lists all locations in a visually hidden element (`sr-only`)."),
            _("Leaflet keyboard navigation is enabled: use arrow keys to pan and `+`/`-` to zoom."),
            _("Markers have `keyboard: true` and `alt` text for accessibility."),
            _("Map controls (zoom in/out, layer switcher) have accessible `aria-label` attributes."),
            _("The map attribution link to OpenStreetMap is accessible."),
            _("Marker popups display title and description as readable text."),
        ]
    }


@register_component(Component.CHART)
def get_charts_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the charts component."""
    return {
        "a11y": [
            _("The chart container has `role='img'` with a descriptive `aria-label`."),
            _("ECharts `aria` option is enabled for automatic ARIA labels and descriptions."),
            _("A screen reader alternative provides the data as a hidden table (`sr-only`)."),
            _("Decal patterns are enabled by default (`show_decal=True`) for colorblind accessibility."),
            _("The chart title is set via ECharts configuration and rendered as part of the chart."),
            _("ECharts provides built-in tooltip support for data exploration."),
            _(
                "**Note:** ECharts has limited keyboard accessibility. "
                "See [GitHub Issue #18585](https://github.com/apache/echarts/issues/18585)."
            ),
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
            _("The output container has `role='log'` and `aria-live='polite'` to announce new messages."),
            _("The `aria-atomic='false'` ensures only new messages are announced, not the entire history."),
            _(
                "Custom events are dispatched for status changes and messages, allowing host applications to implement accessible UI."
            ),
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
            _("The container has `role='feed'` for proper infinite scroll semantics."),
            _("The container has `aria-live='polite'` and `aria-busy` to announce loading state."),
            _("The 'Load more' button provides a manual alternative to automatic loading."),
            _("Content items use semantic `<h3>` headings for screen reader navigation."),
            _("The loading indicator has `role='status'` and the visual spinner is hidden with `aria-hidden='true'`."),
        ]
    }


@register_component(Component.PAGINATION)
def get_pagination_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the pagination component."""
    return {
        "a11y": [
            _("The component uses `<nav>` with `role='navigation'` and `aria-label='Pagination'`."),
            _("Navigation buttons use `sr-only` text to provide descriptive labels for screen readers."),
            _("Disabled buttons explain their state (e.g., 'Deactivated because there are no more previous pages')."),
            _("The current page is marked with `aria-current='page'`."),
            _("The current page information is displayed as text on mobile devices."),
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
            _("Sortable columns have `aria-sort` attribute and use `<button>` elements for click targets."),
            _("Sort icons inherit `aria-hidden='true'` from the icon component."),
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
            _("The form element has `role='search'` for landmark navigation."),
            _("The search input uses `type='search'` for semantic meaning and browser optimizations."),
            _("A visually hidden `<label>` with `sr-only` is linked to the input via `for`/`id`."),
            _("The search icon is decorative and hidden from assistive technologies."),
            _("The submit button has a descriptive text label when displayed."),
        ]
    }


@register_component(Component.GENERIC_FILTER)
def get_generic_filter_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the generic filter component."""
    return {
        "a11y": [
            _("The form element has `role='search'` for landmark navigation."),
            _("Filter fields use the Select component with proper label associations."),
        ]
    }


@register_component(Component.QUERY_BUILDER)
def get_query_builder_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the query builder component."""
    return {
        "a11y": [
            _("The form has `aria-label='Query Builder'` describing its purpose."),
            _("Each filter is wrapped in `role='group'` with `aria-label='Filter N'`."),
            _("All form controls have unique IDs and associated `<label>` elements (sr-only)."),
            _("A live region announces when filters are added or removed."),
            _("Remove buttons announce the filter label (e.g., 'Filter 2 removed')."),
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
            _("The container has `role='region'` with `aria-roledescription='carousel'` and `aria-label`."),
            _("Navigation buttons use `sr-only` text to provide descriptive labels for screen readers."),
            _("Pagination dots include `sr-only` text describing which page they navigate to."),
            _("Full keyboard navigation: Arrow Left/Right to navigate, Home/End to jump to first/last slide."),
            _("Touch gestures (swipe) are supported for mobile navigation."),
            _("Autoplay pauses on hover and focus, giving users more time to read content."),
        ]
    }


@register_component(Component.IMAGE_CAROUSEL)
def get_image_carousel_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the image carousel component."""
    carousel_url = reverse("component_detail_page_view", args=[Component.CARD_CAROUSEL.value])
    return {
        "a11y": [
            _("Inherits accessibility features from [Card Carousel](%(url)s).") % {"url": carousel_url},
            _("The `alt` field is required, ensuring developers provide meaningful descriptions."),
            _("Description overlays are rendered as readable text."),
        ]
    }


@register_component(Component.THREE_D_CAROUSEL)
def get_3d_carousel_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the 3D carousel component."""
    return {
        "a11y": [
            _("The container has `role='region'` with `aria-roledescription='carousel'` and `aria-label`."),
            _("Navigation buttons include descriptive text ('Back', 'Next') alongside icons."),
            _("Keyboard navigation: Arrow Left/Right to navigate between items."),
            _("Responsive: animation distance adapts to screen size for better visibility."),
            _("Respects `prefers-reduced-motion`: animations are instant when reduced motion is preferred."),
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
            _("The content area has `aria-live='polite'` to announce view changes to screen readers."),
            _("The content container has `tabindex='-1'` allowing programmatic focus after view changes."),
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
            _("The loading indicator has `role='status'` and `aria-live='polite'` for screen reader announcements."),
            _("The loading spinner SVG is hidden from assistive technologies with `aria-hidden='true'`."),
        ]
    }
