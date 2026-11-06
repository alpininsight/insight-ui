// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Carousel component for Insight UI.
 *
 * Browses any items page by page, with autoplay, page dots, touch gestures, keyboard
 * navigation and RTL layouts. How many items fit on a page follows the width of the
 * carousel when a minimum item width is set; items on other pages are inert, so the
 * keyboard focus cannot move into hidden items.
 *
 * @example
 * // HTML structure (rendered by {% carousel %})
 * <div data-insight-carousel data-items-per-slide="3" data-min-item-width="16rem" data-show-dots="true">
 *   <div class="carousel-viewport">
 *     <div class="carousel-track">
 *       <div class="carousel-item">...</div>
 *     </div>
 *   </div>
 *   <button class="carousel-prev">Previous</button>
 *   <div class="carousel-dots"></div>
 *   <span class="carousel-index-text"></span>
 *   <button class="carousel-next">Next</button>
 * </div>
 *
 * // JavaScript initialization
 * Carousel.initAll();
 */
export class Carousel {
    /** @type {WeakMap<HTMLElement, Carousel>} Weak references to prevent multiple initialization */
    static instances = new WeakMap();

    /** @type {string[]} Classes of a page dot button; 24px wide, so it meets the minimum target size */
    static DOT_CLASSES = ["carousel-dot", "grid", "place-items-center", "size-6", "rounded-insight-full"];

    /** @type {string[]} Classes of the visible mark inside a dot; the mark of the current page is filled */
    static DOT_MARK_CLASSES = ["size-3", "border", "border-insight-surface", "rounded-insight-full", "transition"];

    /**
     * Creates a new Carousel instance.
     *
     * @param {HTMLElement} element - The carousel container element with data-insight-carousel attribute
     */
    constructor(element) {
        // If an instance for this element already exists, return it
        if (Carousel.instances.has(element)) {
            return Carousel.instances.get(element);
        }

        this.element = element;
        this.isRTL =
            this.element.dir === "rtl" ||
            document.documentElement.dir === "rtl" ||
            getComputedStyle(this.element).direction === "rtl";
        this.viewport = element.querySelector(".carousel-viewport") || element;
        this.track = element.querySelector(".carousel-track");
        this.items = [...element.querySelectorAll(".carousel-item")];
        this.prevBtn = element.querySelector(".carousel-prev");
        this.nextBtn = element.querySelector(".carousel-next");
        this.dotsContainer = element.querySelector(".carousel-dots");
        this.indexText = element.querySelector(".carousel-index-text");

        this.autoplayEnabled = element.dataset.autoplay === "true";
        this.showDots = element.dataset.showDots === "true";
        this.showIndex = element.dataset.showIndex === "true";
        this.maxItemsPerSlide = Math.max(1, parseInt(element.dataset.itemsPerSlide || "1"));
        this.minItemWidth = element.dataset.minItemWidth || "";

        this.itemsPerSlide = 0;
        this.totalSlides = 0;
        this.index = 0;
        this.autoplayInterval = null;
        this.dots = [];
        this.dotsHidden = false;

        // Bind handlers for proper cleanup
        this.boundPrevClick = () => { this.prev(); this.restartAutoplay(); };
        this.boundNextClick = () => { this.next(); this.restartAutoplay(); };
        this.boundTouchStart = (e) => { this.startX = e.touches[0].clientX; };
        this.boundTouchEnd = this.handleTouchEnd.bind(this);
        this.boundWindowResize = () => this.layout();
        this.boundKeyDown = this.handleKeyDown.bind(this);
        this.boundMouseEnter = () => this.pauseAutoplay();
        this.boundMouseLeave = () => this.resumeAutoplay();
        this.boundFocusIn = () => this.pauseAutoplay();
        this.boundFocusOut = () => this.resumeAutoplay();
        this.boundDotsClick = this.handleDotsClick.bind(this);
        this.autoplayPaused = false;

        this.init();

        this.element.__insightInstance = this;
        Carousel.instances.set(this.element, this);

        debugLog("New carousel created: ", this.element);
    }

