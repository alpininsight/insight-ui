/**
 * Checkbox group component for Insight UI.
 *
 * Manages a group of checkboxes with configurable minimum and maximum
 * selection constraints. Automatically enforces these constraints when
 * checkboxes are toggled.
 *
 * @example
 * // HTML structure
 * <div data-insight-checkbox-group data-minimum-checked="1" data-maximum-checked="3">
 *   <input type="checkbox" name="options" value="1">
 *   <input type="checkbox" name="options" value="2">
 * </div>
 */
export class Checkbox {
    /** @type {WeakMap<HTMLElement, Checkbox>} Weak references to prevent multiple initialization */
    static instances = new WeakMap();

    /**
     * Creates a new Checkbox group instance.
     *
     * @param {HTMLElement} element - The container element with data-insight-checkbox-group attribute
     */
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

        this.element.__insightInstance = this;
        Checkbox.instances.set(element, this);

        debugLog("New checkbox group created: ", this.element);
    }

    /**
     * Initializes the checkbox group by enforcing min/max constraints.
     * Automatically checks or unchecks boxes to meet the configured limits.
     */
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

    /**
     * Binds change event listeners to all checkboxes in the group.
     * Prevents selections that would violate min/max constraints.
     */
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
        delete this.element.__insightInstance;

        this.element = null;
    }

    /**
     * Initializes all checkbox group instances on the page.
     *
     * @static
     */
    static initAll() {
        document.querySelectorAll('[data-insight-checkbox-group]').forEach(el => new Checkbox(el));
    }
}
