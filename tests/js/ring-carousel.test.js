// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Tests for RingCarousel component functionality
 */

import { describe, it, expect, beforeEach } from 'vitest';
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

/** Returns the angle of an item on the ring in degrees. */
function angle(item) {
  return parseFloat(item.style.transform.match(/rotateY\(([-\d.]+)deg\)/)[1]);
}

/** Returns the items that are not inert. */
function frontItems(element) {
  return [...element.querySelectorAll('.ring-carousel-item')].filter(item => !item.inert);
}

function setup(itemCount = 4, options = {}) {
  const container = TestUtils.createRingCarousel('carousel', itemCount, options);
  const element = container.querySelector('[data-insight-ring-carousel]');
  const carousel = new InsightUI.RingCarousel(element);
  return { element, carousel, items: [...element.querySelectorAll('.ring-carousel-item')] };
}

function press(target, key) {
  const event = new KeyboardEvent('keydown', { key, bubbles: true, cancelable: true });
  target.dispatchEvent(event);
  return event;
}

function swipe(element, fromX, toX) {
  const stage = element.querySelector('.ring-carousel-stage');
  const start = new Event('touchstart');
  start.touches = [{ clientX: fromX }];
  stage.dispatchEvent(start);
  const end = new Event('touchend');
  end.changedTouches = [{ clientX: toX }];
  stage.dispatchEvent(end);
}

