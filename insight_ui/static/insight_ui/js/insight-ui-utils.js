/**
 * Insight UI - Shared Utilities
 */
window.InsightUI = window.InsightUI || {};

/**
 * Component lifecycle utilities for proper cleanup and memory management.
 * All components should use these patterns to prevent memory leaks.
 */
window.InsightUI.lifecycle = {
    /**
     * Destroys all component instances within a container.
     * Call this before removing DOM elements (e.g., before HTMX swaps).
     * @param {HTMLElement} container - The container to search within
     */
    destroyAllIn: function(container) {
        if (!container) return;

        debugLog("Cleanup: ", container);

        const components = [
            { Class: window.InsightUI.Dropdown, selector: '[data-dropdown-toggle]' },
            { Class: window.InsightUI.Floater, selector: '[data-popover], [data-tooltip]' },
            { Class: window.InsightUI.Modal, selector: '[data-insight-toggle="modal"]' },
            { Class: window.InsightUI.Accordion, selector: '[data-accordion]' },
            { Class: window.InsightUI.Tabs, selector: '[data-tabs]' },
            { Class: window.InsightUI.Checkbox, selector: '[data-insight-checkbox-group]' },
            { Class: window.InsightUI.Multiselect, selector: '[data-multiselect]' },
            { Class: window.InsightUI.Sidebar, selector: '[data-insight-sidebar]' },
            { Class: window.InsightUI.Carousel, selector: '.carousel' },
            { Class: window.InsightUI.ThreeDCarousel, selector: '[data-3D-carousel]' },
        ];

        components.forEach(({ Class, selector }) => {
            if (!Class || !Class.instances) return;

            // Check children of the container
            container.querySelectorAll(selector).forEach(el => {
                const instance = Class.instances.get(el);
                if (instance && typeof instance.destroy === 'function') {
                    instance.destroy();
                }
            });

            // Check the container itself (handles the case where
            // the swap target IS the component root element)
            if (container.matches && container.matches(selector)) {
                const instance = Class.instances.get(container);
                if (instance && typeof instance.destroy === 'function') {
                    instance.destroy();
                }
            }
        });
    },

    /**
     * Registers HTMX lifecycle hooks for automatic component cleanup.
     * Call this once during initialization.
     */
    registerHTMXHooks: function() {
        if (typeof htmx === 'undefined') return;

        htmx.on('htmx:beforeSwap', (evt) => {
            const target = evt.detail.target;
            if (target) {
                window.InsightUI.lifecycle.destroyAllIn(target);
            }
        });
    }
};

/**
 * Event delegation handlers for components that use data attributes
 * instead of inline onclick handlers (security hardening).
 */
window.InsightUI.handlers = {
    /**
     * Initialize delegated event handlers.
     * Call this once during initialization.
     */
    init: function() {
        debugLog("Register event listeners...");

        // Radio block callback handler
        document.addEventListener('change', function(e) {
            const target = e.target;
            if (target.type === 'radio' && target.dataset.radioCallback) {
                const methodName = target.dataset.radioCallback;
                const value = target.value;
                // Call the method if it exists on window
                if (typeof window[methodName] === 'function') {
                    window[methodName](value);
                } else {
                    console.warn(`InsightUI: Radio callback "${methodName}" is not defined`);
                }
            }
        });

        // Alert/notification dismiss handler
        document.addEventListener('click', function(e) {
            const dismissBtn = e.target.closest('[data-insight-dismiss="alert"]');
            if (dismissBtn) {
                const alert = dismissBtn.closest('[role="alert"]');
                if (alert) {
                    alert.remove();
                }
            }
        });

        // Form errors dismiss handler
        document.addEventListener('click', function(e) {
            const dismissBtn = e.target.closest('[data-insight-dismiss="form-errors"]');
            if (dismissBtn) {
                const formResult = dismissBtn.closest('#form-result');
                if (formResult) {
                    formResult.innerHTML = '';
                }
            }
        });

        debugLog("Event listeners registered.");
    }
};

window.InsightUI.utils = {
    /**
     * This function is used to lock the keyboard focus within a modal dialog,
     * i.e., to implement what is known as focus trapping.
     * This is particularly important for accessibility,
     * so that users who navigate with the keyboard (e.g., using the tab key)
     * cannot accidentally move the focus out of the open modal.
     */
    trapFocus: function (modal) {
        const focusableElements = modal.querySelectorAll('a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])');
        const firstFocusableElement = focusableElements[0];
        const lastFocusableElement = focusableElements[focusableElements.length - 1];

        modal.addEventListener('keydown', function (e) {
            if (e.key === 'Tab') {
                if (e.shiftKey) { // Shift + Tab
                    if (document.activeElement === firstFocusableElement) {
                        lastFocusableElement.focus();
                        e.preventDefault();
                    }
                } else { // Tab
                    if (document.activeElement === lastFocusableElement) {
                        firstFocusableElement.focus();
                        e.preventDefault();
                    }
                }
            }
        });

        // Focus on the first element when the modal opens
        firstFocusableElement.focus();
    },

    blockScroll: function () {
        // Prevents scrolling of the body
        document.body.style.overflow = 'hidden';
    },

    unblockScroll: function () {
        // Enables scrolling of the body again
        document.body.style.overflow = '';
    }
};
