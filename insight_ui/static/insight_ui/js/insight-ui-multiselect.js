/**
 * A select field which allows multiple selected values.
 *
 * The multiselect has an integrated searchfield to search for specific values.
 * Selected values are shows as badges in the searchfield and can be easily removed.
 *
 * There are optional buttons to select or deselect all values at once and the maximum amount
 * of selected values is customizable.
 */
export class Multiselect {
    // Manages all Multiselect instances of the DOM
    static instances = new WeakMap();

    constructor(container) {
        // If an instance for this element already exists, return it
        if (Multiselect.instances.has(container)) {
            return Multiselect.instances.get(container);
        }

        this.container = container;
        this.name = container.dataset.name || "multiselect";
        this.max = parseInt(container.dataset.max) || Infinity;
        if (!container.dataset.selected || !container.dataset.selected.trim()) this.selectedValues = [];
        else this.selectedValues = JSON.parse(container.dataset.selected.replace(/'/g, '"'));
        this.focusedIndex = -1;

        this.combobox = this.container.querySelector('[role="combobox"]');
        this.selected = this.container.querySelector('.selected');
        this.tags = this.container.querySelector('.tags');
        this.search = this.container.querySelector('.search');
        this.options = this.container.querySelector('.options');
        this.optionItems = Array.from(this.container.querySelectorAll('.option'));
        this.info = this.container.querySelector('.info');
        this.ariaStatus = this.container.querySelector(`#${this.name}-aria-status`);
        this.selectAllBtn = this.container.querySelector('.select-all');
        this.deselectAllBtn = this.container.querySelector('.deselect-all');

        this.bindEvents();
        this.renderSelected();

        this.updateInfo();
        this.updateAriaStatus();

        Multiselect.instances.set(container, this);

        debugLog("New multiselect created: ", this.container, this.name);
    }

    /**
     * Bind all EventListener to the searchfield, buttons and options.
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

    handleDocumentClick(e) {
        if (!this.container.contains(e.target)) this.toggleDropdown(false);
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
        const value = opt.textContent.trim();
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
            opt.style.display = 'none';
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
     * @param {String} value Text of the option.
     */
    deselectValue(value) {
        this.selectedValues = this.selectedValues.filter(v => v !== value);
        this.optionItems.forEach(o => {
            if (o.textContent.trim() === value) {
                o.setAttribute('aria-selected', 'false');
                o.style.display = 'block';
            }
        });
        this.renderSelected();
        this.dispatchEvent();
        // this.toggleDropdown(true);
        this.search.focus();
    }

    /**
     * Create badges for the selected options.
     *
     * Create a badge with the value of the option and a remove button for each selected option.
     * The badges are placed at the begin of the search field.
     * Update information and 'aria-status' for each option.
     */
    renderSelected() {
        this.tags.innerHTML = '';
        this.container.querySelectorAll('input[type=hidden]').forEach(i => i.remove());
        this.selectedValues.forEach(value => {
            const tag = document.createElement('span');
            tag.className = 'inline-tag me-1';
            tag.textContent = value;
            const remove = document.createElement('button');
            remove.innerHTML = '&times;';
            remove.className = 'text-blue-500 hover:text-blue-700 ml-1';
            remove.addEventListener('click', e => { e.stopPropagation(); this.deselectValue(value); });
            tag.appendChild(remove);
            this.tags.appendChild(tag);

            const hidden = document.createElement('input');
            hidden.type = 'hidden'; hidden.name = this.name; hidden.value = value;
            this.container.appendChild(hidden);
        });
        this.updateInfo();
        this.updateAriaStatus();
    }

    /**
     * Filter option in relation to the given term.
     *
     * Hide all option whose value does not contain the given term (not case sensitive).
     * Set 'focusedIndex' to -1.
     *
     * @param {String} term Search input.
     */
    filterOptions(term) {
        const lower = term.toLowerCase();
        this.optionItems.forEach(opt => {
            const value = opt.textContent.toLowerCase();
            const hiddenBySelection = this.selectedValues.includes(opt.textContent.trim());
            opt.style.display = (!hiddenBySelection && value.includes(lower)) ? 'block' : 'none';
        });
        this.focusedIndex = -1;
    }

    /**
     * Update the info text.
     */
    updateInfo() {this.info.textContent = this.max === Infinity ? '' : `${this.selectedValues.length}/${this.max} ausgewählt`; }

    /**
     * Update the 'aria-status'.
     */
    updateAriaStatus() { this.ariaStatus.textContent = `${this.selectedValues.length} Option${this.selectedValues.length !== 1 ? 'en' : ''} ausgewählt`; }

    /**
     * Select every option, so that all is selected.
     *
     * Add every option to the list of selected values, set 'aria-selected' to 'true' and
     * 'display' to 'none' for every option. Update DOM.
     */
    selectAll() {
        this.optionItems.forEach(opt => {
            const value = opt.textContent.trim();
            if (!this.selectedValues.includes(value)) {
                this.selectedValues.push(value);
                opt.setAttribute('aria-selected', 'true');
                opt.style.display = 'none';
            }
        });
        this.renderSelected();
        this.dispatchEvent();
    }

    /**
     * Deselect every option, so that nothing is selected.
     *
     * Clear list of selected values, set 'aria-selected' to 'false' and
     * 'display' to 'block' for every option. Update DOM and open search field.
     */
    deselectAll() {
        this.selectedValues = [];
        this.optionItems.forEach(opt => {
            opt.setAttribute('aria-selected', 'false');
            opt.style.display = 'block';
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
        this.container.dispatchEvent(new CustomEvent("change", {
            detail: { value: this.selectedValues },
            bubbles: true
        }));
    }

    /**
     * Destroys the multiselect instance and removes all event listeners.
     * Call this before removing the element from DOM.
     */
    destroy() {
        debugLog("Destroy multiselect: ", this.container, this.name);

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

        Multiselect.instances.delete(this.container);
        this.container = null;
    }

    // Static method for initializing all multiselect elements
    static initAll() {
        document.querySelectorAll('[data-multiselect]').forEach(el => new Multiselect(el));
    }
}
