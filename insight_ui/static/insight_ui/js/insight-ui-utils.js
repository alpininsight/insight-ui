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
     * Registers HTMX lifecycle hooks for automatic component cleanup.
     * Call this once during initialization.
     */
    registerHTMXHooks: function() {
        if (typeof htmx === 'undefined') return;

        htmx.on('htmx:beforeCleanupElement', (evt) => {
            const el = evt.detail.elt;
            if (el.__insightInstance?.destroy) {
                el.__insightInstance.destroy();
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
