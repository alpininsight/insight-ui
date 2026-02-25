export class Collapsible {
    // Weak references used to prevent multiple initialization of the same instance
    static instances = new WeakMap();

    constructor(trigger) {
        // If an instance for this element already exists, return it
        if (Collapsible.instances.has(trigger)) {
            return Collapsible.instances.get(trigger);
        }

        this.trigger = trigger;
        this.targetID = this.trigger.getAttribute('data-insight-target');
        this.targetElement = document.getElementById(this.targetID);

        this.clickHandler = () => { this.targetElement.classList.toggle("hidden"); };

        this.init();

        this.trigger.__insightInstance = this;
        Collapsible.instances.set(trigger, this);

        debugLog("New collapsible created: ", this.trigger, this.targetElement);
    }

    init() {
        this.trigger.addEventListener("click", this.clickHandler);
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
        document.querySelectorAll('[data-insight-toggle="collapsible"]').forEach(el => new Collapsible(el));
    }
}
