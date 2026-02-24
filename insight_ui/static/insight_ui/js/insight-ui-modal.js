export class Modal {
    // Weak references used to prevent multiple initialization of the same instance
    static instances = new WeakMap();

    // Handle of the open dialog
    static currentOpen = null;

    constructor(trigger) {
        // If an instance for this element already exists, return it
        if (Modal.instances.has(trigger)) {
            return Modal.instances.get(trigger);
        }

        this.trigger = trigger;
        this.targetId = trigger.getAttribute('data-insight-target');
        this.modal = document.getElementById(this.targetId);

        if (!this.modal) return;

        // Store bound handlers for cleanup
        this.boundButtonClick = null;
        this.boundCloseButtons = [];
        this.boundModalClick = null;

        this.bindEvents();

        this.trigger.__insightInstance = this;
        Modal.instances.set(trigger, this);

        debugLog("New modal created: ", this.trigger, this.modal);
    }

    bindEvents() {
        this.boundButtonClick = (e) => {
            e.preventDefault();
            this.open();
        };
        this.trigger.addEventListener('click', this.boundButtonClick);

        this.modal.querySelectorAll('[data-insight-dismiss="modal"]').forEach(closeBtn => {
            const handler = (e) => {
                e.preventDefault();
                this.close();
            };
            this.boundCloseButtons.push({ element: closeBtn, handler });
            closeBtn.addEventListener('click', handler);
        });

        this.boundModalClick = (e) => {
            if (e.target === this.modal) this.close();
        };
        this.modal.addEventListener('click', this.boundModalClick);
    }

    open() {
        if (Modal.currentOpen && Modal.currentOpen !== this) {
            Modal.currentOpen.close();
        }

        this.modal.style.display = 'block';
        Modal.currentOpen = this;

        InsightUI.utils.blockScroll();
        InsightUI.utils.trapFocus(this.modal);
    }

    close() {
        this.modal.style.display = 'none';
        if (Modal.currentOpen === this) {
            Modal.currentOpen = null;
        }

        InsightUI.utils.unblockScroll();
    }

    /**
     * Destroys the modal instance and removes all event listeners.
     * Call this before removing the element from DOM.
     */
    destroy() {
        debugLog("Destroy modal: ", this.trigger, this.modal);

        // Close modal if open
        if (Modal.currentOpen === this) {
            this.close();
        }

        // Remove button click handler
        if (this.boundButtonClick) {
            this.trigger.removeEventListener('click', this.boundButtonClick);
        }

        // Remove close button handlers
        this.boundCloseButtons.forEach(({ element, handler }) => {
            element.removeEventListener('click', handler);
        });
        this.boundCloseButtons = [];

        // Remove modal backdrop click handler
        if (this.boundModalClick) {
            this.modal.removeEventListener('click', this.boundModalClick);
        }

        Modal.instances.delete(this.trigger);
        delete this.trigger.__insightInstance;

        this.trigger = null;
        this.modal = null;
    }

    // Static method for initializing all modals
    static initAll() {
        document.querySelectorAll('[data-insight-toggle="modal"]').forEach(openButton => new Modal(openButton));
    }
};
