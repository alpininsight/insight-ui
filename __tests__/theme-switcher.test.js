/**
 * Tests for ThemeSwitcher component functionality.
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
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

function createThemeSwitcherDOM() {
  return TestUtils.createDOM(`
    <link id="insight-ui-theme-stylesheet" href="/static/insight_ui/css/themes/default.css">
    <select data-insight-theme-switcher data-storage-key="test-theme">
      <option value="default" data-theme-href="/static/insight_ui/css/themes/default.css">Original</option>
      <option value="brite" data-theme-href="/static/insight_ui/css/themes/brite.css">Brite</option>
    </select>
  `);
}

describe('ThemeSwitcher Component', () => {
  let mockLocalStorage;

  beforeEach(() => {
    TestUtils.cleanup();
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;

    mockLocalStorage = {
      store: {},
      getItem: vi.fn((key) => mockLocalStorage.store[key] || null),
      setItem: vi.fn((key, value) => { mockLocalStorage.store[key] = value; }),
    };
    Object.defineProperty(globalThis, 'localStorage', { value: mockLocalStorage, writable: true });
    Object.defineProperty(globalThis, 'CSS', { value: { escape: (value) => String(value) }, writable: true });

    loadComponent('insight-ui-theme-switcher.js');
  });

  it('updates root and theme stylesheet when theme changes', () => {
    const container = createThemeSwitcherDOM();
    const selector = container.querySelector('[data-insight-theme-switcher]');

    const switcher = new InsightUI.ThemeSwitcher(selector);
    switcher.setTheme('brite');

    expect(document.documentElement.getAttribute('data-insight-design-theme')).toBe('brite');
    expect(document.getElementById('insight-ui-theme-stylesheet').getAttribute('href')).toBe('/static/insight_ui/css/themes/brite.css');
    expect(mockLocalStorage.setItem).toHaveBeenCalledWith('test-theme', 'brite');
  });

  it('ignores not-yet-ready iframe documents', () => {
    const container = createThemeSwitcherDOM();
    const selector = container.querySelector('[data-insight-theme-switcher]');
    const switcher = new InsightUI.ThemeSwitcher(selector);

    expect(() => switcher.applyThemeToIframe({ contentDocument: { documentElement: null } })).not.toThrow();
  });

  it('syncs ready iframe documents', () => {
    const container = createThemeSwitcherDOM();
    const selector = container.querySelector('[data-insight-theme-switcher]');
    const switcher = new InsightUI.ThemeSwitcher(selector);
    switcher.setTheme('brite');

    const frameDocument = document.implementation.createHTMLDocument('Demo');
    frameDocument.head.innerHTML = '<link id="insight-ui-theme-stylesheet" href="/static/insight_ui/css/themes/default.css">';

    switcher.applyThemeToIframe({ contentDocument: frameDocument });

    expect(frameDocument.documentElement.getAttribute('data-insight-design-theme')).toBe('brite');
    expect(frameDocument.getElementById('insight-ui-theme-stylesheet').getAttribute('href')).toBe('/static/insight_ui/css/themes/brite.css');
  });
});
