export class Floater {
    // Weak references used to prevent multiple initialization of the same instance
    static instances = new WeakMap();

    // Handle of the open floater
    static currentOpen = null;

    constructor(trigger, type = 'popover') {
        // If an instance for this element already exists, return it
        if (Floater.instances.has(trigger)) {
            return Floater.instances.get(trigger);
        }

        this.trigger = trigger;
        this.type = type; // 'tooltip' or 'popover'

        if (this.trigger.getAttribute("data-show-arrow")) {
            this.arrow = document.createElement('div');
            this.arrow.classList.add("absolute", "left-1/2", "-top-2", "-translate-x-1/2", "size-0", "border-10", "border-t-0", "border-transparent", "border-b-white", "dark:border-b-gray-600");
        }

        if (type == "tooltip") {
            this.target = document.createElement('span');
            this.target.classList.add("text-primary", "bg-white", "dark:bg-gray-600", "px-3", "py-1", "border", "border-gray-300", "dark:border-0", "rounded-sm", "shadow");
            this.target.textContent = this.trigger.getAttribute("data-tooltip");
        }
        else {
            this.targetId = trigger.getAttribute("data-popover");
            this.target = document.getElementById(this.targetId);
        }

        if (!this.target) return;
        if (this.arrow) { this.target.appendChild(this.arrow); }

        this.target.classList.add("absolute", "hidden", "z-50");
        this.trigger.parentNode.appendChild(this.target);

        this.triggerType = trigger.dataset.trigger || 'hover'; // hover or click
        this.autoClose = trigger.dataset.autoClose === "true";  // optional for click
        this.hideTimeout = null;

        // Bind handlers for proper cleanup
        this.boundTriggerMouseover = this.handleTriggerMouseover.bind(this);
        this.boundTriggerMouseout = this.handleTriggerMouseout.bind(this);
        this.boundTargetMouseover = this.handleTargetMouseover.bind(this);
        this.boundTargetMouseout = this.handleTargetMouseout.bind(this);
        this.boundTriggerClick = this.handleTriggerClick.bind(this);
        this.boundDocumentClick = this.handleDocumentClick.bind(this);
        this.boundWindowScroll = this.handleWindowScroll.bind(this);

        this.bindEvents();

        this.trigger.__insightInstance = this;
        Floater.instances.set(trigger, this);

        if (type == "popover") debugLog("New popover created: ", this.trigger, this.target);
        else debugLog("New tooltip created: ", this.trigger, this.target);
    }

    handleTriggerMouseover(e) { e.stopPropagation(); this.show(); }
    handleTriggerMouseout(e) { e.stopPropagation(); this.hideWithDelay(); }
    handleTargetMouseover(e) { e.stopPropagation(); this.show(); }
    handleTargetMouseout(e) { e.stopPropagation(); this.hideWithDelay(); }
    handleTriggerClick(e) {
        e.stopPropagation();
        this.target.classList.contains("hidden") ? this.show() : this.hide();
    }
    handleDocumentClick(e) {
        if (!this.target.contains(e.target) && !this.trigger.contains(e.target)) {
            this.hide();
        }
    }
    handleWindowScroll() { this.updatePosition(); }

    bindEvents() {
        if (this.triggerType === 'hover') {
            this.trigger.addEventListener("mouseover", this.boundTriggerMouseover);
            this.trigger.addEventListener("mouseout", this.boundTriggerMouseout);
            this.target.addEventListener("mouseover", this.boundTargetMouseover);
            this.target.addEventListener("mouseout", this.boundTargetMouseout);
        } else if (this.triggerType === 'click') {
            this.trigger.addEventListener("click", this.boundTriggerClick);
            if (this.autoClose) {
                document.addEventListener("click", this.boundDocumentClick);
            }
        }

        window.addEventListener("scroll", this.boundWindowScroll);
    }

