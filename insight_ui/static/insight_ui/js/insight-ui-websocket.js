// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Insight UI WebSocket bridge for the HTMX ws extension.
 *
 * This layer stays transport-neutral and does not render payload-specific UI.
 * HTML messages remain owned by HTMX, while non-HTML frames are surfaced as
 * DOM events so host adapters can decide how to render them.
 *
 * @namespace InsightUI.WebSocket
 * @example
 * // HTML structure
 * <div data-insight-websocket hx-ext="ws" ws-connect="/ws/endpoint">
 *   <span data-insight-websocket-status></span>
 * </div>
 *
 * // Listen for custom events
 * element.addEventListener('insight-ui:websocket-message', (e) => {
 *   console.log(e.detail.message, e.detail.data);
 * });
 */
window.InsightUI = window.InsightUI || {};
InsightUI.WebSocket = InsightUI.WebSocket || {};

Object.assign(InsightUI.WebSocket, {
  /** @type {boolean} Whether the WebSocket bridge has been initialized */
  initialized: InsightUI.WebSocket.initialized || false,

  /** @type {Object} Event handler references for cleanup */
  handlers: InsightUI.WebSocket.handlers || {},

  /**
   * Initializes the WebSocket bridge by registering HTMX event listeners.
   * Safe to call multiple times - will only initialize once.
   */
  init: function() {
    if (this.initialized || typeof htmx === 'undefined' || !document.body) {
      return;
    }

    this.handlers = {
      open: (evt) => this.handleStatusEvent(evt, 'connected'),
      close: (evt) => this.handleStatusEvent(evt, 'disconnected'),
      error: (evt) => this.handleStatusEvent(evt, 'error'),
      connecting: (evt) => this.handleStatusEvent(evt, 'connecting'),
      message: (evt) => this.handleMessageEvent(evt),
    };

    document.body.addEventListener('htmx:wsOpen', this.handlers.open);
    document.body.addEventListener('htmx:wsClose', this.handlers.close);
    document.body.addEventListener('htmx:wsError', this.handlers.error);
    document.body.addEventListener('htmx:wsConnecting', this.handlers.connecting);
    document.body.addEventListener('htmx:wsAfterMessage', this.handlers.message);

    this.initialized = true;
  },

  /**
   * Destroys the WebSocket bridge and removes all event listeners.
   */
  destroy: function() {
    if (!this.initialized || !document.body) {
      return;
    }

    document.body.removeEventListener('htmx:wsOpen', this.handlers.open);
    document.body.removeEventListener('htmx:wsClose', this.handlers.close);
    document.body.removeEventListener('htmx:wsError', this.handlers.error);
    document.body.removeEventListener('htmx:wsConnecting', this.handlers.connecting);
    document.body.removeEventListener('htmx:wsAfterMessage', this.handlers.message);

    this.handlers = {};
    this.initialized = false;
  },

  /**
   * Handles WebSocket status events (open, close, error, connecting).
   *
   * @param {Event} evt - The HTMX WebSocket event
   * @param {string} state - The connection state: "connected", "disconnected", "error", or "connecting"
   */
  handleStatusEvent: function(evt, state) {
    const component = this.getComponent(evt.target);
    if (!component) {
      return;
    }

    this.updateStatus(component, state);
  },

  /**
   * Handles incoming WebSocket messages.
   * HTML messages are ignored (handled by HTMX), non-HTML messages trigger custom events.
   *
   * @param {Event} evt - The HTMX wsAfterMessage event
   */
  handleMessageEvent: function(evt) {
    const component = this.getComponent(evt.target);
    const message = evt.detail?.message;
    if (!component || typeof message !== 'string') {
      return;
    }

    const trimmedMessage = message.trim();
    if (!trimmedMessage || trimmedMessage.startsWith('<')) {
      return;
    }

    const detail = { message };
    const parsedData = this.parseJsonMessage(message);
    if (parsedData !== null) {
      detail.data = parsedData;
    }

    component.dispatchEvent(
      new CustomEvent('insight-ui:websocket-message', {
        bubbles: true,
        detail,
      })
    );

    if (parsedData !== null) {
      component.dispatchEvent(
        new CustomEvent('insight-ui:websocket-json-message', {
          bubbles: true,
          detail: {
            message,
            data: parsedData,
          },
        })
      );
    }
  },

  /**
   * Finds the closest WebSocket component ancestor of an element.
   *
   * @param {HTMLElement} target - The element to search from
   * @returns {HTMLElement|null} The WebSocket component element or null
   */
  getComponent: function(target) {
    if (!target || typeof target.closest !== 'function') {
      return null;
    }

    return target.closest('[data-insight-websocket]');
  },

  /**
   * Gets the status display element within a WebSocket component.
   *
   * @param {HTMLElement} component - The WebSocket component element
   * @returns {HTMLElement|null} The status element or null
   */
  getStatusElement: function(component) {
    return component?.querySelector('[data-insight-websocket-status]') || null;
  },

  /**
   * Updates the status display and dispatches a status event.
   *
   * @param {HTMLElement} component - The WebSocket component element
   * @param {string} state - The connection state
   */
  updateStatus: function(component, state) {
    const statusElement = this.getStatusElement(component);
    const stateConfig = this.statusMap[state];
    if (!statusElement || !stateConfig) {
      return;
    }

    statusElement.textContent = stateConfig.text;
    statusElement.className = stateConfig.className;

    component.dispatchEvent(
      new CustomEvent('insight-ui:websocket-status', {
        bubbles: true,
        detail: { state },
      })
    );
  },

  /**
   * Attempts to parse a message as JSON.
   *
   * @param {string} message - The message to parse
   * @returns {Object|null} The parsed JSON object or null if parsing fails
   */
  parseJsonMessage: function(message) {
    try {
      return JSON.parse(message);
    } catch {
      return null;
    }
  },

  /**
   * Status configuration map with display text and CSS classes for each state.
   * @type {Object.<string, {text: string, className: string}>}
   */
  statusMap: {
    connected: {
      text: 'Connected',
      className: 'insight-websocket__status-text insight-websocket__status-text--connected',
    },
    disconnected: {
      text: 'Disconnected',
      className: 'insight-websocket__status-text insight-websocket__status-text--disconnected',
    },
    error: {
      text: 'Connection error',
      className: 'insight-websocket__status-text insight-websocket__status-text--error',
    },
    connecting: {
      text: 'Establishing connection...',
      className: 'insight-websocket__status-text insight-websocket__status-text--connecting',
    },
  },
});
