// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Insight UI - Shared Utilities
 *
 * Provides shared utility functions and lifecycle management for all Insight UI components.
 * Includes focus trapping, scroll blocking, HTMX cleanup hooks, and event delegation handlers.
 *
 * @namespace InsightUI
 */
window.InsightUI = window.InsightUI || {};

/**
 * Component lifecycle utilities for proper cleanup and memory management.
 * All components should use these patterns to prevent memory leaks.
 *
 * @namespace InsightUI.lifecycle
 */
window.InsightUI.lifecycle = {
    /**
     * Registers HTMX lifecycle hooks for automatic component cleanup.
     * Listens for `htmx:beforeCleanupElement` and calls `destroy()` on any
     * attached Insight UI component instance.
     * Call this once during initialization.
     *
     * @function
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
 *
 * @namespace InsightUI.handlers
 */
window.InsightUI.handlers = {
    /**
     * Initializes delegated event handlers for radio callbacks, alert dismissal,
     * and form error dismissal.
     * Call this once during initialization.
     *
     * @function
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
        // The form component renders its HTMX error container as #form-error
        // (role="alert"); #form-result is kept for existing integrations.
        document.addEventListener('click', function(e) {
            const dismissBtn = e.target.closest('[data-insight-dismiss="form-errors"]');
            if (dismissBtn) {
                const formResult = dismissBtn.closest('#form-error, #form-result') || dismissBtn.closest('[role="alert"]');
                if (formResult) {
                    formResult.innerHTML = '';
                }
            }
        });

        debugLog("Event listeners registered.");
    }
};

/**
 * General utility functions for Insight UI components.
 *
 * @namespace InsightUI.utils
 */
window.InsightUI.utils = {
    /**
     * Traps keyboard focus within a modal or dialog element.
     * Implements focus cycling so Tab/Shift+Tab stays within the container.
     * This is essential for accessibility (WCAG 2.1 AA compliance).
     *
     * @param {HTMLElement} modal - The modal/dialog element to trap focus within
     * @returns {Function} Cleanup function to remove the event listener
     */
    trapFocus: function (modal) {
        const focusableElements = modal.querySelectorAll('a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])');
        const firstFocusableElement = focusableElements[0];
        const lastFocusableElement = focusableElements[focusableElements.length - 1];

        const handler = function (e) {
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
        };

        modal.addEventListener('keydown', handler);

        // Focus on the first element when the modal opens
        if (firstFocusableElement) {
            firstFocusableElement.focus();
        }

        // Return cleanup function
        return function () {
            modal.removeEventListener('keydown', handler);
        };
    },

    /**
     * Blocks page scrolling by setting `overflow: hidden` on the body.
     * Use when opening modals or drawers to prevent background scrolling.
     */
    blockScroll: function () {
        document.body.style.overflow = 'hidden';
    },

    /**
     * Restores page scrolling by removing the overflow style from the body.
     * Call when closing modals or drawers.
     */
    unblockScroll: function () {
        document.body.style.overflow = '';
    }
};
