/**
 * Vitest setup file for Insight UI component tests
 */

import { vi, beforeEach, afterEach } from 'vitest';

// Mock debugLog function used by components
globalThis.debugLog = vi.fn();

// Mock gettext for i18n (used by CodeBlock)
globalThis.gettext = vi.fn((text) => text);

// Mock Prism for syntax highlighting (used by CodeBlock)
globalThis.Prism = {
  highlightElement: vi.fn(),
};

// Mock navigator.clipboard (used by CodeBlock)
Object.defineProperty(navigator, 'clipboard', {
  value: {
    writeText: vi.fn().mockResolvedValue(undefined),
  },
  writable: true,
});

// Mock Element.animate (used by ThreeDCarousel)
Element.prototype.animate = vi.fn(() => ({
  finished: Promise.resolve(),
  cancel: vi.fn(),
  pause: vi.fn(),
  play: vi.fn(),
}));

// Mock window.matchMedia (used by ThreeDCarousel)
window.matchMedia = vi.fn().mockImplementation((query) => ({
  matches: false,
  media: query,
  onchange: null,
  addListener: vi.fn(),
  removeListener: vi.fn(),
  addEventListener: vi.fn(),
  removeEventListener: vi.fn(),
  dispatchEvent: vi.fn(),
}));

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
        <button data-insight-dropdown="${id}">Toggle</button>
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
      <div data-insight-accordion="${id}" data-exclusive="${exclusive}">
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
      <div data-insight-carousel data-autoplay="false">
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
      <button data-insight-modal="${id}">Open Modal</button>
      <div id="${id}" style="display: none;">
        <div class="modal-content">
          <button data-insight-dismiss="modal">Close</button>
          <p>Modal content</p>
        </div>
      </div>
    `);
  },

  /**
   * Creates a code block component DOM structure
   * Note: Code must have leading newline and indentation to match real HTML template usage,
   * as cleanIndentation() expects lines[1] to exist.
   * @param {string} id - Unique ID for the code block
   * @param {string} lang - Programming language
   * @param {string} code - Code content (will be wrapped with newlines and indentation)
   * @param {string} filename - Optional filename
   * @returns {HTMLElement} Container with code block element
   */
  createCodeBlock(id = 'test-code-block', lang = 'javascript', code = 'const x = 1;', filename = '') {
    const filenameAttr = filename ? `data-filename="${filename}"` : '';
    // Simulate real HTML template structure with leading newline and indentation
    const wrappedCode = `
        ${code}
    `;
    return this.createDOM(`
      <div id="${id}" data-insight-code-block="${lang}" ${filenameAttr}>${wrappedCode}</div>
    `);
  },

  /**
   * Creates a 3D carousel component DOM structure
   * @param {string} id - Unique ID for the carousel
   * @param {number} itemCount - Number of carousel items
   * @param {boolean} faceCamera - Whether items face the camera
   * @param {number} velocity - Animation duration in ms
   * @returns {HTMLElement} Container with 3D carousel elements
   */
  create3DCarousel(id = 'test-3d-carousel', itemCount = 4, faceCamera = false, velocity = 1000) {
    const items = Array.from({ length: itemCount }, (_, i) => `
      <div class="carousel-item" style="--position: ${i + 1}">
        <div class="item-content">Item ${i + 1}</div>
      </div>
    `).join('');

    return this.createDOM(`
      <div id="${id}" data-insight-3D-carousel data-face-camera="${faceCamera}" data-velocity="${velocity}">
        <div class="carousel-track" style="--quantity: ${itemCount}">
          ${items}
        </div>
        <div class="carousel-controls">
          <button class="carousel-prev">Previous</button>
          <button class="carousel-next">Next</button>
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
  // Reset URL state that might have been modified by previous tests
  if (window.history && window.history.replaceState) {
    window.history.replaceState({}, '', window.location.pathname);
  }
});

afterEach(() => {
  if (globalThis.InsightUI?.WebSocket?.destroy) {
    globalThis.InsightUI.WebSocket.destroy();
  }
  TestUtils.cleanup();
  vi.clearAllMocks();
});
