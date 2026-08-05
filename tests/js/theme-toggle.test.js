/**
 * Tests for ThemeToggle component functionality
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

function createThemeToggleDOM() {
  return TestUtils.createDOM(`
    <button data-insight-theme-toggle>Toggle Theme</button>
  `);
}

describe('ThemeToggle Component', () => {
  let originalLocalStorage;
  let mockLocalStorage;

  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;

    // Mock localStorage
    mockLocalStorage = {
      store: {},
      getItem: vi.fn((key) => mockLocalStorage.store[key] || null),
      setItem: vi.fn((key, value) => { mockLocalStorage.store[key] = value; }),
      removeItem: vi.fn((key) => { delete mockLocalStorage.store[key]; }),
      clear: vi.fn(() => { mockLocalStorage.store = {}; }),
    };
    originalLocalStorage = globalThis.localStorage;
    Object.defineProperty(globalThis, 'localStorage', { value: mockLocalStorage, writable: true });

    // Mock matchMedia
    globalThis.matchMedia = vi.fn().mockImplementation((query) => ({
      matches: false,
      media: query,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
    }));

    // Reset document state
    document.documentElement.classList.remove('dark');
    document.documentElement.removeAttribute('data-theme');

    loadComponent('insight-ui-theme-toggle.js');
  });

  afterEach(() => {
    Object.defineProperty(globalThis, 'localStorage', { value: originalLocalStorage, writable: true });
  });

  describe('Singleton Pattern', () => {
    it('should have static instances WeakMap', () => {
      expect(InsightUI.ThemeToggle.instances).toBeInstanceOf(WeakMap);
    });

    it('should return existing instance for same element', () => {
      const container = createThemeToggleDOM();
      const button = container.querySelector('[data-insight-theme-toggle]');

      const instance1 = new InsightUI.ThemeToggle(button);
      const instance2 = new InsightUI.ThemeToggle(button);

      expect(instance1).toBe(instance2);
    });
  });

  describe('Initial Theme Loading', () => {
    it('should load theme from localStorage if saved', () => {
      mockLocalStorage.store['insight-ui-theme'] = 'dark';

      const container = createThemeToggleDOM();
      const button = container.querySelector('[data-insight-theme-toggle]');

      new InsightUI.ThemeToggle(button);

      expect(document.documentElement.classList.contains('dark')).toBe(true);
      expect(document.documentElement.getAttribute('data-theme')).toBe('dark');
    });

    it('should use system preference if no saved theme', () => {
      globalThis.matchMedia = vi.fn().mockImplementation((query) => ({
        matches: query === '(prefers-color-scheme: dark)',
        media: query,
      }));

      const container = createThemeToggleDOM();
      const button = container.querySelector('[data-insight-theme-toggle]');

      new InsightUI.ThemeToggle(button);

      expect(document.documentElement.classList.contains('dark')).toBe(true);
    });

    it('should default to light if no preference and no saved theme', () => {
      globalThis.matchMedia = vi.fn().mockImplementation(() => ({
        matches: false,
      }));

      const container = createThemeToggleDOM();
      const button = container.querySelector('[data-insight-theme-toggle]');

      new InsightUI.ThemeToggle(button);

      expect(document.documentElement.classList.contains('dark')).toBe(false);
      expect(document.documentElement.getAttribute('data-theme')).toBe('light');
    });
  });

  describe('Theme Toggle', () => {
    it('should toggle from light to dark on click', () => {
      const container = createThemeToggleDOM();
      const button = container.querySelector('[data-insight-theme-toggle]');

      new InsightUI.ThemeToggle(button);

      // Start with light theme
      document.documentElement.classList.remove('dark');

      TestUtils.click(button);

      expect(document.documentElement.classList.contains('dark')).toBe(true);
      expect(document.documentElement.getAttribute('data-theme')).toBe('dark');
    });

    it('should toggle from dark to light on click', () => {
      mockLocalStorage.store['insight-ui-theme'] = 'dark';

      const container = createThemeToggleDOM();
      const button = container.querySelector('[data-insight-theme-toggle]');

      new InsightUI.ThemeToggle(button);

      expect(document.documentElement.classList.contains('dark')).toBe(true);

      TestUtils.click(button);

      expect(document.documentElement.classList.contains('dark')).toBe(false);
      expect(document.documentElement.getAttribute('data-theme')).toBe('light');
    });
  });

  describe('Persistence', () => {
    it('should save theme to localStorage', () => {
      const container = createThemeToggleDOM();
      const button = container.querySelector('[data-insight-theme-toggle]');

      const toggle = new InsightUI.ThemeToggle(button);

      toggle.setTheme('dark');

      expect(mockLocalStorage.setItem).toHaveBeenCalledWith('insight-ui-theme', 'dark');
    });

    it('should save theme to cookie', () => {
      const container = createThemeToggleDOM();
      const button = container.querySelector('[data-insight-theme-toggle]');

      const toggle = new InsightUI.ThemeToggle(button);

      toggle.setTheme('dark');

      expect(document.cookie).toContain('theme=dark');
    });
  });

  describe('setTheme() method', () => {
    it('should add dark class for dark theme', () => {
      const container = createThemeToggleDOM();
      const button = container.querySelector('[data-insight-theme-toggle]');

      const toggle = new InsightUI.ThemeToggle(button);

      toggle.setTheme('dark');

      expect(document.documentElement.classList.contains('dark')).toBe(true);
    });

    it('should remove dark class for light theme', () => {
      const container = createThemeToggleDOM();
      const button = container.querySelector('[data-insight-theme-toggle]');

      const toggle = new InsightUI.ThemeToggle(button);

      toggle.setTheme('dark');
      toggle.setTheme('light');

      expect(document.documentElement.classList.contains('dark')).toBe(false);
    });

    it('should set data-theme attribute', () => {
      const container = createThemeToggleDOM();
      const button = container.querySelector('[data-insight-theme-toggle]');

      const toggle = new InsightUI.ThemeToggle(button);

      toggle.setTheme('dark');
      expect(document.documentElement.getAttribute('data-theme')).toBe('dark');

      toggle.setTheme('light');
      expect(document.documentElement.getAttribute('data-theme')).toBe('light');
    });
  });

  describe('destroy() method', () => {
    it('should remove click listener', () => {
      const container = createThemeToggleDOM();
      const button = container.querySelector('[data-insight-theme-toggle]');

      const toggle = new InsightUI.ThemeToggle(button);

      // Set to light first
      toggle.setTheme('light');

      toggle.destroy();

      // Click should not toggle anymore
      TestUtils.click(button);

      expect(document.documentElement.classList.contains('dark')).toBe(false);
    });

    it('should remove instance from WeakMap', () => {
      const container = createThemeToggleDOM();
      const button = container.querySelector('[data-insight-theme-toggle]');

      const toggle = new InsightUI.ThemeToggle(button);

      expect(InsightUI.ThemeToggle.instances.has(button)).toBe(true);

      toggle.destroy();

      expect(InsightUI.ThemeToggle.instances.has(button)).toBe(false);
    });

    it('should nullify trigger reference', () => {
      const container = createThemeToggleDOM();
      const button = container.querySelector('[data-insight-theme-toggle]');

      const toggle = new InsightUI.ThemeToggle(button);
      toggle.destroy();

      expect(toggle.trigger).toBeNull();
    });
  });

  describe('initAll() static method', () => {
    it('should initialize all theme toggles in DOM', () => {
      createThemeToggleDOM();
      createThemeToggleDOM();

      InsightUI.ThemeToggle.initAll();

      const buttons = document.querySelectorAll('[data-insight-theme-toggle]');
      buttons.forEach(btn => {
        expect(InsightUI.ThemeToggle.instances.has(btn)).toBe(true);
      });
    });
  });
});
