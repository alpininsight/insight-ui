/**
 * Tests for Sidebar component functionality
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

function createSidebarDOM(options = {}) {
  const {
    side = 'left',
    isStatic = false,
    autoClose = false,
    withOpenButton = false,
  } = options;

  const openButton = withOpenButton
    ? `<button class="open-btn" data-sidebar-target="${side}">Open</button>`
    : '';

  return TestUtils.createDOM(`
    ${openButton}
    <div data-insight-sidebar="${side}" data-static="${isStatic ? 'true' : 'false'}">
      <aside data-auto-close="${autoClose}">
        <button data-insight-dismiss="sidebar">Close</button>
        <nav>Sidebar content</nav>
      </aside>
    </div>
  `);
}

describe('Sidebar Component', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
    loadComponent('insight-ui-utils.js');
    loadComponent('insight-ui-sidebar.js');
  });

  describe('Initialization', () => {
    it('should create sidebar instance', () => {
      const container = createSidebarDOM();
      const wrapper = container.querySelector('[data-insight-sidebar]');

      const sidebar = new InsightUI.Sidebar(wrapper);

      expect(InsightUI.Sidebar.instances.has(wrapper)).toBe(true);
      expect(sidebar.side).toBe('left');
    });

    it('should skip initialization for static sidebar', () => {
      const container = createSidebarDOM({ isStatic: true });
      const wrapper = container.querySelector('[data-insight-sidebar]');
      const aside = wrapper.querySelector('aside');

      new InsightUI.Sidebar(wrapper);

      // Static sidebar should not have transform applied
      expect(aside.style.transform).toBe('');
    });

    it('should set initial transform for left sidebar (LTR)', () => {
      const container = createSidebarDOM({ side: 'left' });
      const wrapper = container.querySelector('[data-insight-sidebar]');
      const aside = wrapper.querySelector('aside');

      new InsightUI.Sidebar(wrapper);

      expect(aside.style.transform).toBe('translateX(-100%)');
    });

    it('should set initial transform for right sidebar (LTR)', () => {
      const container = createSidebarDOM({ side: 'right' });
      const wrapper = container.querySelector('[data-insight-sidebar]');
      const aside = wrapper.querySelector('aside');

      new InsightUI.Sidebar(wrapper);

      expect(aside.style.transform).toBe('translateX(100%)');
    });
  });

  describe('Open/Close Functionality', () => {
    it('should open sidebar on openSidebar() call', async () => {
      const container = createSidebarDOM();
      const wrapper = container.querySelector('[data-insight-sidebar]');
      const aside = wrapper.querySelector('aside');

      const sidebar = new InsightUI.Sidebar(wrapper);

      sidebar.openSidebar();
      await TestUtils.nextFrame();

      expect(aside.style.transform).toBe('translateX(0)');
      expect(wrapper.classList.contains('hidden')).toBe(false);
    });

    it('should close sidebar on closeSidebar() call', () => {
      const container = createSidebarDOM({ side: 'left' });
      const wrapper = container.querySelector('[data-insight-sidebar]');
      const aside = wrapper.querySelector('aside');

      const sidebar = new InsightUI.Sidebar(wrapper);

      sidebar.openSidebar();
      sidebar.closeSidebar();

      expect(aside.style.transform).toBe('translateX(-100%)');
    });

    it('should close sidebar on dismiss button click', () => {
      const container = createSidebarDOM({ side: 'right' });
      const wrapper = container.querySelector('[data-insight-sidebar]');
      const aside = wrapper.querySelector('aside');
      const closeBtn = wrapper.querySelector('[data-insight-dismiss="sidebar"]');

      const sidebar = new InsightUI.Sidebar(wrapper);

      sidebar.openSidebar();
      TestUtils.click(closeBtn);

      expect(aside.style.transform).toBe('translateX(100%)');
    });
  });

  describe('Open Button', () => {
    it('should open sidebar when open button is clicked', async () => {
      const container = createSidebarDOM({ withOpenButton: true });
      const wrapper = container.querySelector('[data-insight-sidebar]');
      const aside = wrapper.querySelector('aside');
      const openBtn = container.querySelector('.open-btn');

      new InsightUI.Sidebar(wrapper);

      TestUtils.click(openBtn);
      await TestUtils.nextFrame();

      expect(aside.style.transform).toBe('translateX(0)');
    });

    it('should hide open button when sidebar opens', () => {
      const container = createSidebarDOM({ withOpenButton: true });
      const wrapper = container.querySelector('[data-insight-sidebar]');
      const openBtn = container.querySelector('.open-btn');

      new InsightUI.Sidebar(wrapper);

      TestUtils.click(openBtn);

      expect(openBtn.classList.contains('hidden')).toBe(true);
    });
  });

  describe('Auto-Close Behavior', () => {
    it('should register mousemove listener when autoClose is true', () => {
      const addSpy = vi.spyOn(document, 'addEventListener');

      const container = createSidebarDOM({ autoClose: true });
      const wrapper = container.querySelector('[data-insight-sidebar]');

      new InsightUI.Sidebar(wrapper);

      expect(addSpy).toHaveBeenCalledWith('mousemove', expect.any(Function));
    });

    it('should not register mousemove listener when autoClose is false', () => {
      const addSpy = vi.spyOn(document, 'addEventListener');

      const container = createSidebarDOM({ autoClose: false });
      const wrapper = container.querySelector('[data-insight-sidebar]');

      new InsightUI.Sidebar(wrapper);

      const mousemoveCalls = addSpy.mock.calls.filter(
        call => call[0] === 'mousemove'
      );
      expect(mousemoveCalls.length).toBe(0);
    });

    it('should register mouseleave listener on aside when autoClose is true', () => {
      const container = createSidebarDOM({ autoClose: true });
      const wrapper = container.querySelector('[data-insight-sidebar]');
      const aside = wrapper.querySelector('aside');

      const addSpy = vi.spyOn(aside, 'addEventListener');

      new InsightUI.Sidebar(wrapper);

      expect(addSpy).toHaveBeenCalledWith('mouseleave', expect.any(Function));
    });
  });

  describe('Focus Trapping', () => {
    it('should call trapFocus when opening sidebar', () => {
      const trapFocusSpy = vi.spyOn(InsightUI.utils, 'trapFocus');

      const container = createSidebarDOM();
      const wrapper = container.querySelector('[data-insight-sidebar]');

      const sidebar = new InsightUI.Sidebar(wrapper);
      sidebar.openSidebar();

      expect(trapFocusSpy).toHaveBeenCalledWith(wrapper);
    });
  });

  describe('destroy() method', () => {
    it('should remove close button handlers', () => {
      const container = createSidebarDOM();
      const wrapper = container.querySelector('[data-insight-sidebar]');
      const closeBtn = wrapper.querySelector('[data-insight-dismiss="sidebar"]');

      const sidebar = new InsightUI.Sidebar(wrapper);

      const removeSpy = vi.spyOn(closeBtn, 'removeEventListener');

      sidebar.destroy();

      expect(removeSpy).toHaveBeenCalledWith('click', expect.any(Function));
    });

    it('should remove mousemove listener when autoClose', () => {
      const container = createSidebarDOM({ autoClose: true });
      const wrapper = container.querySelector('[data-insight-sidebar]');

      const sidebar = new InsightUI.Sidebar(wrapper);

      const removeSpy = vi.spyOn(document, 'removeEventListener');

      sidebar.destroy();

      expect(removeSpy).toHaveBeenCalledWith('mousemove', expect.any(Function));
    });

    it('should remove instance from WeakMap', () => {
      const container = createSidebarDOM();
      const wrapper = container.querySelector('[data-insight-sidebar]');

      const sidebar = new InsightUI.Sidebar(wrapper);

      expect(InsightUI.Sidebar.instances.has(wrapper)).toBe(true);

      sidebar.destroy();

      expect(InsightUI.Sidebar.instances.has(wrapper)).toBe(false);
    });

    it('should nullify references', () => {
      const container = createSidebarDOM();
      const wrapper = container.querySelector('[data-insight-sidebar]');

      const sidebar = new InsightUI.Sidebar(wrapper);
      sidebar.destroy();

      expect(sidebar.wrapper).toBeNull();
      expect(sidebar.sidebar).toBeNull();
    });
  });

  describe('Singleton Pattern', () => {
    it('should return existing instance for same element', () => {
      const container = createSidebarDOM();
      const wrapper = container.querySelector('[data-insight-sidebar]');

      const sidebar1 = new InsightUI.Sidebar(wrapper);
      const sidebar2 = new InsightUI.Sidebar(wrapper);

      expect(sidebar1).toBe(sidebar2);
    });
  });
});
