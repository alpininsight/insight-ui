// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Tests for Dropdown component functionality
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

describe('Dropdown Component', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
    loadComponent('insight-ui-dropdown.js');
  });

  describe('Toggle Functionality', () => {
    it('should show dropdown menu on trigger click', () => {
      const container = TestUtils.createDropdown();
      const button = container.querySelector('[data-insight-dropdown]');
      const menu = container.querySelector('#test-dropdown');

      new InsightUI.Dropdown(button);

      expect(menu.classList.contains('hidden')).toBe(true);

      TestUtils.click(button);

      expect(menu.classList.contains('hidden')).toBe(false);
    });

    it('should hide dropdown menu on second trigger click', () => {
      const container = TestUtils.createDropdown();
      const button = container.querySelector('[data-insight-dropdown]');
      const menu = container.querySelector('#test-dropdown');

      new InsightUI.Dropdown(button);

      TestUtils.click(button); // open
      expect(menu.classList.contains('hidden')).toBe(false);

      TestUtils.click(button); // close
      expect(menu.classList.contains('hidden')).toBe(true);
    });

    it('should hide dropdown on document click', () => {
      const container = TestUtils.createDropdown();
      const button = container.querySelector('[data-insight-dropdown]');
      const menu = container.querySelector('#test-dropdown');

      new InsightUI.Dropdown(button);

      TestUtils.click(button); // open
      expect(menu.classList.contains('hidden')).toBe(false);

      // Click somewhere else in document
      document.body.click();

      expect(menu.classList.contains('hidden')).toBe(true);
    });

    it('should stop event propagation on trigger click', () => {
      const container = TestUtils.createDropdown();
      const button = container.querySelector('[data-insight-dropdown]');

      new InsightUI.Dropdown(button);

      const propagationSpy = vi.fn();
      document.addEventListener('click', propagationSpy);

      // The dropdown's click handler calls stopPropagation
      button.dispatchEvent(new MouseEvent('click', { bubbles: true }));

      // The document listener should not receive the event
      // Note: This tests that stopPropagation was called
      expect(propagationSpy).not.toHaveBeenCalled();

      document.removeEventListener('click', propagationSpy);
    });
  });

  describe('Multiple Dropdowns', () => {
    it('should close other dropdowns when opening a new one', () => {
      const container1 = TestUtils.createDropdown('dropdown-1');
      const container2 = TestUtils.createDropdown('dropdown-2');
      const button1 = container1.querySelector('[data-insight-dropdown]');
      const button2 = container2.querySelector('[data-insight-dropdown]');
      const menu1 = container1.querySelector('#dropdown-1');
      const menu2 = container2.querySelector('#dropdown-2');

      new InsightUI.Dropdown(button1);
      new InsightUI.Dropdown(button2);

      // Open first dropdown
      TestUtils.click(button1);
      expect(menu1.classList.contains('hidden')).toBe(false);
      expect(menu2.classList.contains('hidden')).toBe(true);

      // Open second dropdown - first should close
      TestUtils.click(button2);
      expect(menu1.classList.contains('hidden')).toBe(true);
      expect(menu2.classList.contains('hidden')).toBe(false);
    });

    it('should track currentOpen correctly', () => {
      const container = TestUtils.createDropdown();
      const button = container.querySelector('[data-insight-dropdown]');

      const dropdown = new InsightUI.Dropdown(button);

      expect(InsightUI.Dropdown.currentOpen).toBeNull();

      TestUtils.click(button);
      expect(InsightUI.Dropdown.currentOpen).toBe(dropdown);

      TestUtils.click(button);
      expect(InsightUI.Dropdown.currentOpen).toBeNull();
    });
  });

  describe('hide() method', () => {
    it('should add hidden class to menu', () => {
      const container = TestUtils.createDropdown();
      const button = container.querySelector('[data-insight-dropdown]');
      const menu = container.querySelector('#test-dropdown');

      const dropdown = new InsightUI.Dropdown(button);

      TestUtils.click(button); // open
      expect(menu.classList.contains('hidden')).toBe(false);

      dropdown.hide();
      expect(menu.classList.contains('hidden')).toBe(true);
    });

    it('should clear currentOpen when hiding', () => {
      const container = TestUtils.createDropdown();
      const button = container.querySelector('[data-insight-dropdown]');

      const dropdown = new InsightUI.Dropdown(button);

      TestUtils.click(button);
      expect(InsightUI.Dropdown.currentOpen).toBe(dropdown);

      dropdown.hide();
      expect(InsightUI.Dropdown.currentOpen).toBeNull();
    });

    it('should do nothing if already hidden', () => {
      const container = TestUtils.createDropdown();
      const button = container.querySelector('[data-insight-dropdown]');
      const menu = container.querySelector('#test-dropdown');

      const dropdown = new InsightUI.Dropdown(button);

      // Menu starts hidden
      expect(menu.classList.contains('hidden')).toBe(true);

      // Calling hide should not throw or cause issues
      expect(() => dropdown.hide()).not.toThrow();
      expect(menu.classList.contains('hidden')).toBe(true);
    });
  });

  describe('CSS Classes', () => {
    it('should add positioning classes to menu on initialization', () => {
      const container = TestUtils.createDropdown();
      const button = container.querySelector('[data-insight-dropdown]');
      const menu = container.querySelector('#test-dropdown');

      new InsightUI.Dropdown(button);

      expect(menu.classList.contains('absolute')).toBe(true);
      expect(menu.classList.contains('z-50')).toBe(true);
      expect(menu.classList.contains('mt-2')).toBe(true);
    });
  });

  describe('Error Handling', () => {
    it('should handle missing menu element gracefully', () => {
      const container = TestUtils.createDOM(`
        <button data-insight-dropdown="nonexistent">Toggle</button>
      `);
      const button = container.querySelector('[data-insight-dropdown]');

      // Should not throw
      expect(() => new InsightUI.Dropdown(button)).not.toThrow();
    });
  });
});
