// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Tests for Sidebar component functionality
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
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

/** A static sidebar with mobile_behavior="drawer": one element, a drawer below the lg breakpoint. */
function createMobileDrawerDOM(side = 'left') {
  const container = TestUtils.createDOM(`
    <button data-sidebar-toggle="${side}" aria-controls="${side}-sidebar"
            aria-expanded="false">Open ${side}</button>
    <div id="${side}-sidebar" data-insight-sidebar="${side}"
         data-static="true" data-mobile-behavior="drawer" class="max-lg:hidden">
      <div data-insight-dismiss="sidebar" class="backdrop"></div>
      <aside style="transition-property: transform; transition-duration: 150ms">
        <button data-insight-dismiss="sidebar">Close</button>
        <a href="#navigation">Navigation</a>
      </aside>
    </div>
  `);
  return {
    container,
    toggle: container.querySelector('[data-sidebar-toggle]'),
    mobile: container.querySelector('[data-insight-sidebar]'),
    aside: container.querySelector('[data-insight-sidebar] aside'),
    dismiss: container.querySelector('[data-insight-sidebar] button'),
    backdrop: container.querySelector('.backdrop'),
  };
}

/** True while the mobile drawer is closed; it hides itself only below the lg breakpoint. */
function isClosed(mobile) {
  return mobile.classList.contains('max-lg:hidden');
}

function transitionEnd(element, propertyName = 'transform', type = 'transitionend') {
  const event = new Event(type, { bubbles: true });
  Object.defineProperty(event, 'propertyName', { value: propertyName });
  element.dispatchEvent(event);
}

// Media queries the tests switch: the window width at the lg breakpoint and reduced motion.
const media = { desktop: false, reducedMotion: false, listeners: new Set() };

function setDesktop(desktop) {
  media.desktop = desktop;
  media.listeners.forEach(listener => listener());
}

