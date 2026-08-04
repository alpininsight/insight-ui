/**
 * Tests for ThreeDCarousel component functionality
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

describe('ThreeDCarousel Component', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
    // Reset animate mock
    Element.prototype.animate = vi.fn(() => ({
      finished: Promise.resolve(),
      cancel: vi.fn(),
      pause: vi.fn(),
      play: vi.fn(),
    }));
    loadComponent('insight-ui-3D-carousel.js');
  });

  describe('Initialization', () => {
    it('should create a 3D carousel from element', () => {
      const container = TestUtils.create3DCarousel('carousel-1');
      const element = container.querySelector('[data-insight-3D-carousel]');

      const instance = new InsightUI.ThreeDCarousel(element);

      expect(instance.element).toBe(element);
      expect(instance.itemsCount).toBe(4);
    });

    it('should return existing instance for same element', () => {
      const container = TestUtils.create3DCarousel('carousel-singleton');
      const element = container.querySelector('[data-insight-3D-carousel]');

      const instance1 = new InsightUI.ThreeDCarousel(element);
      const instance2 = new InsightUI.ThreeDCarousel(element);

      expect(instance1).toBe(instance2);
    });

    it('should store instance reference on element', () => {
      const container = TestUtils.create3DCarousel('carousel-ref');
      const element = container.querySelector('[data-insight-3D-carousel]');

      const instance = new InsightUI.ThreeDCarousel(element);

      expect(element.__insightInstance).toBe(instance);
    });

    it('should calculate correct angle based on item count', () => {
      const container = TestUtils.create3DCarousel('carousel-angle', 6);
      const element = container.querySelector('[data-insight-3D-carousel]');

      const instance = new InsightUI.ThreeDCarousel(element);

      expect(instance.angle).toBe(60); // 360 / 6
    });

    it('should read velocity from data attribute', () => {
      const container = TestUtils.create3DCarousel('carousel-velocity', 4, false, 500);
      const element = container.querySelector('[data-insight-3D-carousel]');

      const instance = new InsightUI.ThreeDCarousel(element);

      expect(instance.spinSettings.duration).toBe(500);
    });

    it('should use default velocity when not specified', () => {
      const container = TestUtils.createDOM(`
        <div id="carousel-default-vel" data-insight-3D-carousel>
          <div class="carousel-track">
            <div class="carousel-item"><div>Item 1</div></div>
            <div class="carousel-item"><div>Item 2</div></div>
          </div>
          <div class="carousel-controls">
            <button>Prev</button>
            <button>Next</button>
          </div>
        </div>
      `);
      const element = container.querySelector('[data-insight-3D-carousel]');

      const instance = new InsightUI.ThreeDCarousel(element);

      expect(instance.spinSettings.duration).toBe(1000);
    });

    it('should read face-camera setting', () => {
      const container = TestUtils.create3DCarousel('carousel-face', 4, true);
      const element = container.querySelector('[data-insight-3D-carousel]');

      const instance = new InsightUI.ThreeDCarousel(element);

      expect(instance.faceCamera).toBe(true);
    });
  });

  describe('Navigation', () => {
    it('should increment currentIndex on previous button click', () => {
      const container = TestUtils.create3DCarousel('carousel-prev');
      const element = container.querySelector('[data-insight-3D-carousel]');

      const instance = new InsightUI.ThreeDCarousel(element);
      expect(instance.currentIndex).toBe(0);

      TestUtils.click(instance.previousBtn);

      expect(instance.currentIndex).toBe(1);
    });

    it('should decrement currentIndex on next button click', () => {
      const container = TestUtils.create3DCarousel('carousel-next');
      const element = container.querySelector('[data-insight-3D-carousel]');

      const instance = new InsightUI.ThreeDCarousel(element);
      expect(instance.currentIndex).toBe(0);

      TestUtils.click(instance.nextBtn);

      expect(instance.currentIndex).toBe(-1);
    });

    it('should call animate on carousel when navigating', () => {
      const container = TestUtils.create3DCarousel('carousel-animate');
      const element = container.querySelector('[data-insight-3D-carousel]');

      const instance = new InsightUI.ThreeDCarousel(element);

      TestUtils.click(instance.nextBtn);

      expect(instance.carousel.animate).toHaveBeenCalled();
    });

    it('should animate with correct keyframes', () => {
      const container = TestUtils.create3DCarousel('carousel-keyframes', 4);
      const element = container.querySelector('[data-insight-3D-carousel]');

      const instance = new InsightUI.ThreeDCarousel(element);
      const animateSpy = vi.spyOn(instance.carousel, 'animate');

      TestUtils.click(instance.nextBtn);

      expect(animateSpy).toHaveBeenCalled();
      const keyframes = animateSpy.mock.calls[0][0];
      expect(keyframes).toHaveLength(2);
      expect(keyframes[0].transform).toContain('rotateY');
      expect(keyframes[1].transform).toContain('rotateY');
    });
  });

  describe('Face Camera Mode', () => {
    it('should animate items when face-camera is enabled', () => {
      const itemCount = 4;
      const container = TestUtils.create3DCarousel('carousel-face-animate', itemCount, true);
      const element = container.querySelector('[data-insight-3D-carousel]');

      new InsightUI.ThreeDCarousel(element);

      // Clear the global animate mock
      Element.prototype.animate.mockClear();

      TestUtils.click(element.querySelector('.carousel-next'));

      // With faceCamera=true: 1 carousel animate + itemCount item animates
      expect(Element.prototype.animate).toHaveBeenCalledTimes(1 + itemCount);
    });

    it('should not animate items when face-camera is disabled', () => {
      const container = TestUtils.create3DCarousel('carousel-no-face', 4, false);
      const element = container.querySelector('[data-insight-3D-carousel]');

      const instance = new InsightUI.ThreeDCarousel(element);

      // Clear the global animate mock
      Element.prototype.animate.mockClear();

      TestUtils.click(instance.nextBtn);

      // With faceCamera=false, only the carousel itself should animate (1 call)
      // With faceCamera=true, it would be 1 + itemCount calls
      expect(Element.prototype.animate).toHaveBeenCalledTimes(1);
    });
  });

  describe('Spin Animation', () => {
    it('should return keyframes array from spin method', () => {
      const container = TestUtils.create3DCarousel('carousel-spin');
      const element = container.querySelector('[data-insight-3D-carousel]');

      const instance = new InsightUI.ThreeDCarousel(element);
      const keyframes = instance.spin(1, true);

      expect(Array.isArray(keyframes)).toBe(true);
      expect(keyframes.length).toBe(2);
    });

    it('should adjust fromIndex based on spin direction (right)', () => {
      const container = TestUtils.create3DCarousel('carousel-spin-right');
      const element = container.querySelector('[data-insight-3D-carousel]');

      const instance = new InsightUI.ThreeDCarousel(element);
      const keyframes = instance.spin(2, true);

      // When spinning right, fromIndex = index + 1 = 3
      // angle = 360/4 = 90
      // fromIndex * angle = 3 * 90 = 270
      expect(keyframes[0].transform).toContain('270deg');
    });

    it('should adjust fromIndex based on spin direction (left)', () => {
      const container = TestUtils.create3DCarousel('carousel-spin-left');
      const element = container.querySelector('[data-insight-3D-carousel]');

      const instance = new InsightUI.ThreeDCarousel(element);
      const keyframes = instance.spin(2, false);

      // When spinning left, fromIndex = index - 1 = 1
      // angle = 360/4 = 90
      // fromIndex * angle = 1 * 90 = 90
      expect(keyframes[0].transform).toContain('90deg');
    });
  });

  describe('Responsive Distance', () => {
    it('should use different distances based on screen size', () => {
      // Mock matchMedia to return true for largest breakpoint
      window.matchMedia = vi.fn().mockImplementation((query) => ({
        matches: query === '(min-width: 1920px)',
        media: query,
        onchange: null,
        addListener: vi.fn(),
        removeListener: vi.fn(),
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
        dispatchEvent: vi.fn(),
      }));

      const container = TestUtils.create3DCarousel('carousel-responsive');
      const element = container.querySelector('[data-insight-3D-carousel]');

      const instance = new InsightUI.ThreeDCarousel(element);
      const keyframes = instance.spin(0, true);

      // At 1920px+, distance should be -550
      expect(keyframes[0].transform).toContain('-550px');
    });

    it('should use default distance when no breakpoint matches', () => {
      // Mock matchMedia to return false for all breakpoints
      window.matchMedia = vi.fn().mockImplementation((query) => ({
        matches: false,
        media: query,
        onchange: null,
        addListener: vi.fn(),
        removeListener: vi.fn(),
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
        dispatchEvent: vi.fn(),
      }));

      const container = TestUtils.create3DCarousel('carousel-default-dist');
      const element = container.querySelector('[data-insight-3D-carousel]');

      const instance = new InsightUI.ThreeDCarousel(element);
      const keyframes = instance.spin(0, true);

      // Default distance should be -850
      expect(keyframes[0].transform).toContain('-850px');
    });
  });

  describe('Destroy', () => {
    it('should remove event listeners on destroy', () => {
      const container = TestUtils.create3DCarousel('carousel-destroy');
      const element = container.querySelector('[data-insight-3D-carousel]');

      const instance = new InsightUI.ThreeDCarousel(element);
      const prevRemoveSpy = vi.spyOn(instance.previousBtn, 'removeEventListener');
      const nextRemoveSpy = vi.spyOn(instance.nextBtn, 'removeEventListener');

      instance.destroy();

      expect(prevRemoveSpy).toHaveBeenCalledWith('click', instance.boundGotoPrevious);
      expect(nextRemoveSpy).toHaveBeenCalledWith('click', instance.boundGotoNext);
    });

    it('should clear instance references on destroy', () => {
      const container = TestUtils.create3DCarousel('carousel-clear');
      const element = container.querySelector('[data-insight-3D-carousel]');

      const instance = new InsightUI.ThreeDCarousel(element);

      instance.destroy();

      expect(instance.element).toBeNull();
      expect(instance.carousel).toBeNull();
    });

    it('should remove instance from WeakMap on destroy', () => {
      const container = TestUtils.create3DCarousel('carousel-weakmap');
      const element = container.querySelector('[data-insight-3D-carousel]');

      const instance = new InsightUI.ThreeDCarousel(element);

      instance.destroy();

      expect(element.__insightInstance).toBeUndefined();
    });
  });

  describe('Static Methods', () => {
    it('should initialize all 3D carousels with initAll', () => {
      TestUtils.create3DCarousel('carousel-all-1');
      TestUtils.create3DCarousel('carousel-all-2');

      InsightUI.ThreeDCarousel.initAll();

      const c1 = document.getElementById('carousel-all-1');
      const c2 = document.getElementById('carousel-all-2');

      expect(c1.__insightInstance).toBeTruthy();
      expect(c2.__insightInstance).toBeTruthy();
    });
  });
});
