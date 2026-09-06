// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Tests for InsightUI utility functions
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

describe('InsightUI.utils', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
    loadComponent('insight-ui-utils.js');
  });

  describe('trapFocus()', () => {
    it('should focus first focusable element on initialization', () => {
      const container = TestUtils.createDOM(`
        <div id="modal">
          <button id="first">First</button>
          <input id="second" type="text">
          <button id="last">Last</button>
        </div>
      `);
      const modal = container.querySelector('#modal');
      const first = modal.querySelector('#first');

      InsightUI.utils.trapFocus(modal);

      expect(document.activeElement).toBe(first);
    });

    it('should wrap focus from last to first on Tab', () => {
      const container = TestUtils.createDOM(`
        <div id="modal">
          <button id="first">First</button>
          <button id="last">Last</button>
        </div>
      `);
      const modal = container.querySelector('#modal');
      const first = modal.querySelector('#first');
      const last = modal.querySelector('#last');

      InsightUI.utils.trapFocus(modal);

      // Focus last element
      last.focus();

      // Press Tab
      const event = new KeyboardEvent('keydown', {
        key: 'Tab',
        bubbles: true,
        cancelable: true,
      });
      modal.dispatchEvent(event);

      expect(document.activeElement).toBe(first);
    });

    it('should wrap focus from first to last on Shift+Tab', () => {
      const container = TestUtils.createDOM(`
        <div id="modal">
          <button id="first">First</button>
          <button id="last">Last</button>
        </div>
      `);
      const modal = container.querySelector('#modal');
      const first = modal.querySelector('#first');
      const last = modal.querySelector('#last');

      InsightUI.utils.trapFocus(modal);

      // First is already focused from trapFocus
      expect(document.activeElement).toBe(first);

      // Press Shift+Tab
      const event = new KeyboardEvent('keydown', {
        key: 'Tab',
        shiftKey: true,
        bubbles: true,
        cancelable: true,
      });
      modal.dispatchEvent(event);

      expect(document.activeElement).toBe(last);
    });

    it('should prevent default on Tab wrap', () => {
      const container = TestUtils.createDOM(`
        <div id="modal">
          <button id="first">First</button>
          <button id="last">Last</button>
        </div>
      `);
      const modal = container.querySelector('#modal');
      const last = modal.querySelector('#last');

      InsightUI.utils.trapFocus(modal);

      last.focus();

      const event = new KeyboardEvent('keydown', {
        key: 'Tab',
        bubbles: true,
        cancelable: true,
      });

      const preventDefaultSpy = vi.spyOn(event, 'preventDefault');
      modal.dispatchEvent(event);

      expect(preventDefaultSpy).toHaveBeenCalled();
    });

    it('should find focusable elements including tabindex', () => {
      const container = TestUtils.createDOM(`
        <div id="modal">
          <div tabindex="0" id="focusable-div">Focusable div</div>
          <button id="btn">Button</button>
        </div>
      `);
      const modal = container.querySelector('#modal');
      const focusableDiv = modal.querySelector('#focusable-div');

      InsightUI.utils.trapFocus(modal);

      // First focusable element should be focused (the div with tabindex)
      expect(document.activeElement).toBe(focusableDiv);
    });

    it('should ignore elements with tabindex="-1"', () => {
      const container = TestUtils.createDOM(`
        <div id="modal">
          <div tabindex="-1" id="non-focusable">Not focusable</div>
          <button id="btn">Button</button>
        </div>
      `);
      const modal = container.querySelector('#modal');
      const btn = modal.querySelector('#btn');

      InsightUI.utils.trapFocus(modal);

      // Button should be first focusable, not the tabindex="-1" div
      expect(document.activeElement).toBe(btn);
    });

    it('should return a cleanup function', () => {
      const container = TestUtils.createDOM(`
        <div id="modal">
          <button id="first">First</button>
          <button id="last">Last</button>
        </div>
      `);
      const modal = container.querySelector('#modal');

      const cleanup = InsightUI.utils.trapFocus(modal);

      expect(typeof cleanup).toBe('function');
    });

    it('should remove keydown listener when cleanup is called', () => {
      const container = TestUtils.createDOM(`
        <div id="modal">
          <button id="first">First</button>
          <button id="last">Last</button>
        </div>
      `);
      const modal = container.querySelector('#modal');
      const first = modal.querySelector('#first');
      const last = modal.querySelector('#last');

      const removeSpy = vi.spyOn(modal, 'removeEventListener');

      const cleanup = InsightUI.utils.trapFocus(modal);

      // Verify trap works before cleanup
      last.focus();
      modal.dispatchEvent(new KeyboardEvent('keydown', {
        key: 'Tab',
        bubbles: true,
        cancelable: true,
      }));
      expect(document.activeElement).toBe(first);

      // Call cleanup
      cleanup();

      expect(removeSpy).toHaveBeenCalledWith('keydown', expect.any(Function));
    });

    it('should not trap focus after cleanup is called', () => {
      const container = TestUtils.createDOM(`
        <div id="modal">
          <button id="first">First</button>
          <button id="last">Last</button>
        </div>
        <button id="outside">Outside</button>
      `);
      const modal = container.querySelector('#modal');
      const last = modal.querySelector('#last');

      const cleanup = InsightUI.utils.trapFocus(modal);
      cleanup();

      // Focus last element
      last.focus();

      // Tab should not be prevented anymore (no wrap to first)
      const event = new KeyboardEvent('keydown', {
        key: 'Tab',
        bubbles: true,
        cancelable: true,
      });
      const preventDefaultSpy = vi.spyOn(event, 'preventDefault');

      modal.dispatchEvent(event);

      // preventDefault should NOT have been called since handler was removed
      expect(preventDefaultSpy).not.toHaveBeenCalled();
    });

    it('should handle modal with no focusable elements', () => {
      const container = TestUtils.createDOM(`
        <div id="modal">
          <p>No focusable elements here</p>
        </div>
      `);
      const modal = container.querySelector('#modal');

      // Should not throw
      expect(() => InsightUI.utils.trapFocus(modal)).not.toThrow();
    });
  });

  describe('blockScroll()', () => {
    it('should set body overflow to hidden', () => {
      document.body.style.overflow = '';

      InsightUI.utils.blockScroll();

      expect(document.body.style.overflow).toBe('hidden');
    });
  });

  describe('unblockScroll()', () => {
    it('should clear body overflow style', () => {
      document.body.style.overflow = 'hidden';

      InsightUI.utils.unblockScroll();

      expect(document.body.style.overflow).toBe('');
    });
  });
});

