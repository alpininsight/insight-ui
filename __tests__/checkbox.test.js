/**
 * Tests for Checkbox group component functionality
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

function createCheckboxGroup(options = {}) {
  const {
    min = 1,
    max = 3,
    count = 4,
    initialChecked = []
  } = options;

  const checkboxes = Array.from({ length: count }, (_, i) => {
    const checked = initialChecked.includes(i) ? 'checked' : '';
    return `<input type="checkbox" id="cb-${i}" value="${i}" ${checked}>`;
  }).join('');

  return TestUtils.createDOM(`
    <div data-insight-checkbox-group data-minimum-checked="${min}" data-maximum-checked="${max}">
      ${checkboxes}
    </div>
  `);
}

describe('Checkbox Group Component', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
    loadComponent('insight-ui-checkbox.js');
  });

  describe('Initialization Constraints', () => {
    it('should auto-check boxes if below minimum', () => {
      // No boxes checked, min is 2
      const container = createCheckboxGroup({ min: 2, max: 4, initialChecked: [] });
      const element = container.querySelector('[data-insight-checkbox-group]');
      const checkboxes = element.querySelectorAll('input');

      new InsightUI.Checkbox(element);

      // First 2 checkboxes should be auto-checked
      expect(checkboxes[0].checked).toBe(true);
      expect(checkboxes[1].checked).toBe(true);
      expect(checkboxes[2].checked).toBe(false);
    });

    it('should auto-uncheck boxes if above maximum', () => {
      // 4 boxes checked, max is 2
      const container = createCheckboxGroup({
        min: 1,
        max: 2,
        count: 4,
        initialChecked: [0, 1, 2, 3]
      });
      const element = container.querySelector('[data-insight-checkbox-group]');
      const checkboxes = element.querySelectorAll('input');

      new InsightUI.Checkbox(element);

      // Should have exactly 2 checked (last 2 unchecked)
      const checkedCount = [...checkboxes].filter(cb => cb.checked).length;
      expect(checkedCount).toBe(2);
    });

    it('should preserve checked state when within constraints', () => {
      const container = createCheckboxGroup({
        min: 1,
        max: 3,
        initialChecked: [1, 2]
      });
      const element = container.querySelector('[data-insight-checkbox-group]');
      const checkboxes = element.querySelectorAll('input');

      new InsightUI.Checkbox(element);

      expect(checkboxes[0].checked).toBe(false);
      expect(checkboxes[1].checked).toBe(true);
      expect(checkboxes[2].checked).toBe(true);
      expect(checkboxes[3].checked).toBe(false);
    });
  });

  describe('Minimum Constraint Enforcement', () => {
    it('should prevent unchecking below minimum', () => {
      const container = createCheckboxGroup({
        min: 2,
        max: 4,
        initialChecked: [0, 1]
      });
      const element = container.querySelector('[data-insight-checkbox-group]');
      const checkboxes = element.querySelectorAll('input');

      new InsightUI.Checkbox(element);

      // Try to uncheck first checkbox
      checkboxes[0].checked = false;
      checkboxes[0].dispatchEvent(new Event('change', { bubbles: true }));

      // Should be re-checked to maintain minimum
      expect(checkboxes[0].checked).toBe(true);
    });

    it('should allow unchecking when above minimum', () => {
      const container = createCheckboxGroup({
        min: 1,
        max: 4,
        initialChecked: [0, 1, 2]
      });
      const element = container.querySelector('[data-insight-checkbox-group]');
      const checkboxes = element.querySelectorAll('input');

      new InsightUI.Checkbox(element);

      // Uncheck first checkbox (still have 2 checked, above min of 1)
      checkboxes[0].checked = false;
      checkboxes[0].dispatchEvent(new Event('change', { bubbles: true }));

      expect(checkboxes[0].checked).toBe(false);
    });
  });

  describe('Maximum Constraint Enforcement', () => {
    it('should prevent checking above maximum', () => {
      const container = createCheckboxGroup({
        min: 1,
        max: 2,
        initialChecked: [0, 1]
      });
      const element = container.querySelector('[data-insight-checkbox-group]');
      const checkboxes = element.querySelectorAll('input');

      new InsightUI.Checkbox(element);

      // Try to check third checkbox
      checkboxes[2].checked = true;
      checkboxes[2].dispatchEvent(new Event('change', { bubbles: true }));

      // Should be unchecked to maintain maximum
      expect(checkboxes[2].checked).toBe(false);
    });

    it('should allow checking when below maximum', () => {
      const container = createCheckboxGroup({
        min: 1,
        max: 3,
        initialChecked: [0]
      });
      const element = container.querySelector('[data-insight-checkbox-group]');
      const checkboxes = element.querySelectorAll('input');

      new InsightUI.Checkbox(element);

      // Check second checkbox (will have 2 checked, below max of 3)
      checkboxes[1].checked = true;
      checkboxes[1].dispatchEvent(new Event('change', { bubbles: true }));

      expect(checkboxes[1].checked).toBe(true);
    });
  });

  describe('Edge Cases', () => {
    it('should handle min equal to max', () => {
      const container = createCheckboxGroup({
        min: 2,
        max: 2,
        initialChecked: [0, 1]
      });
      const element = container.querySelector('[data-insight-checkbox-group]');
      const checkboxes = element.querySelectorAll('input');

      new InsightUI.Checkbox(element);

      // Try to uncheck
      checkboxes[0].checked = false;
      checkboxes[0].dispatchEvent(new Event('change', { bubbles: true }));

      // Should stay checked
      expect(checkboxes[0].checked).toBe(true);

      // Try to check another
      checkboxes[2].checked = true;
      checkboxes[2].dispatchEvent(new Event('change', { bubbles: true }));

      // Should stay unchecked
      expect(checkboxes[2].checked).toBe(false);
    });

    it('should handle single checkbox with min=1, max=1', () => {
      const container = TestUtils.createDOM(`
        <div data-insight-checkbox-group data-minimum-checked="1" data-maximum-checked="1">
          <input type="checkbox" id="single" value="single">
        </div>
      `);
      const element = container.querySelector('[data-insight-checkbox-group]');
      const checkbox = element.querySelector('input');

      new InsightUI.Checkbox(element);

      // Should be auto-checked to meet minimum
      expect(checkbox.checked).toBe(true);

      // Try to uncheck
      checkbox.checked = false;
      checkbox.dispatchEvent(new Event('change', { bubbles: true }));

      // Should stay checked
      expect(checkbox.checked).toBe(true);
    });
  });

  describe('destroy() method', () => {
    it('should remove change listeners', () => {
      const container = createCheckboxGroup();
      const element = container.querySelector('[data-insight-checkbox-group]');
      const checkboxes = element.querySelectorAll('input');

      const checkbox = new InsightUI.Checkbox(element);

      const removeSpy = vi.spyOn(checkboxes[0], 'removeEventListener');

      checkbox.destroy();

      expect(removeSpy).toHaveBeenCalledWith('change', expect.any(Function));
    });

    it('should remove instance from WeakMap', () => {
      const container = createCheckboxGroup();
      const element = container.querySelector('[data-insight-checkbox-group]');

      const checkbox = new InsightUI.Checkbox(element);

      expect(InsightUI.Checkbox.instances.has(element)).toBe(true);

      checkbox.destroy();

      expect(InsightUI.Checkbox.instances.has(element)).toBe(false);
    });
  });
});
