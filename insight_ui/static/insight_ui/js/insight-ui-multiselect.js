// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Multiselect component for Insight UI.
 *
 * A select field which allows multiple selected values with an integrated
 * search field to filter options. Selected values are shown as removable badges.
 * Supports configurable maximum selections and select/deselect all buttons.
 *
 * @example
 * // HTML structure
 * <div data-insight-multiselect data-name="tags" data-max="5" data-selected="['Tag1']">
 *   <div role="combobox" aria-expanded="false">
 *     <div class="selected">
 *       <div class="tags"></div>
 *       <input type="text" class="search">
 *     </div>
 *   </div>
 *   <div class="options hidden">
 *     <div class="option" id="opt-1">Option 1</div>
 *   </div>
 * </div>
 */
export class Multiselect {
    /** @type {WeakMap<HTMLElement, Multiselect>} Weak references to prevent multiple initialization */
    static instances = new WeakMap();

    /**
     * Creates a new Multiselect instance.
     *
     * @param {HTMLElement} element - The multiselect container element with data-insight-multiselect attribute
     */
    constructor(element) {
        // If an instance for this element already exists, return it
        if (Multiselect.instances.has(element)) {
            return Multiselect.instances.get(element);
        }

        this.element = element;
        this.name = element.dataset.name || "multiselect";
        this.max = parseInt(element.dataset.max) || Infinity;
        this.disabled = element.dataset.disabled === "true";
        if (!element.dataset.selected || !element.dataset.selected.trim()) this.selectedValues = [];
        else this.selectedValues = JSON.parse(element.dataset.selected.replace(/'/g, '"'));
        this.focusedIndex = -1;

        this.combobox = this.element.querySelector('[role="combobox"]');
        this.selected = this.element.querySelector('.selected');
        this.tags = this.element.querySelector('.tags');
        this.search = this.element.querySelector('.search');
        this.options = this.element.querySelector('.options');
        this.optionItems = Array.from(this.element.querySelectorAll('.option'));
        this.info = this.element.querySelector('.info');
        this.ariaStatus = this.element.querySelector(`#${this.name}-aria-status`);
        this.selectAllBtn = this.element.querySelector('.select-all');
        this.deselectAllBtn = this.element.querySelector('.deselect-all');

        // Hide already selected options
        this.optionItems.forEach(opt => {
            const value = opt.dataset.value ?? opt.textContent.trim();
            if (this.selectedValues.includes(value)) {
                opt.setAttribute('aria-selected', 'true');
                opt.hidden = true;
            }
        });

        // Only bind interactive events if not disabled
        if (!this.disabled) {
            this.bindEvents();
        }
        this.renderSelected();

        this.updateInfo();
        this.updateAriaStatus();

        this.element.__insightInstance = this;
        Multiselect.instances.set(element, this);

        debugLog("New multiselect created: ", this.element, this.name);
    }

    /**
     * Binds all event listeners to the search field, buttons, and options.
     */
    bindEvents() {
        // Bind handlers for proper cleanup
        this.boundSearchInput = () => { this.filterOptions(this.search.value); this.toggleDropdown(true); };
        this.boundSearchFocus = () => { this.toggleDropdown(true); };
        this.boundSearchBlur = () => { this.search.value = ''; this.filterOptions(''); };
        this.boundSelectedClick = () => { this.toggleDropdown(true); this.search.focus(); };
        this.boundSearchKeydown = this.handleSearchKeydown.bind(this);
        this.boundDocumentClick = this.handleDocumentClick.bind(this);
        this.boundSelectAll = () => { this.selectAll(); };
        this.boundDeselectAll = () => { this.deselectAll(); };

        this.search.addEventListener('input', this.boundSearchInput);
        this.search.addEventListener('focus', this.boundSearchFocus);
        this.search.addEventListener('blur', this.boundSearchBlur);
        this.selected.addEventListener('click', this.boundSelectedClick);
        this.search.addEventListener('keydown', this.boundSearchKeydown);

        // Store bound option click handlers for cleanup
        this.boundOptionClicks = [];
        this.optionItems.forEach(opt => {
            const handler = () => this.toggleSelect(opt);
            this.boundOptionClicks.push({ element: opt, handler });
            opt.addEventListener('click', handler);
        });

        document.addEventListener('click', this.boundDocumentClick);

        if (this.selectAllBtn) this.selectAllBtn.addEventListener('click', this.boundSelectAll);
        if (this.deselectAllBtn) this.deselectAllBtn.addEventListener('click', this.boundDeselectAll);
    }

    /**
     * Handles keyboard navigation in the search field.
     * Supports Arrow keys, Enter, Backspace, Escape, and Tab.
     *
     * @param {KeyboardEvent} e - The keydown event
     */
    handleSearchKeydown(e) {
        const visible = this.optionItems.filter(o => o.style.display !== 'none');
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            if (!visible.length) return;
            this.focusedIndex = (this.focusedIndex + 1) % visible.length;
            this.focusOption(visible[this.focusedIndex]);
        }
        else if (e.key === 'ArrowUp') {
            e.preventDefault();
            if (!visible.length) return;
            this.focusedIndex = (this.focusedIndex - 1 + visible.length) % visible.length;
            this.focusOption(visible[this.focusedIndex]);
        }
        else if (e.key === 'Enter') {
            e.preventDefault();
            if (!visible.length) return;
            if (this.search.value.trim() === '' && this.focusedIndex === -1) return;
            const opt = this.focusedIndex >= 0 ? visible[this.focusedIndex] : visible[0];
            this.toggleSelect(opt);
        }
        else if (e.key === 'Backspace' && this.search.value === '') {
            if (this.selectedValues.length > 0)
                this.deselectValue(this.selectedValues[this.selectedValues.length - 1]);
        }
        else if (e.key === 'Escape' || e.key === 'Tab') this.toggleDropdown(false);
    }

    /**
     * Handles clicks to close the dropdown when clicking outside the interactive area.
     *
     * Closes the dropdown when clicking outside the combobox area, except for
     * the select/deselect all buttons which have their own handlers.
     *
     * @param {MouseEvent} e - The click event
     */
    handleDocumentClick(e) {
        // Always close if click is outside the entire component
        if (!this.element.contains(e.target)) {
            this.toggleDropdown(false);
            return;
        }

        // Keep open if clicking within the input area or options dropdown.
        if (this.selected.contains(e.target) || this.options.contains(e.target)) return;

        // Keep open if clicking select/deselect all buttons
        if (this.selectAllBtn?.contains(e.target)) return;
        if (this.deselectAllBtn?.contains(e.target)) return;

        // Close for clicks on other areas (label, info text, empty space)
        this.toggleDropdown(false);
    }

    /**
     * Show or hide the list of options.
     *
     * Toggle the 'hidden' class and set 'aria-expanded' to 'true' or 'false'.
     * Set 'focusedIndex' to -1 if the list is shown.
     *
     * @param {boolean} show 'true' to show the list of options, otherwise 'false'.
     */
    toggleDropdown(show) {
        if (show) {
            this.options.classList.remove('hidden');
            this.combobox.setAttribute('aria-expanded', 'true');
        } else {
            this.options.classList.add('hidden');
            this.combobox.setAttribute('aria-expanded', 'false');
            this.focusedIndex = -1;
        }
    }

    /**
     * Highlight the focused option in the list.
     *
     * @param {HTMLElement} opt The option element.
     * @returns null If the option ist empty.
     */
    focusOption(opt) {
        this.optionItems.forEach(o => o.classList.remove('bg-blue-50'));
        if (!opt) return;

        opt.classList.add('bg-blue-50');
        this.combobox.setAttribute('aria-activedescendant', opt.id);
    }

    /**
     * Select or deselect the given option.
     *
     * @param {HTMLElement} opt The option element.
     * @returns null If the maximum amount of selected values is reached.
     */
    toggleSelect(opt) {
        const value = opt.dataset.value ?? opt.textContent.trim();
        if (this.selectedValues.includes(value))
            this.deselectValue(value);
        else {
            if (this.selectedValues.length >= this.max) {
                this.selected.classList.add('animate-shake', 'border-red-500');
                setTimeout(() => this.selected.classList.remove('animate-shake', 'border-red-500'), 300);
                return;
            }
            this.selectedValues.push(value);
            opt.setAttribute('aria-selected', 'true');
            opt.hidden = true;
            this.renderSelected();
            this.dispatchEvent();
        }
        this.search.value = '';
        this.filterOptions('');
        this.search.focus();
    }

    /**
     * Deselect the option with the given value.
     *
     * Remove the corresponding option from the list of selected options,
     * set 'aria-selected' to 'false' and 'display' to 'block' for the option.
     * Update DOM and open search field.
     *
     * @param {String} value Value of the option (from data-value or textContent).
     */
    deselectValue(value) {
        this.selectedValues = this.selectedValues.filter(v => v !== value);
        this.optionItems.forEach(opt => {
            const optValue = opt.dataset.value ?? opt.textContent.trim();
            if (optValue === value) {
                opt.setAttribute('aria-selected', 'false');
                opt.hidden = false;
            }
        });
        this.renderSelected();
        this.dispatchEvent();
        this.search.focus();
    }

    /**
     * Create badges for the selected options.
     *
     * Create a badge with the display text of the option and a remove button for each selected option.
     * The badges are placed at the begin of the search field.
     * Update information and 'aria-status' for each option.
     */
    renderSelected() {
        this.tags.innerHTML = '';
        this.element.querySelectorAll('input[type=hidden]').forEach(i => i.remove());
        this.selectedValues.forEach(value => {
            // Find the option element to get its display text
            const opt = this.optionItems.find(o => (o.dataset.value ?? o.textContent.trim()) === value);
            const displayText = opt ? opt.textContent.trim() : value;

            const tag = document.createElement('span');
            tag.className = 'inline-tag me-1';
            tag.textContent = displayText;
            // Only add remove button if not disabled
            if (!this.disabled) {
                const remove = document.createElement('button');
                remove.innerHTML = '&times;';
                remove.className = 'text-blue-500 hover:text-blue-700 ml-1';
                remove.addEventListener('click', e => { e.stopPropagation(); this.deselectValue(value); });
                tag.appendChild(remove);
            }
            this.tags.appendChild(tag);

            const hidden = document.createElement('input');
            hidden.type = 'hidden'; hidden.name = this.name; hidden.value = value;
            this.element.appendChild(hidden);
        });
        this.updateInfo();
        this.updateAriaStatus();
    }

    /**
     * Filter option in relation to the given term.
     *
     * Hide all option whose display text does not contain the given term (not case sensitive).
     * Set 'focusedIndex' to -1.
     *
     * @param {String} term Search input.
     */
    filterOptions(term) {
        const lower = term.toLowerCase();
        this.optionItems.forEach(opt => {
            const displayText = opt.textContent.toLowerCase();
            const optValue = opt.dataset.value ?? opt.textContent.trim();
            const hiddenBySelection = this.selectedValues.includes(optValue);
            opt.hidden = (!hiddenBySelection && displayText.includes(lower)) ? false : true;
        });
        this.focusedIndex = -1;
    }

    /**
     * Update the info text.
     */
    updateInfo() {
        if (this.max === Infinity) {
            this.info.textContent = '';
            return;
        }

        const text = gettext('%(count)s/%(max)s selected');
        this.info.textContent = interpolate(text, {
            count: this.selectedValues.length,
            max: this.max
        }, true);
    }

    /**
     * Update the 'aria-status'.
     */
    updateAriaStatus() {
        const count = this.selectedValues.length;

        const text = ngettext(
            '%(count)s option selected',
            '%(count)s options selected',
            count
        );

        this.ariaStatus.textContent = interpolate(text, {
            count: count
        }, true);
    }

    /**
     * Select options up to the maximum allowed limit.
     *
     * Adds options to the selected values until the max limit is reached.
     * If max is not set (Infinity), selects all options.
     */
    selectAll() {
        this.optionItems.forEach(opt => {
            const value = opt.dataset.value ?? opt.textContent.trim();
            if (!this.selectedValues.includes(value)) {
                // Respect max limit
                if (this.selectedValues.length >= this.max) {
                    return;
                }
                this.selectedValues.push(value);
                opt.setAttribute('aria-selected', 'true');
                opt.hidden = true;
            }
        });
        this.renderSelected();
        this.dispatchEvent();
    }

    /**
     * Deselect every option, so that nothing is selected.
     *
     * Clear list of selected values, set 'aria-selected' to 'false' and
     * 'hidden' to 'false' for every option. Update DOM and open search field.
     */
    deselectAll() {
        this.selectedValues = [];
        this.optionItems.forEach(opt => {
            opt.setAttribute('aria-selected', 'false');
            opt.hidden = false;
        });
        this.renderSelected();
        this.dispatchEvent();
        this.search.focus();
    }

    /**
     * Dispatch a "change" event with a list of the selected values.
     *
     * Because this is a custom input-element the event has to be dispatched manually.
     */
    dispatchEvent() {
        this.element.dispatchEvent(new CustomEvent("change", {
            detail: { value: this.selectedValues },
            bubbles: true
        }));
    }

    /**
     * Destroys the multiselect instance and removes all event listeners.
     * Call this before removing the element from DOM.
     */
    destroy() {
        debugLog("Destroy multiselect: ", this.element, this.name);

        // Only remove event listeners if they were bound (not disabled)
        if (!this.disabled) {
            // Remove search and selected listeners
            this.search.removeEventListener('input', this.boundSearchInput);
            this.search.removeEventListener('focus', this.boundSearchFocus);
            this.search.removeEventListener('blur', this.boundSearchBlur);
            this.selected.removeEventListener('click', this.boundSelectedClick);
            this.search.removeEventListener('keydown', this.boundSearchKeydown);

            // Remove option click handlers
            this.boundOptionClicks.forEach(({ element, handler }) => {
                element.removeEventListener('click', handler);
            });
            this.boundOptionClicks = [];

            // Remove document click handler
            document.removeEventListener('click', this.boundDocumentClick);

            // Remove button handlers
            if (this.selectAllBtn) this.selectAllBtn.removeEventListener('click', this.boundSelectAll);
            if (this.deselectAllBtn) this.deselectAllBtn.removeEventListener('click', this.boundDeselectAll);
        }

        Multiselect.instances.delete(this.element);
        delete this.element.__insightInstance;

        this.element = null;
    }

    /**
     * Initializes all multiselect instances on the page.
     *
     * @static
     */
    static initAll() {
        document.querySelectorAll('[data-insight-multiselect]').forEach(el => new Multiselect(el));
    }
}
