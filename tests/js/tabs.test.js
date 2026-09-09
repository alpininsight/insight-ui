// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Tests for Tabs component functionality
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

function createTabsDOM(tabCount = 3) {
  const tabButtons = Array.from({ length: tabCount }, (_, i) =>
    `<button id="tab-${i}" role="tab" aria-selected="${i === 0 ? 'true' : 'false'}" tabindex="${i === 0 ? '0' : '-1'}">Tab ${i + 1}</button>`
  ).join('');

  return TestUtils.createDOM(`
    <div data-insight-tabs>
      <div role="tablist">
        ${tabButtons}
      </div>
      <div id="tab-content" tabindex="-1">Content</div>
    </div>
  `);
}

describe('Tabs Component', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
    loadComponent('insight-ui-tabs.js');
  });

  describe('Tab Activation', () => {
    it('should activate tab on click', () => {
      const container = createTabsDOM();
      const element = container.querySelector('[data-insight-tabs]');
      const tabs = element.querySelectorAll('[role="tab"]');

      new InsightUI.Tabs(element);

      // First tab is selected by default
      expect(tabs[0].getAttribute('aria-selected')).toBe('true');
      expect(tabs[1].getAttribute('aria-selected')).toBe('false');

      TestUtils.click(tabs[1]);

      expect(tabs[0].getAttribute('aria-selected')).toBe('false');
      expect(tabs[1].getAttribute('aria-selected')).toBe('true');
    });

    it('should update CSS classes on activation', () => {
      const container = createTabsDOM();
      const element = container.querySelector('[data-insight-tabs]');
      const tabs = element.querySelectorAll('[role="tab"]');

      new InsightUI.Tabs(element);

      TestUtils.click(tabs[1]);

      // Active tab should have primary styling
      expect(tabs[1].classList.contains('border-insight-primary')).toBe(true);
      expect(tabs[1].classList.contains('text-insight-primary')).toBe(true);

      // Inactive tab should have transparent/secondary styling
      expect(tabs[0].classList.contains('border-transparent')).toBe(true);
      expect(tabs[0].classList.contains('text-insight-body')).toBe(true);
    });

    it('should update tab content aria-label', () => {
      const container = createTabsDOM();
      const element = container.querySelector('[data-insight-tabs]');
      const tabs = element.querySelectorAll('[role="tab"]');
      const content = element.querySelector('#tab-content');

      new InsightUI.Tabs(element);

      TestUtils.click(tabs[1]);

      expect(content.getAttribute('aria-label')).toBe('tab-1');
    });
  });

  describe('Keyboard Navigation', () => {
    it('should move focus to next tab on ArrowRight', () => {
      const container = createTabsDOM();
      const element = container.querySelector('[data-insight-tabs]');
      const tabs = element.querySelectorAll('[role="tab"]');

      new InsightUI.Tabs(element);

      tabs[0].focus();
      TestUtils.keydown(tabs[0], 'ArrowRight');

      expect(document.activeElement).toBe(tabs[1]);
    });

    it('should move focus to previous tab on ArrowLeft', () => {
      const container = createTabsDOM();
      const element = container.querySelector('[data-insight-tabs]');
      const tabs = element.querySelectorAll('[role="tab"]');

      new InsightUI.Tabs(element);

      tabs[1].focus();
      TestUtils.keydown(tabs[1], 'ArrowLeft');

      expect(document.activeElement).toBe(tabs[0]);
    });

    it('should wrap focus from last to first on ArrowRight', () => {
      const container = createTabsDOM();
      const element = container.querySelector('[data-insight-tabs]');
      const tabs = element.querySelectorAll('[role="tab"]');

      new InsightUI.Tabs(element);

      tabs[2].focus(); // last tab
      TestUtils.keydown(tabs[2], 'ArrowRight');

      expect(document.activeElement).toBe(tabs[0]);
    });

    it('should wrap focus from first to last on ArrowLeft', () => {
      const container = createTabsDOM();
      const element = container.querySelector('[data-insight-tabs]');
      const tabs = element.querySelectorAll('[role="tab"]');

      new InsightUI.Tabs(element);

      tabs[0].focus();
      TestUtils.keydown(tabs[0], 'ArrowLeft');

      expect(document.activeElement).toBe(tabs[2]);
    });

    it('should move focus to first tab on Home', () => {
      const container = createTabsDOM();
      const element = container.querySelector('[data-insight-tabs]');
      const tabs = element.querySelectorAll('[role="tab"]');

      new InsightUI.Tabs(element);

      tabs[2].focus();
      TestUtils.keydown(tabs[2], 'Home');

      expect(document.activeElement).toBe(tabs[0]);
    });

    it('should move focus to last tab on End', () => {
      const container = createTabsDOM();
      const element = container.querySelector('[data-insight-tabs]');
      const tabs = element.querySelectorAll('[role="tab"]');

      new InsightUI.Tabs(element);

      tabs[0].focus();
      TestUtils.keydown(tabs[0], 'End');

      expect(document.activeElement).toBe(tabs[2]);
    });
  });

  describe('HTMX Integration', () => {
    it('should register htmx:afterSwap listener', () => {
      const addEventListenerSpy = vi.spyOn(document.body, 'addEventListener');

      const container = createTabsDOM();
      const element = container.querySelector('[data-insight-tabs]');

      new InsightUI.Tabs(element);

      expect(addEventListenerSpy).toHaveBeenCalledWith('htmx:afterSwap', expect.any(Function));
    });

    it('should remove htmx:afterSwap listener on destroy', () => {
      const removeEventListenerSpy = vi.spyOn(document.body, 'removeEventListener');

      const container = createTabsDOM();
      const element = container.querySelector('[data-insight-tabs]');

      const tabs = new InsightUI.Tabs(element);
      tabs.destroy();

      expect(removeEventListenerSpy).toHaveBeenCalledWith('htmx:afterSwap', expect.any(Function));
    });
  });

  describe('destroy() method', () => {
    it('should remove tab event listeners', () => {
      const container = createTabsDOM();
      const element = container.querySelector('[data-insight-tabs]');
      const tabButtons = element.querySelectorAll('[role="tab"]');

      const tabs = new InsightUI.Tabs(element);

      const removeSpy = vi.spyOn(tabButtons[0], 'removeEventListener');

      tabs.destroy();

      expect(removeSpy).toHaveBeenCalledWith('keydown', expect.any(Function));
      expect(removeSpy).toHaveBeenCalledWith('click', expect.any(Function));
    });

    it('should nullify references', () => {
      const container = createTabsDOM();
      const element = container.querySelector('[data-insight-tabs]');

      const tabs = new InsightUI.Tabs(element);
      tabs.destroy();

      expect(tabs.element).toBeNull();
      expect(tabs.panelContainer).toBeNull();
    });
  });
});
