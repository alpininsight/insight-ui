class Floater {
    static instances = new WeakMap();
    static currentOpen = null;

    constructor(trigger, type = 'popover') {
        if (Floater.instances.has(trigger)) {
            return Floater.instances.get(trigger);
        }

        this.trigger = trigger;
        this.type = type; // 'tooltip' oder 'popover'
        this.targetId = trigger.getAttribute(`data-${type}-trigger`);
        this.target = document.getElementById(this.targetId);
        this.arrow = this.target?.querySelector(`.${type}-arrow`);
        this.hideTimeout = null;

        if (!this.target) return;

        this.triggerType = trigger.dataset.trigger || 'hover'; // hover or click
        this.autoClose = trigger.dataset.autoClose === "true";  // optional for click

        this.target.classList.add("absolute", "hidden", "z-50");

        this.bindEvents();

        Floater.instances.set(trigger, this);

        if (type == "popover") debugLog("New popover created: ", this.trigger, this.target);
        else debugLog("New tooltip created: ", this.trigger, this.target);
    }

    bindEvents() {
        if (this.triggerType === 'hover') {
            this.trigger.addEventListener("mouseover", e => { e.stopPropagation(); this.show(); });
            this.trigger.addEventListener("mouseout", e => { e.stopPropagation(); this.hideWithDelay(); });

            this.target.addEventListener("mouseover", e => { e.stopPropagation(); this.show(); });
            this.target.addEventListener("mouseout", e => { e.stopPropagation(); this.hideWithDelay(); });
        } else if (this.triggerType === 'click') {
            this.trigger.addEventListener("click", e => {
                e.stopPropagation();
                this.target.classList.contains("hidden") ? this.show() : this.hide();
            });

            if (this.autoClose) {
                document.addEventListener("click", (e) => {
                    if (!this.target.contains(e.target) && !this.trigger.contains(e.target)) {
                        this.hide();
                    }
                });
            }
        }

        window.addEventListener("scroll", () => this.updatePosition());
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

    // Static method for initializing all popovers and tooltips
    static initAll() {
        const popoverTriggers = document.querySelectorAll("[data-popover-trigger]");
        popoverTriggers.forEach(trigger => new Floater(trigger, 'popover'));

        const tooltipTriggers = document.querySelectorAll("[data-tooltip-trigger]");
        tooltipTriggers.forEach(trigger => new Floater(trigger, 'tooltip'));
    }
}

window.InsightUI = window.InsightUI || {};
window.InsightUI.Floater = Floater;
