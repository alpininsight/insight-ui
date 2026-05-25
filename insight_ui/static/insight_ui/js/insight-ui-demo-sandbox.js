/**
 * Demo Sandbox
 *
 * Prevents navigation, form submissions, and network requests in demo iframes
 * while keeping pointer events and visual feedback intact.
 *
 * This script runs automatically in the components.html template context.
 */
(function () {
  "use strict";

  const DEBUG = window.JS_DEBUG || false;

  function log(...args) {
    if (DEBUG) {
      console.debug("[DemoSandbox]", ...args);
    }
  }

  // ─────────────────────────────────────────────────────────────────────────
  // Link clicks - prevent navigation but allow visual feedback
  // ─────────────────────────────────────────────────────────────────────────
  document.addEventListener(
    "click",
    (e) => {
      const anchor = e.target.closest("a");
      if (anchor && anchor.hasAttribute("href")) {
        e.preventDefault();
        e.stopPropagation();
        log("Blocked link navigation:", anchor.href);
      }
    },
    true // capture phase to intercept before other handlers
  );

  // ─────────────────────────────────────────────────────────────────────────
  // Form submissions - prevent GET/POST but allow visual feedback
  // ─────────────────────────────────────────────────────────────────────────
  document.addEventListener(
    "submit",
    (e) => {
      e.preventDefault();
      e.stopPropagation();
      log("Blocked form submission");
    },
    true
  );

  // ─────────────────────────────────────────────────────────────────────────
  // HTMX requests - prevent all HTMX-initiated requests
  // ─────────────────────────────────────────────────────────────────────────
  document.addEventListener("htmx:beforeRequest", (e) => {
    e.preventDefault();
    log("Blocked HTMX request:", e.detail.pathInfo?.requestPath || e.detail);
  });

  // Also handle htmx:confirm for elements with hx-confirm
  document.addEventListener("htmx:confirm", (e) => {
    e.preventDefault();
    log("Blocked HTMX confirm request");
  });

  // ─────────────────────────────────────────────────────────────────────────
  // fetch() - block network requests
  // ─────────────────────────────────────────────────────────────────────────
  const originalFetch = window.fetch;
  window.fetch = function (...args) {
    log("Blocked fetch:", args[0]);
    // Return a resolved promise with empty response to avoid errors
    return Promise.resolve(
      new Response(null, { status: 200, statusText: "Blocked in demo" })
    );
  };

  // ─────────────────────────────────────────────────────────────────────────
  // XMLHttpRequest - block XHR requests
  // ─────────────────────────────────────────────────────────────────────────
  const originalXHROpen = XMLHttpRequest.prototype.open;
  const originalXHRSend = XMLHttpRequest.prototype.send;

  XMLHttpRequest.prototype.open = function (method, url, ...rest) {
    this._blockedUrl = url;
    this._blockedMethod = method;
    // Still call original open so the object is in a valid state
    return originalXHROpen.call(this, method, url, ...rest);
  };

  XMLHttpRequest.prototype.send = function () {
    log("Blocked XHR:", this._blockedMethod, this._blockedUrl);
    // Simulate a successful empty response
    Object.defineProperty(this, "status", { value: 200, writable: false });
    Object.defineProperty(this, "statusText", {
      value: "Blocked in demo",
      writable: false,
    });
    Object.defineProperty(this, "readyState", { value: 4, writable: false });
    Object.defineProperty(this, "responseText", { value: "", writable: false });
    Object.defineProperty(this, "response", { value: "", writable: false });

    // Fire readystatechange and load events
    const readyStateEvent = new Event("readystatechange");
    const loadEvent = new Event("load");
    setTimeout(() => {
      this.dispatchEvent(readyStateEvent);
      this.dispatchEvent(loadEvent);
    }, 0);
  };

  log("Demo sandbox initialized - links, forms, and requests are blocked");
})();
