window.debugLog = function (...args) {
    if (window.JS_DEBUG) {
        console.log(...args);
    }
};
