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

        this.bindEvents();
        InsightUI.Modal.instances.set(button, this);

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

    // Static method for initializing all modals
    static initAll() {
        document.querySelectorAll('[data-insight-toggle="modal"]').forEach(button => {
            new InsightUI.Modal(button);
        });
    }
};

window.InsightUI = window.InsightUI || {};
window.InsightUI.Modal = Modal;
