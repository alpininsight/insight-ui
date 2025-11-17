class Dropdown {
    static instances = new WeakMap();
    static currentOpen = null;

    constructor(toggleButton) {
        if (Dropdown.instances.has(toggleButton)) {
            return Dropdown.instances.get(toggleButton);
        }

        this.toggleButton = toggleButton;
        this.targetId = toggleButton.getAttribute("data-dropdown-toggle");
        this.menu = document.getElementById(this.targetId);

        if (!this.menu) return;

        this.menu.classList.add("absolute", "hidden", "z-50", "mt-2");

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
        const buttons = document.querySelectorAll("[data-dropdown-toggle]");
        buttons.forEach(btn => new Dropdown(btn));
    }
}

window.InsightUI = window.InsightUI || {};
window.InsightUI.Dropdown = Dropdown;
