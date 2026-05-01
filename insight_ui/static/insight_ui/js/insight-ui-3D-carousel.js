export class ThreeDCarousel {
    // Weak references used to prevent multiple initialization of the same instance
    static instances = new WeakMap();

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
        this.spinSettings = {
            duration: parseInt(element.getAttribute("data-velocity")) || 1000,
            fill: "forwards",
        };

        // Store bound handlers for cleanup
        this.boundGotoPrevious = this.gotoPrevious.bind(this);
        this.boundGotoNext = this.gotoNext.bind(this);

        this.bindEvents();

        this.element.__insightInstance = this;
        ThreeDCarousel.instances.set(element, this);

        debugLog("New 3D carousel created: ", this.element);
    }

    bindEvents() {
        this.previousBtn.addEventListener("click", this.boundGotoPrevious);
        this.nextBtn.addEventListener("click", this.boundGotoNext);
    }

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
            { transform: "translateX(-50%) perspective(1000px) translateZ(" + distance + "px) rotateX(var(--carousel-tilt)) rotateY(" + (fromIndex * this.angle) + "deg)" },
            { transform: "translateX(-50%) perspective(1000px) translateZ(" + distance + "px) rotateX(var(--carousel-tilt)) rotateY(" + (index * this.angle) + "deg)" },
        ];
    }

    rotateFaceCamera() {
        if (!this.faceCamera) return;

        for (let item of this.carousel.children) {
            item.firstElementChild.animate([
                {
                    transform: `rotateY(calc((var(--position) + ${this.currentIndex} - 1) * (360 / var(--quantity)) * -1deg)) rotateX(calc(var(--carousel-tilt) * -1))`
                }
            ], this.spinSettings);
        }
    }

    gotoPrevious() {
        this.currentIndex++;
        this.carousel.animate(this.spin(this.currentIndex, false), this.spinSettings);

        if (this.faceCamera) {
            for (let item of this.carousel.children) {
                item.firstElementChild.animate([{ transform: "rotateY(calc((var(--position) + " + this.currentIndex + " - 1) * (360 / var(--quantity)) * -1deg)) rotateX(calc(var(--carousel-tilt) * -1))" }], this.spinSettings);
            }
        }
    }

    gotoNext() {
        this.currentIndex--;
        this.carousel.animate(this.spin(this.currentIndex, true), this.spinSettings);

        if (this.faceCamera) {
            for (let item of this.carousel.children) {
                item.firstElementChild.animate([{ transform: "rotateY(calc((var(--position) + " + this.currentIndex + " - 1) * (360 / var(--quantity)) * -1deg)) rotateX(calc(var(--carousel-tilt) * -1))" }], this.spinSettings);
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

        ThreeDCarousel.instances.delete(this.element);
        delete this.element.__insightInstance;

        this.element = null;
        this.carousel = null;
    }

    // Static method for initializing all 3D carousels
    static initAll() {
        document.querySelectorAll("[data-insight-3D-carousel]").forEach(el => new ThreeDCarousel(el));
    }
}