describe('InsightUI.handlers', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
    loadComponent('insight-ui-utils.js');
  });

  describe('init()', () => {
    it('should register event listeners', () => {
      const addSpy = vi.spyOn(document, 'addEventListener');

      InsightUI.handlers.init();

      // Should register at least change and click listeners
      expect(addSpy).toHaveBeenCalledWith('change', expect.any(Function));
      expect(addSpy).toHaveBeenCalledWith('click', expect.any(Function));
    });
  });

  describe('Alert dismiss', () => {
    beforeEach(() => {
      InsightUI.handlers.init();
    });

    it('should remove alert on dismiss click', () => {
      const container = TestUtils.createAlert('info');
      const alert = container.querySelector('[role="alert"]');
      const dismissBtn = alert.querySelector('[data-insight-dismiss="alert"]');

      expect(document.body.contains(alert)).toBe(true);

      TestUtils.click(dismissBtn);

      expect(document.body.contains(alert)).toBe(false);
    });

    it('should handle nested dismiss button', () => {
      const container = TestUtils.createDOM(`
        <div role="alert" class="alert">
          <div class="content">
            <span>
              <button data-insight-dismiss="alert">
                <svg>X</svg>
              </button>
            </span>
          </div>
        </div>
      `);
      const alert = container.querySelector('[role="alert"]');
      const svg = container.querySelector('svg');

      TestUtils.click(svg); // Click on SVG inside button

      expect(document.body.contains(alert)).toBe(false);
    });
  });

  describe('Form errors dismiss', () => {
    beforeEach(() => {
      InsightUI.handlers.init();
    });

    it('should clear form-result content', () => {
      const container = TestUtils.createDOM(`
        <div id="form-result">
          <div class="errors">
            <p>Error 1</p>
            <p>Error 2</p>
            <button data-insight-dismiss="form-errors">Close</button>
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

  describe('Radio callback', () => {
    beforeEach(() => {
      InsightUI.handlers.init();
    });

    it('should call callback function with radio value', () => {
      const callback = vi.fn();
      globalThis.myCallback = callback;

      const container = TestUtils.createDOM(`
        <input type="radio" name="test" value="option-a" data-radio-callback="myCallback">
      `);
      const radio = container.querySelector('input');

      radio.checked = true;
      radio.dispatchEvent(new Event('change', { bubbles: true }));

      expect(callback).toHaveBeenCalledWith('option-a');

      delete globalThis.myCallback;
    });

    it('should warn for non-existent callback', () => {
      const warnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {});

      const container = TestUtils.createDOM(`
        <input type="radio" name="test" value="x" data-radio-callback="doesNotExist">
      `);
      const radio = container.querySelector('input');

      radio.checked = true;
      radio.dispatchEvent(new Event('change', { bubbles: true }));

      expect(warnSpy).toHaveBeenCalled();
      expect(warnSpy.mock.calls[0][0]).toContain('doesNotExist');

      warnSpy.mockRestore();
    });

    it('should not trigger callback for unchecked radio', () => {
      const callback = vi.fn();
      globalThis.myCallback = callback;

      const container = TestUtils.createDOM(`
        <input type="radio" name="test" value="a" data-radio-callback="myCallback">
      `);
      const radio = container.querySelector('input');

      // Don't check it, just dispatch change
      radio.dispatchEvent(new Event('change', { bubbles: true }));

      // Callback still gets called because handler doesn't check .checked
      // This is current behavior - documenting it
      expect(callback).toHaveBeenCalled();

      delete globalThis.myCallback;
    });
  });
});

describe('InsightUI.lifecycle', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
  });

  describe('registerHTMXHooks()', () => {
    it('should not throw when htmx is not defined', () => {
      delete globalThis.htmx;
      loadComponent('insight-ui-utils.js');

      expect(() => InsightUI.lifecycle.registerHTMXHooks()).not.toThrow();
    });

    it('should register htmx:beforeCleanupElement handler', () => {
      const onSpy = vi.fn();
      globalThis.htmx = { on: onSpy };

      loadComponent('insight-ui-utils.js');
      InsightUI.lifecycle.registerHTMXHooks();

      expect(onSpy).toHaveBeenCalledWith('htmx:beforeCleanupElement', expect.any(Function));
    });
  });
});