describe('RingCarousel Component', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
    globalThis.interpolate = (s, vars) => s.replace(/%\((\w+)\)s/g, (_, key) => vars[key]);
    loadComponent('insight-ui-ring-carousel.js');
  });

  describe('Initialization', () => {
    it('returns the existing instance for an element', () => {
      const { element, carousel } = setup();

      expect(new InsightUI.RingCarousel(element)).toBe(carousel);
      expect(element.__insightInstance).toBe(carousel);
    });

    it('initializes every carousel on the page', () => {
      const container = TestUtils.createRingCarousel('carousel', 3);

      InsightUI.RingCarousel.initAll();

      const element = container.querySelector('[data-insight-ring-carousel]');
      expect(InsightUI.RingCarousel.instances.has(element)).toBe(true);
    });

    it('shows the first item in front and only that one is reachable', () => {
      const { element, items } = setup();

      expect(frontItems(element)).toEqual([items[0]]);
      expect(angle(items[0])).toBe(0);
      expect(items[0].hasAttribute('data-current')).toBe(true);
    });

    it('announces the position', () => {
      const { element } = setup();

      expect(element.querySelector('[data-ring-carousel-status]').textContent).toBe('1 of 4');
    });
  });

  describe('Turning', () => {
    it('brings the next item to the front', () => {
      const { element, items } = setup();

      element.querySelector('.ring-carousel-next').click();

      expect(frontItems(element)).toEqual([items[1]]);
      expect(element.querySelector('[data-ring-carousel-status]').textContent).toBe('2 of 4');
    });

    it('brings the last item to the front before the first', () => {
      const { element, items } = setup();

      element.querySelector('.ring-carousel-prev').click();

      expect(frontItems(element)).toEqual([items[3]]);
    });

    it('keeps turning in one direction around a full ring', () => {
      const { element, items } = setup(4);
      const next = element.querySelector('.ring-carousel-next');

      for (let turn = 0; turn < 4; turn++) next.click();

      // The first item is in front again after a full turn; the second stands at -270 degrees, the
      // place of 90 degrees, instead of turning back by a full turn.
      expect(frontItems(element)).toEqual([items[0]]);
      expect(angle(items[1])).toBe(-270);
    });

    it('does nothing with a single item', () => {
      const { element, carousel, items } = setup(1);

      carousel.goTo(1);

      expect(frontItems(element)).toEqual([items[0]]);
    });
  });

  describe('Many items', () => {
    it('shows at most 12 items and keeps the others hidden at the back', () => {
      const { element, items } = setup(30);

      const visible = items.filter(item => item.style.visibility !== 'hidden');
      const hidden = items.filter(item => item.style.visibility === 'hidden');
      expect(visible).toHaveLength(12);
      expect(new Set(visible.map(item => ((angle(item) % 360) + 360) % 360)).size).toBe(12);
      expect(hidden.every(item => Math.abs(angle(item)) === 180)).toBe(true);
      expect(element.querySelector('[data-ring-carousel-status]').textContent).toBe('1 of 30');
    });

    it('shows a hidden item when it comes into view', () => {
      const { element, items } = setup(30);
      const next = element.querySelector('.ring-carousel-next');

      for (let turn = 0; turn < 10; turn++) next.click();

      expect(frontItems(element)).toEqual([items[10]]);
      expect(items[16].style.visibility).toBe('visible');
      expect(items[0].style.visibility).toBe('hidden');
    });
  });

  describe('Tilt', () => {
    it('tilts the items with the ring', () => {
      const { items } = setup(4, { tilt: 15 });

      expect(items[1].style.transform).toMatch(/rotateX\(15deg\)$/);
      expect(items[1].style.transform).not.toMatch(/rotateY\(.*rotateY/);
    });

    it('turns every item towards the camera with face_camera', () => {
      const { items } = setup(4, { tilt: 15, faceCamera: true });

      expect(items[1].style.transform).toMatch(/rotateY\(90deg\) translateZ\(.+\) rotateY\(-90deg\) rotateX\(15deg\)/);
    });
  });

  describe('Viewport changes', () => {
    it('updates the height cap when only viewport height changes with ResizeObserver present', () => {
      const callbacks = [];
      vi.stubGlobal('ResizeObserver', class {
        constructor(callback) { callbacks.push(callback); }
        observe() {}
        disconnect() {}
      });
      vi.useFakeTimers();
      const originalHeight = Object.getOwnPropertyDescriptor(window, 'innerHeight');
      Object.defineProperty(window, 'innerHeight', { configurable: true, writable: true, value: 1000 });
      let carousel;
      try {
        const container = TestUtils.createRingCarousel('height-only', 4);
        const element = container.querySelector('[data-insight-ring-carousel]');
        const stage = element.querySelector('.ring-carousel-stage');
        const items = [...element.querySelectorAll('.ring-carousel-item')];
        Object.defineProperty(stage, 'clientWidth', { configurable: true, value: 800 });
        items.forEach(item => Object.defineProperty(item, 'offsetHeight', { configurable: true, value: 900 }));
        carousel = new InsightUI.RingCarousel(element);
        callbacks[0]();
        expect(items[0].style.height).toBe('700px');

        window.innerHeight = 400;
        window.dispatchEvent(new Event('resize'));
        vi.advanceTimersToNextFrame();
        expect(stage.clientWidth).toBe(800);
        expect(items.every(item => item.style.height === '280px')).toBe(true);
      } finally {
        carousel?.destroy();
        Object.defineProperty(window, 'innerHeight', originalHeight);
        vi.useRealTimers();
        vi.unstubAllGlobals();
      }
    });
  });

  describe('Keyboard and touch', () => {
    it.each(['input', 'select', 'textarea', 'editable'])('leaves touch gestures on %s content to the control', (kind) => {
      const { element, items } = setup();
      const control = document.createElement(kind === 'editable' ? 'div' : kind);
      if (kind === 'input') control.type = 'range';
      if (kind === 'editable') control.setAttribute('contenteditable', 'true');
      items[0].querySelector('.ring-carousel-front').appendChild(control);
      const start = new Event('touchstart', { bubbles: true });
      start.touches = [{ clientX: 200, clientY: 0 }];
      control.dispatchEvent(start);
      const end = new Event('touchend', { bubbles: true });
      end.changedTouches = [{ clientX: 100, clientY: 0 }];
      control.dispatchEvent(end);
      expect(frontItems(element)).toEqual([items[0]]);
    });

    it('does not turn after a cancelled touch gesture', () => {
      const { element, items } = setup();
      const stage = element.querySelector('.ring-carousel-stage');
      const start = new Event('touchstart');
      start.touches = [{ clientX: 200, clientY: 0 }];
      stage.dispatchEvent(start);
      stage.dispatchEvent(new Event('touchcancel'));
      const end = new Event('touchend');
      end.changedTouches = [{ clientX: 100, clientY: 0 }];
      stage.dispatchEvent(end);
      expect(frontItems(element)).toEqual([items[0]]);
    });

    it('leaves a mostly vertical gesture to page scrolling', () => {
      const { element, items } = setup();
      const stage = element.querySelector('.ring-carousel-stage');
      const start = new Event('touchstart');
      start.touches = [{ clientX: 200, clientY: 0 }];
      stage.dispatchEvent(start);
      const end = new Event('touchend');
      end.changedTouches = [{ clientX: 100, clientY: 200 }];
      stage.dispatchEvent(end);
      expect(frontItems(element)).toEqual([items[0]]);
    });
    it('turns with the arrow keys on the controls', () => {
      const { element, items } = setup();

      press(element.querySelector('.ring-carousel-next'), 'ArrowRight');

      expect(frontItems(element)).toEqual([items[1]]);
    });

    it('swaps the arrow keys right to left', () => {
      const { element, items } = setup();
      element.style.direction = 'rtl';

      press(element.querySelector('.ring-carousel-next'), 'ArrowLeft');

      expect(frontItems(element)).toEqual([items[1]]);
    });

    it('jumps to the first and last item with Home and End', () => {
      const { element, items } = setup(6);
      const button = element.querySelector('.ring-carousel-next');

      press(button, 'End');
      expect(frontItems(element)).toEqual([items[5]]);

      press(button, 'Home');
      expect(frontItems(element)).toEqual([items[0]]);
    });

    it('leaves the keys inside an item to its content', () => {
      const { element, items } = setup();

      const event = press(items[0].querySelector('a'), 'ArrowRight');

      expect(event.defaultPrevented).toBe(false);
      expect(frontItems(element)).toEqual([items[0]]);
    });

    it('turns with a swipe', () => {
      const { element, items } = setup();

      swipe(element, 200, 100);

      expect(frontItems(element)).toEqual([items[1]]);
    });

    it('ignores a short swipe', () => {
      const { element, items } = setup();

      swipe(element, 200, 180);

      expect(frontItems(element)).toEqual([items[0]]);
    });
  });

  describe('destroy()', () => {
    it('removes the instance and stops reacting to the controls', () => {
      const { element, carousel, items } = setup();

      carousel.destroy();
      element.querySelector('.ring-carousel-next').click();

      expect(InsightUI.RingCarousel.instances.has(element)).toBe(false);
      expect(element.__insightInstance).toBeUndefined();
      expect(frontItems(element)).toEqual([items[0]]);
    });
  });
});
