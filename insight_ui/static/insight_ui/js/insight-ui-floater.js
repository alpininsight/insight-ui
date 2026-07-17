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
            this.arrow.classList.add("absolute", "left-1/2", "-translate-x-1/2", "rotate-45", "size-4", "bg-insight-secondary-background", "border-r", "border-b", "border-insight-primary-border");
        }

        if (type == "tooltip") {
            this.target = document.createElement('span');
            this.target.classList.add("text-primary", "bg-insight-secondary-background", "px-3", "py-1", "border", "border-insight-primary-border", "rounded-insight-overlay", "insight-shadow-subtle", "whitespace-nowrap");
            this.target.textContent = this.trigger.getAttribute("data-insight-tooltip");
        }
        else {
            this.targetId = trigger.getAttribute("data-insight-popover");
            this.target = document.getElementById(this.targetId);
        }

        if (!this.target) return;
        if (this.arrow) { this.target.appendChild(this.arrow); }

        this.target.classList.add("absolute", "hidden", "z-50");
        this.trigger.parentNode.appendChild(this.target);

        this.triggerType = trigger.dataset.trigger || 'hover'; // hover or click
        this.autoClose = trigger.dataset.autoClose === "true";  // optional for click
        this.followMouse = trigger.dataset.followMouse === "true";  // follow mouse position horizontally
        this.hideTimeout = null;
        this.attributeObserver = null;

        // Bind handlers for proper cleanup
        this.boundTriggerMouseover = this.handleTriggerMouseover.bind(this);
        this.boundTriggerMouseout = this.handleTriggerMouseout.bind(this);
        this.boundTargetMouseover = this.handleTargetMouseover.bind(this);
        this.boundTargetMouseout = this.handleTargetMouseout.bind(this);
        this.boundTriggerClick = this.handleTriggerClick.bind(this);
        this.boundDocumentClick = this.handleDocumentClick.bind(this);
        this.boundWindowScroll = this.handleWindowScroll.bind(this);
        this.boundTriggerMousemove = this.handleTriggerMousemove.bind(this);

        this.bindEvents();
        this.observeAttributeChanges();

        this.trigger.__insightInstance = this;
        Floater.instances.set(trigger, this);

        if (type == "popover") debugLog("New popover created: ", this.trigger, this.target);
        else debugLog("New tooltip created: ", this.trigger, this.target);
    }

    handleTriggerMouseover(e) { e.stopPropagation(); this.show(); }
    handleTriggerMouseout(e) { e.stopPropagation(); this.hideWithDelay(); }
    handleTargetMouseover(e) { e.stopPropagation(); this.show(); }
    handleTargetMouseout(e) { e.stopPropagation(); this.hideWithDelay(); }
    handleTriggerMousemove(e) {
        if (this.followMouse) {
            this.updatePositionFollowMouse(e);
        }
    }

    /**
     * Observe changes to the data-insight-tooltip attribute for dynamic updates.
     */
    observeAttributeChanges() {
        if (this.type !== "tooltip") return;

        this.attributeObserver = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'attributes' && mutation.attributeName === 'data-insight-tooltip') {
                    this.updateTooltipText();
                }
            });
        });
        this.attributeObserver.observe(this.trigger, { attributes: true, attributeFilter: ['data-insight-tooltip'] });
    }

    /**
     * Update the tooltip text from the trigger's data-insight-tooltip attribute.
     */
    updateTooltipText() {
        if (this.type !== "tooltip" || !this.target) return;
        const newText = this.trigger.getAttribute("data-insight-tooltip");
        if (this.target.textContent !== newText) {
            this.target.textContent = newText;
            if (this.arrow) {
                this.target.appendChild(this.arrow);
            }
        }
    }
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
            if (this.followMouse) {
                this.trigger.addEventListener("mousemove", this.boundTriggerMousemove);
            }
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

        // Check if already visible (e.g., mouse moved from trigger to tooltip)
        const wasVisible = !this.target.classList.contains("hidden");

        // Re-read tooltip text from attribute to support dynamic updates
        if (this.type === "tooltip") {
            this.target.textContent = this.trigger.getAttribute("data-insight-tooltip");
            if (this.arrow) {
                this.target.appendChild(this.arrow);
            }
        }

        this.target.classList.remove("hidden");

        // Only update position if tooltip was not already visible
        // For followMouse tooltips that are already visible, keep current position
        if (!wasVisible) {
            this.updatePosition();
        }

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
        const distanceToTarget = 12;
        const arrowSize = 8;

        // Some directions need slight adjustments, like + or - 1px.
        switch (position) {
            case 'top':
                this.target.style.top = `${rect.top + scrollY - this.target.offsetHeight - distanceToTarget}px`;
                this.target.style.left = `${rect.left + rect.width / 2 - this.target.offsetWidth / 2}px`;
                if (this.arrow) { this.arrow.style.top = `${this.target.offsetHeight - (arrowSize + 1)}px`; }
                break;

            case 'bottom':
                this.target.style.top = `${rect.bottom + scrollY + distanceToTarget}px`;
                this.target.style.left = `${rect.left + rect.width / 2 - this.target.offsetWidth / 2}px`;
                if (this.arrow) { this.arrow.classList.add('rotate-225'); this.arrow.style.top = `${-this.target.offsetHeight / 2 + arrowSize}px`; }
                break;

            case 'left':
                this.target.style.top = `${rect.top + rect.height / 2 - this.target.offsetHeight / 2 + scrollY}px`;
                this.target.style.left = `${rect.left - this.target.offsetWidth - distanceToTarget}px`;
                if (this.arrow) { this.arrow.classList.add('rotate-315'); this.arrow.style.top = `${this.target.offsetHeight / 2 - arrowSize}px`; this.arrow.style.left = `${this.target.offsetWidth - 1}px`; }
                break;

            case 'right':
                this.target.style.top = `${rect.top + rect.height / 2 - this.target.offsetHeight / 2 + scrollY}px`;
                this.target.style.left = `${rect.right + distanceToTarget}px`;
                if (this.arrow) { this.arrow.classList.add('rotate-135'); this.arrow.style.top = `${this.target.offsetHeight / 2 - arrowSize}px`; this.arrow.style.left = `-1px`; }
                break;
        }
    }

    /**
     * Update tooltip position to follow mouse cursor horizontally.
     * Vertical position remains relative to the trigger element.
     * Tooltip stays within viewport bounds and "sticks" to edges until
     * the cursor moves far enough for the tooltip to be centered again.
     * @param {MouseEvent} event - The mousemove event
     */
    updatePositionFollowMouse(event) {
        const position = this.trigger.getAttribute('data-position') || "top";
        const triggerRect = this.trigger.getBoundingClientRect();
        const parentRect = this.target.parentNode.getBoundingClientRect();
        const tooltipWidth = this.target.offsetWidth;
        const tooltipHalfWidth = tooltipWidth / 2;

        // Calculate horizontal position relative to parent, following mouse
        const mouseX = Math.max(triggerRect.left, Math.min(event.clientX, triggerRect.right));
        let left = mouseX - parentRect.left - tooltipHalfWidth;

        // Clamp to viewport bounds (tooltip sticks to edge until cursor is far enough for centering)
        const minLeft = -parentRect.left;  // Left edge of viewport relative to parent
        const maxLeft = window.innerWidth - parentRect.left - tooltipWidth;  // Right edge
        left = Math.max(minLeft, Math.min(left, maxLeft));

        this.target.style.left = `${left}px`;

        // Vertical position relative to parent
        switch (position) {
            case 'top':
                this.target.style.top = `${triggerRect.top - parentRect.top - this.target.offsetHeight - 8}px`;
                if (this.arrow) {
                    this.arrow.classList.add('rotate-180');
                    this.arrow.style.top = `${this.target.offsetHeight - 2}px`;
                    this.arrow.style.left = '50%';
                }
                break;

            case 'bottom':
                this.target.style.top = `${triggerRect.bottom - parentRect.top + 8}px`;
                if (this.arrow) {
                    this.arrow.classList.remove('rotate-180');
                    this.arrow.style.top = '';
                    this.arrow.style.left = '50%';
                }
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
            if (this.followMouse) {
                this.trigger.removeEventListener("mousemove", this.boundTriggerMousemove);
            }
        } else if (this.triggerType === 'click') {
            this.trigger.removeEventListener("click", this.boundTriggerClick);
            if (this.autoClose) {
                document.removeEventListener("click", this.boundDocumentClick);
            }
        }

        window.removeEventListener("scroll", this.boundWindowScroll);

        // Disconnect attribute observer
        if (this.attributeObserver) {
            this.attributeObserver.disconnect();
            this.attributeObserver = null;
        }

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
        document.querySelectorAll("[data-insight-popover]").forEach(trigger => new Floater(trigger, 'popover'));
        document.querySelectorAll("[data-insight-tooltip]").forEach(trigger => new Floater(trigger, 'tooltip'));
    }
}
