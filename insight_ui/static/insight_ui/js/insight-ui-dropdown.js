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

        this.bindEvents();

        Dropdown.instances.set(toggleButton, this);

        debugLog("New dropdown created: ", this.toggleButton, this.menu);
    }

    bindEvents() {
        this.toggleButton.addEventListener("click", e => {
            e.stopPropagation();
            if (Dropdown.currentOpen && Dropdown.currentOpen !== this) {
                Dropdown.currentOpen.hide();
            }
            this.menu.classList.toggle("hidden");
            Dropdown.currentOpen = this.menu.classList.contains("hidden") ? null : this;
        });

        // Close when clicking outside
        document.addEventListener("click", () => {
            this.hide();
        });
    }

    hide() {
        if (!this.menu.classList.contains("hidden")) {
            this.menu.classList.add("hidden");
            if (Dropdown.currentOpen === this) {
                Dropdown.currentOpen = null;
            }
        }
    }

    // Static method for initializing all dropdown menus
    static initAll() {
        document.querySelectorAll("[data-dropdown-toggle]").forEach(openButton => new Dropdown(openButton));
    }
}
