/**
 * 3D Carousel component for Insight UI.
 *
 * Creates a rotating 3D carousel effect with perspective transforms.
 * Supports configurable rotation velocity and optional "face camera" mode
 * where items rotate to face the viewer.
 *
 * @example
 * // HTML structure
 * <div data-insight-3D-carousel data-velocity="800" data-face-camera="true">
 *   <div class="carousel-track">
 *     <div><div>Item 1</div></div>
 *     <div><div>Item 2</div></div>
 *   </div>
 *   <div>
 *     <button>Previous</button>
 *     <button>Next</button>
 *   </div>
 * </div>
 */
export class ThreeDCarousel {
    /** @type {WeakMap<HTMLElement, ThreeDCarousel>} Weak references to prevent multiple initialization */
    static instances = new WeakMap();

    /**
     * Creates a new ThreeDCarousel instance.
     *
     * @param {HTMLElement} element - The carousel container element with data-insight-3D-carousel attribute
     */
    constructor(element) {
        // If an instance for this element already exists, return it
        if (ThreeDCarousel.instances.has(element)) {
            return ThreeDCarousel.instances.get(element);
        }

        this.element = element;
        this.carousel = element.firstElementChild;
        this.previousBtn = element.lastElementChild.firstElementChild;
        this.nextBtn = element.lastElementChild.lastElementChild;

        this.faceCamera = element.getAttribute("data-face-camera") === 'true';
        this.distances = [-1100, -750, -750, -550];
        this.screens = [
            window.matchMedia('(min-width: 640px)'),
            window.matchMedia('(min-width: 1024px)'),
            window.matchMedia('(min-width: 1536px)'),
            window.matchMedia('(min-width: 1920px)')
        ];

        this.itemsCount = this.carousel.children.length;
        this.angle = 360 / this.itemsCount;
        this.currentIndex = 0;

        // Respect prefers-reduced-motion for users sensitive to animations
        this.prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        this.spinSettings = {
            duration: this.prefersReducedMotion ? 0 : (parseInt(element.getAttribute("data-velocity")) || 1000),
            fill: "forwards",
        };

        // Store bound handlers for cleanup
        this.boundGotoPrevious = this.gotoPrevious.bind(this);
        this.boundGotoNext = this.gotoNext.bind(this);
        this.boundKeyDown = this.handleKeyDown.bind(this);

        this.bindEvents();

        this.element.__insightInstance = this;
        ThreeDCarousel.instances.set(element, this);

        debugLog("New 3D carousel created: ", this.element);
    }

    /**
     * Binds click and keyboard event listeners for navigation.
     */
    bindEvents() {
        this.previousBtn.addEventListener("click", this.boundGotoPrevious);
        this.nextBtn.addEventListener("click", this.boundGotoNext);
        this.element.addEventListener("keydown", this.boundKeyDown);
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
                this.gotoPrevious();
                break;
            case 'ArrowRight':
                e.preventDefault();
                this.gotoNext();
                break;
        }
    }

    /**
     * Creates animation keyframes for spinning to a specific index.
     *
     * @param {number} index - The target index to spin to
     * @param {boolean} toRight - True if spinning clockwise, false for counter-clockwise
     * @returns {Keyframe[]} Animation keyframes array
     */
    spin(index, toRight) {
        /* get the correct distance for the current window width (media-query) */
        let distance = -850;
        for (let i = this.screens.length - 1; i >= 0; i--) {
            if (this.screens[i].matches) {
                distance = this.distances[i];
                break;
            }
        }

        /* adjust start index, in relation to the spin direction */
        let fromIndex = index;

        if (toRight) fromIndex += 1;
        else fromIndex -= 1;

        /* apply animation */
        return [
            { transform: `translateX(-50%) perspective(1000px) translateZ(${distance}px) rotateX(var(--carousel-tilt)) rotateY(${fromIndex * this.angle}deg)` },
            { transform: `translateX(-50%) perspective(1000px) translateZ(${distance}px) rotateX(var(--carousel-tilt)) rotateY(${index * this.angle}deg)` },
        ];
    }

    /**
     * Rotates items to face the camera when faceCamera mode is enabled.
     */
    rotateFaceCamera() {
        if (!this.faceCamera) return;

        for (const item of this.carousel.children) {
            item.firstElementChild.animate([
                {
                    transform: `rotateY(calc((var(--position) + ${this.currentIndex} - 1) * (360 / var(--quantity)) * -1deg)) rotateX(calc(var(--carousel-tilt) * -1))`
                }
            ], this.spinSettings);
        }
    }

    /**
     * Navigates to the previous item in the carousel (counter-clockwise rotation).
     */
    gotoPrevious() {
        this.currentIndex++;
        this.carousel.animate(this.spin(this.currentIndex, false), this.spinSettings);

        if (this.faceCamera) {
            for (const item of this.carousel.children) {
                item.firstElementChild.animate([{
                    transform: `rotateY(calc((var(--position) + ${this.currentIndex} - 1) * (360 / var(--quantity)) * -1deg)) rotateX(calc(var(--carousel-tilt) * -1))`
                }], this.spinSettings);
            }
        }
    }

    /**
     * Navigates to the next item in the carousel (clockwise rotation).
     */
    gotoNext() {
        this.currentIndex--;
        this.carousel.animate(this.spin(this.currentIndex, true), this.spinSettings);

        if (this.faceCamera) {
            for (const item of this.carousel.children) {
                item.firstElementChild.animate([{
                    transform: `rotateY(calc((var(--position) + ${this.currentIndex} - 1) * (360 / var(--quantity)) * -1deg)) rotateX(calc(var(--carousel-tilt) * -1))`
                }], this.spinSettings);
            }
        }
    }

    /**
     * Destroys the 3D carousel instance and removes all event listeners.
     * Call this before removing the element from DOM.
     */
    destroy() {
        debugLog("Destroy 3D carousel: ", this.element);

        this.previousBtn.removeEventListener("click", this.boundGotoPrevious);
        this.nextBtn.removeEventListener("click", this.boundGotoNext);
        this.element.removeEventListener("keydown", this.boundKeyDown);

        ThreeDCarousel.instances.delete(this.element);
        delete this.element.__insightInstance;

        this.element = null;
        this.carousel = null;
    }

    /**
     * Initializes all 3D carousel instances on the page.
     *
     * @static
     */
    static initAll() {
        document.querySelectorAll("[data-insight-3D-carousel]").forEach(el => new ThreeDCarousel(el));
    }
}
