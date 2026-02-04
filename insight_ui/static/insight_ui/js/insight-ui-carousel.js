export class Carousel {
    // Manages all Carousel instances of the DOM
    static instances = new WeakMap();

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

        this.dots = [...this.element.querySelectorAll(".carousel-dot")];
        this.dots.forEach((dot, i) => {
            dot.addEventListener("click", () => {
                this.index = i;
                this.update();
                this.restartAutoplay();
            });
        });

        this.init();

        Carousel.instances.set(element, this);

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

        this.prevBtn.addEventListener("click", () => {
            this.prev();
            this.restartAutoplay();
        });

        this.nextBtn.addEventListener("click", () => {
            this.next();
            this.restartAutoplay();
        });

        this.element.addEventListener("touchstart", (e) => {
            this.startX = e.touches[0].clientX;
        });

        this.element.addEventListener("touchend", (e) => {
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
        });

        if (this.autoplayEnabled) this.startAutoplay();

        window.addEventListener("resize", () => this.resizeItems());

        // Add MutationObserver for "dir" changes
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (
                    mutation.type === 'attributes' &&
                    mutation.attributeName === 'dir'
                ) {
                    this.isRTL = document.documentElement.getAttribute('dir') == "rtl";
                    this.update();
                }
            });
        });

        observer.observe(document.documentElement, {
            attributes: true,
            attributeFilter: ['dir']
        });
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
            this.indexText.textContent = `Seite ${this.index + 1} / ${this.totalSlides}`;
        }
    }

    // Static method for initializing all carousels
    static initAll() {
        document.querySelectorAll('[data-insight-carousel]').forEach(el => new Carousel(el));
    }
};
