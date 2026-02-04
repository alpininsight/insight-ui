export class Collapsible {
    // Manages all Collapsible instances of the DOM
    static instances = new WeakMap();

    constructor(element) {
        // If an instance for this element already exists, return it
        if (Collapsible.instances.has(element)) {
            return Collapsible.instances.get(element);
        }

        this.element = element;
        this.targetID = this.element.getAttribute('data-insight-target');
        this.targetElement = document.getElementById(this.targetID);

        this.bindEvents();

        Collapsible.instances.set(element, this);

        debugLog("New collapsible created: ", this.element, this.targetElement);
    }

    bindEvents() {
        this.element.addEventListener("click", () => {
            this.targetElement.classList.toggle("hidden");
        });
    }

    // Static method for initializing all collapsible
    static initAll() {
        document.querySelectorAll('[data-insight-toggle="collapsible"]').forEach(el => new Collapsible(el));
    }
}
