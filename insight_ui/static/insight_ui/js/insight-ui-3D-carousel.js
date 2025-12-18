class ThreeDCarousel {
    static instances = new WeakMap();

    constructor(carouselWrapper) {
        if (ThreeDCarousel.instances.has(carouselWrapper)) {
            return ThreeDCarousel.instances.get(carouselWrapper);
        }

        this.carouselWrapper = carouselWrapper;

        // Media-Queries
        this.screens = [
            window.matchMedia('(min-width: 640px)'),
            window.matchMedia('(min-width: 1024px)'),
            window.matchMedia('(min-width: 1536px)'),
            window.matchMedia('(min-width: 1920px)')
        ];

        this.faceCamera = carouselWrapper.getAttribute("data-carousel-face-camera") === 'true';
        this.carousel = carouselWrapper.firstElementChild;
        this.previous = carouselWrapper.lastElementChild.firstElementChild;
        this.next = carouselWrapper.lastElementChild.lastElementChild;

        // Distances: first -> smallest screen, last -> biggest screen
        this.distances = [-1100, -750, -750, -550];
        this.itemsCount = this.carousel.children.length;
        this.angle = 360 / this.itemsCount;
        this.currentIndex = 0;

        this.spinSettings = {
            duration: parseInt(carouselWrapper.getAttribute("data-carousel-velocity")),
            fill: "forwards",
        };

        // Store bound handlers for cleanup
        this.boundGotoPrevious = this.gotoPrevious.bind(this);
        this.boundGotoNext = this.gotoNext.bind(this);

        this.bindEvents();

        ThreeDCarousel.instances.set(carouselWrapper, this);

        debugLog("New 3D carousel created: ", this.carouselWrapper);
    }

    bindEvents() {
        this.previous.addEventListener("click", this.boundGotoPrevious);
        this.next.addEventListener("click", this.boundGotoNext);
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
        this.previous.removeEventListener("click", this.boundGotoPrevious);
        this.next.removeEventListener("click", this.boundGotoNext);

        ThreeDCarousel.instances.delete(this.carouselWrapper);
        this.carouselWrapper = null;
        this.carousel = null;
    }

    // Static method for initializing all 3D carousels
    static initAll() {
        document.querySelectorAll("[data-3D-carousel]").forEach(el => {
            if (!ThreeDCarousel.instances.has(el)) {
                new ThreeDCarousel(el);
            }
        });
    }

    // Backwards compatibility
    static init() {
        ThreeDCarousel.initAll();
    }
}

window.InsightUI = window.InsightUI || {};
window.InsightUI.ThreeDCarousel = ThreeDCarousel;
