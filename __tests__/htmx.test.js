/**
 * Tests for HTMX integration and lifecycle cleanup
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const jsDir = path.join(__dirname, '../insight_ui/static/insight_ui/js');

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

  describe('lifecycle.destroyAllIn()', () => {
    beforeEach(() => {
      loadComponent('insight-ui-dropdown.js');
      loadComponent('insight-ui-accordion.js');
    });

    it('should destroy all component instances within a container', () => {
      const container = document.createElement('div');
      document.body.appendChild(container);

      // Create dropdown inside container
      container.innerHTML = `
        <button data-dropdown-toggle="test-dd">Toggle</button>
        <div id="test-dd">Menu</div>
      `;
      const button = container.querySelector('[data-dropdown-toggle]');
      const dropdown = new InsightUI.Dropdown(button);

      expect(InsightUI.Dropdown.instances.has(button)).toBe(true);

      InsightUI.lifecycle.destroyAllIn(container);

      expect(InsightUI.Dropdown.instances.has(button)).toBe(false);
    });

    it('should handle containers with multiple component types', () => {
      const container = document.createElement('div');
      document.body.appendChild(container);

      container.innerHTML = `
        <div>
          <button data-dropdown-toggle="dd1">Dropdown</button>
          <div id="dd1">Menu</div>
        </div>
        <div data-accordion="acc1">
          <button aria-controls="acc1-panel" aria-expanded="false">Panel</button>
          <div id="acc1-panel" style="height:0;opacity:0;">Content</div>
        </div>
      `;

      const dropdownBtn = container.querySelector('[data-dropdown-toggle]');
      const accordionEl = container.querySelector('[data-accordion]');

      new InsightUI.Dropdown(dropdownBtn);
      new InsightUI.Accordion(accordionEl);

      expect(InsightUI.Dropdown.instances.has(dropdownBtn)).toBe(true);
      expect(InsightUI.Accordion.instances.has(accordionEl)).toBe(true);

      InsightUI.lifecycle.destroyAllIn(container);

      expect(InsightUI.Dropdown.instances.has(dropdownBtn)).toBe(false);
      expect(InsightUI.Accordion.instances.has(accordionEl)).toBe(false);
    });

    it('should not throw for empty containers', () => {
      const container = document.createElement('div');
      document.body.appendChild(container);

      expect(() => {
        InsightUI.lifecycle.destroyAllIn(container);
      }).not.toThrow();
    });

    it('should not throw for null container', () => {
      expect(() => {
        InsightUI.lifecycle.destroyAllIn(null);
      }).not.toThrow();
    });

    it('should destroy component when container itself is the component root', () => {
      // This tests the case where HTMX swaps out a component root directly
      // (e.g., the swap target IS the [data-accordion] element)
      const accordion = document.createElement('div');
      accordion.setAttribute('data-accordion', 'root-acc');
      accordion.innerHTML = `
        <button aria-controls="root-acc-panel" aria-expanded="false">Panel</button>
        <div id="root-acc-panel" style="height:0;opacity:0;">Content</div>
      `;
      document.body.appendChild(accordion);

      new InsightUI.Accordion(accordion);
      expect(InsightUI.Accordion.instances.has(accordion)).toBe(true);

      // Pass the component root itself as the container
      InsightUI.lifecycle.destroyAllIn(accordion);

      expect(InsightUI.Accordion.instances.has(accordion)).toBe(false);
    });

    it('should destroy carousel instances using data-insight-carousel selector', () => {
      const container = document.createElement('div');
      const carousel = document.createElement('div');
      carousel.setAttribute('data-insight-carousel', '');
      container.appendChild(carousel);
      document.body.appendChild(container);

      const destroySpy = vi.fn();
      InsightUI.Carousel = {
        instances: new WeakMap([[carousel, { destroy: destroySpy }]]),
      };

      InsightUI.lifecycle.destroyAllIn(container);

      expect(destroySpy).toHaveBeenCalled();
    });
  });

  describe('lifecycle.registerHTMXHooks()', () => {
    it('should register htmx:beforeSwap handler', () => {
      InsightUI.lifecycle.registerHTMXHooks();

      expect(htmx.on).toHaveBeenCalledWith('htmx:beforeSwap', expect.any(Function));
    });

    it('should call destroyAllIn on htmx:beforeSwap event', () => {
      loadComponent('insight-ui-dropdown.js');

      const container = document.createElement('div');
      document.body.appendChild(container);

      container.innerHTML = `
        <button data-dropdown-toggle="swap-dd">Toggle</button>
        <div id="swap-dd">Menu</div>
      `;
      const button = container.querySelector('[data-dropdown-toggle]');
      new InsightUI.Dropdown(button);

      InsightUI.lifecycle.registerHTMXHooks();

      // Simulate htmx:beforeSwap event
      htmx.trigger('htmx:beforeSwap', { target: container });

      expect(InsightUI.Dropdown.instances.has(button)).toBe(false);
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
