// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Ring carousel component for Insight UI.
 *
 * Places any items on a turning ring. The ring has as many places as fit the width of the
 * carousel, at most 12; with more items only those around the front one are shown and the
 * others wait hidden at the back. Items get the width the ring sets and the height of the
 * tallest content; every item except the front one is inert.
 *
 * @example
 * // HTML structure (rendered by {% ring_carousel %})
 * <div data-insight-ring-carousel data-tilt="15" data-face-camera="false" class="ring-carousel">
 *   <div class="ring-carousel-stage">
 *     <div class="ring-carousel-ring">
 *       <div class="ring-carousel-item">
 *         <div class="ring-carousel-faces">
 *           <div class="ring-carousel-front">...</div>
 *           <div class="ring-carousel-back"></div>
 *         </div>
 *       </div>
 *     </div>
 *   </div>
 *   <button class="ring-carousel-prev">Previous</button>
 *   <span class="ring-carousel-status"></span>
 *   <button class="ring-carousel-next">Next</button>
 * </div>
 */
export class RingCarousel {
    /** @type {WeakMap<HTMLElement, RingCarousel>} Weak references to prevent multiple initialization */
    static instances = new WeakMap();

    /** @type {number} Most places on the ring */
    static MAX_PLACES = 12;

    /** @type {number} Largest radius of the ring as part of the carousel width */
    static MAX_RADIUS = 0.65;

    /** @type {number} Largest item height as part of the window height; above it the front item scrolls */
    static MAX_HEIGHT = 0.7;

    /**
     * Creates a new RingCarousel instance.
     *
     * @param {HTMLElement} element - The carousel container element with data-insight-ring-carousel attribute
     */
    constructor(element) {
        // If an instance for this element already exists, return it
        if (RingCarousel.instances.has(element)) {
            return RingCarousel.instances.get(element);
        }

        this.element = element;
        this.stage = element.querySelector(".ring-carousel-stage");
        this.ring = element.querySelector(".ring-carousel-ring");
        this.items = [...element.querySelectorAll(".ring-carousel-item")];
        this.prevBtn = element.querySelector(".ring-carousel-prev");
        this.nextBtn = element.querySelector(".ring-carousel-next");
        this.status = element.querySelector(".ring-carousel-status");

        this.tilt = parseFloat(element.dataset.tilt) || 0;
        this.faceCamera = element.dataset.faceCamera === "true";

        this.index = 0;
        this.direction = 1;
        this.placed = new Map();
        this.width = null;
        this.frame = null;

        // Bind handlers for proper cleanup
        this.boundPrev = () => this.goTo(this.index - 1);
        this.boundNext = () => this.goTo(this.index + 1);
        this.boundKeyDown = this.handleKeyDown.bind(this);
        this.boundTouchStart = (e) => { this.startX = e.touches[0].clientX; };
        this.boundTouchEnd = this.handleTouchEnd.bind(this);
        this.boundRelayout = () => this.scheduleRelayout();

        this.init();

        this.element.__insightInstance = this;
        RingCarousel.instances.set(element, this);

        debugLog("New ring carousel created: ", this.element);
    }

    /**
     * Registers the listeners and lays out the ring. The layout follows the width of the carousel and
     * the size of the item content, e.g. images that load later or a larger font.
     */
    init() {
        this.prevBtn?.addEventListener("click", this.boundPrev);
        this.nextBtn?.addEventListener("click", this.boundNext);
        this.element.addEventListener("keydown", this.boundKeyDown);
        this.stage.addEventListener("touchstart", this.boundTouchStart, { passive: true });
        this.stage.addEventListener("touchend", this.boundTouchEnd);
        this.element.addEventListener("load", this.boundRelayout, true);

        if ("ResizeObserver" in window) {
            this.stageObserver = new ResizeObserver(() => {
                if (this.stage.clientWidth === this.width) return;
                this.width = this.stage.clientWidth;
                this.relayout();
            });
            this.stageObserver.observe(this.stage);
            this.contentObserver = new ResizeObserver(this.boundRelayout);
            this.items.forEach((item) => {
                const content = item.querySelector(".ring-carousel-front > *");
                if (content) this.contentObserver.observe(content);
            });
        } else {
            window.addEventListener("resize", this.boundRelayout);
            this.relayout();
        }
    }

    /**
     * Returns whether the carousel is laid out right to left; read on every turn, since the direction
     * can change at runtime (e.g. a language switch).
     *
     * @returns {boolean}
     */
    isRTL() {
        return getComputedStyle(this.element).direction === "rtl";
    }

