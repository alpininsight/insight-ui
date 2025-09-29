/**
 * Insight UI – HTMX Extensions
 */

(function () {
  'use strict';

  if (typeof htmx === 'undefined') {
    console.warn('HTMX not found; InsightUI extensions will not be initialized!');
    return;
  }

  // Ensure namespace
  window.InsightUI = window.InsightUI || {};

  // ----------------------------------------
  // HTMX Extension: Infinite Scroll
  // ----------------------------------------
  htmx.defineExtension('infinite-scroll', {
    onEvent: function (name, evt) {
      if (name !== 'htmx:afterRequest') return;
      const target = evt.detail.elt;
      if (!target.hasAttribute('hx-infinite-scroll')) return;

      const threshold = parseInt(target.getAttribute('data-threshold') || '100', 10);
      const scrollPosition = window.innerHeight + window.scrollY;
      const documentHeight = document.documentElement.offsetHeight;

      if (documentHeight - scrollPosition < threshold) {
        const nextUrl = target.getAttribute('data-next-url');
        if (nextUrl) {
          htmx.ajax('GET', nextUrl, { target: target, swap: 'beforeend' });
        }
      }
    }
  });

  // ----------------------------------------
  // HTMX Extension: Progressive Enhancement
  // ----------------------------------------
  htmx.defineExtension('progressive-enhancement', {
    onEvent: function (name, evt) {
      const el = evt.detail.elt;
      // Guard: ensure elt supports getAttribute
      if (!el || typeof el.getAttribute !== 'function') return;
      const loadingClass = el.getAttribute('data-loading-class') || 'htmx-loading';

      if (name === 'htmx:beforeRequest') {
        el.classList.add(loadingClass);
        const spinner = el.querySelector('.htmx-spinner');
        if (spinner) spinner.style.display = 'block';
      }

      if (name === 'htmx:afterRequest') {
        el.classList.remove(loadingClass);
        const spinner = el.querySelector('.htmx-spinner');
        if (spinner) spinner.style.display = 'none';
      }
    }
  });

  // ----------------------------------------
  // Auto-Init All Extensions
  // ----------------------------------------
  document.addEventListener('DOMContentLoaded', function () {
    htmx.config.extensions = ['infinite-scroll', 'progressive-enhancement', 'ws'];
  });
})();