describe('Sidebar Component', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
    loadComponent('insight-ui-utils.js');
    loadComponent('insight-ui-sidebar.js');
    media.desktop = false;
    media.reducedMotion = false;
    media.listeners.clear();
    window.matchMedia.mockImplementation(query => ({
      get matches() {
        if (query === InsightUI.Sidebar.DESKTOP_QUERY) return media.desktop;
        return query.includes('reduce') && media.reducedMotion;
      },
      media: query,
      addEventListener: (_type, listener) => media.listeners.add(listener),
      removeEventListener: (_type, listener) => media.listeners.delete(listener),
    }));
  });

  afterEach(() => {
    document.querySelectorAll('[data-insight-sidebar]').forEach(wrapper => {
      wrapper.__insightInstance?.destroy();
    });
    document.documentElement.dir = '';
    vi.useRealTimers();
    vi.restoreAllMocks();
  });

  describe('Mobile drawer lifecycle', () => {
    beforeEach(() => vi.useFakeTimers({
      toFake: ['setTimeout', 'clearTimeout', 'requestAnimationFrame', 'cancelAnimationFrame'],
    }));

    it.each(['left', 'right'])('binds one controller for the %s mobile drawer', side => {
      const { mobile, toggle, aside } = createMobileDrawerDOM(side);
      const toggleSpy = vi.spyOn(InsightUI.Sidebar.prototype, 'toggleMobileDrawer');
      const trapSpy = vi.spyOn(InsightUI.utils, 'trapFocus');
      InsightUI.Sidebar.initAll();
      InsightUI.Sidebar.initAll();
      toggle.click();
      vi.advanceTimersToNextFrame();
      transitionEnd(aside);

      expect(toggleSpy).toHaveBeenCalledTimes(1);
      expect(trapSpy).toHaveBeenCalledExactlyOnceWith(mobile);
      expect(isClosed(mobile)).toBe(false);
      expect(toggle.getAttribute('aria-expanded')).toBe('true');
      expect(mobile.__insightInstance.releaseFocusTrap).toBeTypeOf('function');
    });

    it.each(['dismiss', 'backdrop', 'escape', 'toggle'])('cleans up through %s on the owning instance', action => {
      const pair = createMobileDrawerDOM();
      InsightUI.Sidebar.initAll();
      pair.toggle.click();
      vi.advanceTimersToNextFrame();
      const owner = pair.mobile.__insightInstance;
      const release = vi.fn(owner.releaseFocusTrap);
      owner.releaseFocusTrap = release;
      const keydown = owner.boundKeyDown;
      const removeSpy = vi.spyOn(document, 'removeEventListener');
      if (action === 'escape') {
        TestUtils.keydown(document, 'Escape');
      } else {
        pair[action].click();
      }
      transitionEnd(pair.aside);

      expect(isClosed(pair.mobile)).toBe(true);
      expect(pair.toggle.getAttribute('aria-expanded')).toBe('false');
      expect(document.activeElement).toBe(pair.toggle);
      expect(release).toHaveBeenCalledTimes(1);
      expect(removeSpy).toHaveBeenCalledWith('keydown', keydown);
      expect(owner.releaseFocusTrap).toBeNull();
      expect(owner.boundKeyDown).toBeNull();
    });

    it('does not leak traps or listeners across repeated clicks and initialization', () => {
      const { mobile, toggle, aside } = createMobileDrawerDOM();
      InsightUI.Sidebar.initAll();
      const owner = mobile.__insightInstance;
      const trapSpy = vi.spyOn(InsightUI.utils, 'trapFocus');
      for (let i = 0; i < 3; i++) {
        InsightUI.Sidebar.initAll();
        toggle.click();
        owner.openSidebar();
        vi.advanceTimersToNextFrame();
        expect(isClosed(mobile)).toBe(false);
        toggle.click();
        owner.closeSidebar();
        transitionEnd(aside);
        expect(isClosed(mobile)).toBe(true);
        expect(owner.releaseFocusTrap).toBeNull();
      }
      expect(trapSpy).toHaveBeenCalledTimes(3);
      // jsdom schedules selectionchange at zero delay after focus restoration.
      vi.advanceTimersByTime(0);
      expect(vi.getTimerCount()).toBe(0);
    });

    it('cancels an opening frame when closed before it runs', () => {
      const { mobile, toggle, aside } = createMobileDrawerDOM();
      InsightUI.Sidebar.initAll();
      toggle.click();
      toggle.click();
      vi.runAllTimers();
      expect(isClosed(mobile)).toBe(true);
      expect(aside.style.transform).toBe('translateX(-100%)');
      expect(toggle.getAttribute('aria-expanded')).toBe('false');
      expect(mobile.__insightInstance.releaseFocusTrap).toBeNull();
    });

    it('cancels stale close callbacks when reopening during a transition', () => {
      const { mobile, toggle, aside } = createMobileDrawerDOM();
      InsightUI.Sidebar.initAll();
      toggle.click();
      vi.advanceTimersToNextFrame();
      toggle.click();
      toggle.click();
      vi.runAllTimers();
      transitionEnd(aside);
      expect(isClosed(mobile)).toBe(false);
      expect(aside.style.transform).toBe('translateX(0)');
      expect(toggle.getAttribute('aria-expanded')).toBe('true');
      expect(mobile.__insightInstance.releaseFocusTrap).toBeTypeOf('function');
    });

    it.each(['reduced motion', 'no transition', 'missing transitionend'])('closes without transitionend: %s', mode => {
      const { mobile, toggle, aside, dismiss } = createMobileDrawerDOM();
      if (mode === 'reduced motion') media.reducedMotion = true;
      if (mode === 'no transition') aside.style.transitionDuration = '0s';
      InsightUI.Sidebar.initAll();
      toggle.click();
      vi.advanceTimersToNextFrame();
      dismiss.click();
      if (mode === 'missing transitionend') vi.advanceTimersByTime(250);
      expect(isClosed(mobile)).toBe(true);
      expect(document.activeElement).toBe(toggle);
      expect(toggle.getAttribute('aria-expanded')).toBe('false');
      expect(mobile.__insightInstance.releaseFocusTrap).toBeNull();
      vi.advanceTimersByTime(0);
      expect(vi.getTimerCount()).toBe(0);
    });

    it('ignores descendant and non-transform transition events', () => {
      const { mobile, toggle, aside, dismiss } = createMobileDrawerDOM();
      InsightUI.Sidebar.initAll();
      toggle.click();
      vi.advanceTimersToNextFrame();
      dismiss.click();
      transitionEnd(dismiss);
      transitionEnd(aside, 'opacity');
      expect(isClosed(mobile)).toBe(false);
      transitionEnd(aside);
      expect(isClosed(mobile)).toBe(true);
    });

    it.each(['left', 'right'])('keeps RTL positioning for %s drawers', side => {
      document.documentElement.dir = 'rtl';
      const { toggle, aside, dismiss } = createMobileDrawerDOM(side);
      InsightUI.Sidebar.initAll();
      const offscreen = side === 'left' ? 'translateX(100%)' : 'translateX(-100%)';
      expect(aside.style.transform).toBe(offscreen);
      toggle.click();
      vi.advanceTimersToNextFrame();
      expect(aside.style.transform).toBe('translateX(0)');
      dismiss.click();
      vi.runAllTimers();
      expect(aside.style.transform).toBe(offscreen);
    });

    it.each(['opening', 'closing'])('destroys safely while %s and supports reinitialization', state => {
      const { mobile, toggle, aside } = createMobileDrawerDOM();
      InsightUI.Sidebar.initAll();
      toggle.click();
      if (state === 'closing') {
        vi.advanceTimersToNextFrame();
        toggle.click();
      }
      const owner = mobile.__insightInstance;
      const release = vi.fn(owner.releaseFocusTrap);
      owner.releaseFocusTrap = release;
      owner.destroy();
      owner.destroy();
      transitionEnd(aside);
      vi.runAllTimers();
      expect(release).toHaveBeenCalledTimes(1);
      expect(vi.getTimerCount()).toBe(0);
      expect(toggle.getAttribute('aria-expanded')).toBe('false');
      expect(mobile.__insightInstance).toBeUndefined();
      expect(InsightUI.Sidebar.instances.has(mobile)).toBe(false);
      InsightUI.Sidebar.initAll();
      toggle.click();
      vi.advanceTimersToNextFrame();
      expect(isClosed(mobile)).toBe(false);
      expect(aside.style.transform).toBe('translateX(0)');
    });

    it('handles a removed trigger without retaining focus resources', () => {
      const { mobile, toggle, dismiss } = createMobileDrawerDOM();
      InsightUI.Sidebar.initAll();
      toggle.click();
      vi.advanceTimersToNextFrame();
      toggle.remove();
      dismiss.click();
      vi.runAllTimers();
      expect(isClosed(mobile)).toBe(true);
      expect(mobile.__insightInstance.triggerElement).toBeNull();
      expect(mobile.__insightInstance.releaseFocusTrap).toBeNull();
    });

    it('keeps left and right pairs independent on the same page', () => {
      const left = createMobileDrawerDOM('left');
      const right = createMobileDrawerDOM('right');
      InsightUI.Sidebar.initAll();
      left.toggle.click();
      vi.advanceTimersToNextFrame();
      expect(isClosed(left.mobile)).toBe(false);
      expect(isClosed(right.mobile)).toBe(true);
      left.dismiss.click();
      vi.runAllTimers();
      right.toggle.click();
      vi.advanceTimersToNextFrame();
      expect(isClosed(left.mobile)).toBe(true);
      expect(left.toggle.getAttribute('aria-expanded')).toBe('false');
      expect(isClosed(right.mobile)).toBe(false);
      right.dismiss.click();
      vi.runAllTimers();
      expect(document.activeElement).toBe(right.toggle);
    });

    it('retains ordinary drawer open, Escape, ARIA and focus return without a mobile toggle', () => {
      const container = createSidebarDOM({ withOpenButton: true });
      const wrapper = container.querySelector('[data-insight-sidebar]');
      const opener = container.querySelector('.open-btn');
      InsightUI.Sidebar.initAll();
      opener.click();
      vi.advanceTimersToNextFrame();
      expect(opener.getAttribute('aria-expanded')).toBe('true');
      expect(wrapper.__insightInstance.releaseFocusTrap).toBeTypeOf('function');
      TestUtils.keydown(document, 'Escape');
      expect(wrapper.classList.contains('hidden')).toBe(true);
      expect(opener.classList.contains('hidden')).toBe(false);
      expect(opener.getAttribute('aria-expanded')).toBe('false');
      expect(document.activeElement).toBe(opener);
      expect(wrapper.__insightInstance.releaseFocusTrap).toBeNull();
    });

    it('does not bind an ordinary drawer opener to a same-side mobile drawer', () => {
      const pair = createMobileDrawerDOM();
      const ordinary = createSidebarDOM({ withOpenButton: true });
      InsightUI.Sidebar.initAll();
      const openSpy = vi.spyOn(pair.mobile.__insightInstance, 'openSidebar');
      ordinary.querySelector('.open-btn').click();
      vi.advanceTimersToNextFrame();
      expect(openSpy).not.toHaveBeenCalled();
      expect(isClosed(pair.mobile)).toBe(true);
      expect(pair.toggle.getAttribute('aria-expanded')).toBe('false');
    });

    it('preserves Tab and Shift+Tab trapping, then releases it on dismissal', () => {
      const { toggle, mobile, dismiss, aside } = createMobileDrawerDOM();
      InsightUI.Sidebar.initAll();
      toggle.click();
      const last = mobile.querySelector('a');
      expect(document.activeElement).toBe(dismiss);
      dismiss.dispatchEvent(new KeyboardEvent('keydown', { key: 'Tab', shiftKey: true, bubbles: true }));
      expect(document.activeElement).toBe(last);
      TestUtils.keydown(last, 'Tab');
      expect(document.activeElement).toBe(dismiss);
      vi.advanceTimersToNextFrame();
      dismiss.click();
      transitionEnd(aside);
      dismiss.focus();
      dismiss.dispatchEvent(new KeyboardEvent('keydown', { key: 'Tab', shiftKey: true, bubbles: true }));
      expect(document.activeElement).toBe(dismiss);
    });

    it('stays in the layout from the lg breakpoint', () => {
      setDesktop(true);
      const { mobile, aside } = createMobileDrawerDOM();
      InsightUI.Sidebar.initAll();

      expect(aside.style.transform).toBe('');
      expect(mobile.__insightInstance.releaseFocusTrap).toBeNull();
    });

    it('closes when the window grows to the lg breakpoint and hides again below it', () => {
      const { mobile, toggle, aside } = createMobileDrawerDOM();
      InsightUI.Sidebar.initAll();
      toggle.click();
      vi.advanceTimersToNextFrame();

      setDesktop(true);
      expect(isClosed(mobile)).toBe(true);
      expect(toggle.getAttribute('aria-expanded')).toBe('false');
      expect(mobile.__insightInstance.releaseFocusTrap).toBeNull();
      expect(mobile.__insightInstance.boundKeyDown).toBeNull();
      expect(aside.style.transform).toBe('');

      setDesktop(false);
      expect(aside.style.transform).toBe('translateX(-100%)');
      toggle.click();
      vi.advanceTimersToNextFrame();
      expect(isClosed(mobile)).toBe(false);
    });

    it('stops following the breakpoint when destroyed', () => {
      const { mobile } = createMobileDrawerDOM();
      InsightUI.Sidebar.initAll();
      expect(media.listeners.size).toBe(1);

      mobile.__insightInstance.destroy();
      expect(media.listeners.size).toBe(0);
    });

    it('waits for the transform delay and falls back after a cancelled transition', () => {
      const { mobile, toggle, aside, dismiss } = createMobileDrawerDOM();
      aside.style.transitionProperty = 'opacity, transform';
      aside.style.transitionDuration = '10s, 0.2s';
      aside.style.transitionDelay = '0s, 75ms';
      InsightUI.Sidebar.initAll();
      toggle.click();
      vi.advanceTimersToNextFrame();
      dismiss.click();
      transitionEnd(aside, 'transform', 'transitioncancel');
      vi.advanceTimersByTime(300);
      expect(isClosed(mobile)).toBe(false);
      vi.advanceTimersByTime(25);
      expect(isClosed(mobile)).toBe(true);
      expect(mobile.__insightInstance.boundKeyDown).toBeNull();
    });
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
