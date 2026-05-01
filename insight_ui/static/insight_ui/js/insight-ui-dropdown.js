export class Dropdown {
    // Weak references used to prevent multiple initialization of the same instance
    static instances = new WeakMap();

    // Handle of the open dropdown
    static currentOpen = null;

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

        this.bindEvents();

        this.trigger.__insightInstance = this;
        Dropdown.instances.set(trigger, this);

        debugLog("New dropdown created: ", this.trigger, this.menu);
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
        this.trigger.addEventListener("click", this.boundToggleClick);
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
        debugLog("Destroy dropdown: ", this.trigger, this.menu);

        this.trigger.removeEventListener("click", this.boundToggleClick);
        document.removeEventListener("click", this.boundDocumentClick);

        if (Dropdown.currentOpen === this) {
            Dropdown.currentOpen = null;
        }

        Dropdown.instances.delete(this.trigger);
        delete this.trigger.__insightInstance;

        this.trigger = null;
        this.menu = null;
    }

    // Static method for initializing all dropdown menus
    static initAll() {
        document.querySelectorAll("[data-insight-dropdown]").forEach(openButton => new Dropdown(openButton));
    }
}
