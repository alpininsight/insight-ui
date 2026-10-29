// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Code block component for Insight UI.
 *
 * Transforms code elements into styled code blocks with syntax highlighting (via Prism.js),
 * a toolbar showing language and optional filename, and a copy-to-clipboard button.
 * Automatically removes common leading indentation for cleaner display.
 *
 * Options (data attributes on the element):
 * - data-filename: shown in the toolbar.
 * - data-diff: the content is a diff with one marker column per line ("+" added, "-" removed,
 *   " " unchanged). Lines are highlighted as added/removed and the code keeps its markers.
 * - data-diff-marks: JSON [[start, end], ...] with the changed parts inside changed lines, as character
 *   offsets in the diff text. Marked with <mark class="insight-diff-mark">.
 * - data-copy="false": hide the copy button. A diff has none.
 *
 * @example
 * // HTML structure (before initialization)
 * <pre id="example" data-insight-code-block="javascript" data-filename="app.js">
 *   const greeting = "Hello, World!";
 *   console.log(greeting);
 * </pre>
 *
 * // JavaScript
 * CodeBlock.initAll();
 */
export class CodeBlock {
    /** @type {WeakMap<HTMLElement, CodeBlock>} Weak references to prevent multiple initialization */
    static instances = new WeakMap();

    /**
     * Creates a new CodeBlock instance.
     * Replaces the original element with a styled code block component.
     *
     * @param {HTMLElement} originalElement - The pre/code element with data-insight-code-block attribute
     */
    constructor(originalElement) {
        // If an instance for this element already exists, return it
        if (CodeBlock.instances.has(originalElement)) {
            return CodeBlock.instances.get(originalElement);
        }

        this.id = originalElement.id;
        this.lang = originalElement.getAttribute('data-insight-code-block');
        this.filename = originalElement.getAttribute('data-filename') || "";
        this.isDiff = originalElement.hasAttribute('data-diff');
        this.diffMarks = this.isDiff ? CodeBlock.parseDiffMarks(originalElement.getAttribute('data-diff-marks')) : [];
        this.showCopy = !this.isDiff && originalElement.getAttribute('data-copy') !== 'false';
        this.code = originalElement.textContent;
        this.copyButton = undefined;
        this.copyEvent = undefined;
        this.element = this.generateCodeBlock(this.id, this.lang, this.filename, this.code);

        this.originalElement = originalElement
        originalElement.replaceWith(this.element);

        this.element.__insightInstance = this;
        CodeBlock.instances.set(this.originalElement, this);

        debugLog("New code block created: ", this.element);
    }

    /**
     * Remove common leading indentation from code.
     *
     * Finds the minimum indentation across all non-empty lines and removes
     * that amount from every line. This ensures code displays flush-left
     * regardless of how it was indented in the HTML template.
     *
     * @param {string} code The code to clean the indentation from.
     * @returns {string} The cleaned code.
     */
    cleanIndentation(code) {
        const lines = code.split('\n');

        // Find minimum indentation across all non-empty lines
        let minIndent = Infinity;
        for (const line of lines) {
            // Skip empty or whitespace-only lines
            if (line.trim().length === 0) continue;

            const indentMatch = line.match(/^\s*/);
            const indentLength = indentMatch ? indentMatch[0].length : 0;
            minIndent = Math.min(minIndent, indentLength);
        }

        // If no non-empty lines found or no indentation, return as-is
        if (minIndent === Infinity || minIndent === 0) {
            return code;
        }

        // Remove the minimum indent from all lines
        const cleanedLines = lines.map(line => line.slice(minIndent));

        return cleanedLines.join('\n');
    }

    /**
     * Create the toolbar with language/filename info and copy button.
     *
     * @param {string} lang The language of the code.
     * @param {string} filename An optional filename.
     * @returns {HTMLElement} The toolbar element.
     */
    #createToolbar(lang, filename) {
        const toolbar = document.createElement('div');
        toolbar.classList.add('flex', 'justify-between', 'bg-insight-raised', 'rounded-t-insight-surface', 'p-2');

        const infobox = document.createElement('div');
        infobox.classList.add('flex');

        const langSpan = document.createElement('span');
        langSpan.classList.add('text-insight-body', 'leading-loose', 'bg-insight-base', 'rounded-insight-control', 'px-2');
        langSpan.textContent = lang;
        infobox.appendChild(langSpan);

