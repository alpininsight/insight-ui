/**
 * Tests for Multiselect component functionality
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

function createMultiselectDOM(options = {}) {
  const {
    name = 'test-multiselect',
    max = '',
    selected = '',
    optionsList = ['Option A', 'Option B', 'Option C', 'Option D'],
    withButtons = false,
  } = options;

  const optionsHTML = optionsList.map((opt, i) =>
    `<div class="option" id="opt-${i}" role="option">${opt}</div>`
  ).join('');

  const buttonsHTML = withButtons ? `
    <button class="select-all">Select All</button>
    <button class="deselect-all">Deselect All</button>
  ` : '';

  return TestUtils.createDOM(`
    <div data-insight-multiselect data-name="${name}" data-max="${max}" data-selected="${selected}">
      <div role="combobox" aria-expanded="false">
        <div class="selected">
          <div class="tags"></div>
          <input type="text" class="search" placeholder="Search...">
        </div>
      </div>
      <div class="options hidden">
        ${optionsHTML}
      </div>
      <div class="info"></div>
      <div id="${name}-aria-status" aria-live="polite"></div>
      ${buttonsHTML}
    </div>
  `);
}

describe('Multiselect Component', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;

    // Mock Django i18n functions
    globalThis.gettext = (s) => s;
    globalThis.ngettext = (s, p, n) => n === 1 ? s : p;
    globalThis.interpolate = (s, vars, useNamed) => {
      if (useNamed) {
        return s.replace(/%\((\w+)\)s/g, (_, key) => vars[key]);
      }
      return s;
    };

    loadComponent('insight-ui-multiselect.js');
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  describe('Singleton Pattern', () => {
    it('should have static instances WeakMap', () => {
      expect(InsightUI.Multiselect.instances).toBeInstanceOf(WeakMap);
    });

    it('should return existing instance for same element', () => {
      const container = createMultiselectDOM();
      const element = container.querySelector('[data-insight-multiselect]');

      const instance1 = new InsightUI.Multiselect(element);
      const instance2 = new InsightUI.Multiselect(element);

      expect(instance1).toBe(instance2);
    });
  });

  describe('Initialization', () => {
    it('should parse initial selected values from data attribute', () => {
      const container = createMultiselectDOM({ selected: "['Option A', 'Option B']" });
      const element = container.querySelector('[data-insight-multiselect]');

      const multiselect = new InsightUI.Multiselect(element);

      expect(multiselect.selectedValues).toEqual(['Option A', 'Option B']);
    });

    it('should hide initially selected options', () => {
      const container = createMultiselectDOM({ selected: "['Option A']" });
      const element = container.querySelector('[data-insight-multiselect]');
      const optionA = element.querySelector('#opt-0');

      new InsightUI.Multiselect(element);

      expect(optionA.hidden).toBe(true);
      expect(optionA.getAttribute('aria-selected')).toBe('true');
    });

    it('should render badges for initially selected values', () => {
      const container = createMultiselectDOM({ selected: "['Option A', 'Option B']" });
      const element = container.querySelector('[data-insight-multiselect]');

      new InsightUI.Multiselect(element);

      const tags = element.querySelectorAll('.tags span');
      expect(tags.length).toBe(2);
    });

    it('should create hidden inputs for form submission', () => {
      const container = createMultiselectDOM({
        name: 'fruits',
        selected: "['Option A']"
      });
      const element = container.querySelector('[data-insight-multiselect]');

      new InsightUI.Multiselect(element);

      const hiddenInput = element.querySelector('input[type="hidden"]');
      expect(hiddenInput).not.toBeNull();
      expect(hiddenInput.name).toBe('fruits');
      expect(hiddenInput.value).toBe('Option A');
    });
  });

  describe('Dropdown Toggle', () => {
    it('should show dropdown on search focus', () => {
      const container = createMultiselectDOM();
      const element = container.querySelector('[data-insight-multiselect]');
      const search = element.querySelector('.search');
      const options = element.querySelector('.options');
      const combobox = element.querySelector('[role="combobox"]');

      new InsightUI.Multiselect(element);

      search.dispatchEvent(new Event('focus', { bubbles: true }));

      expect(options.classList.contains('hidden')).toBe(false);
      expect(combobox.getAttribute('aria-expanded')).toBe('true');
    });

    it('should hide dropdown on outside click', () => {
      const container = createMultiselectDOM();
      const element = container.querySelector('[data-insight-multiselect]');
      const search = element.querySelector('.search');
      const options = element.querySelector('.options');

      new InsightUI.Multiselect(element);

      // Open dropdown
      search.dispatchEvent(new Event('focus', { bubbles: true }));
      expect(options.classList.contains('hidden')).toBe(false);

      // Click outside
      document.body.dispatchEvent(new MouseEvent('click', { bubbles: true }));

      expect(options.classList.contains('hidden')).toBe(true);
    });
  });

  describe('Option Selection', () => {
    it('should select option on click', () => {
      const container = createMultiselectDOM();
      const element = container.querySelector('[data-insight-multiselect]');
      const option = element.querySelector('#opt-0');

      const multiselect = new InsightUI.Multiselect(element);

      TestUtils.click(option);

      expect(multiselect.selectedValues).toContain('Option A');
      expect(option.hidden).toBe(true);
      expect(option.getAttribute('aria-selected')).toBe('true');
    });

    it('should deselect option when clicking again', () => {
      const container = createMultiselectDOM({ selected: "['Option A']" });
      const element = container.querySelector('[data-insight-multiselect]');
      const option = element.querySelector('#opt-0');

      const multiselect = new InsightUI.Multiselect(element);

      // Option is already selected, click to deselect
      TestUtils.click(option);

      expect(multiselect.selectedValues).not.toContain('Option A');
      expect(option.hidden).toBe(false);
      expect(option.getAttribute('aria-selected')).toBe('false');
    });

    it('should dispatch change event on selection', () => {
      const container = createMultiselectDOM();
      const element = container.querySelector('[data-insight-multiselect]');
      const option = element.querySelector('#opt-0');

      new InsightUI.Multiselect(element);

      const changeHandler = vi.fn();
      element.addEventListener('change', changeHandler);

      TestUtils.click(option);

      expect(changeHandler).toHaveBeenCalled();
      expect(changeHandler.mock.calls[0][0].detail.value).toContain('Option A');
    });
  });

  describe('Maximum Selection Limit', () => {
    it('should prevent selection beyond max', () => {
      vi.useFakeTimers();

      const container = createMultiselectDOM({ max: '2' });
      const element = container.querySelector('[data-insight-multiselect]');
      const options = element.querySelectorAll('.option');
      const selected = element.querySelector('.selected');

      const multiselect = new InsightUI.Multiselect(element);

      // Select two options
      TestUtils.click(options[0]);
      TestUtils.click(options[1]);

      expect(multiselect.selectedValues.length).toBe(2);

      // Try to select third
      TestUtils.click(options[2]);

      // Should not be added
      expect(multiselect.selectedValues.length).toBe(2);
      expect(multiselect.selectedValues).not.toContain('Option C');

      // Should show shake animation
      expect(selected.classList.contains('animate-shake')).toBe(true);

      vi.advanceTimersByTime(300);
      expect(selected.classList.contains('animate-shake')).toBe(false);
    });

    it('should show count info when max is set', () => {
      const container = createMultiselectDOM({ max: '3', selected: "['Option A']" });
      const element = container.querySelector('[data-insight-multiselect]');
      const info = element.querySelector('.info');

      new InsightUI.Multiselect(element);

      expect(info.textContent).toContain('1');
      expect(info.textContent).toContain('3');
    });
  });

  describe('Search Filtering', () => {
    it('should filter options on input', () => {
      const container = createMultiselectDOM();
      const element = container.querySelector('[data-insight-multiselect]');
      const search = element.querySelector('.search');
      const options = element.querySelectorAll('.option');

      new InsightUI.Multiselect(element);

      // Type in search
      search.value = 'Option A';
      search.dispatchEvent(new Event('input', { bubbles: true }));

      // Only Option A should be visible
      expect(options[0].hidden).toBe(false);
      expect(options[1].hidden).toBe(true);
      expect(options[2].hidden).toBe(true);
    });

    it('should filter case-insensitively', () => {
      const container = createMultiselectDOM();
      const element = container.querySelector('[data-insight-multiselect]');
      const search = element.querySelector('.search');
      const options = element.querySelectorAll('.option');

      new InsightUI.Multiselect(element);

      search.value = 'option a';
      search.dispatchEvent(new Event('input', { bubbles: true }));

      expect(options[0].hidden).toBe(false);
    });

    it('should clear search on blur', () => {
      const container = createMultiselectDOM();
      const element = container.querySelector('[data-insight-multiselect]');
      const search = element.querySelector('.search');

      new InsightUI.Multiselect(element);

      search.value = 'test';
      search.dispatchEvent(new Event('blur', { bubbles: true }));

      expect(search.value).toBe('');
    });
  });

  describe('Keyboard Navigation', () => {
    it('should move focus down with ArrowDown', () => {
      const container = createMultiselectDOM();
      const element = container.querySelector('[data-insight-multiselect]');
      const search = element.querySelector('.search');
      const options = element.querySelectorAll('.option');

      const multiselect = new InsightUI.Multiselect(element);

      // Open dropdown
      search.dispatchEvent(new Event('focus', { bubbles: true }));

      // Press ArrowDown
      search.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowDown', bubbles: true }));

      expect(multiselect.focusedIndex).toBe(0);
      expect(options[0].classList.contains('bg-blue-50')).toBe(true);
    });

    it('should move focus up with ArrowUp', () => {
      const container = createMultiselectDOM();
      const element = container.querySelector('[data-insight-multiselect]');
      const search = element.querySelector('.search');
      const options = element.querySelectorAll('.option');

      const multiselect = new InsightUI.Multiselect(element);

      // Open dropdown and move to second option
      search.dispatchEvent(new Event('focus', { bubbles: true }));
      search.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowDown', bubbles: true }));
      search.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowDown', bubbles: true }));

      expect(multiselect.focusedIndex).toBe(1);

      // Press ArrowUp
      search.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowUp', bubbles: true }));

      expect(multiselect.focusedIndex).toBe(0);
    });

    it('should select focused option on Enter', () => {
      const container = createMultiselectDOM();
      const element = container.querySelector('[data-insight-multiselect]');
      const search = element.querySelector('.search');

      const multiselect = new InsightUI.Multiselect(element);

      // Open and focus first option
      search.dispatchEvent(new Event('focus', { bubbles: true }));
      search.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowDown', bubbles: true }));

      // Press Enter
      search.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true }));

      expect(multiselect.selectedValues).toContain('Option A');
    });

    it('should remove last selected value on Backspace when search is empty', () => {
      const container = createMultiselectDOM({ selected: "['Option A', 'Option B']" });
      const element = container.querySelector('[data-insight-multiselect]');
      const search = element.querySelector('.search');

      const multiselect = new InsightUI.Multiselect(element);

      expect(multiselect.selectedValues).toEqual(['Option A', 'Option B']);

      // Press Backspace with empty search
      search.value = '';
      search.dispatchEvent(new KeyboardEvent('keydown', { key: 'Backspace', bubbles: true }));

      expect(multiselect.selectedValues).toEqual(['Option A']);
    });

    it('should close dropdown on Escape', () => {
      const container = createMultiselectDOM();
      const element = container.querySelector('[data-insight-multiselect]');
      const search = element.querySelector('.search');
      const options = element.querySelector('.options');

      new InsightUI.Multiselect(element);

      // Open dropdown
      search.dispatchEvent(new Event('focus', { bubbles: true }));
      expect(options.classList.contains('hidden')).toBe(false);

      // Press Escape
      search.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));

      expect(options.classList.contains('hidden')).toBe(true);
    });
  });

  describe('Select/Deselect All', () => {
    it('should select all options', () => {
      const container = createMultiselectDOM({ withButtons: true });
      const element = container.querySelector('[data-insight-multiselect]');
      const selectAllBtn = element.querySelector('.select-all');

      const multiselect = new InsightUI.Multiselect(element);

      TestUtils.click(selectAllBtn);

      expect(multiselect.selectedValues.length).toBe(4);
    });

    it('should respect max limit when selecting all', () => {
      const container = createMultiselectDOM({ withButtons: true, max: '2' });
      const element = container.querySelector('[data-insight-multiselect]');
      const selectAllBtn = element.querySelector('.select-all');

      const multiselect = new InsightUI.Multiselect(element);

      TestUtils.click(selectAllBtn);

      // Should only select up to max (2), not all 4
      expect(multiselect.selectedValues.length).toBe(2);
    });

    it('should respect max limit when some options are already selected', () => {
      const container = createMultiselectDOM({
        withButtons: true,
        max: '3',
        selected: "['Option A']"
      });
      const element = container.querySelector('[data-insight-multiselect]');
      const selectAllBtn = element.querySelector('.select-all');

      const multiselect = new InsightUI.Multiselect(element);

      expect(multiselect.selectedValues.length).toBe(1);

      TestUtils.click(selectAllBtn);

      // Should add 2 more (up to max of 3)
      expect(multiselect.selectedValues.length).toBe(3);
    });

    it('should deselect all options', () => {
      const container = createMultiselectDOM({
        withButtons: true,
        selected: "['Option A', 'Option B']"
      });
      const element = container.querySelector('[data-insight-multiselect]');
      const deselectAllBtn = element.querySelector('.deselect-all');

      const multiselect = new InsightUI.Multiselect(element);

      expect(multiselect.selectedValues.length).toBe(2);

      TestUtils.click(deselectAllBtn);

      expect(multiselect.selectedValues.length).toBe(0);
    });
  });

  describe('Tag Removal', () => {
    it('should remove tag on remove button click', () => {
      const container = createMultiselectDOM({ selected: "['Option A', 'Option B']" });
      const element = container.querySelector('[data-insight-multiselect]');

      const multiselect = new InsightUI.Multiselect(element);

      const removeBtn = element.querySelector('.tags span button');
      TestUtils.click(removeBtn);

      expect(multiselect.selectedValues.length).toBe(1);
    });
  });

  describe('destroy() method', () => {
    it('should remove search listeners', () => {
      const container = createMultiselectDOM();
      const element = container.querySelector('[data-insight-multiselect]');
      const search = element.querySelector('.search');

      const multiselect = new InsightUI.Multiselect(element);

      const removeSpy = vi.spyOn(search, 'removeEventListener');

      multiselect.destroy();

      expect(removeSpy).toHaveBeenCalledWith('input', expect.any(Function));
      expect(removeSpy).toHaveBeenCalledWith('focus', expect.any(Function));
      expect(removeSpy).toHaveBeenCalledWith('blur', expect.any(Function));
      expect(removeSpy).toHaveBeenCalledWith('keydown', expect.any(Function));
    });

    it('should remove document click listener', () => {
      const container = createMultiselectDOM();
      const element = container.querySelector('[data-insight-multiselect]');

      const multiselect = new InsightUI.Multiselect(element);

      const removeSpy = vi.spyOn(document, 'removeEventListener');

      multiselect.destroy();

      expect(removeSpy).toHaveBeenCalledWith('click', expect.any(Function));
    });

    it('should remove instance from WeakMap', () => {
      const container = createMultiselectDOM();
      const element = container.querySelector('[data-insight-multiselect]');

      const multiselect = new InsightUI.Multiselect(element);

      expect(InsightUI.Multiselect.instances.has(element)).toBe(true);

      multiselect.destroy();

      expect(InsightUI.Multiselect.instances.has(element)).toBe(false);
    });

    it('should nullify element reference', () => {
      const container = createMultiselectDOM();
      const element = container.querySelector('[data-insight-multiselect]');

      const multiselect = new InsightUI.Multiselect(element);
      multiselect.destroy();

      expect(multiselect.element).toBeNull();
    });
  });
});
