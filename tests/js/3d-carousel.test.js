// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Tests for ThreeDCarousel component functionality
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
  return [...element.querySelectorAll('.three-d-carousel-item')].filter(item => !item.inert);
}

function setup(itemCount = 4, options = {}) {
  const container = TestUtils.create3DCarousel('carousel', itemCount, options);
  const element = container.querySelector('[data-insight-3D-carousel]');
  const carousel = new InsightUI.ThreeDCarousel(element);
  return { element, carousel, items: [...element.querySelectorAll('.three-d-carousel-item')] };
}

function press(target, key) {
  const event = new KeyboardEvent('keydown', { key, bubbles: true, cancelable: true });
  target.dispatchEvent(event);
  return event;
}

function swipe(element, fromX, toX) {
  const stage = element.querySelector('.three-d-carousel-stage');
  const start = new Event('touchstart');
  start.touches = [{ clientX: fromX }];
  stage.dispatchEvent(start);
  const end = new Event('touchend');
  end.changedTouches = [{ clientX: toX }];
  stage.dispatchEvent(end);
}

describe('ThreeDCarousel Component', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
    globalThis.interpolate = (s, vars) => s.replace(/%\((\w+)\)s/g, (_, key) => vars[key]);
    loadComponent('insight-ui-3D-carousel.js');
  });

  describe('Initialization', () => {
    it('returns the existing instance for an element', () => {
      const { element, carousel } = setup();

      expect(new InsightUI.ThreeDCarousel(element)).toBe(carousel);
      expect(element.__insightInstance).toBe(carousel);
    });

    it('initializes every carousel on the page', () => {
      const container = TestUtils.create3DCarousel('carousel', 3);

      InsightUI.ThreeDCarousel.initAll();

      const element = container.querySelector('[data-insight-3D-carousel]');
      expect(InsightUI.ThreeDCarousel.instances.has(element)).toBe(true);
    });

    it('shows the first item in front and only that one is reachable', () => {
      const { element, items } = setup();

      expect(frontItems(element)).toEqual([items[0]]);
      expect(angle(items[0])).toBe(0);
      expect(items[0].hasAttribute('data-current')).toBe(true);
    });

    it('announces the position', () => {
      const { element } = setup();

      expect(element.querySelector('.three-d-carousel-status').textContent).toBe('1 of 4');
    });
  });

  describe('Turning', () => {
    it('brings the next item to the front', () => {
      const { element, items } = setup();

      element.querySelector('.three-d-carousel-next').click();

      expect(frontItems(element)).toEqual([items[1]]);
      expect(element.querySelector('.three-d-carousel-status').textContent).toBe('2 of 4');
    });

    it('brings the last item to the front before the first', () => {
      const { element, items } = setup();

      element.querySelector('.three-d-carousel-prev').click();

      expect(frontItems(element)).toEqual([items[3]]);
    });

    it('keeps turning in one direction around a full ring', () => {
      const { element, items } = setup(4);
      const next = element.querySelector('.three-d-carousel-next');

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
      expect(element.querySelector('.three-d-carousel-status').textContent).toBe('1 of 30');
    });

    it('shows a hidden item when it comes into view', () => {
      const { element, items } = setup(30);
      const next = element.querySelector('.three-d-carousel-next');

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

  describe('Keyboard and touch', () => {
    it('turns with the arrow keys on the controls', () => {
      const { element, items } = setup();

      press(element.querySelector('.three-d-carousel-next'), 'ArrowRight');

      expect(frontItems(element)).toEqual([items[1]]);
    });

    it('swaps the arrow keys right to left', () => {
      const { element, items } = setup();
      element.style.direction = 'rtl';

      press(element.querySelector('.three-d-carousel-next'), 'ArrowLeft');

      expect(frontItems(element)).toEqual([items[1]]);
    });

    it('jumps to the first and last item with Home and End', () => {
      const { element, items } = setup(6);
      const button = element.querySelector('.three-d-carousel-next');

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
      element.querySelector('.three-d-carousel-next').click();

      expect(InsightUI.ThreeDCarousel.instances.has(element)).toBe(false);
      expect(element.__insightInstance).toBeUndefined();
      expect(frontItems(element)).toEqual([items[0]]);
    });
  });
});
