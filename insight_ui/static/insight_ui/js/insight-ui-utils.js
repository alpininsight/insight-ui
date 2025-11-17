/**
 * Insight UI - Shared Utilities
 */
window.InsightUI = window.InsightUI || {};
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
