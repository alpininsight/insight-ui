/**
 * Tests for Floater (Popover/Tooltip) component functionality
 */

import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
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

describe('Floater Component', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
    loadComponent('insight-ui-floater.js');
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  describe('Tooltip Creation', () => {
    it('should create tooltip element dynamically', () => {
      const container = TestUtils.createDOM(`
        <div>
          <button data-insight-tooltip="Hello World">Hover me</button>
        </div>
      `);
      const trigger = container.querySelector('[data-insight-tooltip]');

      new InsightUI.Floater(trigger, 'tooltip');

      const tooltip = trigger.parentNode.querySelector('span');
      expect(tooltip).not.toBeNull();
      expect(tooltip.textContent).toBe('Hello World');
    });

    it('should add positioning classes to tooltip', () => {
      const container = TestUtils.createDOM(`
        <div>
          <button data-insight-tooltip="Test">Hover me</button>
        </div>
      `);
      const trigger = container.querySelector('[data-insight-tooltip]');

      const floater = new InsightUI.Floater(trigger, 'tooltip');

      expect(floater.target.classList.contains('absolute')).toBe(true);
      expect(floater.target.classList.contains('hidden')).toBe(true);
      expect(floater.target.classList.contains('z-50')).toBe(true);
    });
  });

  describe('Popover Reference', () => {
    it('should reference existing DOM element for popover', () => {
      const container = TestUtils.createDOM(`
        <div>
          <button data-insight-popover="my-popover">Click me</button>
          <div id="my-popover">Popover content</div>
        </div>
      `);
      const trigger = container.querySelector('[data-insight-popover]');
      const popoverEl = container.querySelector('#my-popover');

      const floater = new InsightUI.Floater(trigger, 'popover');

      expect(floater.target).toBe(popoverEl);
    });
  });

  describe('Hover Trigger', () => {
    it('should show floater on mouseover', () => {
      const container = TestUtils.createDOM(`
        <div>
          <button data-insight-tooltip="Test" data-trigger="hover">Hover</button>
        </div>
      `);
      const trigger = container.querySelector('[data-insight-tooltip]');

      const floater = new InsightUI.Floater(trigger, 'tooltip');

      expect(floater.target.classList.contains('hidden')).toBe(true);

      trigger.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));

      expect(floater.target.classList.contains('hidden')).toBe(false);
    });

    it('should hide floater on mouseout after delay', () => {
      const container = TestUtils.createDOM(`
        <div>
          <button data-insight-tooltip="Test" data-trigger="hover">Hover</button>
        </div>
      `);
      const trigger = container.querySelector('[data-insight-tooltip]');

      const floater = new InsightUI.Floater(trigger, 'tooltip');

      // Show
      trigger.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
      expect(floater.target.classList.contains('hidden')).toBe(false);

      // Mouseout starts hide timer
      trigger.dispatchEvent(new MouseEvent('mouseout', { bubbles: true }));

      // Not hidden yet
      expect(floater.target.classList.contains('hidden')).toBe(false);

      // After delay
      vi.advanceTimersByTime(100);

      expect(floater.target.classList.contains('hidden')).toBe(true);
    });

    it('should cancel hide if mouse enters target', () => {
      const container = TestUtils.createDOM(`
        <div>
          <button data-insight-tooltip="Test" data-trigger="hover">Hover</button>
        </div>
      `);
      const trigger = container.querySelector('[data-insight-tooltip]');

      const floater = new InsightUI.Floater(trigger, 'tooltip');

      // Show via trigger
      trigger.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));

      // Start hide timer
      trigger.dispatchEvent(new MouseEvent('mouseout', { bubbles: true }));

      // Move to target before timeout
      floater.target.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));

      // Advance past hide timeout
      vi.advanceTimersByTime(200);

      // Should still be visible
      expect(floater.target.classList.contains('hidden')).toBe(false);
    });
  });

  describe('Click Trigger', () => {
    it('should toggle floater on click', () => {
      const container = TestUtils.createDOM(`
        <div>
          <button data-insight-popover="pop" data-trigger="click">Click</button>
          <div id="pop">Content</div>
        </div>
      `);
      const trigger = container.querySelector('[data-insight-popover]');

      const floater = new InsightUI.Floater(trigger, 'popover');

      expect(floater.target.classList.contains('hidden')).toBe(true);

      // First click shows
      trigger.dispatchEvent(new MouseEvent('click', { bubbles: true }));
      expect(floater.target.classList.contains('hidden')).toBe(false);

      // Second click hides
      trigger.dispatchEvent(new MouseEvent('click', { bubbles: true }));
      expect(floater.target.classList.contains('hidden')).toBe(true);
    });

    it('should close on document click when autoClose is true', () => {
      const container = TestUtils.createDOM(`
        <div>
          <button data-insight-popover="pop" data-trigger="click" data-auto-close="true">Click</button>
          <div id="pop">Content</div>
        </div>
      `);
      const trigger = container.querySelector('[data-insight-popover]');

      const floater = new InsightUI.Floater(trigger, 'popover');

      // Open
      trigger.dispatchEvent(new MouseEvent('click', { bubbles: true }));
      expect(floater.target.classList.contains('hidden')).toBe(false);

      // Click outside
      document.body.dispatchEvent(new MouseEvent('click', { bubbles: true }));

      expect(floater.target.classList.contains('hidden')).toBe(true);
    });
  });

  describe('show() and hide() methods', () => {
    it('should show floater programmatically', () => {
      const container = TestUtils.createDOM(`
        <div>
          <button data-insight-tooltip="Test">Hover</button>
        </div>
      `);
      const trigger = container.querySelector('[data-insight-tooltip]');

      const floater = new InsightUI.Floater(trigger, 'tooltip');

      floater.show();

      expect(floater.target.classList.contains('hidden')).toBe(false);
    });

    it('should hide floater programmatically', () => {
      const container = TestUtils.createDOM(`
        <div>
          <button data-insight-tooltip="Test">Hover</button>
        </div>
      `);
      const trigger = container.querySelector('[data-insight-tooltip]');

      const floater = new InsightUI.Floater(trigger, 'tooltip');

      floater.show();
      floater.hide();

      expect(floater.target.classList.contains('hidden')).toBe(true);
    });

    it('should track currentOpen state', () => {
      const container = TestUtils.createDOM(`
        <div>
          <button data-insight-tooltip="Test">Hover</button>
        </div>
      `);
      const trigger = container.querySelector('[data-insight-tooltip]');

      const floater = new InsightUI.Floater(trigger, 'tooltip');

      expect(InsightUI.Floater.currentOpen).toBeNull();

      floater.show();
      expect(InsightUI.Floater.currentOpen).toBe(floater);

      floater.hide();
      expect(InsightUI.Floater.currentOpen).toBeNull();
    });
  });

  describe('Multiple Floaters', () => {
    it('should close other floaters when showing new one', () => {
      const container = TestUtils.createDOM(`
        <div>
          <button data-insight-tooltip="First" id="trigger1">First</button>
          <button data-insight-tooltip="Second" id="trigger2">Second</button>
        </div>
      `);
      const trigger1 = container.querySelector('#trigger1');
      const trigger2 = container.querySelector('#trigger2');

      const floater1 = new InsightUI.Floater(trigger1, 'tooltip');
      const floater2 = new InsightUI.Floater(trigger2, 'tooltip');

      floater1.show();
      expect(floater1.target.classList.contains('hidden')).toBe(false);

      floater2.show();
      expect(floater1.target.classList.contains('hidden')).toBe(true);
      expect(floater2.target.classList.contains('hidden')).toBe(false);
    });
  });

  describe('Window Scroll Handling', () => {
    it('should add scroll listener', () => {
      const addSpy = vi.spyOn(window, 'addEventListener');

      const container = TestUtils.createDOM(`
        <div>
          <button data-insight-tooltip="Test">Hover</button>
        </div>
      `);
      const trigger = container.querySelector('[data-insight-tooltip]');

      new InsightUI.Floater(trigger, 'tooltip');

      expect(addSpy).toHaveBeenCalledWith('scroll', expect.any(Function));
    });

    it('should remove scroll listener on destroy', () => {
      const removeSpy = vi.spyOn(window, 'removeEventListener');

      const container = TestUtils.createDOM(`
        <div>
          <button data-insight-tooltip="Test">Hover</button>
        </div>
      `);
      const trigger = container.querySelector('[data-insight-tooltip]');

      const floater = new InsightUI.Floater(trigger, 'tooltip');
      floater.destroy();

      expect(removeSpy).toHaveBeenCalledWith('scroll', expect.any(Function));
    });
  });

  describe('destroy() method', () => {
    it('should clear pending hide timeout', () => {
      const container = TestUtils.createDOM(`
        <div>
          <button data-insight-tooltip="Test" data-trigger="hover">Hover</button>
        </div>
      `);
      const trigger = container.querySelector('[data-insight-tooltip]');

      const floater = new InsightUI.Floater(trigger, 'tooltip');

      // Start hide with delay
      floater.show();
      floater.hideWithDelay();

      // Destroy before timeout
      floater.destroy();

      // Advance timers - should not throw
      expect(() => vi.advanceTimersByTime(200)).not.toThrow();
    });

    it('should nullify references', () => {
      const container = TestUtils.createDOM(`
        <div>
          <button data-insight-tooltip="Test">Hover</button>
        </div>
      `);
      const trigger = container.querySelector('[data-insight-tooltip]');

      const floater = new InsightUI.Floater(trigger, 'tooltip');
      floater.destroy();

      expect(floater.trigger).toBeNull();
      expect(floater.target).toBeNull();
    });
  });
});
