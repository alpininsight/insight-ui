export class CodeBlock {
    // Weak references used to prevent multiple initialization of the same instance
    static instances = new WeakMap();

    constructor(originalElement) {
        // If an instance for this element already exists, return it
        if (CodeBlock.instances.has(originalElement)) {
            return CodeBlock.instances.get(originalElement);
        }

        this.id = originalElement.id;
        this.lang = originalElement.getAttribute('data-insight-code-block');
        this.filename = originalElement.getAttribute('data-filename') || "";
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
     * @param {string} filename An optional filename, shown in the topbar as hint for the user.
     * @param {string} code The code.
     * @returns The wrapper element of the created HTML structure.
     */
    generateCodeBlock(id, lang, filename, code) {
        // Create wrapper-div
        const wrapper = document.createElement('div');
        wrapper.classList.add('bg-[#f9fafb]', 'dark:bg-[#030712]', 'rounded', 'border', 'border-gray-300', 'dark:border-gray-700');
        wrapper.id = id;

        // Create flex-box for the copy button
        const flexContainer = document.createElement('div');
        flexContainer.classList.add('flex', 'justify-between', 'bg-gray-200', 'dark:bg-gray-900', 'rounded-t', 'p-2');

        // Create lang and filename infobox
        const infobox = document.createElement('div');
        infobox.classList.add("flex")

        const langSpan = document.createElement('span');
        langSpan.classList.add("text-secondary", "leading-loose", "bg-gray-50", "dark:bg-gray-700", "rounded-sm", "px-2");
        langSpan.appendChild(document.createTextNode(`${lang}`));
        infobox.appendChild(langSpan);

        if (filename) {
            const fileSpan = document.createElement('span');
            fileSpan.classList.add("text-secondary", "leading-loose", "bg-gray-50", "dark:bg-gray-700", "rounded-sm", "px-2", "ms-2");
            fileSpan.appendChild(document.createTextNode(`${filename}`));
            infobox.appendChild(fileSpan);
        }

        flexContainer.appendChild(infobox);

        // Create copy button
        this.copyButton = document.createElement('button');
        this.copyButton.classList.add('btn', 'btn-secondary', 'btn-sm');

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

        this.copyButton.appendChild(svg);
        this.copyButton.appendChild(document.createTextNode('Copy'));

        flexContainer.appendChild(this.copyButton);

        // Create actual code block
        const codeWrapper = document.createElement('div');
        codeWrapper.classList.add('max-w-2xs', 'md:max-w-2xl', 'lg:max-w-5xl', 'overflow-x-scroll');

        const pre = document.createElement('pre');
        pre.classList.add('line-numbers', `language-${lang}`);

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

        // Add Event Listener for copy button
        this.copyEvent = async () => {
            try {
                await navigator.clipboard.writeText(codeElement.textContent);
                this.copyButton.textContent = gettext('✔ copied');
            } catch (err) {
                // Use a temporary textarea as fallback
                const textarea = document.createElement('textarea');
                textarea.value = codeElement.textContent;
                document.body.appendChild(textarea);
                textarea.select();

                const copied = document.execCommand('copy');  // Copies the content of the selected element
                document.body.removeChild(textarea);

                if (copied)
                {
                    this.copyButton.textContent = gettext('✔ copied');
                }
                else
                {
                    console.error('Failed to copy', err);
                    this.copyButton.textContent = gettext('✖ Copy failed!');
                }
            }

            setTimeout(() => {
                this.copyButton.textContent = '';
                this.copyButton.appendChild(svg);
                this.copyButton.appendChild(document.createTextNode('Copy'));
            }, 1200);
        }

        this.copyButton.addEventListener('click', this.copyEvent);

        // Apply Prism.js syntax highlighting
        Prism.highlightElement(codeElement);

        return wrapper;
    }

    /**
     * Destroys the code block instance and removes all event listeners.
     * Call this before removing the element from DOM.
     */
    destroy() {
        debugLog("Destroy code block: ", this.element);

        this.copyButton.removeEventListener("click", this.copyEvent);

        CodeBlock.instances.delete(this.originalElement);
        delete this.element.__insightInstance;

        this.originalElement = null;
        this.element = null;
    }

    // Static method for initializing all code blocks
    static initAll() {
        document.querySelectorAll("[data-insight-code-block]").forEach(el => new CodeBlock(el));
    }
}
