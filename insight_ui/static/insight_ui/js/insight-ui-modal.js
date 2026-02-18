export class Modal {
    // Manages all Modal instances of the DOM
    static instances = new WeakMap();

    // Handle of the open dialog
    static currentOpen = null;

    constructor(button) {
        // If an instance for this element already exists, return it
        if (Modal.instances.has(button)) {
            return Modal.instances.get(button);
        }

        this.button = button;
        this.targetId = button.getAttribute('data-insight-target');
        this.modal = document.getElementById(this.targetId);

        if (!this.modal) return;

        this.bindEvents();
        Modal.instances.set(button, this);

        debugLog("New modal created: ", this.button, this.modal);
    }

    bindEvents() {
        this.button.addEventListener('click', e => {
            e.preventDefault();
            this.open();
        });

        this.modal.querySelectorAll('[data-insight-dismiss="modal"]').forEach(closeBtn => {
            closeBtn.addEventListener('click', e => {
                e.preventDefault();
                this.close();
            });
        });

        this.modal.addEventListener('click', e => {
            if (e.target === this.modal) this.close();
        });
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

    // Static method for initializing all modals
    static initAll() {
        document.querySelectorAll('[data-insight-toggle="modal"]').forEach(openButton => new Modal(openButton));
    }
};