    /**
     * Lay out the first page, register the listeners and start autoplay if enabled.
     * The layout follows the width of the carousel, also when only its container resizes.
     */
    init() {
        this.layout();

        this.prevBtn.addEventListener("click", this.boundPrevClick);
        this.nextBtn.addEventListener("click", this.boundNextClick);
        this.dotsContainer?.addEventListener("click", this.boundDotsClick);
        this.element.addEventListener("touchstart", this.boundTouchStart);
        this.element.addEventListener("touchend", this.boundTouchEnd);
        this.element.addEventListener("keydown", this.boundKeyDown);

        // Pause autoplay on hover/focus for users who need more time
        if (this.autoplayEnabled) {
            this.element.addEventListener("mouseenter", this.boundMouseEnter);
            this.element.addEventListener("mouseleave", this.boundMouseLeave);
            this.element.addEventListener("focusin", this.boundFocusIn);
            this.element.addEventListener("focusout", this.boundFocusOut);
            this.startAutoplay();
        }

        if ("ResizeObserver" in window) {
            this.viewportWidth = null;
            this.resizeObserver = new ResizeObserver(([entry]) => {
                if (entry.contentRect.width === this.viewportWidth) return;
                this.viewportWidth = entry.contentRect.width;
                this.layout();
            });
            this.resizeObserver.observe(this.viewport);
        } else {
            window.addEventListener("resize", this.boundWindowResize);
        }

        // Add MutationObserver for "dir" changes
        this.dirObserver = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (
                    mutation.type === 'attributes' &&
                    mutation.attributeName === 'dir'
                ) {
                    this.isRTL = document.documentElement.getAttribute('dir') === "rtl";
                    this.update();
                }
            });
        });

        this.dirObserver.observe(document.documentElement, {
            attributes: true,
            attributeFilter: ['dir']
        });
    }

    /**
     * Returns how many items fit on a page: at most data-items-per-slide, and with a minimum item
     * width only as many as fit into the current width, at least one.
     *
     * @returns {number}
     */
    fittingItemsPerSlide() {
        if (!this.minItemWidth) return this.maxItemsPerSlide;
        const minWidth = this.measure(this.minItemWidth);
        const width = this.viewport.clientWidth;
        if (!minWidth || !width) return this.maxItemsPerSlide;
        return Math.max(1, Math.min(this.maxItemsPerSlide, Math.floor(width / minWidth)));
    }

    /**
     * Converts a CSS length such as "16rem" to pixels in the context of the carousel.
     *
     * @param {string} length - The CSS length
     * @returns {number} The width in pixels
     */
    measure(length) {
        const probe = document.createElement("div");
        probe.style.cssText = `position:absolute;visibility:hidden;width:${length}`;
        this.viewport.append(probe);
        const width = probe.getBoundingClientRect().width;
        probe.remove();
        return width;
    }

    /**
     * Sizes the items for the number that fits on a page and rebuilds the page dots. The page
     * keeps showing the item that was first on it.
     */
    layout() {
        const itemsPerSlide = this.fittingItemsPerSlide();
        const firstItem = this.index * (this.itemsPerSlide || itemsPerSlide);
        const changed = itemsPerSlide !== this.itemsPerSlide;
        this.itemsPerSlide = itemsPerSlide;
        this.totalSlides = Math.ceil(this.items.length / itemsPerSlide);

        this.items.forEach(item => {
            item.style.flex = `0 0 ${100 / itemsPerSlide}%`;
        });
        this.index = Math.min(Math.floor(firstItem / itemsPerSlide), Math.max(this.totalSlides - 1, 0));
        if (changed) this.buildDots();
        this.fitDots();
        this.update();
    }

    /**
     * Creates one dot per page; the dots are buttons that name their page.
     */
    buildDots() {
        if (!this.showDots || !this.dotsContainer) return;
        this.dots = Array.from({ length: this.totalSlides }, (_, page) => {
            const dot = document.createElement("button");
            dot.type = "button";
            dot.classList.add(...Carousel.DOT_CLASSES);
            dot.dataset.index = String(page);
            dot.setAttribute("aria-label", interpolate(gettext("Go to page %(page)s"), { page: page + 1 }, true));
            const mark = document.createElement("span");
            mark.classList.add(...Carousel.DOT_MARK_CLASSES);
            dot.append(mark);
            return dot;
        });
        this.dotsContainer.replaceChildren(...this.dots);
    }

    /**
     * Shows the page number instead of the dots when the dots do not fit into the control row.
     */
    fitDots() {
        if (!this.showDots || !this.dotsContainer) return;
        const row = this.dotsContainer.parentElement;
        this.dotsContainer.hidden = false;
        if (this.indexText) this.indexText.hidden = !this.showIndex;
        this.dotsHidden = row.scrollWidth > row.clientWidth;
        this.dotsContainer.hidden = this.dotsHidden;
        if (this.indexText) this.indexText.hidden = !this.showIndex && !this.dotsHidden;
    }

    /**
     * Shows the page of a clicked dot.
     *
     * @param {MouseEvent} event - The click event
     */
    handleDotsClick(event) {
        const dot = event.target.closest(".carousel-dot");
        if (!dot) return;
        this.goTo(parseInt(dot.dataset.index));
    }

    /**
     * Shows a page and restarts autoplay.
     *
     * @param {number} index - The page to show
     */
    goTo(index) {
        if (!this.totalSlides) return;
        this.index = (index + this.totalSlides) % this.totalSlides;
        this.update();
        this.restartAutoplay();
    }

    /**
     * Handles touch end events for swipe navigation.
     *
     * @param {TouchEvent} e - The touch end event
     */
    handleTouchEnd(e) {
        const endX = e.changedTouches[0].clientX;
        const diff = endX - this.startX;
        if (Math.abs(diff) > 50) {
            if ((diff > 0) !== this.isRTL) {
                this.prev();
            } else {
                this.next();
            }
            this.restartAutoplay();
        }
    }

    /**
     * Handles keyboard navigation on the controls. Keys inside the items belong to their content,
     * e.g. a text field. On a dot the focus follows to the dot of the new page, so Enter stays there.
     *
     * @param {KeyboardEvent} e - The keyboard event
     */
    handleKeyDown(e) {
        if (e.target.closest(".carousel-item")) return;
        const forward = this.isRTL ? -1 : 1;
        const targets = {
            ArrowLeft: this.index - forward,
            ArrowRight: this.index + forward,
            Home: 0,
            End: this.totalSlides - 1,
        };
        if (!(e.key in targets)) return;
        e.preventDefault();
        this.goTo(targets[e.key]);
        if (e.target.closest(".carousel-dot")) this.dots[this.index]?.focus();
    }

    /**
     * Pauses autoplay when user hovers or focuses the carousel.
     */
    pauseAutoplay() {
        if (this.autoplayEnabled && !this.autoplayPaused) {
            this.stopAutoplay();
            this.autoplayPaused = true;
        }
    }

    /**
     * Resumes autoplay when user stops hovering or focus leaves the carousel.
     */
    resumeAutoplay() {
        if (this.autoplayEnabled && this.autoplayPaused) {
            this.startAutoplay();
            this.autoplayPaused = false;
        }
    }

    /**
     * Translate the track to the current page, make items on other pages inert and update the
     * page dots and the page number.
     */
    update() {
        const offset = this.index * 100 * (this.isRTL ? 1 : -1);
        this.track.style.transform = `translateX(${offset}%)`;
        const first = this.index * this.itemsPerSlide;
        this.items.forEach((item, position) => {
            item.inert = position < first || position >= first + this.itemsPerSlide;
        });
        if (this.showDots) this.updateDots();
        if (this.showIndex || this.dotsHidden) this.updateIndexText();
    }

    /**
     * Show the next page; after the last page the first one follows.
     */
    next() {
        if (!this.totalSlides) return;
        this.index = (this.index + 1) % this.totalSlides;
        this.update();
    }

    /**
     * Show the previous page; before the first page the last one follows.
     */
    prev() {
        if (!this.totalSlides) return;
        this.index = (this.index - 1 + this.totalSlides) % this.totalSlides;
        this.update();
    }

    /**
     * Start autoplay of the carousel, which switches to the next page every 5 seconds.
     */
    startAutoplay() {
        this.autoplayInterval = setInterval(() => this.next(), 5000);
    }

    /**
     * Stop autoplay by clearing interval.
     */
    stopAutoplay() {
        clearInterval(this.autoplayInterval);
    }

    /**
     * Stop the autoplay loop and start it again, to reset the interval (only if autoplay is activated).
     */
    restartAutoplay() {
        if (this.autoplayEnabled) {
            this.stopAutoplay();
            this.startAutoplay();
        }
    }

    /**
     * Fill the dot of the current page and mark it as current. Only that dot is in the tab order;
     * the arrow keys move between the dots.
     */
    updateDots() {
        this.dots.forEach((dot, i) => {
            const current = i === this.index;
            dot.firstElementChild.classList.toggle("bg-insight-primary", current);
            dot.firstElementChild.classList.toggle("bg-transparent", !current);
            dot.tabIndex = current ? 0 : -1;
            if (current) {
                dot.setAttribute("aria-current", "true");
            } else {
                dot.removeAttribute("aria-current");
            }
        });
    }

    /**
     * Update the current page number (if shown).
     */
    updateIndexText() {
        if (this.indexText) {
            const text = gettext('Page %(current)s / %(total)s');
            this.indexText.textContent = interpolate(text, {
                current: this.index + 1,
                total: this.totalSlides
            }, true);
        }
    }

    /**
     * Destroys the carousel instance and removes all event listeners.
     * Call this before removing the element from DOM.
     */
    destroy() {
        debugLog("Destroy carousel: ", this.element);

        // Stop autoplay interval
        this.stopAutoplay();

        this.prevBtn.removeEventListener("click", this.boundPrevClick);
        this.nextBtn.removeEventListener("click", this.boundNextClick);
        this.dotsContainer?.removeEventListener("click", this.boundDotsClick);
        this.element.removeEventListener("touchstart", this.boundTouchStart);
        this.element.removeEventListener("touchend", this.boundTouchEnd);
        this.element.removeEventListener("keydown", this.boundKeyDown);
        this.element.removeEventListener("mouseenter", this.boundMouseEnter);
        this.element.removeEventListener("mouseleave", this.boundMouseLeave);
        this.element.removeEventListener("focusin", this.boundFocusIn);
        this.element.removeEventListener("focusout", this.boundFocusOut);
        window.removeEventListener("resize", this.boundWindowResize);
        this.resizeObserver?.disconnect();

        // Disconnect RTL observer
        if (this.dirObserver) {
            this.dirObserver.disconnect();
            this.dirObserver = null;
        }

        Carousel.instances.delete(this.element);
        delete this.element.__insightInstance;

        this.element = null;
    }

    /**
     * Initializes all carousel instances on the page.
     * Finds all elements with `data-insight-carousel` attribute and creates Carousel instances.
     *
     * @static
     */
    static initAll() {
        document.querySelectorAll('[data-insight-carousel]').forEach(el => new Carousel(el));
    }
}
