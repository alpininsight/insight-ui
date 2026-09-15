// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Sidebar component for Insight UI.
 *
 * Handles both static sidebars and drawer sidebars, with support for
 * mobile drawer behavior where static sidebars become drawers on small screens.
 */
export class Sidebar {
    /** @type {WeakMap<HTMLElement, Sidebar>} Weak references to prevent multiple initialization */
    static instances = new WeakMap();

    /**
     * Creates a new Sidebar instance.
     *
     * @param {HTMLElement} wrapper - The sidebar wrapper element with data-insight-sidebar attribute
     */
    constructor(wrapper) {
        // If an instance for this element already exists, return it
        if (Sidebar.instances.has(wrapper)) {
            return Sidebar.instances.get(wrapper);
        }

        this.wrapper = wrapper;
        this.sidebar = wrapper.getElementsByTagName("aside")[0];
        this.side = wrapper.getAttribute("data-insight-sidebar");
        this.isStatic = wrapper.getAttribute("data-static") === "true";
        this.mobileBehavior = wrapper.getAttribute("data-mobile-behavior") || "hidden";
        this.isMobileDrawer = wrapper.getAttribute("data-mobile-drawer") === "true";

        // The mobile wrapper owns the pair's interaction lifecycle. Its static
        // sibling must never bind the same external toggle or acquire a trap.
        this.toggleBtn = this.isMobileDrawer
            ? document.querySelector(`[data-sidebar-toggle="${this.side}"]`)
            : null;

        // Find open button for drawer sidebars
        this.openBtn = !this.isStatic && !this.isMobileDrawer
            ? document.querySelector(`[data-sidebar-target="${this.side}"]`)
            : null;

        this.autoClose = this.sidebar?.getAttribute("data-auto-close") === "true";

        // Store bound handlers for cleanup
        this.boundCloseButtons = [];
        this.boundToggleBtnClick = null;
        this.boundOpenBtnClick = null;
        this.boundMouseMove = null;
        this.boundMouseLeave = null;
        this.boundResizeHandler = null;
        this.boundKeyDown = null;
        this.releaseFocusTrap = null;
        this.triggerElement = null;
        this.state = "closed";
        this.openFrame = null;
        this.closeTimer = null;
        this.boundTransitionEnd = null;

        this.init();

        this.wrapper.__insightInstance = this;
        Sidebar.instances.set(wrapper, this);

        debugLog("New sidebar created: ", this.sidebar, this.side, { isStatic: this.isStatic, mobileBehavior: this.mobileBehavior });
    }

    /**
     * Initializes the sidebar by setting up event listeners and initial state.
     */
    init() {
        if (!this.wrapper || !this.sidebar) return;

        // Static content stays inert even when it has a separate mobile drawer.
        if (this.isStatic) {
            return;
        }

        // Setup close buttons (dismiss handlers)
        this.wrapper.querySelectorAll('[data-insight-dismiss="sidebar"]').forEach(closeButton => {
            const handler = () => this.closeSidebar();
            this.boundCloseButtons.push({ element: closeButton, handler });
            closeButton.addEventListener('click', handler);
        });

        // Initialize sidebar position for drawers
        if (!this.isStatic || this.isMobileDrawer) {
            this.initSidebar();
        }

        // Setup auto-close behavior
        if (this.autoClose) {
            this.setupAutoClose();
        }

        // Setup toggle button for mobile drawer mode
        if (this.toggleBtn) {
            this.boundToggleBtnClick = () => this.toggleMobileDrawer();
            this.toggleBtn.addEventListener('click', this.boundToggleBtnClick);
        }

        // Legacy: support old open button
        if (this.openBtn) {
            this.boundOpenBtnClick = () => this.openSidebar(this.openBtn);
            this.openBtn.addEventListener('click', this.boundOpenBtnClick);
        }
    }

    /**
     * Initializes the sidebar transform for off-screen positioning.
     */
    initSidebar() {
        this.sidebar.style.transform = this.getOffscreenTransform();
    }

