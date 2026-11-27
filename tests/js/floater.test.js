// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Tests for Floater (Popover/Tooltip) component functionality
 */

import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
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

      expect(floater.target.classList.contains('fixed')).toBe(true);
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
      vi.advanceTimersByTime(InsightUI.Floater.DEFAULT_TOOLTIP_SHOW_DELAY);

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
      vi.advanceTimersByTime(InsightUI.Floater.DEFAULT_TOOLTIP_SHOW_DELAY);
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
      vi.advanceTimersByTime(InsightUI.Floater.DEFAULT_TOOLTIP_SHOW_DELAY);

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

  describe('Tooltip show delay', () => {
    function createTooltip(attributes = '') {
      const container = TestUtils.createDOM(`
        <div>
          <button data-insight-tooltip="Help" ${attributes}><span class="label">Hover</span></button>
        </div>
      `);
      const trigger = container.querySelector('[data-insight-tooltip]');
      return { trigger, floater: new InsightUI.Floater(trigger, 'tooltip') };
    }

    const isVisible = floater => !floater.target.classList.contains('hidden');

    it('should show the tooltip only after the global delay', () => {
      const { trigger, floater } = createTooltip();

      trigger.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
      vi.advanceTimersByTime(InsightUI.Floater.DEFAULT_TOOLTIP_SHOW_DELAY - 1);
      expect(isVisible(floater)).toBe(false);

      vi.advanceTimersByTime(1);
      expect(isVisible(floater)).toBe(true);
    });

    it('should not show the tooltip if the pointer leaves before the delay', () => {
      const { trigger, floater } = createTooltip();

      trigger.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
      vi.advanceTimersByTime(100);
      trigger.dispatchEvent(new MouseEvent('mouseout', { bubbles: true }));
      vi.advanceTimersByTime(1000);

      expect(isVisible(floater)).toBe(false);
    });

    it('should not restart the delay when moving between child elements of the trigger', () => {
      const { trigger, floater } = createTooltip();
      const child = trigger.querySelector('.label');
      const delay = InsightUI.Floater.DEFAULT_TOOLTIP_SHOW_DELAY;

      trigger.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
      vi.advanceTimersByTime(delay / 2);
      trigger.dispatchEvent(new MouseEvent('mouseout', { bubbles: true, relatedTarget: child }));
      child.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
      vi.advanceTimersByTime(delay / 2);

      expect(isVisible(floater)).toBe(true);
    });

    it('should show immediately with data-tooltip-delay="0"', () => {
      const { trigger, floater } = createTooltip('data-tooltip-delay="0"');

      trigger.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));

      expect(isVisible(floater)).toBe(true);
    });

    it('should use the global delay that base.html sets on <html>', () => {
      document.documentElement.dataset.tooltipDelay = '100';
      try {
        const { trigger, floater } = createTooltip();

        trigger.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
        vi.advanceTimersByTime(100);

        expect(isVisible(floater)).toBe(true);
      } finally {
        delete document.documentElement.dataset.tooltipDelay;
      }
    });

    it('should use the delay of a surrounding container', () => {
      const container = TestUtils.createDOM(`
        <div data-tooltip-delay="0">
          <button data-insight-tooltip="Help">Hover</button>
        </div>
      `);
      const trigger = container.querySelector('[data-insight-tooltip]');
      const floater = new InsightUI.Floater(trigger, 'tooltip');

      trigger.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));

      expect(isVisible(floater)).toBe(true);
    });

    it('should show immediately on keyboard focus', () => {
      const { trigger, floater } = createTooltip();
      // jsdom does not track the keyboard modality behind :focus-visible.
      vi.spyOn(trigger, 'matches').mockImplementation(selector => selector === ':focus-visible');

      trigger.dispatchEvent(new FocusEvent('focus'));

      expect(isVisible(floater)).toBe(true);
    });

    it('should cancel a pending show when destroyed', () => {
      const { trigger, floater } = createTooltip();

      trigger.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
      floater.destroy();

      expect(() => vi.advanceTimersByTime(1000)).not.toThrow();
    });

    it('should show hover popovers without delay', () => {
      const container = TestUtils.createDOM(`
        <div>
          <button data-insight-popover="delay-popover">Hover</button>
          <div id="delay-popover">Content</div>
        </div>
      `);
      const trigger = container.querySelector('[data-insight-popover]');
      const floater = new InsightUI.Floater(trigger, 'popover');

      trigger.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));

      expect(isVisible(floater)).toBe(true);
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

    it('should remove tooltip element from DOM on destroy', () => {
      const container = TestUtils.createDOM(`
        <div>
          <button data-insight-tooltip="Test">Hover</button>
        </div>
      `);
      const trigger = container.querySelector('[data-insight-tooltip]');
      const parent = trigger.parentNode;

      const floater = new InsightUI.Floater(trigger, 'tooltip');

      // Tooltip element should exist in DOM (appended to document.body)
      const tooltipBefore = document.body.querySelector('span[role="tooltip"]');
      expect(tooltipBefore).not.toBeNull();

      floater.destroy();

      // Tooltip element should be removed from DOM
      const tooltipAfter = document.body.querySelector('span[role="tooltip"]');
      expect(tooltipAfter).toBeNull();
    });

    it('should remove popover element from DOM on destroy', () => {
      const container = TestUtils.createDOM(`
        <div>
          <button data-insight-popover="my-popover" data-trigger="click">Click</button>
          <div id="my-popover">Popover content</div>
        </div>
      `);
      const trigger = container.querySelector('[data-insight-popover]');

      const floater = new InsightUI.Floater(trigger, 'popover');

      // Popover element should exist (moved to document.body)
      expect(document.body.querySelector('#my-popover')).not.toBeNull();

      floater.destroy();

      // Popover element should be removed to prevent orphaned floaters
      expect(document.body.querySelector('#my-popover')).toBeNull();
    });
  });
});
