// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Tests for shared navigation state management.
 */

import { beforeAll, describe, expect, it } from 'vitest';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const stateScript = path.join(
  __dirname,
  '../../insight_ui/static/insight_ui/js/insight-ui-state.js'
);

beforeAll(() => {
  eval(fs.readFileSync(stateScript, 'utf-8'));
});

function renderNavigation() {
  return TestUtils.createDOM(`
    <nav data-insight-nav>
      <a href="/docs/">Documentation</a>
      <a href="/#capabilities">Capabilities</a>
      <a href="/#architecture">Architecture</a>
      <a href="https://example.com/">External</a>
    </nav>
  `);
}

function updateNavigation() {
  document.dispatchEvent(new Event('DOMContentLoaded'));
}

function getStyleRules(rules) {
  return Array.from(rules).flatMap(rule => [
    ...(rule.selectorText ? [rule] : []),
    ...(rule.cssRules ? getStyleRules(rule.cssRules) : []),
  ]);
}

describe('Navigation state', () => {
  it('marks only the matching fragment as the current location', () => {
    window.history.replaceState({}, '', '/#architecture');
    const navigation = renderNavigation();

    updateNavigation();

    expect(
      navigation.querySelector('a[href="/#architecture"]').getAttribute('aria-current')
    ).toBe('location');
    expect(
      navigation.querySelector('a[href="/#capabilities"]').getAttribute('aria-current')
    ).toBeNull();
  });

  it('keeps path matches as the current page', () => {
    window.history.replaceState({}, '', '/docs/integration/');
    const navigation = renderNavigation();

    updateNavigation();

    expect(navigation.querySelector('a[href="/docs/"]').getAttribute('aria-current')).toBe(
      'page'
    );
  });

  it('does not mark an external link with the same path as active', () => {
    window.history.replaceState({}, '', '/');
    const navigation = renderNavigation();

    updateNavigation();

    expect(
      navigation
        .querySelector('a[href="https://example.com/"]')
        .getAttribute('aria-current')
    ).toBeNull();
  });

  it('updates fragment navigation without a page reload', () => {
    window.history.replaceState({}, '', '/#capabilities');
    const navigation = renderNavigation();
    updateNavigation();

    window.history.replaceState({}, '', '/#architecture');
    window.dispatchEvent(new HashChangeEvent('hashchange'));

    expect(
      navigation.querySelector('a[href="/#capabilities"]').getAttribute('aria-current')
    ).toBeNull();
    expect(
      navigation.querySelector('a[href="/#architecture"]').getAttribute('aria-current')
    ).toBe('location');
  });

  it.each([
    ['usage', '%75sage', 'usage'],
    ['%75sage', 'usage', 'usage'],
    ['%C3%BCberblick', '%c3%bcberblick', '\u00fcberblick'],
  ])('matches equivalent fragments #%s and #%s', (current, href, target) => {
    window.history.replaceState({}, '', `/docs/#${current}`);
    const navigation = TestUtils.createDOM(`
      <nav data-insight-nav>
        <button data-insight-dropdown="fragment-menu">Sections</button>
        <div id="fragment-menu"><a href="/docs/#${href}">Section</a></div>
      </nav>
      <aside data-insight-side-nav><a href="/docs/#${href}">Section</a></aside>
      <section id="${target}"></section>
    `);

    updateNavigation();

    navigation.querySelectorAll('a[href]').forEach(link => {
      expect(link.getAttribute('aria-current')).toBe('location');
    });
    expect(navigation.querySelector('button').getAttribute('aria-current')).toBe('true');
  });

  it.each(['Usage', '%2575sage'])('does not equate #usage with #%s', fragment => {
    window.history.replaceState({}, '', '/#usage');
    const navigation = TestUtils.createDOM(`
      <nav data-insight-nav><a href="/#${fragment}">Other target</a></nav>
      <section id="usage"></section>
    `);

    updateNavigation();

    expect(navigation.querySelector('a').getAttribute('aria-current')).toBeNull();
  });

  it.each(['id', 'name'])('preserves a literal encoded %s target', attribute => {
    window.history.replaceState({}, '', '/docs/#usage');
    const navigation = TestUtils.createDOM(`
      <nav data-insight-nav><a href="/docs/#%75sage">Literal target</a></nav>
      <a ${attribute}="%75sage"></a>
      <section id="usage"></section>
    `);

    updateNavigation();

    expect(navigation.querySelector('a[href]').getAttribute('aria-current')).toBeNull();
  });

  it.each(['%', '%E0%A4%A'])('tolerates malformed fragment encoding %s', fragment => {
    window.history.replaceState({}, '', '/docs/#usage');
    const navigation = TestUtils.createDOM(`
      <nav data-insight-nav>
        <a href="/docs/#${fragment}">Malformed</a>
        <a href="/docs/#usage">Usage</a>
      </nav>
    `);

    updateNavigation();

    expect(navigation.querySelector('a').getAttribute('aria-current')).toBeNull();
    expect(navigation.querySelector('a[href="/docs/#usage"]').getAttribute('aria-current')).toBe(
      'location'
    );
  });

  it.each([
    'insight_ui/utils/input.css',
    'insight_ui/static/insight_ui/css/tailwind.css',
  ])('keeps fragment active styles in %s', stylesheet => {
    window.history.replaceState({}, '', '/#architecture');
    const navigation = TestUtils.createDOM(`
      <nav data-insight-nav>
        <a class="insight-nav-link" href="/#architecture">Architecture</a>
        <button class="insight-nav-link" data-insight-dropdown="fragment-menu">Sections</button>
        <div id="fragment-menu">
          <a class="insight-nav-dropdown-item" href="/#architecture">Architecture</a>
        </div>
      </nav>
      <aside data-insight-side-nav>
        <a class="insight-sidebar-link" href="/#architecture">Architecture</a>
      </aside>
    `);
    const sheet = new CSSStyleSheet();
    sheet.replaceSync(fs.readFileSync(path.join(__dirname, '../..', stylesheet), 'utf-8'));
    const rules = getStyleRules(sheet.cssRules);

    updateNavigation();

    for (const className of ['insight-nav-link', 'insight-nav-dropdown-item', 'insight-sidebar-link']) {
      const rule = rules.find(rule =>
        rule.selectorText.split(',').some(selector => selector.trim() === `.${className}[aria-current="page"]`)
      );
      expect(rule).toBeDefined();
      const link = navigation.querySelector(`a.${className}`);
      expect(link.getAttribute('aria-current')).toBe('location');
      expect(link.matches(rule.selectorText)).toBe(true);
      link.setAttribute('aria-current', 'page');
      expect(link.matches(rule.selectorText)).toBe(true);
      link.removeAttribute('aria-current');
      expect(link.matches(rule.selectorText)).toBe(false);

      if (className === 'insight-nav-link') {
        expect(navigation.querySelector('button').matches(rule.selectorText)).toBe(true);
      }
      if (className === 'insight-sidebar-link' && stylesheet.endsWith('/tailwind.css')) {
        const style = document.createElement('style');
        style.textContent = rule.cssText;
        navigation.append(style);
        link.setAttribute('aria-current', 'location');
        expect(getComputedStyle(link).borderInlineStartWidth).toBe('4px');
      }
    }
  });
});
