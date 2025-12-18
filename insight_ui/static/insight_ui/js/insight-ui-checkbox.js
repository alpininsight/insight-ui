export class Checkbox {
    // Manages all Checkbox instances of the DOM
    static instances = new WeakMap();

    constructor(element) {
        // If an instance for this element already exists, return it
        if (Checkbox.instances.has(element)) {
            return Checkbox.instances.get(element);
        }

        this.element = element;
        this.checkboxes = element.getElementsByTagName('input');
        this.minChecked = element.dataset.minimumChecked;
        this.maxChecked = element.dataset.maximumChecked;

        // Store bound handlers for cleanup
        this.boundChangeHandlers = [];

        this.init();
        this.bindEvents();

        Checkbox.instances.set(element, this);

        debugLog("New checkbox group created: ", this.element);
    }

    init() {
        const checkedCount = [...this.checkboxes].filter(b => b.checked).length;
        if (checkedCount < this.minChecked) {
            // Too few checkboxes are selected, so select the first missing ones.
            let missingCount = this.minChecked - checkedCount;
            let checkboxesToCheck = [...this.checkboxes].filter(b => !b.checked);
            for (let i = 0; i < missingCount; i++) {
                checkboxesToCheck[i].checked = true;
            }
        } else if (checkedCount > this.maxChecked) {
            // Too many checkboxes are selected, so deselect the last few.
            let excessCount = checkedCount - this.maxChecked;
            let checkboxesToUncheck = [...this.checkboxes].filter(b => b.checked);
            for (let i = 0; i < excessCount; i++) {
                checkboxesToUncheck[checkboxesToUncheck.length - 1 - i].checked = false;
            }
        }
    }

    bindEvents() {
        for (let box of this.checkboxes) {
            const handler = () => {
                const checkedCount = [...this.checkboxes].filter(b => b.checked).length;
                if (checkedCount < this.minChecked) { box.checked = true; }
                else if (checkedCount > this.maxChecked) { box.checked = false; }
            };
            this.boundChangeHandlers.push({ element: box, handler });
            box.addEventListener('change', handler);
        }
    }

    /**
     * Destroys the checkbox group instance and removes all event listeners.
     * Call this before removing the element from DOM.
     */
    destroy() {
        debugLog("Destroy checkbox group: ", this.element);

        this.boundChangeHandlers.forEach(({ element, handler }) => {
            element.removeEventListener('change', handler);
        });
        this.boundChangeHandlers = [];

        Checkbox.instances.delete(this.element);
        this.element = null;
    }

    // Static method for initializing all checkboxes
    static initAll() {
        document.querySelectorAll('[data-insight-checkbox-group]').forEach(el => new Checkbox(el));
    }
}
