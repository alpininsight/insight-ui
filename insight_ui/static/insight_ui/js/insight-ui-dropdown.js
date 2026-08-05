/**
 * Dropdown menu component for Insight UI.
 *
 * Creates a toggleable dropdown menu that closes when clicking outside.
 * Only one dropdown can be open at a time.
 *
 * @example
 * // HTML structure
 * <button data-insight-dropdown="menu1">Open Menu</button>
 * <div id="menu1" class="hidden">
 *   <a href="#">Item 1</a>
 *   <a href="#">Item 2</a>
 * </div>
 */
export class Dropdown {
    /** @type {WeakMap<HTMLElement, Dropdown>} Weak references to prevent multiple initialization */
    static instances = new WeakMap();

    /** @type {Dropdown|null} Currently open dropdown instance */
    static currentOpen = null;

    /**
     * Creates a new Dropdown instance.
     *
     * @param {HTMLElement} trigger - The trigger button element with data-insight-dropdown attribute
     */
    constructor(trigger) {
        // If an instance for this element already exists, return it
        if (Dropdown.instances.has(trigger)) {
            return Dropdown.instances.get(trigger);
        }

        this.trigger = trigger;
        this.targetId = trigger.getAttribute("data-insight-dropdown");
        this.menu = document.getElementById(this.targetId);

        if (!this.menu) {
            debugLog("Dropdown menu target not found!")
            return;
        }

        this.menu.classList.add("absolute", "z-50", "mt-2");

        // Bind handlers for proper cleanup
        this.boundToggleClick = this.handleToggleClick.bind(this);
        this.boundDocumentClick = this.handleDocumentClick.bind(this);
        this.boundKeyDown = this.handleKeyDown.bind(this);

        // Track focusable items in the menu
        this.menuItems = [];
        this.currentFocusIndex = -1;

        this.bindEvents();

        this.trigger.__insightInstance = this;
        Dropdown.instances.set(trigger, this);

        debugLog("New dropdown created: ", this.trigger, this.menu);
    }

    /**
     * Handles click on the dropdown trigger button.
     * Closes any other open dropdown before toggling this one.
     *
     * @param {Event} e - The click event
     */
    handleToggleClick(e) {
        e.stopPropagation();
        if (Dropdown.currentOpen && Dropdown.currentOpen !== this) {
            Dropdown.currentOpen.hide();
        }
        this.menu.classList.toggle("hidden");
        Dropdown.currentOpen = this.menu.classList.contains("hidden") ? null : this;
    }

    /**
     * Handles clicks outside the dropdown to close it.
     */
    handleDocumentClick() {
        this.hide();
    }

    /**
     * Handles keyboard navigation within the dropdown.
     *
     * @param {KeyboardEvent} e - The keyboard event
     */
    handleKeyDown(e) {
        // Only handle if dropdown is open
        if (this.menu.classList.contains("hidden")) return;

        switch (e.key) {
            case 'Escape':
                e.preventDefault();
                this.hide();
                this.trigger.focus();
                break;

            case 'ArrowDown':
                e.preventDefault();
                this.focusNextItem();
                break;

            case 'ArrowUp':
                e.preventDefault();
                this.focusPreviousItem();
                break;

            case 'Home':
                e.preventDefault();
                this.focusFirstItem();
                break;

            case 'End':
                e.preventDefault();
                this.focusLastItem();
                break;
        }
    }

    /**
     * Gets all focusable menu items.
     *
     * @returns {HTMLElement[]} Array of focusable elements
     */
    getMenuItems() {
        return Array.from(this.menu.querySelectorAll('a, button, [tabindex]:not([tabindex="-1"])'));
    }

    /**
     * Focuses the next menu item.
     */
    focusNextItem() {
        const items = this.getMenuItems();
        if (items.length === 0) return;

        this.currentFocusIndex = (this.currentFocusIndex + 1) % items.length;
        items[this.currentFocusIndex].focus();
    }

    /**
     * Focuses the previous menu item.
     */
    focusPreviousItem() {
        const items = this.getMenuItems();
        if (items.length === 0) return;

        this.currentFocusIndex = this.currentFocusIndex <= 0 ? items.length - 1 : this.currentFocusIndex - 1;
        items[this.currentFocusIndex].focus();
    }

    /**
     * Focuses the first menu item.
     */
    focusFirstItem() {
        const items = this.getMenuItems();
        if (items.length === 0) return;

        this.currentFocusIndex = 0;
        items[0].focus();
    }

    /**
     * Focuses the last menu item.
     */
    focusLastItem() {
        const items = this.getMenuItems();
        if (items.length === 0) return;

        this.currentFocusIndex = items.length - 1;
        items[this.currentFocusIndex].focus();
    }

    /**
     * Binds event listeners to the trigger and document.
     */
    bindEvents() {
        this.trigger.addEventListener("click", this.boundToggleClick);
        document.addEventListener("click", this.boundDocumentClick);
        document.addEventListener("keydown", this.boundKeyDown);
    }

    /**
     * Hides the dropdown menu.
     */
    hide() {
        if (!this.menu.classList.contains("hidden")) {
            this.menu.classList.add("hidden");
            this.currentFocusIndex = -1;
            if (Dropdown.currentOpen === this) {
                Dropdown.currentOpen = null;
            }
        }
    }

    /**
     * Destroys the dropdown instance and removes all event listeners.
     * Call this before removing the element from DOM.
     */
    destroy() {
        debugLog("Destroy dropdown: ", this.trigger, this.menu);

        this.trigger.removeEventListener("click", this.boundToggleClick);
        document.removeEventListener("click", this.boundDocumentClick);
        document.removeEventListener("keydown", this.boundKeyDown);

        if (Dropdown.currentOpen === this) {
            Dropdown.currentOpen = null;
        }

        Dropdown.instances.delete(this.trigger);
        delete this.trigger.__insightInstance;

        this.trigger = null;
        this.menu = null;
    }

    /**
     * Initializes all dropdown instances on the page.
     *
     * @static
     */
    static initAll() {
        document.querySelectorAll("[data-insight-dropdown]").forEach(openButton => new Dropdown(openButton));
    }
}
