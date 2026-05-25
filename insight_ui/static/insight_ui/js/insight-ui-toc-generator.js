/**
 * Table of Contents with scroll-aware highlighting.
 *
 * Features:
 * - Builds a nested ToC from headings
 * - Highlights active heading while scrolling
 * - Different logic for scrolling down vs up
 * - Stable handling of anchor jumps & hash navigation
 */
class TableOfContents {
    /**
     * @param {Object} options
     * @param {string} options.contentSelector - ID of the content container
     * @param {string} options.tocSelector - ID of the ToC container
     * @param {string} [options.headingSelector] - CSS selector for headings
     * @param {number} [options.offsetTop] - Activation offset from top (scrolling down)
     * @param {number} [options.offsetBottom] - Activation offset from bottom (scrolling up)
     */
    constructor({
        contentSelector = "main",
        tocSelector,
        headingSelector = "h1, h2, h3, h4, h5, h6",
        offsetTop = 200,
        offsetBottom = 300
    }) {
        this.content = document.getElementById(contentSelector);
        this.toc = document.getElementById(tocSelector);
        if (!this.content || !this.toc) return;

        this.headings = Array.from(
            this.content.querySelectorAll(headingSelector)
        );
        if (!this.headings.length) return;

        this.offsetTop = offsetTop;
        this.offsetBottom = offsetBottom;

        this.linkMap = new Map();
        this.currentHeading = null;
        this.lastScrollY = window.scrollY;
        this.ticking = false;

        this.buildTOC();
        this.bindEvents();
        this.onScroll({ force: true });
    }

    /**
     * Builds the nested ToC structure from headings.
     */
    buildTOC() {
        const rootList = document.createElement("ul");
        rootList.className = "list-none";

        const listStack = [rootList];
        let currentLevel = 1;

        this.headings.forEach((heading, index) => {
            const level = parseInt(heading.tagName.substring(1), 10);

            // Ensure unique IDs
            if (!heading.id) {
                heading.id =
                    heading.textContent
                        .toLowerCase()
                        .trim()
                        .replace(/[^\w]+/g, "-") +
                    "-" +
                    index;
            }

            while (level > currentLevel) {
                const ul = document.createElement("ul");
                ul.className = "list-none";

                listStack[listStack.length - 1]
                    .lastElementChild
                    ?.appendChild(ul);

                listStack.push(ul);
                currentLevel++;
            }

            while (level < currentLevel) {
                listStack.pop();
                currentLevel--;
            }

            const li = document.createElement("li");
            const a = document.createElement("a");

            a.href = `#${heading.id}`;
            a.textContent = heading.textContent;
            a.className = `
        pe-2 py-1 text-sm text-primary line-clamp-1
        border-s border-gray-200 dark:border-gray-700
        hover:border-gray-400 hover:text-gray-400
        aria-[current=location]:font-bold
        aria-[current=location]:text-insight-primary-hover
        focus-visible:outline focus-visible:outline-2
        focus-visible:outline-insight-primary-hover focus-visible:outline-offset-2
      `.trim();

            a.style.paddingInlineStart = `${0.5 * currentLevel}rem`;

            li.appendChild(a);
            listStack[listStack.length - 1].appendChild(li);
            this.linkMap.set(heading, a);
        });

        this.toc.appendChild(rootList);
    }

    /**
     * Checks whether an element is visible in the viewport.
     *
     * @param {HTMLElement} el
     * @param {number} minVisiblePx
     * @returns {boolean}
     */
    isInViewport(el, minVisiblePx = 100) {
        const rect = el.getBoundingClientRect();
        const vh = window.innerHeight;

        return (
            rect.bottom > minVisiblePx &&
            rect.top < vh - minVisiblePx
        );
    }

    /**
     * Sets the active heading and updates ToC highlighting.
     *
     * @param {HTMLElement} heading
     */
    setActiveHeading(heading) {
        if (!heading || heading === this.currentHeading) return;

        this.currentHeading = heading;

        this.toc
            .querySelectorAll('a[aria-current="location"]')
            .forEach(link => link.removeAttribute("aria-current"));

        this.linkMap
            .get(heading)
            ?.setAttribute("aria-current", "location");
    }

    /**
     * Recalculates the active heading without scroll direction logic.
     * Used for anchor jumps and initial load.
     */
    recalcActiveHeading() {
        let candidate = null;

        for (const heading of this.headings) {
            if (heading.getBoundingClientRect().top <= this.offsetTop) {
                candidate = heading;
            } else {
                break;
            }
        }

        if (candidate) {
            this.setActiveHeading(candidate);
        }
    }

    /**
     * Scroll handler with direction-aware logic.
     *
     * @param {Object} [options]
     * @param {boolean} [options.force=false] - Ignore scroll direction
     */
    onScroll({ force = false } = {}) {
        const scrollY = window.scrollY;

        if (force) {
            this.lastScrollY = scrollY;
            this.recalcActiveHeading();
            return;
        }

        const scrollingDown = scrollY > this.lastScrollY;
        this.lastScrollY = scrollY;

        if (scrollingDown) {
            // Scroll down
            let candidate = null;

            for (const heading of this.headings) {
                if (heading.getBoundingClientRect().top <= this.offsetTop) {
                    candidate = heading;
                } else {
                    break;
                }
            }

            if (candidate) {
                this.setActiveHeading(candidate);
            }

        } else {
            // Scroll up
            if (!this.currentHeading) return;

            const rect = this.currentHeading.getBoundingClientRect();
            const distanceFromBottom = window.innerHeight - rect.bottom;

            const index = this.headings.indexOf(this.currentHeading);
            const previous = this.headings[index - 1];

            if (
                previous &&
                (distanceFromBottom < this.offsetBottom ||
                    this.isInViewport(previous))
            ) {
                this.setActiveHeading(previous);
            }
        }
    }

    /**
     * Binds scroll and ToC click handlers.
     */
    bindEvents() {
        window.addEventListener("scroll", () => {
            if (!this.ticking) {
                requestAnimationFrame(() => {
                    this.onScroll();
                    this.ticking = false;
                });
                this.ticking = true;
            }
        });

        this.toc.addEventListener("click", e => {
            const link = e.target.closest('a[href^="#"]');
            if (!link) return;

            requestAnimationFrame(() => {
                requestAnimationFrame(() => {
                    this.onScroll({ force: true });
                });
            });
        });
    }
}
