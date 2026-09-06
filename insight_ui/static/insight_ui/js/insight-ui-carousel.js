// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Carousel component for Insight UI.
 *
 * A responsive image/content carousel with support for autoplay, pagination dots,
 * touch gestures, keyboard navigation, and RTL layouts.
 *
 * @example
 * // HTML structure
 * <div data-insight-carousel data-autoplay="true" data-show-dots="true">
 *   <div class="carousel-track">
 *     <div class="carousel-item">...</div>
 *   </div>
 *   <button class="carousel-prev">Previous</button>
 *   <button class="carousel-next">Next</button>
 * </div>
 *
 * // JavaScript initialization
 * Carousel.initAll();
 */
export class Carousel {
    /** @type {WeakMap<HTMLElement, Carousel>} Weak references to prevent multiple initialization */
    static instances = new WeakMap();

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
        this.track = element.querySelector(".carousel-track");
        this.items = [...element.querySelectorAll(".carousel-item")];
        this.prevBtn = element.querySelector(".carousel-prev");
        this.nextBtn = element.querySelector(".carousel-next");
        this.dotsContainer = element.querySelector(".carousel-dots");
        this.indexText = element.querySelector(".carousel-index-text");

        this.autoplayEnabled = element.dataset.autoplay === "true";
        this.showDots = element.dataset.showDots === "true";
        this.showIndex = element.dataset.showIndex === "true";
        this.itemsPerSlide = parseInt(element.dataset.itemsPerSlide || "1");

        this.totalSlides = Math.ceil(this.items.length / this.itemsPerSlide);
        this.index = 0;
        this.autoplayInterval = null;

        // Bind handlers for proper cleanup
        this.boundPrevClick = () => { this.prev(); this.restartAutoplay(); };
        this.boundNextClick = () => { this.next(); this.restartAutoplay(); };
        this.boundTouchStart = (e) => { this.startX = e.touches[0].clientX; };
        this.boundTouchEnd = this.handleTouchEnd.bind(this);
        this.boundWindowResize = () => this.resizeItems();
        this.boundKeyDown = this.handleKeyDown.bind(this);
        this.boundMouseEnter = () => this.pauseAutoplay();
        this.boundMouseLeave = () => this.resumeAutoplay();
        this.boundFocusIn = () => this.pauseAutoplay();
        this.boundFocusOut = () => this.resumeAutoplay();
        this.boundDotClicks = [];
        this.autoplayPaused = false;

        this.dots = [...this.element.querySelectorAll(".carousel-dot")];
        this.dots.forEach((dot, i) => {
            const handler = () => {
                this.index = i;
                this.update();
                this.restartAutoplay();
            };
            this.boundDotClicks.push({ element: dot, handler });
            dot.addEventListener("click", handler);
        });

        this.init();

        this.element.__insightInstance = this;
        Carousel.instances.set(this.element, this);

        debugLog("New carousel created: ", this.element);
    }

    /**
     * Initialize the carousel with start values e.g. index = 0, to show the first page.
     * Add EventListeners to the 'next' and 'previous' Buttons and for the resize event.
     * Add MutationObserver for changes of the "dir" attribute of the <html> tag.
     * If autoplay is activated, start the autoplay interval.
     */
    init() {
        this.resizeItems();
        if (this.showIndex) this.updateIndexText();
        this.update();

        this.prevBtn.addEventListener("click", this.boundPrevClick);
        this.nextBtn.addEventListener("click", this.boundNextClick);
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

        window.addEventListener("resize", this.boundWindowResize);

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
     * Handles keyboard events for carousel navigation.
     *
     * @param {KeyboardEvent} e - The keyboard event
     */
    handleKeyDown(e) {
        switch (e.key) {
            case 'ArrowLeft':
                e.preventDefault();
                if (this.isRTL) { this.next(); } else { this.prev(); }
                this.restartAutoplay();
                break;
            case 'ArrowRight':
                e.preventDefault();
                if (this.isRTL) { this.prev(); } else { this.next(); }
                this.restartAutoplay();
                break;
            case 'Home':
                e.preventDefault();
                this.index = 0;
                this.update();
                this.restartAutoplay();
                break;
            case 'End':
                e.preventDefault();
                this.index = this.totalSlides - 1;
                this.update();
                this.restartAutoplay();
                break;
        }
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
     * Resize elements to fit the carousel width.
     */
    resizeItems() {
        this.items.forEach(item => {
            item.style.flex = `0 0 ${100 / this.itemsPerSlide}%`;
        });
    }

    /**
     * Translate the carousel items to show the elements of current page.
     * Update the pagination bubbles and the page number in the bottom corner.
     */
    update() {
        const offset = this.index * 100 * (this.isRTL ? 1 : -1);
        this.track.style.transform = `translateX(${offset}%)`;
        if (this.showDots) this.updateDots();
        if (this.showIndex) this.updateIndexText();
    }

    /**
     * Update current page index and translate the carousel items to show the elements of
     * the next page. Update the pagination bubbles and the page number in the bottom corner.
     */
    next() {
        this.index = (this.index + 1) % this.totalSlides;
        this.update();
    }

    /**
     * Update current page index and translate the carousel items to show the elements of
     * the previous page. Update the pagination bubbles and the page number in the bottom corner.
     */
    prev() {
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
     * Set the corresponding css classes to the pagination bubbles, to highlight the active page.
     */
    updateDots() {
        this.dots.forEach((dot, i) => {
            dot.classList.toggle("bg-insight-primary", i === this.index);
            dot.classList.toggle("bg-transparent", i !== this.index);
        });
    }

    /**
     * Update current page number in the bottom corner (if shown).
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

        // Remove button listeners
        this.prevBtn.removeEventListener("click", this.boundPrevClick);
        this.nextBtn.removeEventListener("click", this.boundNextClick);

        // Remove touch listeners
        this.element.removeEventListener("touchstart", this.boundTouchStart);
        this.element.removeEventListener("touchend", this.boundTouchEnd);

        // Remove keyboard listener
        this.element.removeEventListener("keydown", this.boundKeyDown);

        // Remove hover/focus listeners for autoplay pause
        this.element.removeEventListener("mouseenter", this.boundMouseEnter);
        this.element.removeEventListener("mouseleave", this.boundMouseLeave);
        this.element.removeEventListener("focusin", this.boundFocusIn);
        this.element.removeEventListener("focusout", this.boundFocusOut);

        // Remove window resize listener
        window.removeEventListener("resize", this.boundWindowResize);

        // Remove dot click handlers
        this.boundDotClicks.forEach(({ element, handler }) => {
            element.removeEventListener("click", handler);
        });
        this.boundDotClicks = [];

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
