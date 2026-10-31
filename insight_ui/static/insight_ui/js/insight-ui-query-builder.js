// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Query builder component for Insight UI.
 *
 * Adds and removes filter rows and fills the condition and value controls of a row when its
 * field changes. The field definitions come from a JSON script element next to the form. Rows
 * are numbered in document order, so the submitted parameters are "<param>-<index>-<part>".
 *
 * @example
 * // HTML structure (rendered by {% query_builder %})
 * <form id="book-filter" data-insight-query-builder data-param-name="filters">
 *   <script id="book-filter-fields" type="application/json">[…]</script>
 *   <div data-insight-query-builder-rows>
 *     <fieldset data-insight-query-builder-row>…</fieldset>
 *   </div>
 *   <template data-insight-query-builder-template><fieldset data-insight-query-builder-row>…</fieldset></template>
 *   <button type="button" data-insight-query-builder-add>Add filter</button>
 *   <p role="status" data-insight-query-builder-status></p>
 * </form>
 */
export class QueryBuilder {
    /** @type {WeakMap<HTMLElement, QueryBuilder>} Weak references to prevent multiple initialization */
    static instances = new WeakMap();

    /**
     * Creates a new QueryBuilder instance.
     *
     * @param {HTMLFormElement} element - The form element with data-insight-query-builder attribute
     */
    constructor(element) {
        if (QueryBuilder.instances.has(element)) {
            return QueryBuilder.instances.get(element);
        }

        this.element = element;
        this.paramName = element.dataset.paramName || "filters";
        this.rows = element.querySelector("[data-insight-query-builder-rows]");
        this.template = element.querySelector("template[data-insight-query-builder-template]");
        this.status = element.querySelector("[data-insight-query-builder-status]");
        this.help = element.querySelector("[data-insight-query-builder-help]");
        this.limitHint = element.querySelector("[data-insight-query-builder-limit]");
        this.addButton = element.querySelector("[data-insight-query-builder-add]");
        this.maxFilters = Number(element.dataset.maxFilters) || Infinity;

        const definitions = document.getElementById(`${element.id}-fields`);
        /** @type {Map<string, {field: string, label: string, operations: Object<string, string>, choices: Object<string, string>, input_type: string}>} */
        this.fields = new Map(JSON.parse(definitions?.textContent || "[]").map(field => [field.field, field]));

        this.boundClickHandler = this.handleClick.bind(this);
        this.boundChangeHandler = this.handleChange.bind(this);
        this.element.addEventListener("click", this.boundClickHandler);
        this.element.addEventListener("change", this.boundChangeHandler);
        this.updateState();

        this.element.__insightInstance = this;
        QueryBuilder.instances.set(element, this);

        debugLog("New query builder created: ", this.element);
    }

    /**
     * Handles the add and remove buttons.
     *
     * @param {MouseEvent} event - The click event
     */
    handleClick(event) {
        if (event.target.closest("[data-insight-query-builder-add]")) {
            this.addRow();
            return;
        }
        const removeButton = event.target.closest("[data-insight-query-builder-remove]");
        if (removeButton) {
            this.removeRow(removeButton.closest("[data-insight-query-builder-row]"));
        }
    }

    /**
     * Rebuilds the condition and value controls when a row's field changes, and shows the
     * OR divider when a row's logic changes.
     *
     * @param {Event} event - The change event
     */
    handleChange(event) {
        if (event.target.matches('[data-insight-query-builder-part="field"]')) {
            this.updateField(event.target.closest("[data-insight-query-builder-row]"));
        } else if (event.target.matches('[data-insight-query-builder-part="logic"]')) {
            this.renumber();
        }
    }

    /**
     * Returns the filter rows in document order.
     *
     * @returns {HTMLElement[]}
     */
    getRows() {
        return [...this.rows.querySelectorAll(":scope > [data-insight-query-builder-row]")];
    }

    /**
     * Appends an empty filter row and moves the focus to its field select.
     */
    addRow() {
        if (this.getRows().length >= this.maxFilters) return;
        const row = this.template.content.firstElementChild.cloneNode(true);
        this.rows.append(row);
        this.renumber();
        row.querySelector('[data-insight-query-builder-part="field"]').focus();
        this.announce(gettext("Filter added"));
    }