    /**
     * Toggle the mobile drawer open/closed.
     * Used for static sidebars with mobile_behavior="drawer".
     */
    toggleMobileDrawer() {
        if (!this.isMobileDrawer || !this.wrapper) return;
        if (this.state === "open") {
            this.closeSidebar();
        } else {
            this.openSidebar(this.toggleBtn);
        }
    }

    /**
     * Closes the mobile drawer with animation.
     *
     * @param {HTMLElement} mobileDrawer - The mobile drawer element to close
     */
    closeMobileDrawer(mobileDrawer = this.wrapper) {
        if (this.isMobileDrawer && mobileDrawer === this.wrapper) this.closeSidebar();
    }

    /**
     * Gets the off-screen transform value based on side and RTL mode.
     *
     * @returns {string} The CSS transform value
     */
    getOffscreenTransform() {
        const isRTL = document.documentElement.dir === "rtl";
        if (isRTL) {
            return this.side === "right" ? 'translateX(-100%)' : 'translateX(100%)';
        }
        return this.side === "right" ? 'translateX(100%)' : 'translateX(-100%)';
    }

    /**
     * Opens the sidebar with focus trapping and keyboard support.
     */
    openSidebar(trigger = document.activeElement) {
        if (!this.wrapper || !this.sidebar || this.isStatic || this.state === "open") return;
        this.cancelAnimation();
        // Keep the original invoker if a closing drawer is reopened.
        this.triggerElement ||= trigger;
        this.state = "open";

        // Ensure sidebar starts off-screen before becoming visible
        this.sidebar.style.transform = this.getOffscreenTransform();
        this.wrapper.classList.remove("hidden");

        // Animate to visible position in next frame
        this.openFrame = requestAnimationFrame(() => {
            this.openFrame = null;
            this.sidebar.style.transform = 'translateX(0)';
        });

        this.releaseFocusTrap ||= InsightUI.utils.trapFocus(this.wrapper);
        this.toggleBtn?.setAttribute("aria-expanded", "true");
        this.openBtn?.setAttribute("aria-expanded", "true");
        this.openBtn?.classList.add("hidden");

        // Add Escape key handler
        if (!this.boundKeyDown) {
            this.boundKeyDown = (e) => {
                if (e.key === 'Escape') {
                    e.preventDefault();
                    this.closeSidebar();
                }
            };
            document.addEventListener('keydown', this.boundKeyDown);
        }
    }

    /**
     * Closes the sidebar with animation.
     */
    closeSidebar() {
        if (!this.wrapper || !this.sidebar || this.isStatic || this.state !== "open") return;
        this.cancelAnimation();
        this.state = "closing";
        this.sidebar.style.transform = this.getOffscreenTransform();
        this.toggleBtn?.setAttribute("aria-expanded", "false");
        this.openBtn?.setAttribute("aria-expanded", "false");

        const duration = this.getTransitionDuration();
        if (!duration) {
            this.finishClose();
            return;
        }
        this.boundTransitionEnd = (event) => {
            if (event.target === this.sidebar && event.propertyName === "transform") {
                this.finishClose();
            }
        };
        this.sidebar.addEventListener('transitionend', this.boundTransitionEnd);
        // Interrupted/absent transitions may never dispatch transitionend.
        this.closeTimer = setTimeout(() => this.finishClose(), duration + 50);
    }

    /** Returns the transform transition's maximum duration including its delay. */
    getTransitionDuration() {
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return 0;
        const style = getComputedStyle(this.sidebar);
        const milliseconds = (value) => (parseFloat(value) || 0) * (value.trim().endsWith('ms') ? 1 : 1000);
        const durations = style.transitionDuration.split(',').map(milliseconds);
        const delays = style.transitionDelay.split(',').map(milliseconds);
        return Math.max(0, ...style.transitionProperty.split(',').map((property, index) => {
            if (!["all", "transform"].includes(property.trim())) return 0;
            return durations[index % durations.length] + delays[index % delays.length];
        }));
    }

    /** Cancel pending work before reversing direction or removing the element. */
    cancelAnimation() {
        if (this.openFrame !== null) cancelAnimationFrame(this.openFrame);
        if (this.closeTimer !== null) clearTimeout(this.closeTimer);
        if (this.boundTransitionEnd) {
            this.sidebar.removeEventListener('transitionend', this.boundTransitionEnd);
        }
        this.openFrame = null;
        this.closeTimer = null;
        this.boundTransitionEnd = null;
    }

