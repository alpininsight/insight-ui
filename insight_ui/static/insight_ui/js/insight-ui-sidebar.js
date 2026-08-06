/**
 * Sidebar component for Insight UI.
 *
 * Handles both static sidebars and drawer sidebars, with support for
 * mobile drawer behavior where static sidebars become drawers on small screens.
 */
export class Sidebar {
    /** @type {WeakMap<HTMLElement, Sidebar>} Weak references to prevent multiple initialization */
    static instances = new WeakMap();

    /** @type {number} XL breakpoint (1280px) - matches Tailwind's xl: breakpoint */
    static XL_BREAKPOINT = 1280;

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

        // Find toggle button for mobile drawer mode
        this.toggleBtn = document.querySelector(`[data-sidebar-toggle="${this.side}"]`);

        // Find open button for drawer sidebars
        this.openBtn = document.querySelector(`[data-sidebar-target="${this.side}"]`);

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

        // Skip initialization for static sidebars (they don't need JS behavior)
        // unless they have mobile drawer behavior
        if (this.isStatic && this.mobileBehavior === "hidden" && !this.isMobileDrawer) {
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
            this.boundOpenBtnClick = () => {
                this.openSidebar();
                this.openBtn.classList.toggle("hidden", true);
            };
            this.openBtn.addEventListener('click', this.boundOpenBtnClick);
        }
    }

    /**
     * Initializes the sidebar transform for off-screen positioning.
     * Handles RTL layouts by inverting the transform direction.
     */
    initSidebar() {
        if (document.documentElement.dir === "rtl") {
            if (this.side === "right") this.sidebar.style.transform = 'translateX(-100%)';
            else if (this.side === "left") this.sidebar.style.transform = 'translateX(100%)';
        } else {
            if (this.side === "right") this.sidebar.style.transform = 'translateX(100%)';
            else if (this.side === "left") this.sidebar.style.transform = 'translateX(-100%)';
        }
    }

    /**
     * Toggle the mobile drawer open/closed.
     * Used for static sidebars with mobile_behavior="drawer".
     */
    toggleMobileDrawer() {
        // Find the mobile drawer wrapper
        const mobileDrawer = document.getElementById(`${this.side}-sidebar-mobile`);
        if (!mobileDrawer) return;

        const isHidden = mobileDrawer.classList.contains("hidden");
        if (isHidden) {
            // Store trigger for focus return
            this.triggerElement = document.activeElement;

            // Open the mobile drawer
            mobileDrawer.classList.remove("hidden");
            const aside = mobileDrawer.getElementsByTagName("aside")[0];
            if (aside) {
                aside.style.transform = 'translateX(0)';
            }
            this.releaseFocusTrap = InsightUI.utils.trapFocus(mobileDrawer);
            this.toggleBtn?.setAttribute("aria-expanded", "true");

            // Add Escape key handler
            this.boundKeyDown = (e) => {
                if (e.key === 'Escape') {
                    e.preventDefault();
                    this.closeMobileDrawer(mobileDrawer);
                }
            };
            document.addEventListener('keydown', this.boundKeyDown);
        } else {
            // Close the mobile drawer
            this.closeMobileDrawer(mobileDrawer);
        }
    }

    /**
     * Closes the mobile drawer with animation.
     *
     * @param {HTMLElement} mobileDrawer - The mobile drawer element to close
     */
    closeMobileDrawer(mobileDrawer) {
        // Remove Escape key handler
        if (this.boundKeyDown) {
            document.removeEventListener('keydown', this.boundKeyDown);
            this.boundKeyDown = null;
        }

        const aside = mobileDrawer.getElementsByTagName("aside")[0];
        if (aside) {
            if (document.documentElement.dir === "rtl") {
                aside.style.transform = this.side === "right" ? 'translateX(-100%)' : 'translateX(100%)';
            } else {
                aside.style.transform = this.side === "right" ? 'translateX(100%)' : 'translateX(-100%)';
            }
        }

        // Store trigger reference for focus return after transition
        const triggerToFocus = this.triggerElement;

        aside?.addEventListener('transitionend', () => {
            mobileDrawer.classList.add("hidden");
            this.toggleBtn?.setAttribute("aria-expanded", "false");
            // Release focus trap
            if (this.releaseFocusTrap) {
                this.releaseFocusTrap();
                this.releaseFocusTrap = null;
            }
            // Return focus to trigger element
            if (triggerToFocus && typeof triggerToFocus.focus === 'function') {
                triggerToFocus.focus();
            }
        }, { once: true });

        this.triggerElement = null;
    }

    /**
     * Opens the sidebar with focus trapping and keyboard support.
     */
    openSidebar() {
        // Store trigger for focus return
        this.triggerElement = document.activeElement;

        this.wrapper.classList.remove("hidden");
        this.releaseFocusTrap = InsightUI.utils.trapFocus(this.wrapper);
        this.sidebar.style.transform = 'translateX(0)';

        // Add Escape key handler
        this.boundKeyDown = (e) => {
            if (e.key === 'Escape') {
                e.preventDefault();
                this.closeSidebar();
            }
        };
        document.addEventListener('keydown', this.boundKeyDown);
    }

    /**
     * Closes the sidebar with animation.
     */
    closeSidebar() {
        // Check if this is a mobile drawer
        if (this.isMobileDrawer) {
            this.closeMobileDrawer(this.wrapper);
            return;
        }

        // Remove Escape key handler
        if (this.boundKeyDown) {
            document.removeEventListener('keydown', this.boundKeyDown);
            this.boundKeyDown = null;
        }

        if (document.documentElement.dir === "rtl") {
            if (this.side === "right") this.sidebar.style.transform = 'translateX(-100%)';
            else if (this.side === "left") this.sidebar.style.transform = 'translateX(100%)';
        } else {
            if (this.side === "right") this.sidebar.style.transform = 'translateX(100%)';
            else if (this.side === "left") this.sidebar.style.transform = 'translateX(-100%)';
        }

        // Store trigger reference for focus return after transition
        const triggerToFocus = this.triggerElement;

        this.sidebar.addEventListener('transitionend', () => {
            this.wrapper.classList.add("hidden");
            if (this.openBtn) this.openBtn.classList.toggle("hidden", false);
            // Release focus trap
            if (this.releaseFocusTrap) {
                this.releaseFocusTrap();
                this.releaseFocusTrap = null;
            }
            // Return focus to trigger element
            if (triggerToFocus && typeof triggerToFocus.focus === 'function') {
                triggerToFocus.focus();
            }
        }, { once: true });

        this.triggerElement = null;
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
        debugLog("Destroy sidebar: ", this.sidebar, this.side);

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
