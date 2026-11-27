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

// htmx passes the same request object as detail to all events of one request.
function request(elt, target = elt) {
  return { elt, target };
}

function fire(type, detail) {
  document.body.dispatchEvent(new CustomEvent(type, { detail }));
}

describe('Global loading indicator', () => {
  let indicator;
  let status;
  let userButton;
  let results;
  let pollingElement;

  beforeEach(() => {
    vi.useFakeTimers();
    // A fresh <body> per test drops the listeners of the previously loaded script.
    document.documentElement.replaceChild(document.createElement('body'), document.body);
    document.body.innerHTML = `
      <div id="insight-global-loading-indicator" aria-hidden="true"></div>
      <div id="insight-global-loading-status" role="status" aria-live="polite" data-message="Loading..."></div>
      <button id="user-button" hx-get="/save">Save</button>
      <div id="results"></div>
      <div data-insight-global-indicator="false"><div id="polling" hx-get="/status"></div></div>
    `;
    indicator = document.getElementById('insight-global-loading-indicator');
    status = document.getElementById('insight-global-loading-status');
    userButton = document.getElementById('user-button');
    results = document.getElementById('results');
    pollingElement = document.getElementById('polling');
    loadIndicatorScript();
  });

  afterEach(() => {
    vi.useRealTimers();
    document.body.innerHTML = '';
  });

  it('should show the bar for a request after the delay', () => {
    fire('htmx:beforeSend', request(userButton));
    vi.advanceTimersByTime(200);

    expect(indicator.classList.contains('visible')).toBe(true);
  });

  it('should ignore requests from elements inside an opted-out container', () => {
    const polling = request(pollingElement);
    fire('htmx:beforeSend', polling);
    vi.advanceTimersByTime(1500);

    expect(indicator.classList.contains('visible')).toBe(false);
    expect(status.textContent).toBe('');
    expect(pollingElement.hasAttribute('aria-busy')).toBe(false);
  });

  it('should keep the bar of a user request when an ignored request finishes', () => {
    const save = request(userButton);
    const polling = request(pollingElement);
    fire('htmx:beforeSend', save);
    fire('htmx:beforeSend', polling);
    vi.advanceTimersByTime(200);

    fire('htmx:afterRequest', polling);
    expect(indicator.classList.contains('visible')).toBe(true);

    fire('htmx:afterRequest', save);
    expect(indicator.classList.contains('visible')).toBe(false);
  });

  it('should keep the bar until the last of parallel requests finishes', () => {
    const first = request(userButton, results);
    const second = request(userButton);
    fire('htmx:beforeSend', first);
    fire('htmx:beforeSend', second);
    vi.advanceTimersByTime(200);

    fire('htmx:afterRequest', first);
    expect(indicator.classList.contains('visible')).toBe(true);

    fire('htmx:afterRequest', second);
    expect(indicator.classList.contains('visible')).toBe(false);
  });

  it('should count a request only once when afterRequest fires twice', () => {
    const replaced = request(userButton);
    const other = request(userButton, results);
    fire('htmx:beforeSend', replaced);
    fire('htmx:beforeSend', other);
    vi.advanceTimersByTime(200);

    // htmx fires afterRequest again on a parent when the element replaced itself.
    fire('htmx:afterRequest', replaced);
    fire('htmx:afterRequest', replaced);

    expect(indicator.classList.contains('visible')).toBe(true);
  });

  it('should mark the request target busy while the request runs', () => {
    const load = request(userButton, results);
    fire('htmx:beforeSend', load);
    expect(results.getAttribute('aria-busy')).toBe('true');

    fire('htmx:afterRequest', load);
    expect(results.hasAttribute('aria-busy')).toBe(false);
  });

  it('should restore an aria-busy value the target already had', () => {
    results.setAttribute('aria-busy', 'false');
    const load = request(userButton, results);
    fire('htmx:beforeSend', load);
    fire('htmx:afterRequest', load);

    expect(results.getAttribute('aria-busy')).toBe('false');
  });

  it('should keep the target busy until all its requests finish', () => {
    const first = request(userButton, results);
    const second = request(userButton, results);
    fire('htmx:beforeSend', first);
    fire('htmx:beforeSend', second);

    fire('htmx:afterRequest', first);
    expect(results.getAttribute('aria-busy')).toBe('true');

    fire('htmx:afterRequest', second);
    expect(results.hasAttribute('aria-busy')).toBe(false);
  });

  it('should stay silent for fast requests', () => {
    const save = request(userButton);
    fire('htmx:beforeSend', save);
    vi.advanceTimersByTime(500);
    fire('htmx:afterRequest', save);
    vi.advanceTimersByTime(1000);

    expect(status.textContent).toBe('');
  });

  it('should announce slow requests and clear the message afterwards', () => {
    const save = request(userButton);
    fire('htmx:beforeSend', save);
    vi.advanceTimersByTime(1000);
    expect(status.textContent).toBe('Loading...');

    fire('htmx:afterRequest', save);
    expect(status.textContent).toBe('');
  });
});
