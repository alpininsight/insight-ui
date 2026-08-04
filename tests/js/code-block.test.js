/**
 * Tests for CodeBlock component functionality
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

describe('CodeBlock Component', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
    loadComponent('insight-ui-code-block.js');
  });

  describe('Initialization', () => {
    it('should create a code block from element', () => {
      const container = TestUtils.createCodeBlock('cb-1', 'python', 'print("hello")');
      const originalElement = container.querySelector('[data-insight-code-block]');

      new InsightUI.CodeBlock(originalElement);

      // Original element should be replaced
      const newElement = document.getElementById('cb-1');
      expect(newElement).toBeTruthy();
      expect(newElement.classList.contains('flex')).toBe(true);
    });

    it('should return existing instance for same element', () => {
      const container = TestUtils.createCodeBlock('cb-singleton', 'javascript', 'const x = 1;');
      const originalElement = container.querySelector('[data-insight-code-block]');

      const instance1 = new InsightUI.CodeBlock(originalElement);
      const instance2 = new InsightUI.CodeBlock(originalElement);

      expect(instance1).toBe(instance2);
    });

    it('should store instance reference on element', () => {
      const container = TestUtils.createCodeBlock('cb-ref', 'javascript', 'let y = 2;');
      const originalElement = container.querySelector('[data-insight-code-block]');

      const instance = new InsightUI.CodeBlock(originalElement);

      expect(instance.element.__insightInstance).toBe(instance);
    });

    it('should call Prism.highlightElement', () => {
      const container = TestUtils.createCodeBlock('cb-prism', 'typescript', 'const z: number = 3;');
      const originalElement = container.querySelector('[data-insight-code-block]');

      new InsightUI.CodeBlock(originalElement);

      expect(Prism.highlightElement).toHaveBeenCalled();
    });
  });

  describe('Toolbar', () => {
    it('should display language in toolbar', () => {
      const container = TestUtils.createCodeBlock('cb-lang', 'rust', 'fn main() {}');
      const originalElement = container.querySelector('[data-insight-code-block]');

      new InsightUI.CodeBlock(originalElement);

      const newElement = document.getElementById('cb-lang');
      const langSpan = newElement.querySelector('span');
      expect(langSpan.textContent).toBe('rust');
    });

    it('should display filename when provided', () => {
      const container = TestUtils.createCodeBlock('cb-file', 'python', 'import os', 'main.py');
      const originalElement = container.querySelector('[data-insight-code-block]');

      new InsightUI.CodeBlock(originalElement);

      const newElement = document.getElementById('cb-file');
      const spans = newElement.querySelectorAll('span');
      expect(spans.length).toBe(2);
      expect(spans[1].textContent).toBe('main.py');
    });

    it('should not display filename span when not provided', () => {
      const container = TestUtils.createCodeBlock('cb-no-file', 'go', 'package main');
      const originalElement = container.querySelector('[data-insight-code-block]');

      new InsightUI.CodeBlock(originalElement);

      const newElement = document.getElementById('cb-no-file');
      const infobox = newElement.querySelector('div > div');
      const spans = infobox.querySelectorAll('span');
      expect(spans.length).toBe(1);
    });

    it('should have a copy button', () => {
      const container = TestUtils.createCodeBlock('cb-copy-btn', 'javascript', 'const a = 1;');
      const originalElement = container.querySelector('[data-insight-code-block]');

      new InsightUI.CodeBlock(originalElement);

      const newElement = document.getElementById('cb-copy-btn');
      const copyButton = newElement.querySelector('button');
      expect(copyButton).toBeTruthy();
      expect(copyButton.textContent).toContain('Copy');
    });
  });

  describe('Copy Functionality', () => {
    it('should copy code to clipboard on button click', async () => {
      const code = 'console.log("test");';
      const container = TestUtils.createCodeBlock('cb-copy', 'javascript', code);
      const originalElement = container.querySelector('[data-insight-code-block]');

      new InsightUI.CodeBlock(originalElement);

      const newElement = document.getElementById('cb-copy');
      const copyButton = newElement.querySelector('button');

      await TestUtils.click(copyButton);

      expect(navigator.clipboard.writeText).toHaveBeenCalled();
    });

    it('should show success message after copying', async () => {
      const container = TestUtils.createCodeBlock('cb-success', 'javascript', 'const b = 2;');
      const originalElement = container.querySelector('[data-insight-code-block]');

      new InsightUI.CodeBlock(originalElement);

      const newElement = document.getElementById('cb-success');
      const copyButton = newElement.querySelector('button');

      await TestUtils.click(copyButton);

      // Wait for async clipboard operation
      await TestUtils.wait(10);

      expect(copyButton.textContent).toContain('copied');
    });

    it('should restore button text after timeout', async () => {
      vi.useFakeTimers();

      const container = TestUtils.createCodeBlock('cb-restore', 'javascript', 'const c = 3;');
      const originalElement = container.querySelector('[data-insight-code-block]');

      new InsightUI.CodeBlock(originalElement);

      const newElement = document.getElementById('cb-restore');
      const copyButton = newElement.querySelector('button');

      await TestUtils.click(copyButton);

      // Fast-forward past the 1200ms timeout
      vi.advanceTimersByTime(1300);

      expect(copyButton.textContent).toContain('Copy');

      vi.useRealTimers();
    });
  });

  describe('Code Indentation Cleaning', () => {
    it('should clean indentation from code', () => {
      const indentedCode = `
        function test() {
          return true;
        }`;
      const container = TestUtils.createCodeBlock('cb-indent', 'javascript', indentedCode);
      const originalElement = container.querySelector('[data-insight-code-block]');

      const instance = new InsightUI.CodeBlock(originalElement);

      const newElement = document.getElementById('cb-indent');
      const codeElement = newElement.querySelector('code');
      // Code should be trimmed and indentation normalized
      expect(codeElement.textContent).not.toMatch(/^\s{8}/);
    });

    it('should use minimum indentation across all lines', () => {
      // First content line has 4 spaces, nested has 8 - should remove 4 from all
      const indentedCode = `
    def outer():
        return inner()`;
      const container = TestUtils.createCodeBlock('cb-min-indent', 'python', indentedCode);
      const originalElement = container.querySelector('[data-insight-code-block]');

      new InsightUI.CodeBlock(originalElement);

      const newElement = document.getElementById('cb-min-indent');
      const codeElement = newElement.querySelector('code');
      // First line should start without indentation, second should have 4 spaces
      expect(codeElement.textContent).toMatch(/^def outer\(\):/m);
      expect(codeElement.textContent).toMatch(/^    return inner\(\)/m);
    });

    it('should handle single-line code', () => {
      const singleLine = '    print("hello")';
      const container = TestUtils.createCodeBlock('cb-single', 'python', singleLine);
      const originalElement = container.querySelector('[data-insight-code-block]');

      new InsightUI.CodeBlock(originalElement);

      const newElement = document.getElementById('cb-single');
      const codeElement = newElement.querySelector('code');
      expect(codeElement.textContent.trim()).toBe('print("hello")');
    });

    it('should preserve relative indentation', () => {
      const nestedCode = `
          class Foo:
              def bar(self):
                  pass`;
      const container = TestUtils.createCodeBlock('cb-nested', 'python', nestedCode);
      const originalElement = container.querySelector('[data-insight-code-block]');

      new InsightUI.CodeBlock(originalElement);

      const newElement = document.getElementById('cb-nested');
      const codeElement = newElement.querySelector('code');
      const lines = codeElement.textContent.trim().split('\n');
      // class should have no indent, def should have 4, pass should have 8
      expect(lines[0]).toBe('class Foo:');
      expect(lines[1]).toBe('    def bar(self):');
      expect(lines[2]).toBe('        pass');
    });

    it('should handle code with no indentation', () => {
      const noIndent = 'print(1)\nprint(2)';
      const container = TestUtils.createCodeBlock('cb-no-indent', 'python', noIndent);
      const originalElement = container.querySelector('[data-insight-code-block]');

      new InsightUI.CodeBlock(originalElement);

      const newElement = document.getElementById('cb-no-indent');
      const codeElement = newElement.querySelector('code');
      expect(codeElement.textContent.trim()).toBe('print(1)\nprint(2)');
    });
  });

  describe('Code Area', () => {
    it('should set LTR direction for code wrapper', () => {
      const container = TestUtils.createCodeBlock('cb-ltr', 'javascript', 'const d = 4;');
      const originalElement = container.querySelector('[data-insight-code-block]');

      new InsightUI.CodeBlock(originalElement);

      const newElement = document.getElementById('cb-ltr');
      const codeWrapper = newElement.querySelector('.overflow-x-auto');
      expect(codeWrapper.dir).toBe('ltr');
    });

    it('should add language class to pre element', () => {
      const container = TestUtils.createCodeBlock('cb-lang-class', 'python', 'print(1)');
      const originalElement = container.querySelector('[data-insight-code-block]');

      new InsightUI.CodeBlock(originalElement);

      const newElement = document.getElementById('cb-lang-class');
      const preElement = newElement.querySelector('pre');
      expect(preElement.classList.contains('language-python')).toBe(true);
    });

    it('should add line-numbers class to pre element', () => {
      const container = TestUtils.createCodeBlock('cb-lines', 'javascript', 'const e = 5;');
      const originalElement = container.querySelector('[data-insight-code-block]');

      new InsightUI.CodeBlock(originalElement);

      const newElement = document.getElementById('cb-lines');
      const preElement = newElement.querySelector('pre');
      expect(preElement.classList.contains('line-numbers')).toBe(true);
    });
  });

  describe('Destroy', () => {
    it('should remove event listeners on destroy', () => {
      const container = TestUtils.createCodeBlock('cb-destroy', 'javascript', 'const f = 6;');
      const originalElement = container.querySelector('[data-insight-code-block]');

      const instance = new InsightUI.CodeBlock(originalElement);
      const copyButton = instance.copyButton;
      const removeEventListenerSpy = vi.spyOn(copyButton, 'removeEventListener');

      instance.destroy();

      expect(removeEventListenerSpy).toHaveBeenCalledWith('click', instance.copyEvent);
    });

    it('should clear instance references on destroy', () => {
      const container = TestUtils.createCodeBlock('cb-clear', 'javascript', 'const g = 7;');
      const originalElement = container.querySelector('[data-insight-code-block]');

      const instance = new InsightUI.CodeBlock(originalElement);

      instance.destroy();

      expect(instance.element).toBeNull();
      expect(instance.originalElement).toBeNull();
    });
  });

  describe('Static Methods', () => {
    it('should initialize all code blocks with initAll', () => {
      TestUtils.createCodeBlock('cb-all-1', 'javascript', 'const h = 8;');
      TestUtils.createCodeBlock('cb-all-2', 'python', 'x = 9');

      InsightUI.CodeBlock.initAll();

      const cb1 = document.getElementById('cb-all-1');
      const cb2 = document.getElementById('cb-all-2');

      expect(cb1.__insightInstance).toBeTruthy();
      expect(cb2.__insightInstance).toBeTruthy();
    });
  });
});
