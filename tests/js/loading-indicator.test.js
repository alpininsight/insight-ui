// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Tests for the global HTMX loading bar (inline script of htmx_loading_indicator.html).
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const templatePath = path.join(
  __dirname,
  '../../insight_ui/templates/insight_ui/components/htmx_loading_indicator.html'
);

function loadIndicatorScript() {
  // Parse the template as HTML instead of matching tags with a regular expression.
  const template = fs.readFileSync(templatePath, 'utf-8');
  const script = new DOMParser().parseFromString(template, 'text/html').querySelector('script').textContent;
  eval(script);
}

function fireRequest(type, elt) {
  document.body.dispatchEvent(new CustomEvent(type, { detail: { elt } }));
}

describe('Global loading indicator', () => {
  let indicator;
  let userButton;
  let pollingElement;

  beforeEach(() => {
    vi.useFakeTimers();
    document.body.innerHTML = `
      <div id="insight-global-loading-indicator"></div>
      <button id="user-button" hx-get="/save">Save</button>
      <div data-insight-global-indicator="false"><div id="polling" hx-get="/status"></div></div>
    `;
    indicator = document.getElementById('insight-global-loading-indicator');
    userButton = document.getElementById('user-button');
    pollingElement = document.getElementById('polling');
    loadIndicatorScript();
  });

  afterEach(() => {
    vi.useRealTimers();
    document.body.innerHTML = '';
  });

  it('should show the bar for a request after the delay', () => {
    fireRequest('htmx:beforeRequest', userButton);
    vi.advanceTimersByTime(200);

    expect(indicator.classList.contains('visible')).toBe(true);
  });

  it('should ignore requests from elements inside an opted-out container', () => {
    fireRequest('htmx:beforeRequest', pollingElement);
    vi.advanceTimersByTime(200);

    expect(indicator.classList.contains('visible')).toBe(false);
  });

  it('should keep the bar of a user request when an ignored request finishes', () => {
    fireRequest('htmx:beforeRequest', userButton);
    vi.advanceTimersByTime(200);

    fireRequest('htmx:afterRequest', pollingElement);
    expect(indicator.classList.contains('visible')).toBe(true);

    fireRequest('htmx:afterRequest', userButton);
    expect(indicator.classList.contains('visible')).toBe(false);
  });
});
