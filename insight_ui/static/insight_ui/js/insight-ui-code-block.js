class CodeBlock {
  // Manages all CodeBlock instances of the DOM
  static instances = new WeakMap();

  constructor(element) {
    // If an instance for this element already exists, return it
    if (CodeBlock.instances.has(element)) {
      return CodeBlock.instances.get(element);
    }

    this.element = element;
    this.id = element.id;
    this.lang = element.getAttribute('data-insight-code-block');
    this.code = element.textContent;
    this.wrapper = this.generateCodeBlock(this.id, this.lang, this.code);
    this.element.replaceWith(this.wrapper);

    CodeBlock.instances.set(element, this);

    debugLog("New code block created: ", this.element);
  }

  /**
   * Remove the indentation of the HTML-Tag, measured by the indentation of the first line.
   *
   * @param {string} code The code to clean the indentation from.
   * @returns The cleaned code.
   */
  cleanIndentation(code) {
    const lines = code.split('\n');

    // Measure the indentation of the first line
    const indentMatch = lines[1].match(/^\s*/);
    const indentLength = indentMatch ? indentMatch[0].length : 0;

    // Remove the measured number of spaces in all lines.
    const cleanedLines = lines.map(line => {
      return line.slice(indentLength);
    });

    return cleanedLines.join('\n');
  }

  /**
   * Create the HTML structure of the code block component.
   *
   * @param {string} id The id of the code block.
   * @param {string} lang The langauge of the code.
   * @param {string} code The code.
   * @returns The wrapper element of the created HTML structure.
   */
  generateCodeBlock(id, lang, code) {
    // Create wrapper-div
    const wrapper = document.createElement('div');
    wrapper.classList.add('bg-[#f5f2f0]', 'rounded', 'border', 'border-gray-300', 'dark:border-0');

    // Create flex-box for the copy button
    const flexContainer = document.createElement('div');
    flexContainer.classList.add('flex', 'justify-end', 'bg-blue-200/75', 'dark:bg-blue-900/75', 'rounded-t', 'p-2');

    // Create copy button
    const button = document.createElement('button');
    button.classList.add('btn', 'btn-secondary', 'btn-xs');
    button.classList.add(id);
    button.setAttribute('data-clipboard-target', `#${id}`);

    // SVG-Icon of the button
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('fill', 'currentColor');
    svg.setAttribute('aria-hidden', "true");
    svg.classList.add('size-5');

    const path1 = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path1.setAttribute('fill-rule', 'evenodd');
    path1.setAttribute('d', 'M7.502 6h7.128A3.375 3.375 0 0 1 18 9.375v9.375a3 3 0 0 0 3-3V6.108c0-1.505-1.125-2.811-2.664-2.94a48.972 48.972 0 0 0-.673-.05A3 3 0 0 0 15 1.5h-1.5a3 3 0 0 0-2.663 1.618c-.225.015-.45.032-.673.05C8.662 3.295 7.554 4.542 7.502 6ZM13.5 3A1.5 1.5 0 0 0 12 4.5h4.5A1.5 1.5 0 0 0 15 3h-1.5Z');

    const path2 = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path2.setAttribute('fill-rule', 'evenodd');
    path2.setAttribute('d', 'M3 9.375C3 8.339 3.84 7.5 4.875 7.5h9.75c1.036 0 1.875.84 1.875 1.875v11.25c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V9.375ZM6 12a.75.75 0 0 1 .75-.75h.008a.75.75 0 0 1 .75.75v.008a.75.75 0 0 1-.75.75H6.75a.75.75 0 0 1-.75-.75V12Zm2.25 0a.75.75 0 0 1 .75-.75h3.75a.75.75 0 0 1 0 1.5H9a.75.75 0 0 1-.75-.75ZM6 15a.75.75 0 0 1 .75-.75h.008a.75.75 0 0 1 .75.75v.008a.75.75 0 0 1-.75.75H6.75a.75.75 0 0 1-.75-.75V15Zm2.25 0a.75.75 0 0 1 .75-.75h3.75a.75.75 0 0 1 0 1.5H9a.75.75 0 0 1-.75-.75ZM6 18a.75.75 0 0 1 .75-.75h.008a.75.75 0 0 1 .75.75v.008a.75.75 0 0 1-.75.75H6.75a.75.75 0 0 1-.75-.75V18Zm2.25 0a.75.75 0 0 1 .75-.75h3.75a.75.75 0 0 1 0 1.5H9a.75.75 0 0 1-.75-.75Z');

    svg.appendChild(path1);
    svg.appendChild(path2);

    button.appendChild(svg);
    button.appendChild(document.createTextNode('Copy'));

    flexContainer.appendChild(button);

    // Create actual code block
    const codeWrapper = document.createElement('div');
    codeWrapper.classList.add('max-w-2xs', 'md:max-w-2xl', 'lg:max-w-5xl', 'overflow-x-scroll');

    const pre = document.createElement('pre');
    pre.id = id;
    pre.classList.add(`language-${lang}`);

    const codeElement = document.createElement('code');
    const cleanCode = this.cleanIndentation(code).trim();
    codeElement.textContent = cleanCode;

    pre.appendChild(codeElement);
    codeWrapper.appendChild(pre);

    // Connect both parts (Head with button and code block)
    wrapper.appendChild(flexContainer);
    wrapper.appendChild(codeWrapper);

    // Add to DOM
    document.body.appendChild(wrapper);

    // Init ClipboardJS for the newly created code block
    new ClipboardJS(`.${id}`);

    // Apply Prism.js syntax highlighting
    Prism.highlightElement(pre);

    return wrapper;
  }

  // Static method for initializing all code blocks
  static initAll() {
    const codeBlocks = document.querySelectorAll("[data-insight-code-block]");
    codeBlocks.forEach((el) => {
      if (!CodeBlock.instances.has(el)) {
        new CodeBlock(el);
      }
    });
  }
}

window.InsightUI = window.InsightUI || {};
window.InsightUI.CodeBlock = CodeBlock;
