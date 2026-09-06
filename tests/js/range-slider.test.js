// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Tests for RangeSlider component functionality
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

function createSingleRangeSlider(options = {}) {
  const { value = 50, min = 0, max = 100, legendMode = 'static' } = options;

  return TestUtils.createDOM(`
    <div data-insight-range-slider data-legend-mode="${legendMode}">
      <input type="range" min="${min}" max="${max}" value="${value}">
      <div class="slider-legend">
        <span class="slider-legend-item">0</span>
        <span class="slider-legend-item">25</span>
        <span class="slider-legend-item">50</span>
        <span class="slider-legend-item">75</span>
        <span class="slider-legend-item">100</span>
      </div>
    </div>
  `);
}

function createDualRangeSlider(options = {}) {
  const { minValue = 25, maxValue = 75, min = 0, max = 100 } = options;

  return TestUtils.createDOM(`
    <div data-insight-range-slider>
      <input type="range" class="slider-input-min" min="${min}" max="${max}" value="${minValue}">
      <input type="range" class="slider-input-max" min="${min}" max="${max}" value="${maxValue}">
      <div class="slider-track"></div>
    </div>
  `);
}

describe('RangeSlider Component', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
    loadComponent('insight-ui-range-slider.js');
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('Singleton Pattern', () => {
    it('should have static instances WeakMap', () => {
      expect(InsightUI.RangeSlider.instances).toBeInstanceOf(WeakMap);
    });

    it('should return existing instance for same element', () => {
      const container = createSingleRangeSlider();
      const element = container.querySelector('[data-insight-range-slider]');

      const instance1 = new InsightUI.RangeSlider(element);
      const instance2 = new InsightUI.RangeSlider(element);

      expect(instance1).toBe(instance2);
    });
  });

  describe('Single Range Mode', () => {
    it('should detect single-range mode with one input', () => {
      const container = createSingleRangeSlider();
      const element = container.querySelector('[data-insight-range-slider]');

      const slider = new InsightUI.RangeSlider(element);

      expect(slider.isDualRange).toBe(false);
    });

    it('should set initial progress CSS variable', () => {
      const container = createSingleRangeSlider({ value: 50 });
      const element = container.querySelector('[data-insight-range-slider]');

      new InsightUI.RangeSlider(element);

      expect(element.style.getPropertyValue('--insight-control-range-progress')).toBe('50%');
    });

    it('should update progress on input change', () => {
      const container = createSingleRangeSlider({ value: 50 });
      const element = container.querySelector('[data-insight-range-slider]');
      const input = element.querySelector('input');

      new InsightUI.RangeSlider(element);

      input.value = '75';
      input.dispatchEvent(new Event('input', { bubbles: true }));

      expect(element.style.getPropertyValue('--insight-control-range-progress')).toBe('75%');
    });

    it('should update aria-valuenow on input change', () => {
      const container = createSingleRangeSlider({ value: 50 });
      const element = container.querySelector('[data-insight-range-slider]');
      const input = element.querySelector('input');

      new InsightUI.RangeSlider(element);

      input.value = '80';
      input.dispatchEvent(new Event('input', { bubbles: true }));

      expect(input.getAttribute('aria-valuenow')).toBe('80');
    });
  });

  describe('Dual Range Mode', () => {
    it('should detect dual-range mode with two inputs', () => {
      const container = createDualRangeSlider();
      const element = container.querySelector('[data-insight-range-slider]');

      const slider = new InsightUI.RangeSlider(element);

      expect(slider.isDualRange).toBe(true);
    });

    it('should set initial range CSS variables', () => {
      const container = createDualRangeSlider({ minValue: 25, maxValue: 75 });
      const element = container.querySelector('[data-insight-range-slider]');

      new InsightUI.RangeSlider(element);

      expect(element.style.getPropertyValue('--insight-control-range-min')).toBe('25%');
      expect(element.style.getPropertyValue('--insight-control-range-max')).toBe('75%');
    });

    it('should update track width on dual range', () => {
      const container = createDualRangeSlider({ minValue: 25, maxValue: 75 });
      const element = container.querySelector('[data-insight-range-slider]');
      const track = element.querySelector('.slider-track');

      new InsightUI.RangeSlider(element);

      expect(track.style.width).toBe('50%');
    });

    it('should prevent min from exceeding max', () => {
      const container = createDualRangeSlider({ minValue: 25, maxValue: 75 });
      const element = container.querySelector('[data-insight-range-slider]');
      const inputMin = element.querySelector('.slider-input-min');
      const inputMax = element.querySelector('.slider-input-max');

      new InsightUI.RangeSlider(element);

      // Try to set min higher than max
      inputMin.value = '80';
      inputMin.dispatchEvent(new Event('input', { bubbles: true }));

      // Should be clamped to max value
      expect(inputMin.value).toBe('75');
    });

    it('should prevent max from going below min', () => {
      const container = createDualRangeSlider({ minValue: 25, maxValue: 75 });
      const element = container.querySelector('[data-insight-range-slider]');
      const inputMin = element.querySelector('.slider-input-min');
      const inputMax = element.querySelector('.slider-input-max');

      new InsightUI.RangeSlider(element);

      // Try to set max lower than min
      inputMax.value = '20';
      inputMax.dispatchEvent(new Event('input', { bubbles: true }));

      // Should be clamped to min value
      expect(inputMax.value).toBe('25');
    });
  });

  describe('getValue() method', () => {
    it('should return single value for single range', () => {
      const container = createSingleRangeSlider({ value: 60 });
      const element = container.querySelector('[data-insight-range-slider]');

      const slider = new InsightUI.RangeSlider(element);

      expect(slider.getValue()).toBe(60);
    });

    it('should return object with min/max for dual range', () => {
      const container = createDualRangeSlider({ minValue: 30, maxValue: 70 });
      const element = container.querySelector('[data-insight-range-slider]');

      const slider = new InsightUI.RangeSlider(element);

      expect(slider.getValue()).toEqual({ min: 30, max: 70 });
    });
  });

  describe('setValue() method', () => {
    it('should set single value', () => {
      const container = createSingleRangeSlider({ value: 50 });
      const element = container.querySelector('[data-insight-range-slider]');
      const input = element.querySelector('input');

      const slider = new InsightUI.RangeSlider(element);

      slider.setValue(80);

      expect(input.value).toBe('80');
      expect(element.style.getPropertyValue('--insight-control-range-progress')).toBe('80%');
    });

    it('should set dual range values', () => {
      const container = createDualRangeSlider({ minValue: 25, maxValue: 75 });
      const element = container.querySelector('[data-insight-range-slider]');
      const inputMin = element.querySelector('.slider-input-min');
      const inputMax = element.querySelector('.slider-input-max');

      const slider = new InsightUI.RangeSlider(element);

      slider.setValue({ min: 10, max: 90 });

      expect(inputMin.value).toBe('10');
      expect(inputMax.value).toBe('90');
    });
  });

  describe('Legend Modes', () => {
    it('should not adjust legend in static mode', () => {
      const container = createSingleRangeSlider({ legendMode: 'static' });
      const element = container.querySelector('[data-insight-range-slider]');
      const legendItems = element.querySelectorAll('.slider-legend-item');

      new InsightUI.RangeSlider(element);

      // All items should remain visible
      legendItems.forEach(item => {
        expect(item.classList.contains('invisible')).toBe(false);
      });
    });

    it('should register resize listener for non-static mode', () => {
      const addSpy = vi.spyOn(window, 'addEventListener');

      const container = createSingleRangeSlider({ legendMode: 'skip' });
      const element = container.querySelector('[data-insight-range-slider]');

      new InsightUI.RangeSlider(element);

      expect(addSpy).toHaveBeenCalledWith('resize', expect.any(Function));
    });

    it('should not register resize listener for static mode', () => {
      const addSpy = vi.spyOn(window, 'addEventListener');

      const container = createSingleRangeSlider({ legendMode: 'static' });
      const element = container.querySelector('[data-insight-range-slider]');

      new InsightUI.RangeSlider(element);

      const resizeCalls = addSpy.mock.calls.filter(call => call[0] === 'resize');
      expect(resizeCalls.length).toBe(0);
    });
  });

  describe('RTL Detection', () => {
    it('should detect RTL from document', () => {
      document.documentElement.dir = 'rtl';

      const container = createSingleRangeSlider();
      const element = container.querySelector('[data-insight-range-slider]');

      const slider = new InsightUI.RangeSlider(element);

      expect(slider.isRTL).toBe(true);

      document.documentElement.dir = '';
    });

    it('should detect LTR by default', () => {
      const container = createSingleRangeSlider();
      const element = container.querySelector('[data-insight-range-slider]');

      const slider = new InsightUI.RangeSlider(element);

      expect(slider.isRTL).toBe(false);
    });
  });

  describe('destroy() method', () => {
    it('should remove input listener for single range', () => {
      const container = createSingleRangeSlider();
      const element = container.querySelector('[data-insight-range-slider]');
      const input = element.querySelector('input');

      const slider = new InsightUI.RangeSlider(element);

      const removeSpy = vi.spyOn(input, 'removeEventListener');

      slider.destroy();

      expect(removeSpy).toHaveBeenCalledWith('input', expect.any(Function));
    });

    it('should remove input listeners for dual range', () => {
      const container = createDualRangeSlider();
      const element = container.querySelector('[data-insight-range-slider]');
      const inputMin = element.querySelector('.slider-input-min');
      const inputMax = element.querySelector('.slider-input-max');

      const slider = new InsightUI.RangeSlider(element);

      const removeMinSpy = vi.spyOn(inputMin, 'removeEventListener');
      const removeMaxSpy = vi.spyOn(inputMax, 'removeEventListener');

      slider.destroy();

      expect(removeMinSpy).toHaveBeenCalledWith('input', expect.any(Function));
      expect(removeMaxSpy).toHaveBeenCalledWith('input', expect.any(Function));
    });

    it('should remove resize listener', () => {
      const removeSpy = vi.spyOn(window, 'removeEventListener');

      const container = createSingleRangeSlider({ legendMode: 'skip' });
      const element = container.querySelector('[data-insight-range-slider]');

      const slider = new InsightUI.RangeSlider(element);
      slider.destroy();

      expect(removeSpy).toHaveBeenCalledWith('resize', expect.any(Function));
    });

    it('should disconnect MutationObserver', () => {
      const container = createSingleRangeSlider();
      const element = container.querySelector('[data-insight-range-slider]');

      const slider = new InsightUI.RangeSlider(element);

      const disconnectSpy = vi.spyOn(slider.dirObserver, 'disconnect');

      slider.destroy();

      expect(disconnectSpy).toHaveBeenCalled();
      expect(slider.dirObserver).toBeNull();
    });

    it('should remove instance from WeakMap', () => {
      const container = createSingleRangeSlider();
      const element = container.querySelector('[data-insight-range-slider]');

      const slider = new InsightUI.RangeSlider(element);

      expect(InsightUI.RangeSlider.instances.has(element)).toBe(true);

      slider.destroy();

      expect(InsightUI.RangeSlider.instances.has(element)).toBe(false);
    });

    it('should nullify element reference', () => {
      const container = createSingleRangeSlider();
      const element = container.querySelector('[data-insight-range-slider]');

      const slider = new InsightUI.RangeSlider(element);
      slider.destroy();

      expect(slider.element).toBeNull();
    });
  });

  describe('initAll() static method', () => {
    it('should initialize all range sliders in DOM', () => {
      createSingleRangeSlider();
      createDualRangeSlider();

      InsightUI.RangeSlider.initAll();

      const sliders = document.querySelectorAll('[data-insight-range-slider]');
      sliders.forEach(el => {
        expect(InsightUI.RangeSlider.instances.has(el)).toBe(true);
      });
    });
  });
});
