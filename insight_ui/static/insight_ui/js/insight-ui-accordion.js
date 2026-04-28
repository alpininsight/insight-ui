export class Accordion {
    // Weak references used to prevent multiple initialization of the same instance
    static instances = new WeakMap();

    constructor(element) {
        // If an instance for this element already exists, return it
        if (Accordion.instances.has(element)) {
            debugLog("Element already instantiated: ", element);
            return Accordion.instances.get(element);
        }

        this.element = element;
        this.buttons = Array.from(element.querySelectorAll("button[aria-controls]"));
        this.exclusive = element.getAttribute("data-accordion-exclusive") === "true";

        // Store bound handlers for cleanup
        this.boundButtonHandlers = [];

        this.bindEvents();
        this.handleInitialOpen();

        this.element.__insightInstance = this;
        Accordion.instances.set(element, this);

        debugLog("New accordion created: ", this.element);
    }

    bindEvents() {
        this.buttons.forEach((button, index) => {
            const panelId = button.getAttribute("aria-controls");
            const panel = document.getElementById(panelId);

            // Click-Event
            const clickHandler = () => {
                const isExpanded = button.getAttribute("aria-expanded") === "true";

                if (this.exclusive) {
                    this.buttons.forEach((btn) => {
                        const pid = btn.getAttribute("aria-controls");
                        const p = document.getElementById(pid);
                        if (btn !== button) this.closePanel(btn, p);
                    });
                }

                if (isExpanded) {
                    this.closePanel(button, panel);
                } else {
                    this.openPanel(button, panel);
                    this.updateURL(panelId);
                }
            };

            // Keyboard navigation
            const keydownHandler = (event) => {
                let targetIndex = null;

                switch (event.key) {
                    case "ArrowDown":
                        targetIndex = (index + 1) % this.buttons.length;
                        break;
                    case "ArrowUp":
                        targetIndex = (index - 1 + this.buttons.length) % this.buttons.length;
                        break;
                    case "Home":
                        targetIndex = 0;
                        break;
                    case "End":
                        targetIndex = this.buttons.length - 1;
                        break;
                }

                if (targetIndex !== null) {
                    event.preventDefault();
                    this.buttons[targetIndex].focus();
                }
            };

            button.addEventListener("click", clickHandler);
            button.addEventListener("keydown", keydownHandler);

            this.boundButtonHandlers.push({
                element: button,
                clickHandler,
                keydownHandler
            });
        });
    }

    closePanel(button, panel) {
        button.setAttribute("aria-expanded", "false");
        button.querySelector("div")?.classList.remove("rotate-180");

        panel.style.height = panel.scrollHeight + "px";
        panel.offsetHeight; // Force reflow

        panel.style.transition = "height 0.3s ease, opacity 0.3s ease";
        panel.style.height = "0px";
        panel.style.opacity = "0";

        const handler = (event) => {
            if (event.propertyName === "height") {
                panel.removeEventListener("transitionend", handler);
                panel.style.transition = "";
                panel.style.height = "0px";
            }
        };

        panel.addEventListener("transitionend", handler);
    }

    openPanel(button, panel, scroll = true) {
        button.setAttribute("aria-expanded", "true");
        button.querySelector("div")?.classList.add("rotate-180");

        panel.style.transition = "none";
        panel.style.height = "auto";
        const height = panel.scrollHeight + "px";
        panel.style.height = "0px";
        panel.offsetHeight;

        panel.style.transition = "height 0.3s ease, opacity 0.3s ease";
        panel.style.height = height;
        panel.style.opacity = "1";

        const handler = (event) => {
            if (event.propertyName === "height") {
                panel.removeEventListener("transitionend", handler);
                panel.style.transition = "";
                panel.style.height = "auto";
            }
        };

        panel.addEventListener("transitionend", handler);
    }

    updateURL(id) {
        const url = new URL(window.location);
        url.searchParams.set("open", id);
        window.history.replaceState({}, "", url);
    }

    handleInitialOpen() {
        const params = new URLSearchParams(window.location.search);
        const openId = params.get("open");
        if (!openId) return;

        const buttonToOpen = this.buttons.find(
            (btn) => btn.getAttribute("aria-controls") === openId
        );
        const panelToOpen = document.getElementById(openId);

        if (buttonToOpen && panelToOpen) {
            if (this.exclusive) {
                this.buttons.forEach((btn) => {
                    const pid = btn.getAttribute("aria-controls");
                    const p = document.getElementById(pid);
                    this.closePanel(btn, p);
                });
            }
            this.openPanel(buttonToOpen, panelToOpen, true);
        }
    }

    /**
     * Destroys the accordion instance and removes all event listeners.
     * Call this before removing the element from DOM.
     */
    destroy() {
        debugLog("Destroy accordion: ", this.element);

        this.boundButtonHandlers.forEach(({ element, clickHandler, keydownHandler }) => {
            element.removeEventListener("click", clickHandler);
            element.removeEventListener("keydown", keydownHandler);
        });
        this.boundButtonHandlers = [];

        Accordion.instances.delete(this.element);
        delete this.element.__insightInstance;

        this.element = null;
    }

    // Static method for initializing all accordions
    static initAll() {
        document.querySelectorAll("[data-accordion]").forEach(el => new Accordion(el));
    }
}
