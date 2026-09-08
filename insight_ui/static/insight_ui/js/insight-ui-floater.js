/**
 * Floater component for Insight UI (tooltips and popovers).
 *
 * Creates floating UI elements that appear on hover or click, with support for
 * multiple positions (top, bottom, left, right), arrows, auto-close behavior,
 * and mouse-following tooltips.
 *
 * @example
 * // Tooltip
 * <span data-insight-tooltip="Help text" data-position="top">Hover me</span>
 *
 * // Popover
 * <button data-insight-popover="popover1" data-trigger="click">Click me</button>
 * <div id="popover1">Popover content</div>
 */
export class Floater {
    /** @type {WeakMap<HTMLElement, Floater>} Weak references to prevent multiple initialization */
    static instances = new WeakMap();

    /** @type {Floater|null} Currently open floater instance */
    static currentOpen = null;

    /**
     * Creates a new Floater instance (tooltip or popover).
     *
     * @param {HTMLElement} trigger - The trigger element
     * @param {string} [type='popover'] - The floater type: "tooltip" or "popover"
     */
    constructor(trigger, type = 'popover') {
        // If an instance for this element already exists, return it
        if (Floater.instances.has(trigger)) {
            return Floater.instances.get(trigger);
        }

        this.trigger = trigger;
        this.type = type; // 'tooltip' or 'popover'

        if (this.trigger.getAttribute("data-show-arrow")) {
            this.arrow = document.createElement('div');
            this.arrow.classList.add("absolute", "left-1/2", "-translate-x-1/2", "rotate-45", "size-4", "bg-insight-surface", "border-r", "border-b", "border-insight-surface");
        }

        if (type === "tooltip") {
            const tooltipText = this.trigger.getAttribute("data-insight-tooltip");

            // Visual tooltip element (hidden by default)
            this.target = document.createElement('span');
            this.target.classList.add("text-insight-headline", "bg-insight-surface", "px-3", "py-2", "border", "border-insight-surface", "rounded-insight-overlay", "shadow-insight-overlay", "max-w-xs", "text-sm");
            this.target.textContent = tooltipText;
            this.target.setAttribute("role", "tooltip");
            this.target.setAttribute("aria-hidden", "true");  // Visual tooltip is decorative

            // Screen-reader accessible description (always available via sr-only)
            this.srDescription = document.createElement('span');
            this.srDescription.classList.add("sr-only");
            this.srDescription.textContent = tooltipText;
            this.targetId = `tooltip-${Math.random().toString(36).substring(2, 9)}`;
            this.srDescription.id = this.targetId;
            this.trigger.appendChild(this.srDescription);
            this.trigger.setAttribute("aria-describedby", this.targetId);
        }
        else {
            this.targetId = trigger.getAttribute("data-insight-popover");
            this.target = document.getElementById(this.targetId);
            // Set ARIA attributes for popover
            if (this.target) {
                this.target.setAttribute("role", "dialog");
                this.trigger.setAttribute("aria-expanded", "false");
                this.trigger.setAttribute("aria-controls", this.targetId);
            }
        }

        if (!this.target)
        {
            debugLog("No floater target for: ", this.trigger, " found!");
            return;
        }
        if (this.arrow) { this.target.appendChild(this.arrow); }

        this.target.classList.add("fixed", "hidden", "z-50");
        document.body.appendChild(this.target);

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
        this.boundTriggerFocus = this.handleTriggerFocus.bind(this);
        this.boundTriggerBlur = this.handleTriggerBlur.bind(this);
        this.boundTargetBlur = this.handleTargetBlur.bind(this);
        this.boundKeyDown = this.handleKeyDown.bind(this);

        this.bindEvents();
        this.observeAttributeChanges();

        this.trigger.__insightInstance = this;
        Floater.instances.set(trigger, this);

        if (type === "popover") debugLog("New popover created: ", this.trigger, this.target);
        else debugLog("New tooltip created: ", this.trigger, this.target);
    }

    /**
     * Handles mouseover on the trigger element.
     *
     * @param {MouseEvent} e - The mouseover event
     */
    handleTriggerMouseover(e) { e.stopPropagation(); this.show(); }

    /**
     * Handles mouseout from the trigger element.
     *
     * @param {MouseEvent} e - The mouseout event
     */
    handleTriggerMouseout(e) { e.stopPropagation(); this.hideWithDelay(); }

    /**
     * Handles mouseover on the target element.
     *
     * @param {MouseEvent} e - The mouseover event
     */
    handleTargetMouseover(e) { e.stopPropagation(); this.show(); }

