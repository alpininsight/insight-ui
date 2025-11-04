window.InsightUI = window.InsightUI || {};

function cleanIndentation(code) {
    // Zuerst teilen wir den Code in Zeilen auf
    const lines = code.split('\n');

    // Bestimme die Anzahl der führenden Leerzeichen oder Tabs in der ersten Zeile
    const indentMatch = lines[1].match(/^\s*/); // Führende Leerzeichen/Tabs der ersten Zeile
    const indentLength = indentMatch ? indentMatch[0].length : 0;

    // Entferne die gleiche Anzahl an führenden Leerzeichen oder Tabs aus jeder Zeile
    const cleanedLines = lines.map(line => {
        // Entferne nur die führenden Leerzeichen/Tabs, die der Anzahl in der ersten Zeile entsprechen
        return line.slice(indentLength);
    });

    // Setze den Code wieder zusammen
    return cleanedLines.join('\n');
}

function generateCodeBlock(id, lang, code) {
    // Erstelle das Wrapper-Div
    const wrapper = document.createElement('div');
    wrapper.classList.add('bg-[#f5f2f0]', 'rounded', 'border', 'border-gray-300', 'dark:border-0');

    // Erstelle die Flex-Box für den Button
    const flexContainer = document.createElement('div');
    flexContainer.classList.add('flex', 'justify-end', 'bg-blue-200/75', 'dark:bg-blue-900/75', 'rounded-t', 'p-2');

    // Erstelle den Button
    const button = document.createElement('button');
    button.classList.add('btn', 'btn-secondary', 'btn-xs');
    button.classList.add(id); // Dynamischer ID hinzufügen
    button.setAttribute('data-clipboard-target', `#${id}`);

    // SVG-Icon für den Button
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('fill', 'currentColor');
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
    button.appendChild(document.createTextNode('Copy')); // Text "Copy" hinzufügen

    flexContainer.appendChild(button);

    // Erstelle den Code-Block
    const codeWrapper = document.createElement('div');
    codeWrapper.classList.add('max-w-2xs', 'md:max-w-2xl', 'lg:max-w-5xl', 'overflow-x-scroll');

    const pre = document.createElement('pre');
    pre.id = id;
    pre.classList.add(`language-${lang}`);

    const codeElement = document.createElement('code');
    const cleanCode = cleanIndentation(code).trim();
    codeElement.textContent = cleanCode;

    pre.appendChild(codeElement);
    codeWrapper.appendChild(pre);

    // Füge beide Teile zusammen
    wrapper.appendChild(flexContainer);
    wrapper.appendChild(codeWrapper);

    // Füge die generierte Struktur zum DOM hinzu
    document.body.appendChild(wrapper);

    // Initialisiere ClipboardJS
    new ClipboardJS(`.${id}`);

    // Wende Prism.js an
    Prism.highlightElement(pre);

    return wrapper;
}

InsightUI.CodeBlock = {
  init: function () {
    const codeBlocks = document.querySelectorAll('[data-insight-code-block]');
    if (!codeBlocks) return;

    for (let codeBlock of codeBlocks)
    {
      const id = codeBlock.id;
      const lang = codeBlock.getAttribute('data-insight-code-block');
      const code = codeBlock.textContent;

      const wrapper = generateCodeBlock(id, lang, code);

      codeBlock.replaceWith(wrapper);
    }

    console.log("Code Blocks: ", codeBlocks);
    console.log("Code Blocks initialized!");
  }
}
