/**
 * Conditional debug logging function for Insight UI components.
 *
 * Logs messages to the console only when the global `JS_DEBUG` flag is enabled.
 * Used throughout all Insight UI components for development debugging.
 *
 * @param {...*} args - Arguments to pass to console.log
 * @example
 * // Enable debug mode
 * window.JS_DEBUG = true;
 * debugLog("Component initialized:", element);
 */
window.debugLog = function (...args) {
    if (window.JS_DEBUG) {
        console.log(...args);
    }
};
