// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Tests for Accordion component functionality
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

describe('Accordion Component', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
    loadComponent('insight-ui-accordion.js');
  });

  describe('Panel Toggle', () => {
    it('should open panel on button click', () => {
      const container = TestUtils.createAccordion();
      const element = container.querySelector('[data-insight-accordion]');
      const button = element.querySelector('button[aria-controls]');

      new InsightUI.Accordion(element);

      expect(button.getAttribute('aria-expanded')).toBe('false');

      TestUtils.click(button);

      expect(button.getAttribute('aria-expanded')).toBe('true');
    });

    it('should close panel on second button click', () => {
      const container = TestUtils.createAccordion();
      const element = container.querySelector('[data-insight-accordion]');
      const button = element.querySelector('button[aria-controls]');

      new InsightUI.Accordion(element);

      TestUtils.click(button); // open
      expect(button.getAttribute('aria-expanded')).toBe('true');

      TestUtils.click(button); // close
      expect(button.getAttribute('aria-expanded')).toBe('false');
    });

    it('should set panel opacity to 1 when opening', () => {
      const container = TestUtils.createAccordion();
      const element = container.querySelector('[data-insight-accordion]');
      const button = element.querySelector('button[aria-controls]');
      const panelId = button.getAttribute('aria-controls');
      const panel = document.getElementById(panelId);

      new InsightUI.Accordion(element);

      TestUtils.click(button);

      expect(panel.style.opacity).toBe('1');
    });

    it('should set panel opacity to 0 when closing', () => {
      const container = TestUtils.createAccordion();
      const element = container.querySelector('[data-insight-accordion]');
      const button = element.querySelector('button[aria-controls]');
      const panelId = button.getAttribute('aria-controls');
      const panel = document.getElementById(panelId);

      new InsightUI.Accordion(element);

      TestUtils.click(button); // open
      TestUtils.click(button); // close

      expect(panel.style.opacity).toBe('0');
    });
  });

  describe('Exclusive Mode', () => {
    it('should close other panels when opening one in exclusive mode', () => {
      const container = TestUtils.createAccordion('exc-accordion', true);
      const element = container.querySelector('[data-insight-accordion]');
      const buttons = element.querySelectorAll('button[aria-controls]');

      new InsightUI.Accordion(element);

      // Open first panel
      TestUtils.click(buttons[0]);
      expect(buttons[0].getAttribute('aria-expanded')).toBe('true');
      expect(buttons[1].getAttribute('aria-expanded')).toBe('false');

      // Open second panel - first should close
      TestUtils.click(buttons[1]);
      expect(buttons[0].getAttribute('aria-expanded')).toBe('false');
      expect(buttons[1].getAttribute('aria-expanded')).toBe('true');
    });

    it('should allow multiple panels open in non-exclusive mode', () => {
      const container = TestUtils.createAccordion('multi-accordion', false);
      const element = container.querySelector('[data-insight-accordion]');
      const buttons = element.querySelectorAll('button[aria-controls]');

      new InsightUI.Accordion(element);

      // Open first panel
      TestUtils.click(buttons[0]);
      expect(buttons[0].getAttribute('aria-expanded')).toBe('true');

      // Open second panel - first should remain open
      TestUtils.click(buttons[1]);
      expect(buttons[0].getAttribute('aria-expanded')).toBe('true');
      expect(buttons[1].getAttribute('aria-expanded')).toBe('true');
    });
  });

  describe('Keyboard Navigation', () => {
    it('should move focus to next button on ArrowDown', () => {
      const container = TestUtils.createAccordion();
      const element = container.querySelector('[data-insight-accordion]');
      const buttons = element.querySelectorAll('button[aria-controls]');

      new InsightUI.Accordion(element);

      buttons[0].focus();
      TestUtils.keydown(buttons[0], 'ArrowDown');

      expect(document.activeElement).toBe(buttons[1]);
    });

    it('should move focus to previous button on ArrowUp', () => {
      const container = TestUtils.createAccordion();
      const element = container.querySelector('[data-insight-accordion]');
      const buttons = element.querySelectorAll('button[aria-controls]');

      new InsightUI.Accordion(element);

      buttons[1].focus();
      TestUtils.keydown(buttons[1], 'ArrowUp');

      expect(document.activeElement).toBe(buttons[0]);
    });

    it('should wrap focus from last to first on ArrowDown', () => {
      const container = TestUtils.createAccordion();
      const element = container.querySelector('[data-insight-accordion]');
      const buttons = element.querySelectorAll('button[aria-controls]');

      new InsightUI.Accordion(element);

      buttons[1].focus(); // last button
      TestUtils.keydown(buttons[1], 'ArrowDown');

      expect(document.activeElement).toBe(buttons[0]); // first button
    });

    it('should wrap focus from first to last on ArrowUp', () => {
      const container = TestUtils.createAccordion();
      const element = container.querySelector('[data-insight-accordion]');
      const buttons = element.querySelectorAll('button[aria-controls]');

      new InsightUI.Accordion(element);

      buttons[0].focus(); // first button
      TestUtils.keydown(buttons[0], 'ArrowUp');

      expect(document.activeElement).toBe(buttons[1]); // last button
    });

    it('should move focus to first button on Home key', () => {
      const container = TestUtils.createAccordion();
      const element = container.querySelector('[data-insight-accordion]');
      const buttons = element.querySelectorAll('button[aria-controls]');

      new InsightUI.Accordion(element);

      buttons[1].focus();
      TestUtils.keydown(buttons[1], 'Home');

      expect(document.activeElement).toBe(buttons[0]);
    });

    it('should move focus to last button on End key', () => {
      const container = TestUtils.createAccordion();
      const element = container.querySelector('[data-insight-accordion]');
      const buttons = element.querySelectorAll('button[aria-controls]');

      new InsightUI.Accordion(element);

      buttons[0].focus();
      TestUtils.keydown(buttons[0], 'End');

      expect(document.activeElement).toBe(buttons[1]);
    });
  });

  describe('URL State Management', () => {
    it('should update URL when opening a panel', () => {
      const container = TestUtils.createAccordion();
      const element = container.querySelector('[data-insight-accordion]');
      const button = element.querySelector('button[aria-controls]');
      const panelId = button.getAttribute('aria-controls');

      const replaceStateSpy = vi.spyOn(window.history, 'replaceState');

      new InsightUI.Accordion(element);

      TestUtils.click(button);

      expect(replaceStateSpy).toHaveBeenCalled();
      const url = replaceStateSpy.mock.calls[0][2];
      expect(url.toString()).toContain(`open=${panelId}`);

      replaceStateSpy.mockRestore();
    });
  });

  describe('Initial State from URL', () => {
    it('should open panel specified in URL query param', () => {
      // Set up URL with open param using history API (safer than overwriting location)
      const originalHref = window.location.href;
      window.history.replaceState({}, '', '?open=url-panel-0');

      const container = TestUtils.createDOM(`
        <div data-insight-accordion="url-accordion">
          <div>
            <button aria-expanded="false" aria-controls="url-panel-0">Panel 1</button>
            <div id="url-panel-0" style="height: 0; opacity: 0;">Content 1</div>
          </div>
        </div>
      `);
      const element = container.querySelector('[data-insight-accordion]');
      const button = element.querySelector('button[aria-controls]');

      new InsightUI.Accordion(element);

      expect(button.getAttribute('aria-expanded')).toBe('true');

      // Restore URL
      window.history.replaceState({}, '', originalHref);
    });
  });
});
