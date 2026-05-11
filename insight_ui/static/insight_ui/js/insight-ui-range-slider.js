/**
 * Insight UI - Range Slider Component
 *
 * A range slider with responsive legend that can adapt to available space.
 * Supports single-thumb and dual-thumb (range selection) modes.
 *
 * Legend modes:
 * - static: No responsive adjustment (default)
 * - skip: Progressively hides legend items when space is limited
 * - rotate: Rotates legend text vertically when space is limited
 */

export class RangeSlider {
    // Weak references used to prevent multiple initialization of the same instance
    static instances = new WeakMap();

    // Tailwind classes for hidden items
    static HIDDEN_CLASSES = ["invisible", "w-0", "overflow-hidden"];
    // Tailwind classes for rotated legend container
    static ROTATE_MODE_CLASSES = ["items-start", "h-auto", "min-h-16"];
    // Tailwind classes for rotated items
    static ROTATED_CLASSES = [
        "[writing-mode:vertical-rl]",
        "[text-orientation:mixed]",
        "rotate-180",
        "whitespace-nowrap",
        "max-h-20",
        "overflow-hidden",
        "text-ellipsis"
    ];

    constructor(element) {
        // If an instance for this element already exists, return it
        if (RangeSlider.instances.has(element)) {
            return RangeSlider.instances.get(element);
        }

        this.element = element;
        this.legend = element.querySelector(".slider-legend");
        this.legendItems = this.legend ? [...this.legend.querySelectorAll(".slider-legend-item")] : [];
        this.legendMode = element.dataset.legendMode || "static";

        // Detect RTL mode
        this.isRTL = this.detectRTL();

        // Detect dual-range mode
        const inputs = element.querySelectorAll('input[type="range"]');
        this.isDualRange = inputs.length === 2;

        if (this.isDualRange) {
            this.inputMin = element.querySelector('.slider-input-min');
            this.inputMax = element.querySelector('.slider-input-max');
            this.track = element.querySelector('.slider-track');
        } else {
            this.input = inputs[0];
        }

        // Bind handlers for proper cleanup
        this.boundResizeHandler = this.adjustLegend.bind(this);

        if (this.isDualRange) {
            this.boundMinInputHandler = this.handleMinInput.bind(this);
            this.boundMaxInputHandler = this.handleMaxInput.bind(this);
        } else {
            this.boundInputHandler = this.updateProgress.bind(this);
        }

        this.init();

        this.element.__insightInstance = this;
        RangeSlider.instances.set(this.element, this);

        debugLog("New RangeSlider created: ", this.element, this.isDualRange ? "(dual-range)" : "(single)", this.isRTL ? "(RTL)" : "(LTR)");
    }

    /**
     * Detect if the document or element is in RTL mode.
     * @returns {boolean} True if RTL mode is active
     */
    detectRTL() {
        return this.element.dir === "rtl" ||
            document.documentElement.dir === "rtl" ||
            getComputedStyle(this.element).direction === "rtl";
    }

