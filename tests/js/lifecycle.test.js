/**
 * Tests for component lifecycle management (destroy methods)
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const jsDir = path.join(__dirname, '../../insight_ui/static/insight_ui/js');

// Load component files
function loadComponent(filename) {
  const filepath = path.join(jsDir, filename);
  const code = fs.readFileSync(filepath, 'utf-8');
  const transformed = code.replace(/export class\s+(\w+)/g, 'window.InsightUI.$1 = class $1');
  eval(transformed);
}

describe('Component Lifecycle - destroy() methods', () => {
  beforeEach(() => {
    // Reset InsightUI namespace
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
  });

  describe('Dropdown', () => {
    beforeEach(() => {
      loadComponent('insight-ui-dropdown.js');
    });

    it('should have a destroy method', () => {
      const container = TestUtils.createDropdown();
      const button = container.querySelector('[data-insight-dropdown]');
      const dropdown = new InsightUI.Dropdown(button);

      expect(typeof dropdown.destroy).toBe('function');
    });

    it('should remove event listeners on destroy', () => {
      const container = TestUtils.createDropdown();
      const button = container.querySelector('[data-insight-dropdown]');
      const dropdown = new InsightUI.Dropdown(button);

      const removeEventListenerSpy = vi.spyOn(button, 'removeEventListener');
      dropdown.destroy();

      expect(removeEventListenerSpy).toHaveBeenCalledWith('click', expect.any(Function));
    });

    it('should remove instance from WeakMap on destroy', () => {
      const container = TestUtils.createDropdown();
      const button = container.querySelector('[data-insight-dropdown]');
      const dropdown = new InsightUI.Dropdown(button);

      expect(InsightUI.Dropdown.instances.has(button)).toBe(true);
      dropdown.destroy();
      expect(InsightUI.Dropdown.instances.has(button)).toBe(false);
    });

    it('should nullify references on destroy', () => {
      const container = TestUtils.createDropdown();
      const button = container.querySelector('[data-insight-dropdown]');
      const dropdown = new InsightUI.Dropdown(button);

      dropdown.destroy();

      expect(dropdown.trigger).toBeNull();
      expect(dropdown.menu).toBeNull();
    });
  });

  describe('Accordion', () => {
    beforeEach(() => {
      loadComponent('insight-ui-accordion.js');
    });

    it('should have a destroy method', () => {
      const container = TestUtils.createAccordion();
      const element = container.querySelector('[data-insight-accordion]');
      const accordion = new InsightUI.Accordion(element);

      expect(typeof accordion.destroy).toBe('function');
    });

    it('should remove button event listeners on destroy', () => {
      const container = TestUtils.createAccordion();
      const element = container.querySelector('[data-insight-accordion]');
      const accordion = new InsightUI.Accordion(element);
      const buttons = element.querySelectorAll('button[aria-controls]');

      const spies = Array.from(buttons).map(btn =>
        vi.spyOn(btn, 'removeEventListener')
      );

      accordion.destroy();

      spies.forEach(spy => {
        expect(spy).toHaveBeenCalledWith('click', expect.any(Function));
        expect(spy).toHaveBeenCalledWith('keydown', expect.any(Function));
      });
    });

    it('should remove instance from WeakMap on destroy', () => {
      const container = TestUtils.createAccordion();
      const element = container.querySelector('[data-insight-accordion]');
      const accordion = new InsightUI.Accordion(element);

      expect(InsightUI.Accordion.instances.has(element)).toBe(true);
      accordion.destroy();
      expect(InsightUI.Accordion.instances.has(element)).toBe(false);
    });
  });

  describe('Carousel', () => {
    beforeEach(() => {
      loadComponent('insight-ui-carousel.js');
    });

    it('should have a destroy method', () => {
      const container = TestUtils.createCarousel();
      const element = container.querySelector('[data-insight-carousel]');
      const carousel = new InsightUI.Carousel(element);

      expect(typeof carousel.destroy).toBe('function');
    });

    it('should stop autoplay interval on destroy', () => {
      const container = TestUtils.createCarousel();
      const element = container.querySelector('[data-insight-carousel]');
      element.dataset.autoplay = 'true';
      const carousel = new InsightUI.Carousel(element);

      const clearIntervalSpy = vi.spyOn(globalThis, 'clearInterval');
      carousel.destroy();

      expect(clearIntervalSpy).toHaveBeenCalled();
    });

    it('should remove window resize listener on destroy', () => {
      const container = TestUtils.createCarousel();
      const element = container.querySelector('[data-insight-carousel]');
      const carousel = new InsightUI.Carousel(element);

      const removeEventListenerSpy = vi.spyOn(window, 'removeEventListener');
      carousel.destroy();

      expect(removeEventListenerSpy).toHaveBeenCalledWith('resize', expect.any(Function));
    });

    it('should remove instance from WeakMap on destroy', () => {
      const container = TestUtils.createCarousel();
      const element = container.querySelector('[data-insight-carousel]');
      const carousel = new InsightUI.Carousel(element);

      expect(InsightUI.Carousel.instances.has(element)).toBe(true);
      carousel.destroy();
      expect(InsightUI.Carousel.instances.has(element)).toBe(false);
    });
  });

  describe('Modal', () => {
    beforeEach(() => {
      loadComponent('insight-ui-utils.js');
      loadComponent('insight-ui-modal.js');
    });

    it('should have a destroy method', () => {
      const container = TestUtils.createModal();
      const button = container.querySelector('[data-insight-modal]');
      const modal = new InsightUI.Modal(button);

      expect(typeof modal.destroy).toBe('function');
    });

    it('should close modal if open on destroy', () => {
      const container = TestUtils.createModal();
      const button = container.querySelector('[data-insight-modal]');
      const modal = new InsightUI.Modal(button);

      modal.open();
      expect(InsightUI.Modal.currentOpen).toBe(modal);

      modal.destroy();
      expect(InsightUI.Modal.currentOpen).toBeNull();
    });

    it('should remove instance from WeakMap on destroy', () => {
      const container = TestUtils.createModal();
      const button = container.querySelector('[data-insight-modal]');
      const modal = new InsightUI.Modal(button);

      expect(InsightUI.Modal.instances.has(button)).toBe(true);
      modal.destroy();
      expect(InsightUI.Modal.instances.has(button)).toBe(false);
    });
  });
});

describe('Component Lifecycle - global listener cleanup', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
  });

  describe('Floater', () => {
    beforeEach(() => {
      loadComponent('insight-ui-floater.js');
    });

    it('should remove window scroll listener on destroy', () => {
      const container = TestUtils.createDOM(`
        <button data-insight-popover="test-popover">Trigger</button>
        <div id="test-popover">Popover content</div>
      `);
      const trigger = container.querySelector('[data-insight-popover]');
      const floater = new InsightUI.Floater(trigger, 'popover');

      const removeEventListenerSpy = vi.spyOn(window, 'removeEventListener');
      floater.destroy();

      expect(removeEventListenerSpy).toHaveBeenCalledWith('scroll', expect.any(Function));
    });
  });

  describe('Sidebar', () => {
    beforeEach(() => {
      loadComponent('insight-ui-utils.js');
      loadComponent('insight-ui-sidebar.js');
    });

    it('should remove document mousemove listener on destroy when autoClose', () => {
      const container = TestUtils.createDOM(`
        <div data-insight-sidebar="left" data-static="False">
          <aside data-auto-close="true">Sidebar content</aside>
        </div>
      `);
      const wrapper = container.querySelector('[data-insight-sidebar]');
      const sidebar = new InsightUI.Sidebar(wrapper);

      const removeEventListenerSpy = vi.spyOn(document, 'removeEventListener');
      sidebar.destroy();

      expect(removeEventListenerSpy).toHaveBeenCalledWith('mousemove', expect.any(Function));
    });
  });

  describe('Tabs', () => {
    beforeEach(() => {
      loadComponent('insight-ui-tabs.js');
    });

    it('should remove document.body htmx:afterSwap listener on destroy', () => {
      const container = TestUtils.createDOM(`
        <div data-insight-tabs>
          <div role="tablist">
            <button role="tab">Tab 1</button>
            <button role="tab">Tab 2</button>
          </div>
          <div id="tab-content">Content</div>
        </div>
      `);
      const tabBar = container.querySelector('[data-insight-tabs]');
      const tabs = new InsightUI.Tabs(tabBar);

      const removeEventListenerSpy = vi.spyOn(document.body, 'removeEventListener');
      tabs.destroy();

      expect(removeEventListenerSpy).toHaveBeenCalledWith('htmx:afterSwap', expect.any(Function));
    });
  });
});