    /** Finish closing exactly once, including focus and document-level cleanup. */
    finishClose() {
        this.cancelAnimation();
        this.state = "closed";
        this.wrapper.classList.add("hidden");
        this.sidebar.style.transform = this.getOffscreenTransform();
        this.toggleBtn?.setAttribute("aria-expanded", "false");
        this.openBtn?.setAttribute("aria-expanded", "false");
        this.openBtn?.classList.remove("hidden");
        if (this.boundKeyDown) {
            document.removeEventListener('keydown', this.boundKeyDown);
            this.boundKeyDown = null;
        }
        this.releaseFocusTrap?.();
        this.releaseFocusTrap = null;
        const triggerToFocus = this.triggerElement;
        this.triggerElement = null;
        if (triggerToFocus?.isConnected && typeof triggerToFocus.focus === 'function') {
            triggerToFocus.focus();
        }
    }

    /**
     * Sets up auto-close behavior where the sidebar opens when mouse approaches
     * the window edge and closes when mouse leaves the sidebar.
     */
    setupAutoClose() {
        // Open when mouse is near window edge
        this.boundMouseMove = (e) => {
            const xThreshold = 50; // Pixels from edge
            const yThreshold = 0;  // Pixels from top (for navbar)

            if (e.clientY > yThreshold) {
                if (document.documentElement.dir === "rtl") {
                    if (this.side === "right" && e.clientX < xThreshold) {
                        this.openSidebar();
                    } else if (this.side === "left" && window.innerWidth - e.clientX < xThreshold) {
                        this.openSidebar();
                    }
                } else {
                    if (this.side === "right" && window.innerWidth - e.clientX < xThreshold) {
                        this.openSidebar();
                    } else if (this.side === "left" && e.clientX < xThreshold) {
                        this.openSidebar();
                    }
                }
            }
        };
        document.addEventListener('mousemove', this.boundMouseMove);

        // Close when mouse leaves sidebar
        this.boundMouseLeave = () => this.closeSidebar();
        this.sidebar.addEventListener('mouseleave', this.boundMouseLeave);
    }

    /**
     * Destroys the sidebar instance and removes all event listeners.
     * Call this before removing the element from DOM.
     */
    destroy() {
        if (!this.wrapper) return;
        debugLog("Destroy sidebar: ", this.sidebar, this.side);
        if (!this.isStatic && this.sidebar) this.finishClose();
        else this.cancelAnimation();

        // Remove close button handlers
        this.boundCloseButtons.forEach(({ element, handler }) => {
            element.removeEventListener('click', handler);
        });
        this.boundCloseButtons = [];

        // Remove toggle button handler
        if (this.toggleBtn && this.boundToggleBtnClick) {
            this.toggleBtn.removeEventListener('click', this.boundToggleBtnClick);
        }

        // Remove open button handler
        if (this.openBtn && this.boundOpenBtnClick) {
            this.openBtn.removeEventListener('click', this.boundOpenBtnClick);
        }

        // Remove auto-close handlers
        if (this.boundMouseMove) {
            document.removeEventListener('mousemove', this.boundMouseMove);
        }
        if (this.boundMouseLeave) {
            this.sidebar.removeEventListener('mouseleave', this.boundMouseLeave);
        }

        // Remove resize handler
        if (this.boundResizeHandler) {
            window.removeEventListener('resize', this.boundResizeHandler);
        }

        // Remove keydown handler
        if (this.boundKeyDown) {
            document.removeEventListener('keydown', this.boundKeyDown);
        }

        // Release focus trap
        if (this.releaseFocusTrap) {
            this.releaseFocusTrap();
            this.releaseFocusTrap = null;
        }

        Sidebar.instances.delete(this.wrapper);
        delete this.wrapper.__insightInstance;

        this.wrapper = null;
        this.sidebar = null;
    }

    /**
     * Initializes all sidebar instances on the page.
     *
     * @static
     */
    static initAll() {
        document.querySelectorAll('[data-insight-sidebar]').forEach(wrapper => new Sidebar(wrapper));
    }
}