    /**
     * Initialize the range slider.
     */
    init() {
        if (this.isDualRange) {
            this.inputMin.addEventListener("input", this.boundMinInputHandler);
            this.inputMax.addEventListener("input", this.boundMaxInputHandler);
            this.updateDualProgress();
        } else if (this.input) {
            this.input.addEventListener("input", this.boundInputHandler);
            this.updateProgress();
        }

        if (this.legendMode !== "static" && this.legendItems.length >= 2) {
            window.addEventListener("resize", this.boundResizeHandler);
            this.adjustLegend();
        }

        // Add MutationObserver for RTL changes on document
        this.dirObserver = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === "attributes" && mutation.attributeName === "dir") {
                    this.isRTL = this.detectRTL();
                    if (this.isDualRange) {
                        this.updateDualProgress();
                    }
                    debugLog("RangeSlider RTL changed: ", this.isRTL);
                }
            });
        });

        this.dirObserver.observe(document.documentElement, {
            attributes: true,
            attributeFilter: ["dir"]
        });
    }

    /**
     * Handle min input changes in dual-range mode.
     * Ensures min value doesn't exceed max value.
     */
    handleMinInput() {
        const minVal = Number(this.inputMin.value);
        const maxVal = Number(this.inputMax.value);

        if (minVal > maxVal) {
            this.inputMin.value = maxVal;
        }

        this.updateDualProgress();
    }

    /**
     * Handle max input changes in dual-range mode.
     * Ensures max value doesn't go below min value.
     */
    handleMaxInput() {
        const minVal = Number(this.inputMin.value);
        const maxVal = Number(this.inputMax.value);

        if (maxVal < minVal) {
            this.inputMax.value = minVal;
        }

        this.updateDualProgress();
    }

    /**
     * Update the progress bar visual for dual-range mode.
     * Shows the selected range between min and max thumbs.
     * Also updates ARIA attributes for accessibility.
     * Handles RTL mode where thumbs are visually inverted.
     */
    updateDualProgress() {
        const min = Number(this.inputMin.min || 0);
        const max = Number(this.inputMin.max || 100);
        const minVal = Number(this.inputMin.value);
        const maxVal = Number(this.inputMax.value);

        const minPercent = ((minVal - min) / (max - min)) * 100;
        const maxPercent = ((maxVal - min) / (max - min)) * 100;

        this.element.style.setProperty("--range-min", `${minPercent}%`);
        this.element.style.setProperty("--range-max", `${maxPercent}%`);

        // Update track highlight position (handle RTL)
        if (this.track) {
            const trackWidth = maxPercent - minPercent;

            if (this.isRTL) {
                // In RTL: thumbs are visually inverted
                // - min thumb appears at (100 - minPercent)% from left
                // - max thumb appears at (100 - maxPercent)% from left
                // Track goes from max thumb position to min thumb position
                this.track.style.right = "auto";
                this.track.style.left = `${100 - maxPercent}%`;
            } else {
                // In LTR: min value is on the left, max value is on the right
                this.track.style.right = "auto";
                this.track.style.left = `${minPercent}%`;
            }
            this.track.style.width = `${trackWidth}%`;
        }

        // Update ARIA attributes for screen readers
        this.inputMin.setAttribute("aria-valuenow", minVal);
        this.inputMax.setAttribute("aria-valuenow", maxVal);
    }

    /**
     * Update the progress bar visual for single-thumb mode (CSS custom property).
     * Also updates ARIA attributes for accessibility.
     */
    updateProgress() {
        const min = Number(this.input.min || 0);
        const max = Number(this.input.max || 100);
        const val = Number(this.input.value);

        const percent = ((val - min) / (max - min)) * 100;
        this.element.style.setProperty("--range-progress", `${percent}%`);

        // Update ARIA attribute for screen readers
        this.input.setAttribute("aria-valuenow", val);
    }

    /**
     * Get the current value(s) of the slider.
     * @returns {number|{min: number, max: number}} Single value or object with min/max
     */
    getValue() {
        if (this.isDualRange) {
            return {
                min: Number(this.inputMin.value),
                max: Number(this.inputMax.value)
            };
        }
        return Number(this.input.value);
    }

    /**
     * Set the value(s) of the slider.
     * @param {number|{min: number, max: number}} value - Single value or object with min/max
     */
    setValue(value) {
        if (this.isDualRange && typeof value === "object") {
            if (value.min !== undefined) {
                this.inputMin.value = value.min;
            }
            if (value.max !== undefined) {
                this.inputMax.value = value.max;
            }
            this.updateDualProgress();
        } else if (!this.isDualRange) {
            this.input.value = value;
            this.updateProgress();
        }
    }

    /**
     * Check if legend items are overlapping.
     * @returns {boolean} True if items overlap
     */
    isOverlapping() {
        const legendRect = this.legend.getBoundingClientRect();
        let totalWidth = 0;

        this.legendItems.forEach(item => {
            if (!item.classList.contains("invisible")) {
                totalWidth += item.getBoundingClientRect().width;
            }
        });

        // Add some spacing buffer (8px per visible item)
        const visibleCount = this.legendItems.filter(i => !i.classList.contains("invisible")).length;
        totalWidth += (visibleCount - 1) * 8;

        return totalWidth > legendRect.width;
    }

    /**
     * Reset all legend items to their default visible state.
     */
    resetLegend() {
        this.legendItems.forEach(item => {
            item.classList.remove(...RangeSlider.HIDDEN_CLASSES, ...RangeSlider.ROTATED_CLASSES);
        });
        this.legend.classList.remove(...RangeSlider.ROTATE_MODE_CLASSES);
    }

    /**
     * Adjust the legend based on available space and legend mode.
     */
    adjustLegend() {
        if (this.legendMode === "static" || this.legendItems.length < 2) return;

        // Reset all items to visible and horizontal
        this.resetLegend();

        if (this.legendMode === "skip") {
            this.applySkipMode();
        } else if (this.legendMode === "rotate") {
            this.applyRotateMode();
        }
    }

    /**
     * Apply skip mode: progressively hide legend items.
     */
    applySkipMode() {
        let skipLevel = 2;
        const itemCount = this.legendItems.length;

        while (this.isOverlapping() && skipLevel <= itemCount) {
            this.legendItems.forEach((item, index) => {
                // Always show first and last
                if (index === 0 || index === itemCount - 1) return;
                // Hide items not at skipLevel intervals
                if (index % skipLevel !== 0) {
                    item.classList.add(...RangeSlider.HIDDEN_CLASSES);
                }
            });
            skipLevel *= 2;
        }
    }

    /**
     * Apply rotate mode: rotate legend text vertically.
     */
    applyRotateMode() {
        if (this.isOverlapping()) {
            this.legend.classList.add(...RangeSlider.ROTATE_MODE_CLASSES);
            this.legendItems.forEach(item => {
                item.classList.add(...RangeSlider.ROTATED_CLASSES);
            });
        }
    }

    /**
     * Destroys the range slider instance and removes all event listeners.
     * Call this before removing the element from DOM.
     */
    destroy() {
        debugLog("Destroy RangeSlider: ", this.element);

        if (this.isDualRange) {
            this.inputMin?.removeEventListener("input", this.boundMinInputHandler);
            this.inputMax?.removeEventListener("input", this.boundMaxInputHandler);
        } else if (this.input) {
            this.input.removeEventListener("input", this.boundInputHandler);
        }

        window.removeEventListener("resize", this.boundResizeHandler);

        // Disconnect RTL observer
        if (this.dirObserver) {
            this.dirObserver.disconnect();
            this.dirObserver = null;
        }

        RangeSlider.instances.delete(this.element);
        delete this.element.__insightInstance;

        this.element = null;
    }

    /**
     * Static method for initializing all range sliders.
     */
    static initAll() {
        document.querySelectorAll("[data-insight-range-slider]").forEach(el => new RangeSlider(el));
    }
}
