/**
 * Insight UI WebSocket bridge for the HTMX ws extension.
 *
 * This layer stays transport-neutral and does not render payload-specific UI.
 * HTML messages remain owned by HTMX, while non-HTML frames are surfaced as
 * DOM events so host adapters can decide how to render them.
 */
window.InsightUI = window.InsightUI || {};
InsightUI.WebSocket = InsightUI.WebSocket || {};

Object.assign(InsightUI.WebSocket, {
  initialized: InsightUI.WebSocket.initialized || false,
  handlers: InsightUI.WebSocket.handlers || {},

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

  handleStatusEvent: function(evt, state) {
    const component = this.getComponent(evt.target);
    if (!component) {
      return;
    }

    this.updateStatus(component, state);
  },

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

  getComponent: function(target) {
    if (!target || typeof target.closest !== 'function') {
      return null;
    }

    return target.closest('[data-insight-websocket]');
  },

  getStatusElement: function(component) {
    return component?.querySelector('[data-insight-websocket-status]') || null;
  },

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

  parseJsonMessage: function(message) {
    try {
      return JSON.parse(message);
    } catch {
      return null;
    }
  },

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