    /**
     * Handles mouseout from the target element.
     *
     * @param {MouseEvent} e - The mouseout event
     */
    handleTargetMouseout(e) { e.stopPropagation(); this.hideWithDelay(); }
    /**
     * Handles mouse movement for follow-mouse mode.
     *
     * @param {MouseEvent} e - The mousemove event
     */
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
            // Also update the screen-reader description
            if (this.srDescription) {
                this.srDescription.textContent = newText;
            }
        }
    }
    /**
     * Handles click on the trigger for click-triggered floaters.
     *
     * @param {MouseEvent} e - The click event
     */
    handleTriggerClick(e) {
        e.stopPropagation();
        this.target.classList.contains("hidden") ? this.show() : this.hide();
    }

    /**
     * Handles clicks outside the floater to close it (for auto-close mode).
     *
     * @param {MouseEvent} e - The click event
     */
    handleDocumentClick(e) {
        if (!this.target.contains(e.target) && !this.trigger.contains(e.target)) {
            this.hide();
        }
    }

    /** Updates position on scroll. */
    handleWindowScroll() { this.updatePosition(); }

    /**
     * Handles focus on the trigger element (for keyboard accessibility).
     * Only shows tooltip if focus is keyboard-initiated (not programmatic).
     */
    handleTriggerFocus() {
        // Only show if focus is visible (keyboard navigation, not programmatic)
        if (this.trigger.matches(':focus-visible')) {
            this.show();
        }
    }

    /**
     * Handles blur from the trigger element.
     * Only hides if focus moves outside both trigger and target.
     *
     * @param {FocusEvent} e - The blur event
     */
    handleTriggerBlur(e) {
        // Check if focus is moving to the target (popover/tooltip content)
        const relatedTarget = e.relatedTarget;
        if (relatedTarget && (this.target.contains(relatedTarget) || this.trigger.contains(relatedTarget))) {
            return; // Don't hide if focus is moving within the floater
        }
        this.hideWithDelay();
    }

    /**
     * Handles blur from the target element (popover/tooltip content).
     * Only hides if focus moves outside both trigger and target.
     *
     * @param {FocusEvent} e - The blur event
     */
    handleTargetBlur(e) {
        const relatedTarget = e.relatedTarget;
        if (relatedTarget && (this.target.contains(relatedTarget) || this.trigger.contains(relatedTarget))) {
            return; // Don't hide if focus is moving within the floater
        }
        this.hideWithDelay();
    }

    /**
     * Handles keyboard events for accessibility.
     *
     * @param {KeyboardEvent} e - The keyboard event
     */
    handleKeyDown(e) {
        // Escape closes the floater
        if (e.key === 'Escape' && !this.target.classList.contains("hidden")) {
            e.preventDefault();
            this.hide();
            return;
        }

        // For click-triggered floaters, Enter/Space toggles
        if (this.triggerType === 'click' && (e.key === 'Enter' || e.key === ' ')) {
            if (document.activeElement === this.trigger) {
                e.preventDefault();
                this.target.classList.contains("hidden") ? this.show() : this.hide();
            }
        }
    }

    /**
     * Binds event listeners based on trigger type (hover or click).
     */
    bindEvents() {
        if (this.triggerType === 'hover') {
            this.trigger.addEventListener("mouseover", this.boundTriggerMouseover);
            this.trigger.addEventListener("mouseout", this.boundTriggerMouseout);
            this.target.addEventListener("mouseover", this.boundTargetMouseover);
            this.target.addEventListener("mouseout", this.boundTargetMouseout);
            // Keyboard accessibility: show on focus, hide on blur
            this.trigger.addEventListener("focus", this.boundTriggerFocus);
            this.trigger.addEventListener("blur", this.boundTriggerBlur);
            this.target.addEventListener("focusout", this.boundTargetBlur);
            if (this.followMouse) {
                this.trigger.addEventListener("mousemove", this.boundTriggerMousemove);
            }
        } else if (this.triggerType === 'click') {
            this.trigger.addEventListener("click", this.boundTriggerClick);
            if (this.autoClose) {
                document.addEventListener("click", this.boundDocumentClick);
            }
        }

        // Keyboard support for both hover and click
        this.trigger.addEventListener("keydown", this.boundKeyDown);
        window.addEventListener("scroll", this.boundWindowScroll);
    }

    /**
     * Shows the floater and updates its position.
     * Closes any other open floater first.
     */
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
            const tooltipText = this.trigger.getAttribute("data-insight-tooltip");
            this.target.textContent = tooltipText;
            if (this.arrow) {
                this.target.appendChild(this.arrow);
            }
            // Also update the screen-reader description
            if (this.srDescription) {
                this.srDescription.textContent = tooltipText;
            }
        }

        this.target.classList.remove("hidden");

        // Update aria-expanded for popovers
        if (this.type === "popover") {
            this.trigger.setAttribute("aria-expanded", "true");
        }

        // Only update position if tooltip was not already visible
        // For followMouse tooltips that are already visible, keep current position
        if (!wasVisible) {
            this.updatePosition();
        }

        Floater.currentOpen = this;
    }

    /**
     * Hides the floater after a short delay (for hover mode).
     */
    hideWithDelay() {
        this.hideTimeout = setTimeout(() => this.hide(), 100);
    }

    /**
     * Immediately hides the floater.
     */
    hide() {
        this.target.classList.add("hidden");

        // Update aria-expanded for popovers
        if (this.type === "popover") {
            this.trigger.setAttribute("aria-expanded", "false");
        }

        if (Floater.currentOpen === this) {
            Floater.currentOpen = null;
        }
    }

    /**
     * Calculates available space around the trigger element.
     * @param {DOMRect} rect - Trigger element bounding rect
     * @param {number} tooltipWidth - Tooltip width
     * @param {number} tooltipHeight - Tooltip height
     * @param {number} distance - Distance from trigger
     * @returns {Object} Available space in each direction
     */
    getAvailableSpace(rect, tooltipWidth, tooltipHeight, distance) {
        return {
            top: rect.top - distance - tooltipHeight,
            bottom: window.innerHeight - rect.bottom - distance - tooltipHeight,
            left: rect.left - distance - tooltipWidth,
            right: window.innerWidth - rect.right - distance - tooltipWidth
        };
    }

    /**
     * Determines the best position for the tooltip based on available space.
     * Tries the preferred position first, then flips to opposite, then tries other axis.
     * @param {string} preferred - Preferred position (top, bottom, left, right)
     * @param {Object} space - Available space in each direction
     * @returns {string} Best position to use
     */
    getBestPosition(preferred, space) {
        const opposite = { top: 'bottom', bottom: 'top', left: 'right', right: 'left' };
        const otherAxis = { top: ['left', 'right'], bottom: ['left', 'right'], left: ['top', 'bottom'], right: ['top', 'bottom'] };

        // Try preferred position
        if (space[preferred] >= 0) return preferred;

        // Try opposite position
        const opp = opposite[preferred];
        if (space[opp] >= 0) return opp;

        // Try other axis
        for (const alt of otherAxis[preferred]) {
            if (space[alt] >= 0) return alt;
        }

        // Fallback: position with most space
        return Object.entries(space).reduce((best, [pos, val]) => val > space[best] ? pos : best, preferred);
    }

    /**
     * Updates the floater position based on trigger location and configured position.
     * Automatically flips to alternative position if preferred position doesn't fit.
     * Uses fixed positioning relative to viewport.
     */
    updatePosition() {
        const preferredPosition = this.trigger.getAttribute('data-position') || "top";
        const rect = this.trigger.getBoundingClientRect();
        const distanceToTarget = 12;
        const arrowSize = 8;

        // Calculate tooltip dimensions
        const tooltipWidth = this.target.offsetWidth;
        const tooltipHeight = this.target.offsetHeight;

        // Determine best position based on available space
        const space = this.getAvailableSpace(rect, tooltipWidth, tooltipHeight, distanceToTarget);
        const position = this.getBestPosition(preferredPosition, space);

        // Reset arrow position and rotation classes before applying new ones
        if (this.arrow) {
            this.arrow.classList.remove('rotate-135', 'rotate-225', 'rotate-315');
            this.arrow.style.top = '';
            this.arrow.style.left = '';
        }

        let top, left;

        // Position relative to trigger (getBoundingClientRect gives viewport coords)
        switch (position) {
            case 'top':
                top = rect.top - tooltipHeight - distanceToTarget;
                left = rect.left + rect.width / 2 - tooltipWidth / 2;
                if (this.arrow) { this.arrow.style.top = `${tooltipHeight - (arrowSize + 1)}px`; }
                break;

            case 'bottom':
                top = rect.bottom + distanceToTarget;
                left = rect.left + rect.width / 2 - tooltipWidth / 2;
                if (this.arrow) { this.arrow.classList.add('rotate-225'); this.arrow.style.top = `${-(arrowSize + 1)}px`; }
                break;

            case 'left':
                top = rect.top + rect.height / 2 - tooltipHeight / 2;
                left = rect.left - tooltipWidth - distanceToTarget;
                if (this.arrow) { this.arrow.classList.add('rotate-315'); this.arrow.style.top = `${tooltipHeight / 2 - arrowSize}px`; this.arrow.style.left = `${tooltipWidth - 1}px`; }
                break;

            case 'right':
                top = rect.top + rect.height / 2 - tooltipHeight / 2;
                left = rect.right + distanceToTarget;
                if (this.arrow) { this.arrow.classList.add('rotate-135'); this.arrow.style.top = `${tooltipHeight / 2 - arrowSize}px`; this.arrow.style.left = `-1px`; }
                break;
        }

        // Clamp to viewport bounds (for horizontal/vertical centering edge cases)
        left = Math.max(0, Math.min(left, window.innerWidth - tooltipWidth));
        top = Math.max(0, Math.min(top, window.innerHeight - tooltipHeight));

        this.target.style.top = `${top}px`;
        this.target.style.left = `${left}px`;
    }

    /**
     * Update tooltip position to follow mouse cursor horizontally.
     * Vertical position remains relative to the trigger element.
     * Tooltip stays within viewport bounds and "sticks" to edges until
     * the cursor moves far enough for the tooltip to be centered again.
     * Uses fixed positioning relative to viewport.
     * @param {MouseEvent} event - The mousemove event
     */
    updatePositionFollowMouse(event) {
        const preferredPosition = this.trigger.getAttribute('data-position') || "top";
        const triggerRect = this.trigger.getBoundingClientRect();
        const distanceToTarget = 8;
        const tooltipWidth = this.target.offsetWidth;
        const tooltipHalfWidth = tooltipWidth / 2;

        // Calculate horizontal position following mouse (clamped to trigger bounds)
        const mouseX = Math.max(triggerRect.left, Math.min(event.clientX, triggerRect.right));
        let left = mouseX - tooltipHalfWidth;

        // Clamp to viewport bounds
        left = Math.max(0, Math.min(left, window.innerWidth - tooltipWidth));

        this.target.style.left = `${left}px`;

        // Re-measure height AFTER horizontal position is set (wrapping may have changed it)
        const tooltipHeight = this.target.offsetHeight;

        // Determine best vertical position (auto-flip if needed)
        const spaceTop = triggerRect.top - distanceToTarget - tooltipHeight;
        const spaceBottom = window.innerHeight - triggerRect.bottom - distanceToTarget - tooltipHeight;
        const position = (preferredPosition === 'top' && spaceTop >= 0) ? 'top' :
                         (preferredPosition === 'bottom' && spaceBottom >= 0) ? 'bottom' :
                         (spaceTop >= spaceBottom) ? 'top' : 'bottom';

        // Reset arrow classes before applying new ones
        if (this.arrow) {
            this.arrow.classList.remove('rotate-180', 'rotate-225');
            this.arrow.style.top = '';
            this.arrow.style.left = '';
        }

        // Vertical position (fixed positioning, so directly use viewport coords)
        switch (position) {
            case 'top':
                this.target.style.top = `${triggerRect.top - tooltipHeight - distanceToTarget}px`;
                if (this.arrow) {
                    this.arrow.style.top = `${tooltipHeight - 2}px`;
                    this.arrow.style.left = '50%';
                }
                break;

            case 'bottom':
                this.target.style.top = `${triggerRect.bottom + distanceToTarget}px`;
                if (this.arrow) {
                    this.arrow.classList.add('rotate-225');
                    this.arrow.style.top = '-7px';
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
            this.trigger.removeEventListener("focus", this.boundTriggerFocus);
            this.trigger.removeEventListener("blur", this.boundTriggerBlur);
            this.target.removeEventListener("focusout", this.boundTargetBlur);
            if (this.followMouse) {
                this.trigger.removeEventListener("mousemove", this.boundTriggerMousemove);
            }
        } else if (this.triggerType === 'click') {
            this.trigger.removeEventListener("click", this.boundTriggerClick);
            if (this.autoClose) {
                document.removeEventListener("click", this.boundDocumentClick);
            }
        }

        this.trigger.removeEventListener("keydown", this.boundKeyDown);
        window.removeEventListener("scroll", this.boundWindowScroll);

        // Disconnect attribute observer
        if (this.attributeObserver) {
            this.attributeObserver.disconnect();
            this.attributeObserver = null;
        }

        if (Floater.currentOpen === this) {
            Floater.currentOpen = null;
        }

        // Remove the target element from DOM to prevent orphaned floaters
        // when HTMX swaps out the trigger element.
        if (this.target && this.target.parentNode) {
            this.target.remove();
        }

        // Remove the screen-reader description element
        if (this.srDescription && this.srDescription.parentNode) {
            this.srDescription.remove();
        }

        Floater.instances.delete(this.trigger);
        delete this.trigger.__insightInstance;

        this.trigger = null;
        this.target = null;
        this.srDescription = null;
    }

    /**
     * Initializes all popover and tooltip instances on the page.
     *
     * @static
     */
    static initAll() {
        document.querySelectorAll("[data-insight-popover]").forEach(trigger => new Floater(trigger, 'popover'));
        document.querySelectorAll("[data-insight-tooltip]").forEach(trigger => new Floater(trigger, 'tooltip'));
    }
}
