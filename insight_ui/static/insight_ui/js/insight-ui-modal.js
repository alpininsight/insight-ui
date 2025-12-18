class Modal {
    static instances = new WeakMap();
    static currentOpen = null;

    constructor(button) {
        if (InsightUI.Modal.instances.has(button)) {
            return InsightUI.Modal.instances.get(button);
        }

        this.button = button;
        this.targetId = button.getAttribute('data-insight-target');
        this.modal = document.getElementById(this.targetId);

        if (!this.modal) return;

        // Store bound handlers for cleanup
        this.boundButtonClick = null;
        this.boundCloseButtons = [];
        this.boundModalClick = null;

        this.bindEvents();
        InsightUI.Modal.instances.set(button, this);

        debugLog("New modal created: ", this.button, this.modal);
    }

    bindEvents() {
        this.boundButtonClick = (e) => {
            e.preventDefault();
            this.open();
        };
        this.button.addEventListener('click', this.boundButtonClick);

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
        if (InsightUI.Modal.currentOpen && InsightUI.Modal.currentOpen !== this) {
            InsightUI.Modal.currentOpen.close();
        }

        this.modal.style.display = 'block';
        InsightUI.Modal.currentOpen = this;

        InsightUI.utils.blockScroll();
        InsightUI.utils.trapFocus(this.modal);
    }

    close() {
        this.modal.style.display = 'none';
        if (InsightUI.Modal.currentOpen === this) {
            InsightUI.Modal.currentOpen = null;
        }

        InsightUI.utils.unblockScroll();
    }

    /**
     * Destroys the modal instance and removes all event listeners.
     * Call this before removing the element from DOM.
     */
    destroy() {
        // Close modal if open
        if (Modal.currentOpen === this) {
            this.close();
        }

        // Remove button click handler
        if (this.boundButtonClick) {
            this.button.removeEventListener('click', this.boundButtonClick);
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

        Modal.instances.delete(this.button);
        this.button = null;
        this.modal = null;
    }

    // Static method for initializing all modals
    static initAll() {
        document.querySelectorAll('[data-insight-toggle="modal"]').forEach(button => {
            new InsightUI.Modal(button);
        });
    }
};

window.InsightUI = window.InsightUI || {};
window.InsightUI.Modal = Modal;
