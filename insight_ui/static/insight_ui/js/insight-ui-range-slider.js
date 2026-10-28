// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
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
    /** @type {WeakMap<HTMLElement, RangeSlider>} Weak references to prevent multiple initialization */
    static instances = new WeakMap();

    /** @type {string} Tailwind class for hidden items; items are positioned absolutely, so they keep no space */
    static HIDDEN_CLASS = "invisible";

    /** @type {string[]} Tailwind classes for the rotated legend container, which gets the height of the rotated items */
    static ROTATE_MODE_CLASSES = ["h-20"];

    /** @type {number} Minimum gap in pixels between two visible legend items */
    static LEGEND_GAP = 8;

    /** @type {string[]} Tailwind classes for rotated items */
    static ROTATED_CLASSES = [
        "[writing-mode:vertical-rl]",
        "[text-orientation:mixed]",
        "rotate-180",
        "whitespace-nowrap",
        "max-h-20",
        "overflow-hidden",
        "text-ellipsis"
    ];

    /**
     * Creates a new RangeSlider instance.
     *
     * @param {HTMLElement} element - The slider container element with data-insight-range-slider attribute
     */
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
        this.boundResetHandler = this.handleFormReset.bind(this);
        this.resetTimer = null;

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

        // Native form reset restores the input values but not the progress visuals.
        this.form = this.element.closest("form");
        this.form?.addEventListener("reset", this.boundResetHandler);

        if (this.legendMode !== "static" && this.legendItems.length >= 2) {
            this.observeLegendWidth();
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

        this.element.style.setProperty("--insight-control-range-min", `${minPercent}%`);
        this.element.style.setProperty("--insight-control-range-max", `${maxPercent}%`);

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
        this.element.style.setProperty("--insight-control-range-progress", `${percent}%`);

        // Update ARIA attribute for screen readers
        this.input.setAttribute("aria-valuenow", val);
    }

    /**
     * Update the progress visuals after the surrounding form was reset.
     * The reset event fires before the browser restores the values, so the update is deferred.
     */
    handleFormReset() {
        clearTimeout(this.resetTimer);
        this.resetTimer = setTimeout(() => {
            if (this.isDualRange) {
                this.updateDualProgress();
            } else if (this.input) {
                this.updateProgress();
            }
        });
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
     * Check if visible legend items overlap or come closer than LEGEND_GAP.
     * Items are positioned under their thumb positions, so neighbors are compared by their real boxes.
     * @returns {boolean} True if two neighboring items overlap
     */
    isOverlapping() {
        const rects = this.legendItems
            .filter(item => !item.classList.contains(RangeSlider.HIDDEN_CLASS))
            .map(item => item.getBoundingClientRect())
            .sort((a, b) => a.left - b.left);

        return rects.some((rect, index) => index > 0 && rect.left < rects[index - 1].right + RangeSlider.LEGEND_GAP);
    }

    /**
     * Reset all legend items to their default visible state.
     */
    resetLegend() {
        this.legendItems.forEach(item => {
            item.classList.remove(RangeSlider.HIDDEN_CLASS, ...RangeSlider.ROTATED_CLASSES);
        });
        this.legend.classList.remove(...RangeSlider.ROTATE_MODE_CLASSES);
    }

    /**
     * Adjust the legend once its layout exists and whenever its width changes, also when only the
     * surrounding container resizes. The items are measured, so adjusting before the stylesheet
     * positioned them would find no overlap. Height changes are ignored: the rotate mode changes the height.
     */
    observeLegendWidth() {
        if (!("ResizeObserver" in window)) {
            window.addEventListener("resize", this.boundResizeHandler);
            this.adjustLegend();
            return;
        }
        this.legendWidth = null;
        this.legendObserver = new ResizeObserver(([entry]) => {
            if (entry.contentRect.width === this.legendWidth) return;
            this.legendWidth = entry.contentRect.width;
            this.adjustLegend();
        });
        this.legendObserver.observe(this.legend);
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
        const last = this.legendItems.length - 1;

        // Try every step from dense to sparse until no items overlap. First and last always stay; a middle
        // item closer to the last one than a step would crowd it, so it is hidden as well.
        for (let step = 2; step <= last && this.isOverlapping(); step++) {
            this.legendItems.forEach((item, index) => {
                const shown = index === 0 || index === last || (index % step === 0 && last - index >= step);
                item.classList.toggle(RangeSlider.HIDDEN_CLASS, !shown);
            });
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
        this.legendObserver?.disconnect();
        this.form?.removeEventListener("reset", this.boundResetHandler);

        // A reset scheduled just before destroy would otherwise access the removed element.
        clearTimeout(this.resetTimer);

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
     * Initializes all range slider instances on the page.
     *
     * @static
     */
    static initAll() {
        document.querySelectorAll("[data-insight-range-slider]").forEach(el => new RangeSlider(el));
    }
}