    /**
     * Lays out the ring without animation and fits the stage to it.
     */
    relayout() {
        this.element.removeAttribute("data-ready");
        this.layout();
        this.fit();
        requestAnimationFrame(() => requestAnimationFrame(() => this.element?.setAttribute("data-ready", "")));
    }

    /**
     * Lays out the ring once per frame, however many sizes changed.
     */
    scheduleRelayout() {
        cancelAnimationFrame(this.frame);
        this.frame = requestAnimationFrame(() => this.relayout());
    }

    /**
     * Returns how many places fit the ring: at most 12, and only as many as keep its radius within
     * part of the carousel width, so the neighbours of the front item stay in view.
     *
     * @param {number} itemWidth - The width of an item
     * @param {number} width - The width of the carousel
     * @returns {number}
     */
    places(itemWidth, width) {
        let places = 3;
        for (let count = 4; count <= RingCarousel.MAX_PLACES; count++) {
            if ((itemWidth / 2) / Math.tan(Math.PI / count) <= width * RingCarousel.MAX_RADIUS) places = count;
        }
        return Math.min(this.items.length, places);
    }

    /**
     * Sizes the items and places them on the ring around the front item.
     */
    layout() {
        const count = this.items.length;
        if (!count) return;
        const width = this.stage.clientWidth;
        // Items take 70% of the carousel on phones, at most 20rem; smaller when tilted, so the ring fits.
        const rem = parseFloat(getComputedStyle(document.documentElement).fontSize) || 16;
        const itemWidth = Math.min(width * (this.tilt ? 0.5 : 0.7), (this.tilt ? 15 : 20) * rem);
        this.items.forEach((item) => {
            item.style.width = `${itemWidth}px`;
            item.style.marginLeft = `${-itemWidth / 2}px`;
            item.style.height = "";
        });
        const natural = Math.max(...this.items.map((item) => item.offsetHeight));
        const height = Math.min(natural, Math.round(window.innerHeight * RingCarousel.MAX_HEIGHT));
        this.items.forEach((item) => { item.style.height = `${height}px`; });

        const places = this.places(itemWidth, width);
        const step = (360 / places) * (this.isRTL() ? -1 : 1);
        // Radius at which neighbouring items just touch, plus a gap; wider when the items face the camera.
        // Tilted items lean in by half their height, so their top edges need that much more room.
        const lean = this.tilt && !this.faceCamera ? (height / 2) * Math.sin(this.tilt * Math.PI / 180) : 0;
        const touching = places > 2 ? (itemWidth / 2) / Math.tan(Math.PI / places) : 0;
        const radius = touching + (this.tilt ? 60 : 16) + lean;
        const half = places / 2;
        // With more items than places the place at the back belongs to the side the ring turns towards,
        // so a new item appears there and the item that leaves fades out there.
        const lowest = this.direction >= 0 ? -(half - 1) : -half;

        this.items.forEach((item, position) => {
            let offset = ((position - this.index) % count + count + count / 2) % count - count / 2;
            const before = this.placed.get(position);
            // A full ring keeps turning in one direction instead of jumping back by a full turn.
            if (count <= places && before) offset += count * Math.round((before.offset - offset) / count);
            const visible = count <= places || (offset >= lowest && offset <= lowest + places - 1);
            // Hidden items wait at the back place, so none of them sits inside a visible item.
            if (!visible) offset = Math.sign(offset) * half;
            const appears = visible && before && !before.visible;
            this.placed.set(position, { offset, visible });

            // Facing the camera undoes the angle; tilted items only undo the tilt, so the front item
            // stands parallel to the camera and the others show the tilt.
            const facing = this.faceCamera
                ? ` rotateY(${-offset * step}deg) rotateX(${this.tilt}deg)`
                : this.tilt ? ` rotateX(${this.tilt}deg)` : "";
            if (appears) {
                item.setAttribute("data-snap", "");
                item.style.setProperty("--insight-ring-carousel-fade", "0");
            }
            item.style.transform = `rotateY(${offset * step}deg) translateZ(${radius}px)${facing}`;
            if (appears) {
                void item.offsetWidth;
                item.removeAttribute("data-snap");
            }
            item.style.visibility = visible ? "visible" : "hidden";
            item.style.setProperty("--insight-ring-carousel-fade", visible ? "1" : "0");
        });
        this.ring.style.transform = `translateZ(${-radius}px) rotateX(${-this.tilt}deg)`;
        this.updateFront();
    }

