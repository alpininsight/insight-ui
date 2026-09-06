// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Collapsible component for Insight UI.
 *
 * Creates a simple toggle button that shows/hides a target element.
 * Supports icon rotation and ARIA accessibility attributes.
 *
 * @example
 * // HTML structure
 * <button data-insight-collapsible="content1" aria-expanded="false">
 *   Toggle <span data-collapsible-icon>▶</span>
 * </button>
 * <div id="content1" class="hidden">Hidden content</div>
 */
export class Collapsible {
    /** @type {WeakMap<HTMLElement, Collapsible>} Weak references to prevent multiple initialization */
    static instances = new WeakMap();

    /**
     * Creates a new Collapsible instance.
     *
     * @param {HTMLElement} trigger - The trigger button element with data-insight-collapsible attribute
     */
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

    /**
     * Initializes the collapsible by binding the click handler.
     */
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

    /**
     * Initializes all collapsible instances on the page.
     *
     * @static
     */
    static initAll() {
        document.querySelectorAll('[data-insight-collapsible]').forEach(el => new Collapsible(el));
    }
}
