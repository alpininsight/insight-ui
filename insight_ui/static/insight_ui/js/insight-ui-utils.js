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
  trapFocus: (modal) => {
    const focusableEls = modal.querySelectorAll('a[href], button, textarea, input, select, [tabindex]:not([tabindex="-1"])');
    const first = focusableEls[0];
    const last = focusableEls[focusableEls.length - 1];
    modal.addEventListener('keydown', function(e) {
      if (e.key === 'Tab') {
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault(); last.focus();
        } else if (document.activeElement === last) {
          e.preventDefault(); first.focus();
        }
      }
    });
    first?.focus();
  }
};
