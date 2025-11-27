class Checkbox {
    static instances = new WeakMap();

    constructor(element) {
        if (Checkbox.instances.has(element)) {
            return Checkbox.instances.get(element);
        }

        this.checkboxes = element.getElementsByTagName('input');
        this.minChecked = element.dataset.minimumChecked;

        this.bindEvents();

        Checkbox.instances.set(element, this);

        debugLog("New checkbox group created: ", element);
    }

    bindEvents() {
        for (let box of this.checkboxes) {
            box.addEventListener('change', () => {
                const checkedCount = [...this.checkboxes].filter(b => b.checked).length;
                if (checkedCount < this.minChecked) { box.checked = true; }
            });
        }
    }

    // Static method for initializing all checkboxes
    static initAll() {
        document.querySelectorAll('[data-insight-checkbox-group]').forEach(c => new Checkbox(c));
    }
}

window.InsightUI = window.InsightUI || {};
window.InsightUI.Checkbox = Checkbox;
