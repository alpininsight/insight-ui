export class ThreeDCarousel {
    // Manages all ThreeDCarousel instances of the DOM
    static instances = new WeakMap();

    constructor(wrapper) {
        // If an instance for this element already exists, return it
        if (ThreeDCarousel.instances.has(wrapper)) {
            return ThreeDCarousel.instances.get(wrapper);
        }

        this.wrapper = wrapper;
        this.carousel = wrapper.firstElementChild;
        this.previousBtn = wrapper.lastElementChild.firstElementChild;
        this.nextBtn = wrapper.lastElementChild.lastElementChild;

        this.faceCamera = wrapper.getAttribute("data-carousel-face-camera") === 'true';
        this.distanceSettings = [-1100, -750, -750, -550];
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
            duration: parseInt(wrapper.getAttribute("data-carousel-velocity")) || 1000,
            fill: "forwards",
        };

        this.initEvents();

        ThreeDCarousel.instances.set(wrapper, this);

        debugLog("New 3D carousel created: ", this.wrapper);
    }

    getDistance() {
        // Bestimme den Abstand basierend auf der aktuellen Bildschirmgröße
        for (let i = this.screens.length - 1; i >= 0; i--) {
            if (this.screens[i].matches) return this.distanceSettings[i];
        }
        return -850; // Default
    }

    spin(index, toRight) {
        let distance = this.getDistance();
        let fromIndex = toRight ? index + 1 : index - 1;

        return [
            {
                transform: `translateX(-50%) perspective(1000px) translateZ(${distance}px) rotateX(var(--carousel-tilt)) rotateY(${fromIndex * this.angle}deg)`
            },
            {
                transform: `translateX(-50%) perspective(1000px) translateZ(${distance}px) rotateX(var(--carousel-tilt)) rotateY(${index * this.angle}deg)`
            }
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
        this.rotateFaceCamera();
    }

    gotoNext() {
        this.currentIndex--;
        this.carousel.animate(this.spin(this.currentIndex, true), this.spinSettings);
        this.rotateFaceCamera();
    }

    initEvents() {
        this.previousBtn.addEventListener("click", () => this.gotoPrevious());
        this.nextBtn.addEventListener("click", () => this.gotoNext());
    }

    // Static method for initializing all 3D carousels
    static initAll() {
        document.querySelectorAll("[data-3D-carousel]").forEach(wrapper => new ThreeDCarousel(wrapper));
    }
}
