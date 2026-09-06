// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Tests for the HTMX websocket bridge.
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const jsDir = path.join(__dirname, '../../insight_ui/static/insight_ui/js');

function loadComponent(filename) {
  const filepath = path.join(jsDir, filename);
  const code = fs.readFileSync(filepath, 'utf-8');
  eval(code);
}

function mockHtmx() {
  globalThis.htmx = {
    config: {
      extensions: ['ws'],
    },
  };
}

function dispatchHtmxEvent(element, eventName, detail = {}) {
  element.dispatchEvent(
    new CustomEvent(eventName, {
      bubbles: true,
      detail,
    })
  );
}

describe('InsightUI.WebSocket', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
    mockHtmx();
    loadComponent('insight-ui-websocket.js');
  });

  it('updates websocket status through data hooks instead of demo-specific ids', () => {
    const container = TestUtils.createDOM(`
      <div data-insight-websocket hx-ext="ws" ws-connect="/runtime/stream/">
        <div data-insight-websocket-output></div>
        <span data-insight-websocket-status>Establishing connection...</span>
      </div>
    `);
    const component = container.querySelector('[data-insight-websocket]');
    const status = container.querySelector('[data-insight-websocket-status]');

    InsightUI.WebSocket.init();

    dispatchHtmxEvent(component, 'htmx:wsOpen');
    expect(status.textContent).toBe('Connected');

    dispatchHtmxEvent(component, 'htmx:wsConnecting');
    expect(status.textContent).toBe('Establishing connection...');

    dispatchHtmxEvent(component, 'htmx:wsError');
    expect(status.textContent).toBe('Connection error');

    dispatchHtmxEvent(component, 'htmx:wsClose');
    expect(status.textContent).toBe('Disconnected');
  });

  it('dispatches neutral DOM events for non-HTML websocket payloads', () => {
    const container = TestUtils.createDOM(`
      <div data-insight-websocket hx-ext="ws" ws-connect="/runtime/stream/">
        <div data-insight-websocket-output></div>
        <span data-insight-websocket-status>Establishing connection...</span>
      </div>
    `);
    const component = container.querySelector('[data-insight-websocket]');
    const messageListener = vi.fn();
    const jsonListener = vi.fn();

    component.addEventListener('insight-ui:websocket-message', messageListener);
    component.addEventListener('insight-ui:websocket-json-message', jsonListener);

    InsightUI.WebSocket.init();

    dispatchHtmxEvent(component, 'htmx:wsAfterMessage', {
      message: JSON.stringify({ type: 'notification.created', id: 'evt-1' }),
    });

    expect(messageListener).toHaveBeenCalledTimes(1);
    expect(messageListener.mock.calls[0][0].detail.data).toEqual({
      type: 'notification.created',
      id: 'evt-1',
    });
    expect(jsonListener).toHaveBeenCalledTimes(1);
  });

  it('leaves HTML websocket fragments to HTMX without dispatching adapter events', () => {
    const container = TestUtils.createDOM(`
      <div data-insight-websocket hx-ext="ws" ws-connect="/runtime/stream/">
        <div data-insight-websocket-output><p>Initial</p></div>
        <span data-insight-websocket-status>Establishing connection...</span>
      </div>
    `);
    const component = container.querySelector('[data-insight-websocket]');
    const output = container.querySelector('[data-insight-websocket-output]');
    const messageListener = vi.fn();

    component.addEventListener('insight-ui:websocket-message', messageListener);

    InsightUI.WebSocket.init();

    dispatchHtmxEvent(component, 'htmx:wsAfterMessage', {
      message: '<div hx-swap-oob="innerHTML:#stream">Rendered by HTMX</div>',
    });

    expect(messageListener).not.toHaveBeenCalled();
    expect(output.innerHTML).toContain('Initial');
  });

  it('binds HTMX listeners only once across repeated init calls', () => {
    const addEventListenerSpy = vi.spyOn(document.body, 'addEventListener');

    InsightUI.WebSocket.init();
    InsightUI.WebSocket.init();

    expect(addEventListenerSpy).toHaveBeenCalledTimes(5);
  });
});
