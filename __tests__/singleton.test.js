/**
 * Tests for WeakMap singleton pattern across components
 */

import { describe, it, expect, beforeEach } from 'vitest';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const jsDir = path.join(__dirname, '../insight_ui/static/insight_ui/js');

function loadComponent(filename) {
  const filepath = path.join(jsDir, filename);
  const code = fs.readFileSync(filepath, 'utf-8');
  eval(code);
}

describe('WeakMap Singleton Pattern', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
  });

  describe('Dropdown', () => {
    beforeEach(() => {
      loadComponent('insight-ui-dropdown.js');
    });

    it('should have static instances WeakMap', () => {
      expect(InsightUI.Dropdown.instances).toBeInstanceOf(WeakMap);
    });

    it('should return existing instance for same element', () => {
      const container = TestUtils.createDropdown();
      const button = container.querySelector('[data-dropdown-toggle]');

      const instance1 = new InsightUI.Dropdown(button);
      const instance2 = new InsightUI.Dropdown(button);

      expect(instance1).toBe(instance2);
    });

    it('should create different instances for different elements', () => {
      const container1 = TestUtils.createDropdown('dropdown-1');
      const container2 = TestUtils.createDropdown('dropdown-2');
      const button1 = container1.querySelector('[data-dropdown-toggle]');
      const button2 = container2.querySelector('[data-dropdown-toggle]');

      const instance1 = new InsightUI.Dropdown(button1);
      const instance2 = new InsightUI.Dropdown(button2);

      expect(instance1).not.toBe(instance2);
    });

    it('should store instance in WeakMap', () => {
      const container = TestUtils.createDropdown();
      const button = container.querySelector('[data-dropdown-toggle]');

      const instance = new InsightUI.Dropdown(button);

      expect(InsightUI.Dropdown.instances.get(button)).toBe(instance);
    });
  });

  describe('Accordion', () => {
    beforeEach(() => {
      loadComponent('insight-ui-accordion.js');
    });

    it('should have static instances WeakMap', () => {
      expect(InsightUI.Accordion.instances).toBeInstanceOf(WeakMap);
    });

    it('should return existing instance for same element', () => {
      const container = TestUtils.createAccordion();
      const element = container.querySelector('[data-accordion]');

      const instance1 = new InsightUI.Accordion(element);
      const instance2 = new InsightUI.Accordion(element);

      expect(instance1).toBe(instance2);
    });
  });

  describe('Carousel', () => {
    beforeEach(() => {
      loadComponent('insight-ui-carousel.js');
    });

    it('should have static instances WeakMap', () => {
      expect(InsightUI.Carousel.instances).toBeInstanceOf(WeakMap);
    });

    it('should return existing instance for same element', () => {
      const container = TestUtils.createCarousel();
      const element = container.querySelector('.carousel');

      const instance1 = new InsightUI.Carousel(element);
      const instance2 = new InsightUI.Carousel(element);

      expect(instance1).toBe(instance2);
    });
  });

  describe('Modal', () => {
    beforeEach(() => {
      loadComponent('insight-ui-utils.js');
      loadComponent('insight-ui-modal.js');
    });

    it('should have static instances WeakMap', () => {
      expect(InsightUI.Modal.instances).toBeInstanceOf(WeakMap);
    });

    it('should return existing instance for same button', () => {
      const container = TestUtils.createModal();
      const button = container.querySelector('[data-insight-toggle="modal"]');

      const instance1 = new InsightUI.Modal(button);
      const instance2 = new InsightUI.Modal(button);

      expect(instance1).toBe(instance2);
    });
  });

  describe('Floater', () => {
    beforeEach(() => {
      loadComponent('insight-ui-floater.js');
    });

    it('should have static instances WeakMap', () => {
      expect(InsightUI.Floater.instances).toBeInstanceOf(WeakMap);
    });

    it('should return existing instance for same trigger', () => {
      const container = TestUtils.createDOM(`
        <button data-tooltip-trigger="test-tip">Hover me</button>
        <div id="test-tip">Tooltip</div>
      `);
      const trigger = container.querySelector('[data-tooltip-trigger]');

      const instance1 = new InsightUI.Floater(trigger, 'tooltip');
      const instance2 = new InsightUI.Floater(trigger, 'tooltip');

      expect(instance1).toBe(instance2);
    });
  });

  describe('Tabs', () => {
    beforeEach(() => {
      loadComponent('insight-ui-tabs.js');
    });

    it('should have static instances WeakMap', () => {
      expect(InsightUI.Tabs.instances).toBeInstanceOf(WeakMap);
    });
  });

  describe('Checkbox', () => {
    beforeEach(() => {
      loadComponent('insight-ui-checkbox.js');
    });

    it('should have static instances WeakMap', () => {
      expect(InsightUI.Checkbox.instances).toBeInstanceOf(WeakMap);
    });
  });

  describe('Multiselect', () => {
    beforeEach(() => {
      loadComponent('insight-ui-multiselect.js');
    });

    it('should have static instances WeakMap', () => {
      expect(InsightUI.Multiselect.instances).toBeInstanceOf(WeakMap);
    });
  });

  describe('Sidebar', () => {
    beforeEach(() => {
      loadComponent('insight-ui-utils.js');
      loadComponent('insight-ui-sidebar.js');
    });

    it('should have static instances WeakMap', () => {
      expect(InsightUI.Sidebar.instances).toBeInstanceOf(WeakMap);
    });
  });

  describe('ThreeDCarousel', () => {
    beforeEach(() => {
      loadComponent('insight-ui-3D-carousel.js');
    });

    it('should have static instances WeakMap', () => {
      expect(InsightUI.ThreeDCarousel.instances).toBeInstanceOf(WeakMap);
    });
  });
});

describe('initAll() static methods', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
  });

  describe('Dropdown.initAll()', () => {
    beforeEach(() => {
      loadComponent('insight-ui-dropdown.js');
    });

    it('should initialize all dropdowns in DOM', () => {
      TestUtils.createDropdown('dropdown-1');
      TestUtils.createDropdown('dropdown-2');

      InsightUI.Dropdown.initAll();

      const buttons = document.querySelectorAll('[data-dropdown-toggle]');
      buttons.forEach(btn => {
        expect(InsightUI.Dropdown.instances.has(btn)).toBe(true);
      });
    });

    it('should not re-initialize existing instances', () => {
      const container = TestUtils.createDropdown();
      const button = container.querySelector('[data-dropdown-toggle]');

      const instance1 = new InsightUI.Dropdown(button);
      InsightUI.Dropdown.initAll();
      const instance2 = InsightUI.Dropdown.instances.get(button);

      expect(instance1).toBe(instance2);
    });
  });

  describe('Accordion.initAll()', () => {
    beforeEach(() => {
      loadComponent('insight-ui-accordion.js');
    });

    it('should initialize all accordions in DOM', () => {
      TestUtils.createAccordion('accordion-1');
      TestUtils.createAccordion('accordion-2');

      InsightUI.Accordion.initAll();

      const accordions = document.querySelectorAll('[data-accordion]');
      accordions.forEach(el => {
        expect(InsightUI.Accordion.instances.has(el)).toBe(true);
      });
    });
  });
});
