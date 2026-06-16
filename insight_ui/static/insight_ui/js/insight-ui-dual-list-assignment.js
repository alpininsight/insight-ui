export class DualListAssignment {
    static instances = new WeakMap();

    constructor(element) {
        if (DualListAssignment.instances.has(element)) {
            return DualListAssignment.instances.get(element);
        }

        this.element = element;
        this.name = element.dataset.name || "dual_list_assignment";
        this.available = element.querySelector("[data-insight-dual-list-available]");
        this.assigned = element.querySelector("[data-insight-dual-list-assigned]");
        this.hidden = element.querySelector("[data-insight-dual-list-hidden]");
        this.status = element.querySelector("[data-insight-dual-list-status]");
        this.availableCount = element.querySelector("[data-insight-dual-list-available-count]");
        this.assignedCount = element.querySelector("[data-insight-dual-list-assigned-count]");
        this.addButton = element.querySelector("[data-insight-dual-list-add]");
        this.removeButton = element.querySelector("[data-insight-dual-list-remove]");
        this.availableFilter = element.querySelector('[data-insight-dual-list-filter="available"]');
        this.assignedFilter = element.querySelector('[data-insight-dual-list-filter="assigned"]');
        this.boundHandlers = [];

        this.bindEvents();
        this.sync();

        this.element.__insightInstance = this;
        DualListAssignment.instances.set(element, this);

        debugLog("New dual list assignment created: ", this.element);
    }

    bindEvents() {
        this.bind(this.addButton, "click", () => this.moveSelected(this.available, this.assigned));
        this.bind(this.removeButton, "click", () => this.moveSelected(this.assigned, this.available));
        this.bind(this.available, "dblclick", () => this.moveSelected(this.available, this.assigned));
        this.bind(this.assigned, "dblclick", () => this.moveSelected(this.assigned, this.available));
        this.bind(this.available, "change", () => this.updateButtons());
        this.bind(this.assigned, "change", () => this.updateButtons());
        this.bind(this.availableFilter, "input", () => this.filterOptions(this.available, this.availableFilter.value));
        this.bind(this.assignedFilter, "input", () => this.filterOptions(this.assigned, this.assignedFilter.value));
    }

    bind(element, type, handler) {
        if (!element) return;

        element.addEventListener(type, handler);
        this.boundHandlers.push({ element, type, handler });
    }

    moveSelected(source, target) {
        if (!source || !target) return;

        const selectedOptions = Array.from(source.selectedOptions).filter(option => !option.disabled);
        if (!selectedOptions.length) return;

        selectedOptions.forEach(option => {
            option.selected = false;
            target.appendChild(option);
        });

        this.sortOptions(source);
        this.sortOptions(target);
        this.sync();
        this.dispatchChange();
        target.focus();
    }

    sortOptions(select) {
        const sortedOptions = Array.from(select.options).sort((left, right) => {
            const leftIndex = Number.parseInt(left.dataset.index || "0", 10);
            const rightIndex = Number.parseInt(right.dataset.index || "0", 10);
            return leftIndex - rightIndex;
        });

        select.replaceChildren(...sortedOptions);
    }

    filterOptions(select, term) {
        if (!select) return;

        const normalizedTerm = term.trim().toLocaleLowerCase();
        Array.from(select.options).forEach(option => {
            const text = option.textContent.toLocaleLowerCase();
            option.hidden = Boolean(normalizedTerm) && !text.includes(normalizedTerm);
        });
    }

    sync() {
        this.syncHiddenInputs();
        this.updateCounts();
        this.updateButtons();
        this.updateStatus();
    }

    syncHiddenInputs() {
        if (!this.hidden || !this.assigned) return;

        this.hidden.replaceChildren();
        Array.from(this.assigned.options).forEach(option => {
            const input = document.createElement("input");
            input.type = "hidden";
            input.name = this.name;
            input.value = option.value;
            this.hidden.appendChild(input);
        });
    }

    updateCounts() {
        if (this.availableCount && this.available) {
            this.availableCount.textContent = `${this.available.options.length}`;
        }
        if (this.assignedCount && this.assigned) {
            this.assignedCount.textContent = `${this.assigned.options.length}`;
        }
    }

    updateButtons() {
        if (this.addButton && this.available) {
            this.addButton.disabled = this.available.selectedOptions.length === 0;
        }
        if (this.removeButton && this.assigned) {
            this.removeButton.disabled = this.assigned.selectedOptions.length === 0;
        }
    }

    updateStatus() {
        if (!this.status || !this.assigned) return;

        this.status.textContent = `${this.assigned.options.length} assigned`;
    }

    dispatchChange() {
        this.element.dispatchEvent(new CustomEvent("change", {
            bubbles: true,
            detail: {
                value: Array.from(this.assigned.options).map(option => option.value),
            },
        }));
    }

    destroy() {
        debugLog("Destroy dual list assignment: ", this.element);

        this.boundHandlers.forEach(({ element, type, handler }) => {
            element.removeEventListener(type, handler);
        });
        this.boundHandlers = [];

        DualListAssignment.instances.delete(this.element);
        delete this.element.__insightInstance;

        this.element = null;
    }

    static initAll() {
        document.querySelectorAll("[data-insight-dual-list-assignment]").forEach(el => new DualListAssignment(el));
    }
}