    /**
     * Makes every item except the front one inert, lets the front item scroll by keyboard when its
     * content is higher than the item and announces the position.
     */
    updateFront() {
        const count = this.items.length;
        const front = ((this.index % count) + count) % count;
        this.items.forEach((item, position) => {
            const current = position === front;
            item.inert = !current;
            item.toggleAttribute("data-current", current);
            const face = item.querySelector(".ring-carousel-front");
            if (current && face.scrollHeight > face.clientHeight) {
                face.tabIndex = 0;
            } else {
                face.removeAttribute("tabindex");
            }
        });
        if (this.status) {
            this.status.textContent = interpolate(gettext("%(current)s of %(total)s"), {
                current: front + 1,
                total: count,
            }, true);
        }
    }

    /**
     * Fits the stage to the ring: measures the items at rest and moves the ring and the perspective
     * origin together, which shifts the picture without changing it.
     */
    fit() {
        if (!this.items.length) return;
        const height = this.items[0].offsetHeight;
        this.items.forEach((item) => { item.style.top = "0px"; });
        this.stage.style.perspectiveOrigin = `50% ${height / 2}px`;
        const top = this.stage.getBoundingClientRect().top;
        let min = Infinity;
        let max = -Infinity;
        this.items.forEach((item) => {
            if (item.style.visibility === "hidden") return;
            const box = item.querySelector(".ring-carousel-front").getBoundingClientRect();
            min = Math.min(min, box.top - top);
            max = Math.max(max, box.bottom - top);
        });
        if (min === Infinity) return;
        const shift = 8 - min;
        this.items.forEach((item) => { item.style.top = `${shift}px`; });
        this.stage.style.perspectiveOrigin = `50% ${shift + height / 2}px`;
        this.stage.style.height = `${max - min + 16}px`;
    }

    /**
     * Turns the ring to an item; the shorter way round for jumps such as Home and End.
     *
     * @param {number} index - The item to bring to the front, may lie outside the item range
     */
    goTo(index) {
        const count = this.items.length;
        if (count < 2) return;
        let step = (index - this.index) % count;
        if (step > count / 2) step -= count;
        if (step < -count / 2) step += count;
        if (!step) return;
        this.direction = Math.sign(step);
        this.index += step;
        this.layout();
    }

    /**
     * Handles keyboard navigation on the controls. Keys inside the items belong to their content,
     * e.g. a text field.
     *
     * @param {KeyboardEvent} e - The keyboard event
     */
    handleKeyDown(e) {
        if (e.target.closest(".ring-carousel-item")) return;
        const forward = this.isRTL() ? -1 : 1;
        const count = this.items.length;
        const front = ((this.index % count) + count) % count;
        const targets = {
            ArrowLeft: this.index - forward,
            ArrowRight: this.index + forward,
            Home: this.index - front,
            End: this.index - front + count - 1,
        };
        if (!(e.key in targets)) return;
        e.preventDefault();
        this.goTo(targets[e.key]);
    }

    /**
     * Handles touch end events for swipe navigation.
     *
     * @param {TouchEvent} e - The touch end event
     */
    handleTouchEnd(e) {
        const diff = e.changedTouches[0].clientX - this.startX;
        if (Math.abs(diff) <= 40) return;
        const forward = (diff < 0) !== this.isRTL();
        this.goTo(this.index + (forward ? 1 : -1));
    }

    /**
     * Destroys the ring carousel instance and removes all event listeners.
     * Call this before removing the element from DOM.
     */
    destroy() {
        debugLog("Destroy ring carousel: ", this.element);

        cancelAnimationFrame(this.frame);
        this.prevBtn?.removeEventListener("click", this.boundPrev);
        this.nextBtn?.removeEventListener("click", this.boundNext);
        this.element.removeEventListener("keydown", this.boundKeyDown);
        this.stage.removeEventListener("touchstart", this.boundTouchStart);
        this.stage.removeEventListener("touchend", this.boundTouchEnd);
        this.element.removeEventListener("load", this.boundRelayout, true);
        window.removeEventListener("resize", this.boundRelayout);
        this.stageObserver?.disconnect();
        this.contentObserver?.disconnect();

        RingCarousel.instances.delete(this.element);
        delete this.element.__insightInstance;

        this.element = null;
    }

    /**
     * Initializes all ring carousel instances on the page.
     *
     * @static
     */
    static initAll() {
        document.querySelectorAll("[data-insight-ring-carousel]").forEach(el => new RingCarousel(el));
    }
}
