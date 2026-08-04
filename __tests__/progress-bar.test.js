/**
 * Tests for ProgressBar component functionality
 */

import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const jsDir = path.join(__dirname, '../insight_ui/static/insight_ui/js');

function loadComponent(filename) {
  const filepath = path.join(jsDir, filename);
  const code = fs.readFileSync(filepath, 'utf-8');
  const transformed = code.replace(/export class\s+(\w+)/g, 'window.InsightUI.$1 = class $1');
  eval(transformed);
}

function createProgressBarDOM(options = {}) {
  const {
    tagId = 'test-progress',
    value = 0,
    label = '',
    maxValue = 100,
    minValue = 0,
    requestUrl = '',
    sseUrl = '',
    interval = 1000,
    hideOnComplete = false,
    stopOnError = false,
    cancelUrl = '',
    withButtons = false,
  } = options;

  const buttonsHTML = withButtons ? `
    <button data-progress-cancel>Cancel</button>
    <button data-progress-retry class="hidden">Retry</button>
  ` : '';

  return TestUtils.createDOM(`
    <div data-insight-progress-bar="${tagId}"
         data-request-url="${requestUrl}"
         data-sse-url="${sseUrl}"
         data-interval="${interval}"
         data-max-value="${maxValue}"
         data-min-value="${minValue}"
         data-hide-on-complete="${hideOnComplete}"
         data-stop-on-error="${stopOnError}"
         data-cancel-url="${cancelUrl}">
      <div data-progress-track role="progressbar" aria-valuenow="${value}" aria-valuemin="${minValue}" aria-valuemax="${maxValue}">
        <div data-progress-fill data-value="${value}" data-label="${label}" style="width: ${value}%"></div>
      </div>
      <span data-progress-value>${value}%</span>
      <span data-progress-label>${label}</span>
      <div data-progress-error class="hidden">
        <span data-error-icon-warning class="hidden">Warning</span>
        <span data-error-icon-error class="hidden">Error</span>
        <span data-error-message></span>
      </div>
      <div data-progress-announce aria-live="polite"></div>
      ${buttonsHTML}
    </div>
  `);
}