    /**
     * Removes a filter row and moves the focus to the row now at its position, or to the add button.
     *
     * @param {HTMLElement} row - The row to remove
     */
    removeRow(row) {
        const index = this.getRows().indexOf(row);
        row.remove();
        this.renumber();

        const rows = this.getRows();
        if (rows.length) {
            rows[Math.min(index, rows.length - 1)].querySelector('[data-insight-query-builder-part="field"]').focus();
        } else {
            this.element.querySelector("[data-insight-query-builder-add]")?.focus();
        }
        this.announce(gettext("Filter removed"));
    }

    /**
     * Sets names, IDs and legends from the row positions; the first row has no AND/OR choice.
     */
    renumber() {
        this.getRows().forEach((row, index) => {
            // OR starts a new group, so a divider separates it from the previous filters.
            const or = row.querySelector('[data-insight-query-builder-part="logic"][value="OR"]');
            row.querySelector("[data-insight-query-builder-divider]").hidden = index === 0 || !or.checked;

            const legend = row.querySelector("[data-insight-query-builder-legend]");
            legend.textContent = interpolate(gettext("Filter %(number)s"), { number: index + 1 }, true);

            const logic = row.querySelector("[data-insight-query-builder-logic]");
            // The first row keeps the space of the AND/OR choice, so the columns of all rows line up.
            logic.classList.toggle("invisible", index === 0);
            logic.classList.toggle("max-md:hidden", index === 0);
            logic.disabled = index === 0;

            row.querySelectorAll("[data-insight-query-builder-part]").forEach(control => {
                const part = control.dataset.insightQueryBuilderPart;
                control.name = `${this.paramName}-${index}-${part}`;
                if (part !== "logic") control.id = `${this.element.id}-${index}-${part}`;
            });
            row.querySelectorAll("[data-insight-query-builder-label]").forEach(label => {
                label.htmlFor = `${this.element.id}-${index}-${label.dataset.insightQueryBuilderLabel}`;
                // Only the first row shows the column labels on wide screens.
                label.classList.toggle("md:sr-only", index > 0);
            });
        });
        this.updateState();
    }

    /**
     * Shows the precedence hint from two filters on and blocks adding beyond the limit.
     */
    updateState() {
        const count = this.getRows().length;
        if (this.help) this.help.hidden = count < 2;
        const atLimit = count >= this.maxFilters;
        if (this.addButton) this.addButton.disabled = atLimit;
        if (this.limitHint) this.limitHint.hidden = !atLimit;
    }

    /**
     * Fills the condition select and replaces the value control for the selected field.
     *
     * @param {HTMLElement} row - The row whose field changed
     */
    updateField(row) {
        const fieldSelect = row.querySelector('[data-insight-query-builder-part="field"]');
        const definition = this.fields.get(fieldSelect.value);

        const operator = row.querySelector('[data-insight-query-builder-part="operator"]');
        const hint = gettext("Choose a field first");
        operator.replaceChildren(...(definition ? QueryBuilder.options(definition.operations) : [new Option(hint, "")]));
        operator.disabled = !definition;

        const oldValue = row.querySelector('[data-insight-query-builder-part="value"]');
        const choices = definition?.choices ?? {};
        let value;
        if (Object.keys(choices).length) {
            value = document.createElement("select");
            value.append(...QueryBuilder.options(choices));
        } else {
            value = document.createElement("input");
            value.type = definition?.input_type || "text";
            if (value.type === "number") value.step = "any";
            if (!definition) value.placeholder = hint;
        }
        value.className = oldValue.className;
        value.dataset.insightQueryBuilderPart = "value";
        value.required = true;
        value.disabled = !definition;
        oldValue.replaceWith(value);
        this.renumber();
    }

    /**
     * Creates option elements from a value-to-label mapping.
     *
     * @param {Object<string, string>} [mapping] - The options
     * @returns {HTMLOptionElement[]}
     */
    static options(mapping) {
        return Object.entries(mapping ?? {}).map(([value, label]) => new Option(label, value));
    }

    /**
     * Announces a change to screen readers.
     *
     * @param {string} message - The message
     */
    announce(message) {
        if (this.status) this.status.textContent = message;
    }

    /**
     * Destroys the query builder instance and removes its event listeners.
     */
    destroy() {
        debugLog("Destroy query builder: ", this.element);

        this.element.removeEventListener("click", this.boundClickHandler);
        this.element.removeEventListener("change", this.boundChangeHandler);

        QueryBuilder.instances.delete(this.element);
        delete this.element.__insightInstance;

        this.element = null;
    }

    /**
     * Initializes all query builder instances on the page.
     *
     * @static
     */
    static initAll() {
        document.querySelectorAll("[data-insight-query-builder]").forEach(el => new QueryBuilder(el));
    }
}
