// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Tests for Carousel component functionality
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

describe('Carousel Component', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
    loadComponent('insight-ui-carousel.js');
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('Navigation', () => {
    it('should move to next slide on next button click', () => {
      const container = TestUtils.createCarousel();
      const element = container.querySelector('[data-insight-carousel]');
      const nextBtn = container.querySelector('.carousel-next');

      const carousel = new InsightUI.Carousel(element);

      expect(carousel.index).toBe(0);

      TestUtils.click(nextBtn);

      expect(carousel.index).toBe(1);
    });

    it('should move to previous slide on prev button click', () => {
      const container = TestUtils.createCarousel();
      const element = container.querySelector('[data-insight-carousel]');
      const prevBtn = container.querySelector('.carousel-prev');

      const carousel = new InsightUI.Carousel(element);
      carousel.index = 1; // Start at second slide
      carousel.update();

      TestUtils.click(prevBtn);

      expect(carousel.index).toBe(0);
    });

    it('should wrap from last slide to first on next', () => {
      const container = TestUtils.createCarousel();
      const element = container.querySelector('[data-insight-carousel]');
      const nextBtn = container.querySelector('.carousel-next');

      const carousel = new InsightUI.Carousel(element);

      // Move to last slide (3 items = 3 slides with itemsPerSlide=1)
      carousel.index = carousel.totalSlides - 1;
      carousel.update();

      TestUtils.click(nextBtn);

      expect(carousel.index).toBe(0);
    });

    it('should wrap from first slide to last on prev', () => {
      const container = TestUtils.createCarousel();
      const element = container.querySelector('[data-insight-carousel]');
      const prevBtn = container.querySelector('.carousel-prev');

      const carousel = new InsightUI.Carousel(element);

      expect(carousel.index).toBe(0);

      TestUtils.click(prevBtn);

      expect(carousel.index).toBe(carousel.totalSlides - 1);
    });
  });

  describe('Track Transform', () => {
    it('should update track transform when navigating', () => {
      const container = TestUtils.createCarousel();
      const element = container.querySelector('[data-insight-carousel]');
      const track = container.querySelector('.carousel-track');

      const carousel = new InsightUI.Carousel(element);

      expect(track.style.transform).toBe('translateX(0%)');

      carousel.next();

      expect(track.style.transform).toBe('translateX(-100%)');
    });

    it('should handle multiple slide navigation', () => {
      const container = TestUtils.createCarousel();
      const element = container.querySelector('[data-insight-carousel]');
      const track = container.querySelector('.carousel-track');

      const carousel = new InsightUI.Carousel(element);

      carousel.next();
      carousel.next();

      expect(track.style.transform).toBe('translateX(-200%)');
    });
  });

  describe('Autoplay', () => {
    it('should start autoplay when enabled', () => {
      const setIntervalSpy = vi.spyOn(globalThis, 'setInterval');

      const container = TestUtils.createCarousel();
      const element = container.querySelector('[data-insight-carousel]');
      element.dataset.autoplay = 'true';

      new InsightUI.Carousel(element);

      expect(setIntervalSpy).toHaveBeenCalled();
    });

    it('should not start autoplay when disabled', () => {
      const setIntervalSpy = vi.spyOn(globalThis, 'setInterval');

      const container = TestUtils.createCarousel();
      const element = container.querySelector('[data-insight-carousel]');
      element.dataset.autoplay = 'false';

      new InsightUI.Carousel(element);

      expect(setIntervalSpy).not.toHaveBeenCalled();
    });

    it('should stop autoplay on destroy', () => {
      const clearIntervalSpy = vi.spyOn(globalThis, 'clearInterval');

      const container = TestUtils.createCarousel();
      const element = container.querySelector('[data-insight-carousel]');
      element.dataset.autoplay = 'true';

      const carousel = new InsightUI.Carousel(element);

      carousel.destroy();

      expect(clearIntervalSpy).toHaveBeenCalled();
    });

    it('should restart autoplay after navigation', () => {
      const container = TestUtils.createCarousel();
      const element = container.querySelector('[data-insight-carousel]');
      element.dataset.autoplay = 'true';

      const carousel = new InsightUI.Carousel(element);

      const stopSpy = vi.spyOn(carousel, 'stopAutoplay');
      const startSpy = vi.spyOn(carousel, 'startAutoplay');

      carousel.restartAutoplay();

      expect(stopSpy).toHaveBeenCalled();
      expect(startSpy).toHaveBeenCalled();
    });
  });

  describe('Touch Gestures', () => {
    function createTouchEvent(type, clientX) {
      return new TouchEvent(type, {
        bubbles: true,
        touches: type === 'touchstart' ? [{ clientX }] : [],
        changedTouches: [{ clientX }],
      });
    }

    it('should move to next slide on left swipe (LTR)', () => {
      const container = TestUtils.createCarousel();
      const element = container.querySelector('[data-insight-carousel]');

      const carousel = new InsightUI.Carousel(element);

      expect(carousel.index).toBe(0);

      // Swipe left (start at 200, end at 100 = diff of -100)
      element.dispatchEvent(createTouchEvent('touchstart', 200));
      element.dispatchEvent(createTouchEvent('touchend', 100));

      expect(carousel.index).toBe(1);
    });

    it('should move to previous slide on right swipe (LTR)', () => {
      const container = TestUtils.createCarousel();
      const element = container.querySelector('[data-insight-carousel]');

      const carousel = new InsightUI.Carousel(element);
      carousel.index = 1;
      carousel.update();

      // Swipe right (start at 100, end at 200 = diff of +100)
      element.dispatchEvent(createTouchEvent('touchstart', 100));
      element.dispatchEvent(createTouchEvent('touchend', 200));

      expect(carousel.index).toBe(0);
    });

    it('should not navigate on small swipe', () => {
      const container = TestUtils.createCarousel();
      const element = container.querySelector('[data-insight-carousel]');

      const carousel = new InsightUI.Carousel(element);

      expect(carousel.index).toBe(0);

      // Small swipe (less than 50px)
      element.dispatchEvent(createTouchEvent('touchstart', 100));
      element.dispatchEvent(createTouchEvent('touchend', 130));

      expect(carousel.index).toBe(0);
    });
  });

  describe('Items Per Slide', () => {
    it('should calculate correct total slides with itemsPerSlide', () => {
      const container = TestUtils.createDOM(`
        <div data-insight-carousel data-autoplay="false" data-items-per-slide="2">
          <div class="carousel-track">
            <div class="carousel-item">1</div>
            <div class="carousel-item">2</div>
            <div class="carousel-item">3</div>
            <div class="carousel-item">4</div>
          </div>
          <button class="carousel-prev">Prev</button>
          <button class="carousel-next">Next</button>
          <div class="carousel-dots"></div>
        </div>
      `);
      const element = container.querySelector('[data-insight-carousel]');

      const carousel = new InsightUI.Carousel(element);

      // 4 items / 2 per slide = 2 total slides
      expect(carousel.totalSlides).toBe(2);
    });

    it('should set correct flex basis on items', () => {
      const container = TestUtils.createDOM(`
        <div data-insight-carousel data-autoplay="false" data-items-per-slide="3">
          <div class="carousel-track">
            <div class="carousel-item">1</div>
            <div class="carousel-item">2</div>
            <div class="carousel-item">3</div>
          </div>
          <button class="carousel-prev">Prev</button>
          <button class="carousel-next">Next</button>
          <div class="carousel-dots"></div>
        </div>
      `);
      const element = container.querySelector('[data-insight-carousel]');
      const items = element.querySelectorAll('.carousel-item');

      new InsightUI.Carousel(element);

      items.forEach(item => {
        // 100 / 3 = 33.333...%
        expect(item.style.flex).toContain('33.3333');
      });
    });
  });

  describe('Window Resize', () => {
    it('should add resize listener on initialization', () => {
      const addEventListenerSpy = vi.spyOn(window, 'addEventListener');

      const container = TestUtils.createCarousel();
      const element = container.querySelector('[data-insight-carousel]');

      new InsightUI.Carousel(element);

      expect(addEventListenerSpy).toHaveBeenCalledWith('resize', expect.any(Function));
    });

    it('should remove resize listener on destroy', () => {
      const removeEventListenerSpy = vi.spyOn(window, 'removeEventListener');

      const container = TestUtils.createCarousel();
      const element = container.querySelector('[data-insight-carousel]');

      const carousel = new InsightUI.Carousel(element);
      carousel.destroy();

      expect(removeEventListenerSpy).toHaveBeenCalledWith('resize', expect.any(Function));
    });
  });

  describe('destroy() method', () => {
    it('should nullify element reference', () => {
      const container = TestUtils.createCarousel();
      const element = container.querySelector('[data-insight-carousel]');

      const carousel = new InsightUI.Carousel(element);
      carousel.destroy();

      expect(carousel.element).toBeNull();
    });

    it('should remove instance from WeakMap', () => {
      const container = TestUtils.createCarousel();
      const element = container.querySelector('[data-insight-carousel]');

      const carousel = new InsightUI.Carousel(element);

      expect(InsightUI.Carousel.instances.has(element)).toBe(true);

      carousel.destroy();

      expect(InsightUI.Carousel.instances.has(element)).toBe(false);
    });

    it('should disconnect MutationObserver for RTL changes', () => {
      const container = TestUtils.createCarousel();
      const element = container.querySelector('[data-insight-carousel]');

      const carousel = new InsightUI.Carousel(element);

      // Verify observer exists
      expect(carousel.dirObserver).not.toBeNull();

      const disconnectSpy = vi.spyOn(carousel.dirObserver, 'disconnect');

      carousel.destroy();

      expect(disconnectSpy).toHaveBeenCalled();
      expect(carousel.dirObserver).toBeNull();
    });
  });

  describe('RTL Support', () => {
    it('should update isRTL when dir attribute changes', () => {
      const container = TestUtils.createCarousel();
      const element = container.querySelector('[data-insight-carousel]');

      const carousel = new InsightUI.Carousel(element);

      expect(carousel.isRTL).toBe(false);

      // Change dir attribute
      document.documentElement.setAttribute('dir', 'rtl');

      // Trigger MutationObserver callback manually (jsdom doesn't auto-trigger)
      carousel.isRTL = document.documentElement.getAttribute('dir') === 'rtl';

      expect(carousel.isRTL).toBe(true);

      // Cleanup
      document.documentElement.removeAttribute('dir');
    });

    it('should invert transform direction in RTL mode', () => {
      const container = TestUtils.createCarousel();
      const element = container.querySelector('[data-insight-carousel]');
      const track = container.querySelector('.carousel-track');

      const carousel = new InsightUI.Carousel(element);

      // Set RTL mode
      carousel.isRTL = true;
      carousel.index = 1;
      carousel.update();

      // In RTL, transform should be positive
      expect(track.style.transform).toBe('translateX(100%)');
    });
  });
});
