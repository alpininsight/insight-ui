/**
 * Tests for Modal component functionality
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

describe('Modal Component', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
    loadComponent('insight-ui-utils.js');
    loadComponent('insight-ui-modal.js');
  });

  describe('Open/Close Functionality', () => {
    it('should open modal on trigger button click', () => {
      const container = TestUtils.createModal();
      const button = container.querySelector('[data-insight-modal]');
      const modalEl = container.querySelector('#test-modal');

      new InsightUI.Modal(button);

      expect(modalEl.style.display).toBe('none');

      TestUtils.click(button);

      expect(modalEl.style.display).toBe('block');
    });

    it('should close modal on dismiss button click', () => {
      const container = TestUtils.createModal();
      const button = container.querySelector('[data-insight-modal]');
      const modalEl = container.querySelector('#test-modal');
      const dismissBtn = container.querySelector('[data-insight-dismiss="modal"]');

      new InsightUI.Modal(button);

      TestUtils.click(button); // open
      expect(modalEl.style.display).toBe('block');

      TestUtils.click(dismissBtn); // close
      expect(modalEl.style.display).toBe('none');
    });

    it('should close modal on backdrop click', () => {
      const container = TestUtils.createModal();
      const button = container.querySelector('[data-insight-modal]');
      const modalEl = container.querySelector('#test-modal');

      new InsightUI.Modal(button);

      TestUtils.click(button); // open
      expect(modalEl.style.display).toBe('block');

      // Click on backdrop (the modal element itself, not content)
      modalEl.dispatchEvent(new MouseEvent('click', { bubbles: true }));

      expect(modalEl.style.display).toBe('none');
    });

    it('should not close modal when clicking inside content', () => {
      const container = TestUtils.createModal();
      const button = container.querySelector('[data-insight-modal]');
      const modalEl = container.querySelector('#test-modal');
      const content = container.querySelector('.modal-content');

      new InsightUI.Modal(button);

      TestUtils.click(button); // open
      expect(modalEl.style.display).toBe('block');

      // Click on content
      content.dispatchEvent(new MouseEvent('click', { bubbles: true }));

      // Modal should stay open because click target is content, not modal
      expect(modalEl.style.display).toBe('block');
    });
  });

  describe('currentOpen State Management', () => {
    it('should set currentOpen when opening modal', () => {
      const container = TestUtils.createModal();
      const button = container.querySelector('[data-insight-modal]');

      const modal = new InsightUI.Modal(button);

      expect(InsightUI.Modal.currentOpen).toBeNull();

      TestUtils.click(button);

      expect(InsightUI.Modal.currentOpen).toBe(modal);
    });

    it('should clear currentOpen when closing modal', () => {
      const container = TestUtils.createModal();
      const button = container.querySelector('[data-insight-modal]');

      const modal = new InsightUI.Modal(button);

      TestUtils.click(button); // open
      expect(InsightUI.Modal.currentOpen).toBe(modal);

      modal.close();
      expect(InsightUI.Modal.currentOpen).toBeNull();
    });

    it('should close previous modal when opening a new one', () => {
      const container1 = TestUtils.createModal('modal-1');
      const container2 = TestUtils.createModal('modal-2');
      const button1 = container1.querySelector('[data-insight-modal]');
      const button2 = container2.querySelector('[data-insight-modal]');
      const modalEl1 = container1.querySelector('#modal-1');
      const modalEl2 = container2.querySelector('#modal-2');

      const modal1 = new InsightUI.Modal(button1);
      new InsightUI.Modal(button2);

      TestUtils.click(button1); // open first
      expect(modalEl1.style.display).toBe('block');
      expect(InsightUI.Modal.currentOpen).toBe(modal1);

      TestUtils.click(button2); // open second - should close first
      expect(modalEl1.style.display).toBe('none');
      expect(modalEl2.style.display).toBe('block');
    });
  });

  describe('Scroll Blocking', () => {
    it('should block body scroll when opening modal', () => {
      const container = TestUtils.createModal();
      const button = container.querySelector('[data-insight-modal]');

      new InsightUI.Modal(button);

      TestUtils.click(button);

      expect(document.body.style.overflow).toBe('hidden');
    });

    it('should unblock body scroll when closing modal', () => {
      const container = TestUtils.createModal();
      const button = container.querySelector('[data-insight-modal]');

      const modal = new InsightUI.Modal(button);

      TestUtils.click(button); // open
      expect(document.body.style.overflow).toBe('hidden');

      modal.close();
      expect(document.body.style.overflow).toBe('');
    });
  });

  describe('Focus Trapping', () => {
    it('should call trapFocus when opening modal', () => {
      const container = TestUtils.createModal();
      const button = container.querySelector('[data-insight-modal]');
      const modalEl = container.querySelector('#test-modal');

      const trapFocusSpy = vi.spyOn(InsightUI.utils, 'trapFocus');

      new InsightUI.Modal(button);

      TestUtils.click(button);

      expect(trapFocusSpy).toHaveBeenCalledWith(modalEl);

      trapFocusSpy.mockRestore();
    });
  });

  describe('open() and close() methods', () => {
    it('should open modal programmatically', () => {
      const container = TestUtils.createModal();
      const button = container.querySelector('[data-insight-modal]');
      const modalEl = container.querySelector('#test-modal');

      const modal = new InsightUI.Modal(button);

      expect(modalEl.style.display).toBe('none');

      modal.open();

      expect(modalEl.style.display).toBe('block');
    });

    it('should close modal programmatically', () => {
      const container = TestUtils.createModal();
      const button = container.querySelector('[data-insight-modal]');
      const modalEl = container.querySelector('#test-modal');

      const modal = new InsightUI.Modal(button);

      modal.open();
      expect(modalEl.style.display).toBe('block');

      modal.close();
      expect(modalEl.style.display).toBe('none');
    });
  });

  describe('destroy() method', () => {
    it('should close modal if open when destroyed', () => {
      const container = TestUtils.createModal();
      const button = container.querySelector('[data-insight-modal]');
      const modalEl = container.querySelector('#test-modal');

      const modal = new InsightUI.Modal(button);

      modal.open();
      expect(modalEl.style.display).toBe('block');

      modal.destroy();

      expect(modalEl.style.display).toBe('none');
      expect(InsightUI.Modal.currentOpen).toBeNull();
    });

    it('should remove click handler from trigger button', () => {
      const container = TestUtils.createModal();
      const button = container.querySelector('[data-insight-modal]');
      const modalEl = container.querySelector('#test-modal');

      const modal = new InsightUI.Modal(button);

      modal.destroy();

      // Click should not open modal anymore
      TestUtils.click(button);
      expect(modalEl.style.display).toBe('none');
    });

    it('should nullify references', () => {
      const container = TestUtils.createModal();
      const button = container.querySelector('[data-insight-modal]');

      const modal = new InsightUI.Modal(button);

      modal.destroy();

      expect(modal.trigger).toBeNull();
      expect(modal.modal).toBeNull();
    });
  });

  describe('Error Handling', () => {
    it('should handle missing modal element gracefully', () => {
      const container = TestUtils.createDOM(`
        <button data-insight-modal="nonexistent">Open</button>
      `);
      const button = container.querySelector('[data-insight-modal]');

      // Should not throw
      expect(() => new InsightUI.Modal(button)).not.toThrow();
    });
  });
});