        if (filename) {
            const fileSpan = document.createElement('span');
            fileSpan.classList.add('text-insight-body', 'leading-loose', 'bg-insight-base', 'rounded-insight-control', 'px-2', 'ms-2');
            fileSpan.textContent = filename;
            infobox.appendChild(fileSpan);
        }

        toolbar.appendChild(infobox);
        return toolbar;
    }

    /**
     * Create the copy button with icon.
     *
     * @returns {{button: HTMLButtonElement, icon: SVGElement}} The button and its icon.
     */
    #createCopyButton() {
        const button = document.createElement('button');
        button.classList.add('btn', 'btn-secondary', 'btn-s');

        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
        svg.setAttribute('viewBox', '0 0 24 24');
        svg.setAttribute('fill', 'currentColor');
        svg.setAttribute('aria-hidden', 'true');
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
        button.appendChild(document.createTextNode(gettext('Copy')));

        return { button, icon: svg };
    }

    /**
     * Create the code area with syntax highlighting.
     *
     * @param {string} lang The language for syntax highlighting.
     * @param {string} code The code content.
     * @returns {{wrapper: HTMLElement, codeElement: HTMLElement}} The wrapper and code element.
     */
    #createCodeArea(lang, code) {
        const wrapper = document.createElement('div');
        wrapper.classList.add('w-full', 'overflow-x-auto');
        // Code is always LTR, even in RTL layouts
        wrapper.dir = 'ltr';

        const pre = document.createElement('pre');
        pre.classList.add('!overflow-visible', '!m-0', 'rounded-insight-surface');
        if (this.isDiff) {
            // Prism's diff-highlight plugin: diff markers plus the language's syntax highlighting.
            // Line numbers would count old and new lines together, so a diff has none.
            pre.classList.add(`language-diff-${lang}`, 'diff-highlight');
        } else {
            pre.classList.add('line-numbers', `language-${lang}`);
        }

        const codeElement = document.createElement('code');
        codeElement.classList.add('block', 'pe-6', this.isDiff ? 'min-w-full' : 'w-fit');
        // Server diff offsets refer to this exact text, including meaningful trailing spaces.
        codeElement.textContent = this.isDiff
            ? code
            : this.cleanIndentation(code).trim();

        pre.appendChild(codeElement);
        wrapper.appendChild(pre);

        return { wrapper, codeElement };
    }

    /**
     * Setup the copy event handler for the copy button.
     *
     * @param {HTMLElement} codeElement The code element to copy from.
     * @param {SVGElement} icon The icon to restore after copying.
     */
    #setupCopyHandler(codeElement, icon) {
        this.copyEvent = async () => {
            const text = codeElement.textContent;
            try {
                await navigator.clipboard.writeText(text);
                this.copyButton.textContent = gettext('✔ copied');
            } catch (err) {
                // Fallback for older browsers
                const textarea = document.createElement('textarea');
                textarea.value = text;
                document.body.appendChild(textarea);
                textarea.select();

                const copied = document.execCommand('copy');
                document.body.removeChild(textarea);

                if (copied) {
                    this.copyButton.textContent = gettext('✔ copied');
                } else {
                    console.error('Failed to copy!', err);
                    this.copyButton.textContent = gettext('✖ Copy failed!');
                }
            }

            setTimeout(() => {
                this.copyButton.textContent = '';
                this.copyButton.appendChild(icon);
                this.copyButton.appendChild(document.createTextNode(gettext('Copy')));
            }, 1200);
        };

        this.copyButton.addEventListener('click', this.copyEvent);
    }

    /** @type {WeakMap<HTMLElement, Array<[number, number]>>} Diff marks of each highlighted code element */
    static pendingMarks = new WeakMap();

    /** @type {boolean} Whether the Prism hook that applies the diff marks is registered */
    static #hookRegistered = false;

    /**
     * Apply the diff marks after every highlighting pass. Prism's autoloader highlights again once the
     * grammar has loaded and replaces the content, so marks set right after highlightElement would be lost.
     */
    static #watchHighlighting() {
        if (CodeBlock.#hookRegistered || !Prism.hooks) return;
        Prism.hooks.add('complete', (env) => {
            const ranges = CodeBlock.pendingMarks.get(env.element);
            if (ranges) CodeBlock.markRanges(env.element, ranges);
        });
        CodeBlock.#hookRegistered = true;
    }

    /**
     * Read the diff marks attribute; anything but a JSON list means no marks.
     *
     * @param {string|null} value The attribute value.
     * @returns {Array<[number, number]>} Sorted [start, end) offsets in the code text.
     */
    static parseDiffMarks(value) {
        if (!value) return [];
        try {
            const marks = JSON.parse(value);
            return Array.isArray(marks) ? marks : [];
        } catch {
            return [];
        }
    }

    /**
     * Wrap character ranges of an element's text in <mark> elements.
     * Works on the text nodes, so ranges may span the token spans Prism created.
     *
     * @param {HTMLElement} root The element whose text is marked.
     * @param {Array<[number, number]>} ranges Sorted Unicode code-point [start, end) offsets, as published by Python.
     */
    static markRanges(root, ranges) {
        if (!ranges.length) return;
        // Python publishes Unicode code-point offsets; DOM text APIs use UTF-16 units.
        const offsets = [0];
        for (const character of root.textContent) {
            offsets.push(offsets[offsets.length - 1] + character.length);
        }
        const domRanges = ranges.map(([start, end]) => [offsets[start], offsets[end]]);
        const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
        const nodes = [];
        while (walker.nextNode()) nodes.push(walker.currentNode);

        let position = 0;
        for (const node of nodes) {
            const nodeStart = position;
            const nodeEnd = nodeStart + node.data.length;
            position = nodeEnd;
            // Collect the parts of this node that fall into a range, then wrap them from the end.
            const parts = domRanges
                .map(([start, end]) => [Math.max(start, nodeStart) - nodeStart, Math.min(end, nodeEnd) - nodeStart])
                .filter(([start, end]) => end > start);
            for (const [start, end] of parts.reverse()) {
                const marked = node.splitText(start);
                marked.splitText(end - start);
                const mark = document.createElement('mark');
                mark.className = 'insight-diff-mark';
                marked.replaceWith(mark);
                mark.appendChild(marked);
            }
        }
    }

    /**
     * Create the HTML structure of the code block component.
     *
     * @param {string} id The id of the code block.
     * @param {string} lang The language of the code.
     * @param {string} filename An optional filename, shown in the toolbar.
     * @param {string} code The code.
     * @returns {HTMLElement} The wrapper element of the created HTML structure.
     */
    generateCodeBlock(id, lang, filename, code) {
        const wrapper = document.createElement('div');
        wrapper.classList.add('flex', 'flex-col', 'bg-insight-surface', 'rounded-insight-surface', 'border', 'border-insight-surface');
        wrapper.id = id;

        const toolbar = this.#createToolbar(lang, filename);
        let icon;
        if (this.showCopy) {
            const created = this.#createCopyButton();
            this.copyButton = created.button;
            icon = created.icon;
            toolbar.appendChild(this.copyButton);
        }

        const { wrapper: codeWrapper, codeElement } = this.#createCodeArea(lang, code);

        wrapper.appendChild(toolbar);
        wrapper.appendChild(codeWrapper);

        // Temporarily add to DOM for Prism to process
        document.body.appendChild(wrapper);
        if (this.isDiff) {
            CodeBlock.pendingMarks.set(codeElement, this.diffMarks);
            CodeBlock.#watchHighlighting();
        }
        Prism.highlightElement(codeElement);
        // Without Prism hooks (no highlighting library), mark the plain text right away.
        if (this.isDiff && !Prism.hooks) {
            CodeBlock.markRanges(codeElement, CodeBlock.pendingMarks.get(codeElement));
        }

        if (this.copyButton) {
            this.#setupCopyHandler(codeElement, icon);
        }

        return wrapper;
    }

    /**
     * Destroys the code block instance and removes all event listeners.
     * Call this before removing the element from DOM.
     */
    destroy() {
        debugLog("Destroy code block: ", this.element);

        this.copyButton?.removeEventListener("click", this.copyEvent);

        CodeBlock.instances.delete(this.originalElement);
        delete this.element.__insightInstance;

        this.originalElement = null;
        this.element = null;
    }

    /**
     * Initializes all code block instances on the page.
     *
     * @static
     */
    static initAll() {
        document.querySelectorAll("[data-insight-code-block]").forEach(el => new CodeBlock(el));
    }
}