describe('ProgressBar Component', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
    loadComponent('insight-ui-progress-bar.js');
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.restoreAllMocks();
    // Clear registry
    if (InsightUI.ProgressBar) {
      InsightUI.ProgressBar.REGISTRY = {};
    }
  });

  describe('Singleton Pattern', () => {
    it('should have static instances WeakMap', () => {
      expect(InsightUI.ProgressBar.instances).toBeInstanceOf(WeakMap);
    });

    it('should return existing instance for same element', () => {
      const container = createProgressBarDOM();
      const element = container.querySelector('[data-insight-progress-bar]');

      const instance1 = new InsightUI.ProgressBar(element);
      const instance2 = new InsightUI.ProgressBar(element);

      expect(instance1).toBe(instance2);
    });

    it('should register instance in REGISTRY by tagId', () => {
      const container = createProgressBarDOM({ tagId: 'my-progress' });
      const element = container.querySelector('[data-insight-progress-bar]');

      new InsightUI.ProgressBar(element);

      expect(InsightUI.ProgressBar.REGISTRY['my-progress']).toBeDefined();
    });
  });

  describe('Initialization', () => {
    it('should parse configuration from data attributes', () => {
      const container = createProgressBarDOM({
        tagId: 'config-test',
        maxValue: 200,
        minValue: 10,
        interval: 2000,
      });
      const element = container.querySelector('[data-insight-progress-bar]');

      const progressBar = new InsightUI.ProgressBar(element);

      expect(progressBar.config.maxValue).toBe(200);
      expect(progressBar.config.minValue).toBe(10);
      expect(progressBar.config.interval).toBe(2000);
    });

    it('should use default values for missing config', () => {
      const container = createProgressBarDOM();
      const element = container.querySelector('[data-insight-progress-bar]');

      const progressBar = new InsightUI.ProgressBar(element);

      expect(progressBar.config.maxValue).toBe(100);
      expect(progressBar.config.minValue).toBe(0);
      expect(progressBar.config.interval).toBe(1000);
    });
  });

  describe('update() method', () => {
    it('should update fill width', () => {
      const container = createProgressBarDOM();
      const element = container.querySelector('[data-insight-progress-bar]');
      const fill = element.querySelector('[data-progress-fill]');

      const progressBar = new InsightUI.ProgressBar(element);

      progressBar.update(50);

      expect(fill.style.width).toBe('50%');
    });

    it('should update data-value attribute', () => {
      const container = createProgressBarDOM();
      const element = container.querySelector('[data-insight-progress-bar]');
      const fill = element.querySelector('[data-progress-fill]');

      const progressBar = new InsightUI.ProgressBar(element);

      progressBar.update(75);

      expect(fill.dataset.value).toBe('75');
    });

    it('should update label when provided', () => {
      const container = createProgressBarDOM();
      const element = container.querySelector('[data-insight-progress-bar]');
      const labelDisplay = element.querySelector('[data-progress-label]');

      const progressBar = new InsightUI.ProgressBar(element);

      progressBar.update(50, 'Uploading...');

      expect(labelDisplay.textContent).toBe('Uploading...');
    });

    it('should update ARIA attributes', () => {
      const container = createProgressBarDOM();
      const element = container.querySelector('[data-insight-progress-bar]');
      const track = element.querySelector('[data-progress-track]');

      const progressBar = new InsightUI.ProgressBar(element);

      progressBar.update(60, 'Processing');

      expect(track.getAttribute('aria-valuenow')).toBe('60');
      expect(track.getAttribute('aria-valuetext')).toContain('60%');
    });

    it('should clamp value to min/max range', () => {
      const container = createProgressBarDOM({ minValue: 0, maxValue: 100 });
      const element = container.querySelector('[data-insight-progress-bar]');
      const fill = element.querySelector('[data-progress-fill]');

      const progressBar = new InsightUI.ProgressBar(element);

      progressBar.update(150); // Above max
      expect(fill.dataset.value).toBe('100');

      progressBar.update(-20); // Below min
      expect(fill.dataset.value).toBe('0');
    });

    it('should dispatch progress-update event', () => {
      const container = createProgressBarDOM({ tagId: 'event-test' });
      const element = container.querySelector('[data-insight-progress-bar]');

      const progressBar = new InsightUI.ProgressBar(element);

      const handler = vi.fn();
      element.addEventListener('insight-ui:progress-update', handler);

      progressBar.update(50, 'Test');

      expect(handler).toHaveBeenCalled();
      expect(handler.mock.calls[0][0].detail).toEqual({
        tagId: 'event-test',
        value: 50,
        label: 'Test',
      });
    });

    it('should trigger onComplete when reaching max value', () => {
      const container = createProgressBarDOM();
      const element = container.querySelector('[data-insight-progress-bar]');

      const progressBar = new InsightUI.ProgressBar(element);

      const completeSpy = vi.spyOn(progressBar, 'onComplete');

      progressBar.update(100);

      expect(completeSpy).toHaveBeenCalled();
    });
  });

  describe('Error Handling', () => {
    it('should show error message', () => {
      const container = createProgressBarDOM();
      const element = container.querySelector('[data-insight-progress-bar]');
      const errorContainer = element.querySelector('[data-progress-error]');
      const errorMessage = element.querySelector('[data-error-message]');

      const progressBar = new InsightUI.ProgressBar(element);

      progressBar.setError('Upload failed', true);

      expect(errorContainer.classList.contains('hidden')).toBe(false);
      expect(errorMessage.textContent).toBe('Upload failed');
      expect(progressBar.hasError).toBe(true);
      expect(progressBar.isFatalError).toBe(true);
    });

    it('should show warning for non-fatal errors', () => {
      const container = createProgressBarDOM();
      const element = container.querySelector('[data-insight-progress-bar]');
      const warningIcon = element.querySelector('[data-error-icon-warning]');
      const errorIcon = element.querySelector('[data-error-icon-error]');

      const progressBar = new InsightUI.ProgressBar(element);

      progressBar.setError('Connection slow', false);

      expect(warningIcon.classList.contains('hidden')).toBe(false);
      expect(errorIcon.classList.contains('hidden')).toBe(true);
      expect(progressBar.isFatalError).toBe(false);
    });

    it('should clear error state', () => {
      const container = createProgressBarDOM();
      const element = container.querySelector('[data-insight-progress-bar]');
      const errorContainer = element.querySelector('[data-progress-error]');

      const progressBar = new InsightUI.ProgressBar(element);

      progressBar.setError('Error', true);
      expect(progressBar.hasError).toBe(true);

      progressBar.clearError();

      expect(errorContainer.classList.contains('hidden')).toBe(true);
      expect(progressBar.hasError).toBe(false);
      expect(progressBar.isFatalError).toBe(false);
    });

    it('should dispatch error event', () => {
      const container = createProgressBarDOM({ tagId: 'error-event' });
      const element = container.querySelector('[data-insight-progress-bar]');

      const progressBar = new InsightUI.ProgressBar(element);

      const handler = vi.fn();
      element.addEventListener('insight-ui:progress-error', handler);

      progressBar.setError('Test error', true);

      expect(handler).toHaveBeenCalled();
      expect(handler.mock.calls[0][0].detail).toEqual({
        tagId: 'error-event',
        error: 'Test error',
        isFatal: true,
      });
    });
  });

  describe('Cancel and Retry', () => {
    it('should cancel progress and show cancelled state', async () => {
      const container = createProgressBarDOM({ withButtons: true });
      const element = container.querySelector('[data-insight-progress-bar]');

      const progressBar = new InsightUI.ProgressBar(element);

      await progressBar.cancel();

      expect(progressBar.isCancelled).toBe(true);
      expect(progressBar.hasError).toBe(true);
    });

    it('should call onCancel callback when set', async () => {
      const container = createProgressBarDOM({ withButtons: true });
      const element = container.querySelector('[data-insight-progress-bar]');

      const progressBar = new InsightUI.ProgressBar(element);
      const callback = vi.fn();
      progressBar.onCancel = callback;

      await progressBar.cancel();

      expect(callback).toHaveBeenCalled();
    });

    it('should retry and clear cancelled state', () => {
      const container = createProgressBarDOM({ withButtons: true });
      const element = container.querySelector('[data-insight-progress-bar]');

      const progressBar = new InsightUI.ProgressBar(element);
      progressBar.isCancelled = true;
      progressBar.hasError = true;

      progressBar.retry();

      expect(progressBar.isCancelled).toBe(false);
      expect(progressBar.hasError).toBe(false);
    });

    it('should dispatch cancel event', async () => {
      const container = createProgressBarDOM({ tagId: 'cancel-test', withButtons: true });
      const element = container.querySelector('[data-insight-progress-bar]');

      const progressBar = new InsightUI.ProgressBar(element);

      const handler = vi.fn();
      element.addEventListener('insight-ui:progress-cancel', handler);

      await progressBar.cancel();

      expect(handler).toHaveBeenCalled();
    });
  });

  describe('Polling Mode', () => {
    it('should start polling when requestUrl is set', () => {
      const setIntervalSpy = vi.spyOn(globalThis, 'setInterval');

      const container = createProgressBarDOM({ requestUrl: '/api/progress' });
      const element = container.querySelector('[data-insight-progress-bar]');

      new InsightUI.ProgressBar(element);

      expect(setIntervalSpy).toHaveBeenCalled();
    });

    it('should not start polling when requestUrl is empty', () => {
      const setIntervalSpy = vi.spyOn(globalThis, 'setInterval');

      const container = createProgressBarDOM({ requestUrl: '' });
      const element = container.querySelector('[data-insight-progress-bar]');

      new InsightUI.ProgressBar(element);

      expect(setIntervalSpy).not.toHaveBeenCalled();
    });

    it('should stop polling on destroy', () => {
      const clearIntervalSpy = vi.spyOn(globalThis, 'clearInterval');

      const container = createProgressBarDOM({ requestUrl: '/api/progress' });
      const element = container.querySelector('[data-insight-progress-bar]');

      const progressBar = new InsightUI.ProgressBar(element);
      progressBar.destroy();

      expect(clearIntervalSpy).toHaveBeenCalled();
    });

    it('should not start polling when cancelled', () => {
      const setIntervalSpy = vi.spyOn(globalThis, 'setInterval');

      const container = createProgressBarDOM({ requestUrl: '/api/progress' });
      const element = container.querySelector('[data-insight-progress-bar]');

      const progressBar = new InsightUI.ProgressBar(element);

      // Clear the interval that was started
      progressBar.stopPolling();
      setIntervalSpy.mockClear();

      // Set cancelled and try to start
      progressBar.isCancelled = true;
      progressBar.startAutoUpdate();

      expect(setIntervalSpy).not.toHaveBeenCalled();
    });
  });

  describe('SSE Mode', () => {
    let MockEventSource;
    let mockEventSourceInstance;

    beforeEach(() => {
      mockEventSourceInstance = {
        onmessage: null,
        onerror: null,
        close: vi.fn(),
      };

      MockEventSource = vi.fn(function(url) {
        this.url = url;
        this.onmessage = null;
        this.onerror = null;
        this.close = mockEventSourceInstance.close;
        return this;
      });

      globalThis.EventSource = MockEventSource;
    });

    afterEach(() => {
      delete globalThis.EventSource;
    });

    it('should prefer SSE over polling when both are configured', () => {
      const setIntervalSpy = vi.spyOn(globalThis, 'setInterval');

      const container = createProgressBarDOM({
        requestUrl: '/api/progress',
        sseUrl: '/api/progress/sse',
      });
      const element = container.querySelector('[data-insight-progress-bar]');

      const progressBar = new InsightUI.ProgressBar(element);

      // SSE should be used, not polling
      expect(MockEventSource).toHaveBeenCalledWith('/api/progress/sse');
      expect(setIntervalSpy).not.toHaveBeenCalled();
      expect(progressBar.eventSource).not.toBeNull();
    });

    it('should close SSE connection on destroy', () => {
      const container = createProgressBarDOM({ sseUrl: '/api/progress/sse' });
      const element = container.querySelector('[data-insight-progress-bar]');

      const progressBar = new InsightUI.ProgressBar(element);
      progressBar.destroy();

      expect(mockEventSourceInstance.close).toHaveBeenCalled();
    });

    it('should not start if already running', () => {
      const container = createProgressBarDOM({ sseUrl: '/api/progress/sse' });
      const element = container.querySelector('[data-insight-progress-bar]');

      const progressBar = new InsightUI.ProgressBar(element);

      // Clear mock and try to start again
      MockEventSource.mockClear();
      progressBar.startAutoUpdate();

      // Should not create another EventSource
      expect(MockEventSource).not.toHaveBeenCalled();
    });
  });

  describe('Static Methods', () => {
    it('should get instance by tagId', () => {
      const container = createProgressBarDOM({ tagId: 'static-test' });
      const element = container.querySelector('[data-insight-progress-bar]');

      const progressBar = new InsightUI.ProgressBar(element);

      expect(InsightUI.ProgressBar.get('static-test')).toBe(progressBar);
    });

    it('should return null for non-existent tagId', () => {
      expect(InsightUI.ProgressBar.get('non-existent')).toBeNull();
    });

    it('should update progress via static method', () => {
      const container = createProgressBarDOM({ tagId: 'static-update' });
      const element = container.querySelector('[data-insight-progress-bar]');

      new InsightUI.ProgressBar(element);

      InsightUI.ProgressBar.update('static-update', 75, 'Processing');

      const fill = element.querySelector('[data-progress-fill]');
      expect(fill.dataset.value).toBe('75');
    });

    it('should set error via static method', () => {
      const container = createProgressBarDOM({ tagId: 'static-error' });
      const element = container.querySelector('[data-insight-progress-bar]');

      new InsightUI.ProgressBar(element);

      InsightUI.ProgressBar.setError('static-error', 'Failed', true);

      const instance = InsightUI.ProgressBar.get('static-error');
      expect(instance.hasError).toBe(true);
    });
  });

  describe('reset() method', () => {
    it('should reset to initial state', () => {
      const container = createProgressBarDOM();
      const element = container.querySelector('[data-insight-progress-bar]');
      const fill = element.querySelector('[data-progress-fill]');

      const progressBar = new InsightUI.ProgressBar(element);

      progressBar.update(75);
      progressBar.setError('Error', true);

      progressBar.reset();

      expect(fill.dataset.value).toBe('0');
      expect(progressBar.hasError).toBe(false);
      expect(progressBar.isCancelled).toBe(false);
    });

    it('should dispatch reset event', () => {
      const container = createProgressBarDOM({ tagId: 'reset-test' });
      const element = container.querySelector('[data-insight-progress-bar]');

      const progressBar = new InsightUI.ProgressBar(element);

      const handler = vi.fn();
      element.addEventListener('insight-ui:progress-reset', handler);

      progressBar.reset();

      expect(handler).toHaveBeenCalled();
    });
  });

  describe('destroy() method', () => {
    it('should remove instance from WeakMap', () => {
      const container = createProgressBarDOM();
      const element = container.querySelector('[data-insight-progress-bar]');

      const progressBar = new InsightUI.ProgressBar(element);

      expect(InsightUI.ProgressBar.instances.has(element)).toBe(true);

      progressBar.destroy();

      expect(InsightUI.ProgressBar.instances.has(element)).toBe(false);
    });

    it('should remove instance from REGISTRY', () => {
      const container = createProgressBarDOM({ tagId: 'destroy-test' });
      const element = container.querySelector('[data-insight-progress-bar]');

      new InsightUI.ProgressBar(element);

      expect(InsightUI.ProgressBar.REGISTRY['destroy-test']).toBeDefined();

      InsightUI.ProgressBar.get('destroy-test').destroy();

      expect(InsightUI.ProgressBar.REGISTRY['destroy-test']).toBeUndefined();
    });

    it('should disconnect MutationObserver', () => {
      const container = createProgressBarDOM();
      const element = container.querySelector('[data-insight-progress-bar]');

      const progressBar = new InsightUI.ProgressBar(element);

      const disconnectSpy = vi.spyOn(progressBar.observer, 'disconnect');

      progressBar.destroy();

      expect(disconnectSpy).toHaveBeenCalled();
    });

    it('should nullify element references', () => {
      const container = createProgressBarDOM();
      const element = container.querySelector('[data-insight-progress-bar]');

      const progressBar = new InsightUI.ProgressBar(element);
      progressBar.destroy();

      expect(progressBar.container).toBeNull();
      expect(progressBar.fill).toBeNull();
      expect(progressBar.track).toBeNull();
    });
  });

  describe('Accessibility', () => {
    it('should announce progress at intervals', () => {
      const container = createProgressBarDOM();
      const element = container.querySelector('[data-insight-progress-bar]');
      const announceElement = element.querySelector('[data-progress-announce]');

      const progressBar = new InsightUI.ProgressBar(element);

      // First update at 10%
      progressBar.update(10);
      expect(announceElement.textContent).toContain('10%');

      // Update at 15% - should not announce (not at threshold)
      progressBar.update(15);
      // Should still show 10% announcement

      // Update at 20% - should announce
      progressBar.update(20);
      expect(announceElement.textContent).toContain('20%');
    });

    it('should announce completion', () => {
      vi.useRealTimers(); // Need real timers for setTimeout in announce

      const container = createProgressBarDOM();
      const element = container.querySelector('[data-insight-progress-bar]');

      const progressBar = new InsightUI.ProgressBar(element);
      const announceSpy = vi.spyOn(progressBar, 'announce');

      progressBar.update(100);

      // Message is "Progress complete" (lowercase 'c')
      expect(announceSpy).toHaveBeenCalledWith(expect.stringContaining('complete'));
    });
  });
});
