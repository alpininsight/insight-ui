/**
 * Vitest setup file for Insight UI component tests
 */

import { vi, beforeEach, afterEach } from 'vitest';

// Mock debugLog function used by components
globalThis.debugLog = vi.fn();

// Initialize InsightUI namespace
globalThis.InsightUI = globalThis.InsightUI || {};
globalThis.window.InsightUI = globalThis.InsightUI;

/**
 * Test utilities for DOM manipulation and component testing
 */
globalThis.TestUtils = {
  /**
   * Creates a DOM element with the given HTML and appends to document.body
   * @param {string} html - HTML string to parse
   * @returns {HTMLElement} The created element
   */
  createDOM(html) {
    const container = document.createElement('div');
    container.innerHTML = html.trim();
    document.body.appendChild(container);
    return container;
  },

  /**
   * Removes all test containers from the DOM
   */
  cleanup() {
    document.body.innerHTML = '';
  },

  /**
   * Creates a dropdown component DOM structure
   * @param {string} id - Unique ID for the dropdown
   * @returns {HTMLElement} Container with dropdown elements
   */
  createDropdown(id = 'test-dropdown') {
    return this.createDOM(`
      <div class="relative">
        <button data-dropdown-toggle="${id}">Toggle</button>
        <div id="${id}" class="hidden">
          <a href="#">Item 1</a>
          <a href="#">Item 2</a>
        </div>
      </div>
    `);
  },

  /**
   * Creates an accordion component DOM structure
   * @param {string} id - Unique ID for the accordion
   * @param {boolean} exclusive - Whether only one panel can be open
   * @returns {HTMLElement} Container with accordion elements
   */
  createAccordion(id = 'test-accordion', exclusive = false) {
    return this.createDOM(`
      <div data-accordion="${id}" data-accordion-exclusive="${exclusive}">
        <div>
          <button aria-expanded="false" aria-controls="${id}-panel-0">Panel 1</button>
          <div id="${id}-panel-0" style="height: 0; opacity: 0;">Content 1</div>
        </div>
        <div>
          <button aria-expanded="false" aria-controls="${id}-panel-1">Panel 2</button>
          <div id="${id}-panel-1" style="height: 0; opacity: 0;">Content 2</div>
        </div>
      </div>
    `);
  },

  /**
   * Creates a carousel component DOM structure
   * @param {string} id - Unique ID for the carousel
   * @returns {HTMLElement} Container with carousel elements
   */
  createCarousel(id = 'test-carousel') {
    return this.createDOM(`
      <div class="carousel" data-autoplay="false">
        <div class="carousel-track">
          <div class="carousel-item">Slide 1</div>
          <div class="carousel-item">Slide 2</div>
          <div class="carousel-item">Slide 3</div>
        </div>
        <button class="carousel-prev">Prev</button>
        <button class="carousel-next">Next</button>
        <div class="carousel-dots"></div>
      </div>
    `);
  },

  /**
   * Creates an alert component DOM structure
   * @param {string} type - Alert type (info, success, warning, error)
   * @returns {HTMLElement} Container with alert elements
   */
  createAlert(type = 'info') {
    return this.createDOM(`
      <div role="alert" class="alert alert-${type}">
        <p>Test alert message</p>
        <button data-insight-dismiss="alert">Close</button>
      </div>
    `);
  },

  /**
   * Creates a modal component DOM structure
   * @param {string} id - Unique ID for the modal
   * @returns {HTMLElement} Container with modal elements
   */
  createModal(id = 'test-modal') {
    return this.createDOM(`
      <button data-insight-toggle="modal" data-insight-target="${id}">Open Modal</button>
      <div id="${id}" style="display: none;">
        <div class="modal-content">
          <button data-insight-dismiss="modal">Close</button>
          <p>Modal content</p>
        </div>
      </div>
    `);
  },

  /**
   * Simulates a click event on an element
   * @param {HTMLElement} element - Element to click
   */
  click(element) {
    element.dispatchEvent(new MouseEvent('click', { bubbles: true }));
  },

  /**
   * Simulates a keyboard event
   * @param {HTMLElement} element - Element to trigger event on
   * @param {string} key - Key name (e.g., 'ArrowDown', 'Enter')
   * @param {string} type - Event type ('keydown' or 'keyup')
   */
  keydown(element, key, type = 'keydown') {
    element.dispatchEvent(new KeyboardEvent(type, { key, bubbles: true }));
  },

  /**
   * Waits for the next animation frame
   * @returns {Promise} Resolves after requestAnimationFrame
   */
  nextFrame() {
    return new Promise(resolve => requestAnimationFrame(resolve));
  },

  /**
   * Waits for a specified number of milliseconds
   * @param {number} ms - Milliseconds to wait
   * @returns {Promise} Resolves after timeout
   */
  wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  },
};

// Cleanup after each test
beforeEach(() => {
  // Reset InsightUI namespace but preserve structure
  Object.keys(globalThis.InsightUI).forEach(key => {
    const component = globalThis.InsightUI[key];
    if (component && component.instances && component.instances instanceof WeakMap) {
      // WeakMaps can't be cleared, but the DOM cleanup will orphan the entries
    }
  });
});

afterEach(() => {
  TestUtils.cleanup();
  vi.clearAllMocks();
});
