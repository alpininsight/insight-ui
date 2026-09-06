// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Tests for HTMX integration and lifecycle cleanup
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
  const transformed = code.replace(/export class\s+(\w+)/g, 'window.InsightUI.$1 = class $1');
  eval(transformed);
}

// Mock htmx
function mockHtmx() {
  const handlers = {};
  globalThis.htmx = {
    on: vi.fn((event, handler) => {
      handlers[event] = handlers[event] || [];
      handlers[event].push(handler);
    }),
    trigger: (event, detail) => {
      if (handlers[event]) {
        handlers[event].forEach(h => h({ detail }));
      }
    },
    _handlers: handlers,
  };
}

describe('HTMX Lifecycle Integration', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
    mockHtmx();
    loadComponent('insight-ui-utils.js');
  });

  describe('lifecycle.registerHTMXHooks()', () => {
    it('should register htmx:beforeCleanupElement handler', () => {
      InsightUI.lifecycle.registerHTMXHooks();

      expect(htmx.on).toHaveBeenCalledWith('htmx:beforeCleanupElement', expect.any(Function));
    });

    it('should call destroy on element __insightInstance during htmx:beforeCleanupElement', () => {
      loadComponent('insight-ui-dropdown.js');

      const container = document.createElement('div');
      document.body.appendChild(container);

      container.innerHTML = `
        <button data-insight-dropdown="cleanup-dd">Toggle</button>
        <div id="cleanup-dd">Menu</div>
      `;
      const button = container.querySelector('[data-insight-dropdown]');
      const dropdown = new InsightUI.Dropdown(button);

      expect(InsightUI.Dropdown.instances.has(button)).toBe(true);
      expect(button.__insightInstance).toBe(dropdown);

      InsightUI.lifecycle.registerHTMXHooks();

      // Simulate htmx:beforeCleanupElement event
      htmx.trigger('htmx:beforeCleanupElement', { elt: button });

      expect(InsightUI.Dropdown.instances.has(button)).toBe(false);
    });

    it('should not throw if element has no __insightInstance', () => {
      InsightUI.lifecycle.registerHTMXHooks();

      const div = document.createElement('div');
      document.body.appendChild(div);

      expect(() => {
        htmx.trigger('htmx:beforeCleanupElement', { elt: div });
      }).not.toThrow();
    });

    it('should not throw if __insightInstance has no destroy method', () => {
      InsightUI.lifecycle.registerHTMXHooks();

      const div = document.createElement('div');
      div.__insightInstance = { someOtherMethod: () => {} };
      document.body.appendChild(div);

      expect(() => {
        htmx.trigger('htmx:beforeCleanupElement', { elt: div });
      }).not.toThrow();
    });

    it('should not throw if htmx is not defined', () => {
      delete globalThis.htmx;

      // Reload utils without htmx
      globalThis.InsightUI = {};
      loadComponent('insight-ui-utils.js');

      expect(() => {
        InsightUI.lifecycle.registerHTMXHooks();
      }).not.toThrow();
    });
  });

  describe('Component __insightInstance binding', () => {
    beforeEach(() => {
      loadComponent('insight-ui-dropdown.js');
      loadComponent('insight-ui-accordion.js');
    });

    it('should set __insightInstance on dropdown trigger element', () => {
      const container = document.createElement('div');
      document.body.appendChild(container);

      container.innerHTML = `
        <button data-insight-dropdown="test-dd">Toggle</button>
        <div id="test-dd">Menu</div>
      `;
      const button = container.querySelector('[data-insight-dropdown]');
      const dropdown = new InsightUI.Dropdown(button);

      expect(button.__insightInstance).toBe(dropdown);
    });

    it('should set __insightInstance on accordion element', () => {
      const container = document.createElement('div');
      document.body.appendChild(container);

      container.innerHTML = `
        <div data-insight-accordion="acc1">
          <button aria-controls="acc1-panel" aria-expanded="false">Panel</button>
          <div id="acc1-panel" style="height:0;opacity:0;">Content</div>
        </div>
      `;

      const accordionEl = container.querySelector('[data-insight-accordion]');
      const accordion = new InsightUI.Accordion(accordionEl);

      expect(accordionEl.__insightInstance).toBe(accordion);
    });

    it('should delete __insightInstance on destroy', () => {
      const container = document.createElement('div');
      document.body.appendChild(container);

      container.innerHTML = `
        <button data-insight-dropdown="destroy-dd">Toggle</button>
        <div id="destroy-dd">Menu</div>
      `;
      const button = container.querySelector('[data-insight-dropdown]');
      const dropdown = new InsightUI.Dropdown(button);

      expect(button.__insightInstance).toBe(dropdown);

      dropdown.destroy();

      expect(button.__insightInstance).toBeUndefined();
    });
  });
});

describe('Event Delegation Handlers', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
    loadComponent('insight-ui-utils.js');
    InsightUI.handlers.init();
  });

  describe('Alert dismiss handler', () => {
    it('should remove alert when dismiss button is clicked', () => {
      const container = TestUtils.createAlert('info');
      const alert = container.querySelector('[role="alert"]');
      const dismissBtn = container.querySelector('[data-insight-dismiss="alert"]');

      expect(document.body.contains(alert)).toBe(true);

      TestUtils.click(dismissBtn);

      expect(document.body.contains(alert)).toBe(false);
    });

    it('should not throw if dismiss button is outside alert', () => {
      const container = TestUtils.createDOM(`
        <button data-insight-dismiss="alert">Orphan button</button>
      `);
      const button = container.querySelector('[data-insight-dismiss="alert"]');

      expect(() => {
        TestUtils.click(button);
      }).not.toThrow();
    });
  });

  describe('Form errors dismiss handler', () => {
    it('should clear form-result content when dismiss button is clicked', () => {
      const container = TestUtils.createDOM(`
        <div id="form-result">
          <div class="error-content">
            <button data-insight-dismiss="form-errors">Close</button>
            <p>Error message</p>
          </div>
        </div>
      `);
      const formResult = container.querySelector('#form-result');
      const dismissBtn = container.querySelector('[data-insight-dismiss="form-errors"]');

      expect(formResult.innerHTML).not.toBe('');

      TestUtils.click(dismissBtn);

      expect(formResult.innerHTML).toBe('');
    });
  });

  describe('Radio callback handler', () => {
    it('should call window function when radio with callback is changed', () => {
      const mockCallback = vi.fn();
      globalThis.testRadioCallback = mockCallback;

      const container = TestUtils.createDOM(`
        <input type="radio" name="test" value="option1" data-radio-callback="testRadioCallback">
        <input type="radio" name="test" value="option2" data-radio-callback="testRadioCallback">
      `);

      const radio = container.querySelector('input[value="option1"]');
      radio.checked = true;
      radio.dispatchEvent(new Event('change', { bubbles: true }));

      expect(mockCallback).toHaveBeenCalledWith('option1');

      delete globalThis.testRadioCallback;
    });

    it('should warn if callback function does not exist', () => {
      const warnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {});

      const container = TestUtils.createDOM(`
        <input type="radio" name="test" value="opt" data-radio-callback="nonExistentFunction">
      `);

      const radio = container.querySelector('input');
      radio.checked = true;
      radio.dispatchEvent(new Event('change', { bubbles: true }));

      expect(warnSpy).toHaveBeenCalledWith(
        expect.stringContaining('nonExistentFunction')
      );

      warnSpy.mockRestore();
    });
  });
});