    show() {
        // Close currently open popover or tooltip
        if (Floater.currentOpen && Floater.currentOpen !== this) {
            Floater.currentOpen.hide();
        }

        clearTimeout(this.hideTimeout);
        this.target.classList.remove("hidden");
        this.updatePosition();

        Floater.currentOpen = this;
    }

    hideWithDelay() {
        this.hideTimeout = setTimeout(() => this.hide(), 100);
    }

    hide() {
        this.target.classList.add("hidden");
        if (Floater.currentOpen === this) {
            Floater.currentOpen = null;
        }
    }

    updatePosition() {
        const position = this.trigger.getAttribute('data-position') || "top";
        const rect = this.trigger.getBoundingClientRect();
        const scrollY = window.scrollY || document.documentElement.scrollTop;

        switch (position) {
            case 'top':
                this.target.style.top = `${rect.top + scrollY - this.target.offsetHeight - 8}px`;
                this.target.style.left = `${rect.left + rect.width / 2 - this.target.offsetWidth / 2}px`;
                if (this.arrow) { this.arrow.classList.add('rotate-180'); this.arrow.style.top = `${this.target.offsetHeight - 2}px`; }
                break;

            case 'bottom':
                this.target.style.top = `${rect.bottom + scrollY + 8}px`;
                this.target.style.left = `${rect.left + rect.width / 2 - this.target.offsetWidth / 2}px`;
                if (this.arrow) { this.arrow.classList.remove('rotate-180'); this.arrow.style.top = ''; }
                break;

            case 'left':
                this.target.style.top = `${rect.top + rect.height / 2 - this.target.offsetHeight / 2 + scrollY}px`;
                this.target.style.left = `${rect.left - this.target.offsetWidth - 8}px`;
                if (this.arrow) { this.arrow.classList.add('rotate-90'); this.arrow.style.top = `${this.target.offsetHeight / 2 - 5}px`; this.arrow.style.left = `${this.target.offsetWidth + 3}px`; }
                break;

            case 'right':
                this.target.style.top = `${rect.top + rect.height / 2 - this.target.offsetHeight / 2 + scrollY}px`;
                this.target.style.left = `${rect.right + 8}px`;
                if (this.arrow) { this.arrow.classList.add('-rotate-90'); this.arrow.style.top = `${this.target.offsetHeight / 2 - 5}px`; this.arrow.style.left = `-3px`; }
                break;
        }
    }

    /**
     * Destroys the floater instance and removes all event listeners.
     * Call this before removing the element from DOM.
     */
    destroy() {
        debugLog("Destroy floater: ", this.trigger, this.target);

        // Clear any pending timeout
        if (this.hideTimeout) {
            clearTimeout(this.hideTimeout);
            this.hideTimeout = null;
        }

        // Remove event listeners based on trigger type
        if (this.triggerType === 'hover') {
            this.trigger.removeEventListener("mouseover", this.boundTriggerMouseover);
            this.trigger.removeEventListener("mouseout", this.boundTriggerMouseout);
            this.target.removeEventListener("mouseover", this.boundTargetMouseover);
            this.target.removeEventListener("mouseout", this.boundTargetMouseout);
        } else if (this.triggerType === 'click') {
            this.trigger.removeEventListener("click", this.boundTriggerClick);
            if (this.autoClose) {
                document.removeEventListener("click", this.boundDocumentClick);
            }
        }

        window.removeEventListener("scroll", this.boundWindowScroll);

        if (Floater.currentOpen === this) {
            Floater.currentOpen = null;
        }

        Floater.instances.delete(this.trigger);
        delete this.trigger.__insightInstance;

        this.trigger = null;
        this.target = null;
    }

    // Static method for initializing all popovers and tooltips
    static initAll() {
        document.querySelectorAll("[data-popover]").forEach(trigger => new Floater(trigger, 'popover'));
        document.querySelectorAll("[data-tooltip]").forEach(trigger => new Floater(trigger, 'tooltip'));
    }
}
