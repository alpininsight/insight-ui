export class Dropdown {
    // Manages all Dropdown instances of the DOM
    static instances = new WeakMap();

    // Handle of the open dropdown
    static currentOpen = null;

    constructor(toggleButton) {
        // If an instance for this element already exists, return it
        if (Dropdown.instances.has(toggleButton)) {
            return Dropdown.instances.get(toggleButton);
        }

        this.toggleButton = toggleButton;
        this.targetId = toggleButton.getAttribute("data-dropdown-toggle");
        this.menu = document.getElementById(this.targetId);

        if (!this.menu) {
            debugLog("Dropdown menu target not found!")
            return;
        }

        this.menu.classList.add("absolute", "z-50", "mt-2");

        // Bind handlers for proper cleanup
        this.boundToggleClick = this.handleToggleClick.bind(this);
        this.boundDocumentClick = this.handleDocumentClick.bind(this);

        this.bindEvents();

        Dropdown.instances.set(toggleButton, this);

        debugLog("New dropdown created: ", this.toggleButton, this.menu);
    }

    handleToggleClick(e) {
        e.stopPropagation();
        if (Dropdown.currentOpen && Dropdown.currentOpen !== this) {
            Dropdown.currentOpen.hide();
        }
        this.menu.classList.toggle("hidden");
        Dropdown.currentOpen = this.menu.classList.contains("hidden") ? null : this;
    }

    handleDocumentClick() {
        this.hide();
    }

    bindEvents() {
        this.toggleButton.addEventListener("click", this.boundToggleClick);
        document.addEventListener("click", this.boundDocumentClick);
    }

    hide() {
        if (!this.menu.classList.contains("hidden")) {
            this.menu.classList.add("hidden");
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
        this.toggleButton.removeEventListener("click", this.boundToggleClick);
        document.removeEventListener("click", this.boundDocumentClick);

        if (Dropdown.currentOpen === this) {
            Dropdown.currentOpen = null;
        }

        Dropdown.instances.delete(this.toggleButton);
        this.toggleButton = null;
        this.menu = null;
    }

    // Static method for initializing all dropdown menus
    static initAll() {
        document.querySelectorAll("[data-dropdown-toggle]").forEach(openButton => new Dropdown(openButton));
    }
}
