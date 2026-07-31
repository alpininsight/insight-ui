export class Collapsible {
    // Weak references used to prevent multiple initialization of the same instance
    static instances = new WeakMap();

    constructor(trigger) {
        // If an instance for this element already exists, return it
        if (Collapsible.instances.has(trigger)) {
            return Collapsible.instances.get(trigger);
        }

        this.trigger = trigger;
        this.targetID = this.trigger.getAttribute('data-insight-collapsible');
        this.targetElement = document.getElementById(this.targetID);
        this.icon = this.trigger.querySelector('[data-collapsible-icon]');

        this.clickHandler = () => this.toggle();

        this.init();

        this.trigger.__insightInstance = this;
        Collapsible.instances.set(trigger, this);

        debugLog("New collapsible created: ", this.trigger, this.targetElement);
    }

    init() {
        this.trigger.addEventListener("click", this.clickHandler);
    }

    /**
     * Toggle the collapsible state.
     */
    toggle() {
        const isHidden = this.targetElement.classList.toggle("hidden");
        const isExpanded = !isHidden;

        // Update aria-expanded attribute
        this.trigger.setAttribute('aria-expanded', isExpanded);

        // Rotate icon if present
        if (this.icon) {
            this.icon.style.transform = isExpanded ? 'rotate(90deg)' : 'rotate(0deg)';
        }
    }

    /**
     * Destroys the collapsible instance and removes all event listeners.
     * Call this before removing the element from DOM.
     */
    destroy() {
        debugLog("Destroy collapsible: ", this.trigger);

        this.trigger.removeEventListener("click", this.clickHandler);

        Collapsible.instances.delete(this.trigger);
        delete this.trigger.__insightInstance;

        this.trigger = null;
        this.targetElement = null;
    }

    // Static method for initializing all collapsible
    static initAll() {
        document.querySelectorAll('[data-insight-collapsible]').forEach(el => new Collapsible(el));
    }
}
