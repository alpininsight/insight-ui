// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Badge list component for Insight UI.
 *
 * Keeps the keyboard focus in a list of removable badges. Removing a badge usually makes the
 * server re-render the list, which drops the focused button and sends the focus back to the
 * start of the page. After the HTMX swap the focus moves to the remove button at the same
 * position (the next badge), to the previous one if the last badge was removed, or to the
 * list itself once it is empty.
 *
 * @example
 * // HTML structure
 * <div id="active-filters" data-insight-badge-list>
 *   <ul role="list" aria-label="Active filters" tabindex="-1">
 *     <li><div class="badge">Country: Germany <button data-insight-badge-remove hx-get="…">×</button></div></li>
 *   </ul>
 *   <button data-insight-badge-clear-all hx-get="…">Remove all</button>
 * </div>
 */
export class BadgeList {
    /** @type {WeakMap<HTMLElement, BadgeList>} Weak references to prevent multiple initialization */
    static instances = new WeakMap();

    /**
     * The remove action waiting for its HTMX swap. It outlives the instance, because the swap
     * replaces the list element. An index of -1 focuses the list itself.
     *
     * @type {{listId: string, index: number, trigger: HTMLElement} | null}
     */
    static pendingFocus = null;

    /** @type {boolean} Whether the document-wide HTMX listeners are registered */
    static documentListenersBound = false;

    /**
     * Creates a new BadgeList instance.
     *
     * @param {HTMLElement} element - The container element with data-insight-badge-list attribute
     */
    constructor(element) {
        if (BadgeList.instances.has(element)) {
            return BadgeList.instances.get(element);
        }

        this.element = element;
        this.boundClickHandler = this.handleClick.bind(this);
        this.element.addEventListener("click", this.boundClickHandler);
        BadgeList.bindDocumentListeners();

        this.element.__insightInstance = this;
        BadgeList.instances.set(element, this);

        debugLog("New badge list created: ", this.element);
    }

    /**
     * Remembers which badge is being removed, so the focus can be restored after the swap.
     *
     * @param {MouseEvent} event - The click event
     */
    handleClick(event) {
        const removeButton = event.target.closest("[data-insight-badge-remove]");
        const clearAllButton = event.target.closest("[data-insight-badge-clear-all]");
        if (removeButton) {
            const buttons = [...this.element.querySelectorAll("[data-insight-badge-remove]")];
            BadgeList.pendingFocus = { listId: this.element.id, index: buttons.indexOf(removeButton), trigger: removeButton };
        } else if (clearAllButton) {
            BadgeList.pendingFocus = { listId: this.element.id, index: -1, trigger: clearAllButton };
        }
    }

    /**
     * Registers the document-wide HTMX listeners once for all badge lists.
     */
    static bindDocumentListeners() {
        if (BadgeList.documentListenersBound) return;
        BadgeList.documentListenersBound = true;

        document.addEventListener("htmx:afterSettle", (event) => BadgeList.restoreFocus(event));
        document.addEventListener("htmx:afterRequest", (event) => {
            // A failed request leaves the list unchanged, so there is nothing to restore.
            if (!event.detail?.successful && event.detail?.requestConfig?.elt === BadgeList.pendingFocus?.trigger) {
                BadgeList.pendingFocus = null;
            }
        });
    }

    /**
     * Moves the focus into the re-rendered list after the remove request was swapped.
     *
     * @param {CustomEvent} event - The htmx:afterSettle event
     */
    static restoreFocus(event) {
        const pending = BadgeList.pendingFocus;
        // Ignore swaps of other requests, e.g. polling content, that settle in the meantime.
        if (!pending || event.detail?.requestConfig?.elt !== pending.trigger) return;
        BadgeList.pendingFocus = null;

        const list = document.getElementById(pending.listId);
        if (!list) return;

        const buttons = list.querySelectorAll("[data-insight-badge-remove]");
        if (pending.index >= 0 && buttons.length > 0) {
            buttons[Math.min(pending.index, buttons.length - 1)].focus();
        } else {
            list.querySelector("ul")?.focus();
        }
    }

    /**
     * Destroys the badge list instance and removes its event listener.
     * A pending focus is kept, because destroy runs when the swap replaces the list.
     */
    destroy() {
        debugLog("Destroy badge list: ", this.element);

        this.element.removeEventListener("click", this.boundClickHandler);

        BadgeList.instances.delete(this.element);
        delete this.element.__insightInstance;

        this.element = null;
    }

    /**
     * Initializes all badge list instances on the page.
     *
     * @static
     */
    static initAll() {
        document.querySelectorAll("[data-insight-badge-list]").forEach(el => new BadgeList(el));
    }
}
