/**
 * Modal dialog component for Insight UI.
 *
 * Creates accessible modal dialogs with focus trapping, backdrop click to close,
 * and scroll blocking. Only one modal can be open at a time.
 *
 * @example
 * // HTML structure
 * <button data-insight-modal="modal1">Open Modal</button>
 * <div id="modal1" style="display: none;">
 *   <div>Modal content</div>
 *   <button data-insight-dismiss="modal">Close</button>
 * </div>
 */
export class Modal {
    /** @type {WeakMap<HTMLElement, Modal>} Weak references to prevent multiple initialization */
    static instances = new WeakMap();

    /** @type {Modal|null} Currently open modal instance */
    static currentOpen = null;

    /**
     * Creates a new Modal instance.
     *
     * @param {HTMLElement} trigger - The trigger button element with data-insight-modal attribute
     */
    constructor(trigger) {
        // If an instance for this element already exists, return it
        if (Modal.instances.has(trigger)) {
            return Modal.instances.get(trigger);
        }

        this.trigger = trigger;
        this.targetId = trigger.getAttribute('data-insight-modal');

        // Don't store modal reference - look it up dynamically to support HTMX swaps
        if (!document.getElementById(this.targetId)) return;

        // Store bound handlers for cleanup
        this.boundButtonClick = null;
        this.boundModalClick = null;
        this.boundKeyDown = null;
        this.releaseFocusTrap = null;
        this.triggerElement = null;

        this.bindEvents();

        this.trigger.__insightInstance = this;
        Modal.instances.set(trigger, this);

        debugLog("New modal created: ", this.trigger, this.targetId);
    }

    /**
     * Gets the current modal element (looked up dynamically to support HTMX swaps).
     *
     * @returns {HTMLElement|null} The modal element or null if not found
     */
    getModal() {
        return document.getElementById(this.targetId);
    }

    /**
     * Binds event listeners to the trigger button.
     * Modal and close button listeners are bound dynamically in open().
     */
    bindEvents() {
        this.boundButtonClick = (e) => {
            e.preventDefault();
            this.open();
        };
        this.trigger.addEventListener('click', this.boundButtonClick);
    }

    /**
     * Opens the modal dialog.
     * Closes any other open modal, blocks scroll, and traps focus.
     */
    open() {
        const modal = this.getModal();
        if (!modal) {
            debugLog("Modal not found: ", this.targetId);
            return;
        }

        if (Modal.currentOpen && Modal.currentOpen !== this) {
            Modal.currentOpen.close();
        }

        // Store trigger for focus return
        this.triggerElement = document.activeElement;

        // Bind close button handlers (dynamic - supports HTMX swaps)
        this.boundCloseButtons = [];
        modal.querySelectorAll('[data-insight-dismiss="modal"]').forEach(closeBtn => {
            const handler = (e) => {
                e.preventDefault();
                this.close();
            };
            this.boundCloseButtons.push({ element: closeBtn, handler });
            closeBtn.addEventListener('click', handler);
        });

        // Bind backdrop click handler
        this.boundModalClick = (e) => {
            if (e.target === modal) this.close();
        };
        modal.addEventListener('click', this.boundModalClick);

        modal.style.display = 'block';
        Modal.currentOpen = this;

        InsightUI.utils.blockScroll();
        this.releaseFocusTrap = InsightUI.utils.trapFocus(modal);

        // Add Escape key handler
        this.boundKeyDown = (e) => {
            if (e.key === 'Escape') {
                e.preventDefault();
                this.close();
            }
        };
        document.addEventListener('keydown', this.boundKeyDown);
    }

    /**
     * Closes the modal dialog and restores scroll.
     */
    close() {
        const modal = this.getModal();

        // Remove Escape key handler
        if (this.boundKeyDown) {
            document.removeEventListener('keydown', this.boundKeyDown);
            this.boundKeyDown = null;
        }

        // Remove close button handlers
        if (this.boundCloseButtons) {
            this.boundCloseButtons.forEach(({ element, handler }) => {
                element.removeEventListener('click', handler);
            });
            this.boundCloseButtons = [];
        }

        // Remove modal backdrop click handler
        if (modal && this.boundModalClick) {
            modal.removeEventListener('click', this.boundModalClick);
            this.boundModalClick = null;
        }

        if (modal) {
            modal.style.display = 'none';
        }

        if (Modal.currentOpen === this) {
            Modal.currentOpen = null;
        }

        // Release focus trap
        if (this.releaseFocusTrap) {
            this.releaseFocusTrap();
            this.releaseFocusTrap = null;
        }

        InsightUI.utils.unblockScroll();

        // Return focus to trigger element
        if (this.triggerElement && typeof this.triggerElement.focus === 'function') {
            this.triggerElement.focus();
        }
        this.triggerElement = null;
    }

    /**
     * Destroys the modal instance and removes all event listeners.
     * Call this before removing the element from DOM.
     */
    destroy() {
        debugLog("Destroy modal: ", this.trigger, this.targetId);

        // Close modal if open (this also cleans up close button and backdrop handlers)
        if (Modal.currentOpen === this) {
            this.close();
        }

        // Remove button click handler
        if (this.boundButtonClick) {
            this.trigger.removeEventListener('click', this.boundButtonClick);
        }

        // Remove keydown handler
        if (this.boundKeyDown) {
            document.removeEventListener('keydown', this.boundKeyDown);
        }

        Modal.instances.delete(this.trigger);
        delete this.trigger.__insightInstance;

        this.trigger = null;
        this.targetId = null;
    }

    /**
     * Initializes all modal instances on the page.
     *
     * @static
     */
    static initAll() {
        document.querySelectorAll('[data-insight-modal]').forEach(openButton => new Modal(openButton));
    }
}
