/**
 * Insight UI - Progress Bar Component
 *
 * A progress bar with optional auto-update modes (polling, SSE),
 * error handling, cancel/retry buttons, and accessible ARIA attributes.
 *
 * JSON Response Format:
 * {
 *     "value": 75,
 *     "label": "Uploading...",      // Optional: update label
 *     "error": "Connection lost",   // Optional: show error message
 *     "complete": true              // Optional: signal completion
 * }
 */

export class ProgressBar {
    // Weak references used to prevent multiple initialization of the same instance
    static instances = new WeakMap();

    // Registry by tag ID for easy access via InsightUI.ProgressBar.get()
    static registry = {};

    // CSS classes for different states (arrays for multi-class values)
    static classes = {
        fillNormal: ['bg-blue-600'],
        fillError: ['bg-red-500'],
        hidden: ['hidden'],
        errorWarning: ['text-amber-600', 'dark:text-amber-400'],
        errorFatal: ['text-red-600', 'dark:text-red-400'],
    };

    /**
     * Helper to add multiple classes to an element.
     * @param {Element} element
     * @param {string[]} classes
     */
    static addClass(element, classes) {
        if (element && classes) {
            element.classList.add(...classes);
        }
    }

    /**
     * Helper to remove multiple classes from an element.
     * @param {Element} element
     * @param {string[]} classes
     */
    static removeClass(element, classes) {
        if (element && classes) {
            element.classList.remove(...classes);
        }
    }

    constructor(element) {
        // If an instance for this element already exists, return it
        if (ProgressBar.instances.has(element)) {
            return ProgressBar.instances.get(element);
        }

        this.container = element;
        this.tagId = element.dataset.insightProgressBar;
        this.fill = element.querySelector('[data-progress-fill]');
        this.track = element.querySelector('[role="progressbar"]');
        this.tooltip = element.querySelector('[role="tooltip"]');
        this.valueDisplay = element.querySelector('[data-progress-value]');
        this.labelDisplay = element.querySelector('[data-progress-label]');
        this.errorContainer = element.querySelector('[data-progress-error]');
        this.errorMessage = element.querySelector('[data-error-message]');
        this.errorIconWarning = element.querySelector('[data-error-icon-warning]');
        this.errorIconError = element.querySelector('[data-error-icon-error]');
        this.cancelButton = element.querySelector('[data-progress-cancel]');
        this.retryButton = element.querySelector('[data-progress-retry]');

        if (!this.fill || !this.track) {
            console.warn('ProgressBar: Missing required elements for', this.tagId);
            return;
        }

        // Parse configuration from data attributes
        this.config = {
            requestUrl: element.dataset.requestUrl || '',
            interval: parseInt(element.dataset.interval, 10) || 1000,
            sseUrl: element.dataset.sseUrl || '',
            hideOnComplete: element.dataset.hideOnComplete === 'true',
            completeDelay: parseInt(element.dataset.completeDelay, 10) || 500,
            maxValue: parseInt(element.dataset.maxValue, 10) || 100,
            minValue: parseInt(element.dataset.minValue, 10) || 0,
            stopOnError: element.dataset.stopOnError === 'true',
            initialError: element.dataset.initialError || '',
            cancelUrl: element.dataset.cancelUrl || '',
        };

        // State
        this.pollingInterval = null;
        this.eventSource = null;
        this.hasError = false;
        this.isFatalError = false;
        this.isCancelled = false;

        // Store bound handlers for cleanup
        this.boundMouseMove = null;
        this.boundFocus = null;
        this.boundCancelClick = null;
        this.boundRetryClick = null;
        this.observer = null;

        this.init();
        this.bindEvents();
        this.startAutoUpdate();

        this.container.__insightInstance = this;
        ProgressBar.instances.set(element, this);
        ProgressBar.registry[this.tagId] = this;

        debugLog("New progress bar created:", this.tagId);
    }

    init() {
        this.updateTooltipContent();

        // Handle initial error state
        if (this.config.initialError) {
            this.hasError = true;
            this.isFatalError = true;
            this.updateButtonVisibility();
        }
    }

    bindEvents() {
        // Tooltip position on mouse move
        this.boundMouseMove = (e) => this.updateTooltipPosition(e);
        this.track.addEventListener('mousemove', this.boundMouseMove);

        // Tooltip position on focus
        this.boundFocus = () => {
            if (!this.tooltip) return;
            const fillWidth = this.fill.offsetWidth;
            this.tooltip.style.left = `${Math.max(20, fillWidth)}px`;
        };
        this.track.addEventListener('focus', this.boundFocus);

        // Cancel button
        if (this.cancelButton) {
            this.boundCancelClick = (e) => {
                e.preventDefault();
                this.cancel();
            };
            this.cancelButton.addEventListener('click', this.boundCancelClick);
        }

        // Retry button
        if (this.retryButton) {
            this.boundRetryClick = (e) => {
                e.preventDefault();
                this.retry();
            };
            this.retryButton.addEventListener('click', this.boundRetryClick);
        }

        // Observe data-value changes for external updates
        this.observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'attributes' && mutation.attributeName === 'data-value') {
                    this.updateTooltipContent();
                }
            });
        });
        this.observer.observe(this.fill, { attributes: true });
    }

    startAutoUpdate() {
        // Don't start if cancelled
        if (this.isCancelled) return;

        // Polling mode
        if (this.config.requestUrl) {
            this.pollingInterval = setInterval(async () => {
                try {
                    const response = await fetch(this.config.requestUrl);
                    if (!response.ok) throw new Error('Network response was not ok');

                    const data = await response.json();
                    this.handleServerResponse(data);
                } catch (error) {
                    console.error('ProgressBar polling error:', error);
                    this.setError(error.message, false);
                }
            }, this.config.interval);
        }

        // SSE mode
        if (this.config.sseUrl) {
            this.eventSource = new EventSource(this.config.sseUrl);

            this.eventSource.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.handleServerResponse(data);
                } catch (error) {
                    console.error('ProgressBar SSE parse error:', error);
                    this.setError(error.message, false);
                }
            };

            this.eventSource.onerror = (error) => {
                console.error('ProgressBar SSE error:', error);
                this.setError('Connection lost', true);
                this.stopSSE();
            };
        }
    }

    /**
     * Handle a response from the server (polling or SSE).
     * @param {Object} data - The parsed JSON response
     */
    handleServerResponse(data) {
        // Handle error in response
        if (data.error) {
            const isFatal = data.complete === true;
            this.setError(data.error, isFatal);

            if (isFatal || this.config.stopOnError) {
                this.stopPolling();
                this.stopSSE();
            }
        } else {
            // Clear any previous error if no error in response
            if (this.hasError && !this.isFatalError) {
                this.clearError();
            }
        }

        // Update value if provided
        if (data.value !== undefined) {
            this.update(data.value, data.label);
        }

        // Stop if complete flag is set or max reached
        if (data.complete === true || (data.value !== undefined && data.value >= this.config.maxValue)) {
            this.stopPolling();
            this.stopSSE();
        }
    }

    stopPolling() {
        if (this.pollingInterval) {
            clearInterval(this.pollingInterval);
            this.pollingInterval = null;
        }
    }

    stopSSE() {
        if (this.eventSource) {
            this.eventSource.close();
            this.eventSource = null;
        }
    }

    /**
     * Update button visibility based on current state.
     */
    updateButtonVisibility() {
        // Cancel button: visible during progress, hidden on error/complete/cancelled
        if (this.cancelButton) {
            const showCancel = !this.hasError && !this.isCancelled && this.getValue() < this.config.maxValue;
            this.cancelButton.classList.toggle('hidden', !showCancel);
        }

        // Retry button: visible on error (fatal or cancelled), hidden otherwise
        if (this.retryButton) {
            const showRetry = this.isFatalError || this.isCancelled;
            this.retryButton.classList.toggle('hidden', !showRetry);
        }
    }

    /**
     * Update the progress bar value and optionally the label.
     * @param {number} value - The new progress value
     * @param {string} [label] - Optional new label text
     */
    update(value, label) {
        const clampedValue = Math.max(this.config.minValue, Math.min(value, this.config.maxValue));

        // Update fill width
        const percentage = ((clampedValue - this.config.minValue) / (this.config.maxValue - this.config.minValue)) * 100;
        this.fill.style.width = percentage + '%';
        this.fill.dataset.value = clampedValue;

        // Update label if provided
        if (label !== undefined && label !== null) {
            this.fill.dataset.label = label;
            if (this.labelDisplay) {
                this.labelDisplay.textContent = label;
            }
        }

        // Update ARIA attributes
        this.track.setAttribute('aria-valuenow', clampedValue);
        const currentLabel = this.fill.dataset.label || '';
        this.track.setAttribute('aria-valuetext', clampedValue + '% ' + currentLabel);

        // Update visible text value
        if (this.valueDisplay) {
            this.valueDisplay.textContent = clampedValue + '%';
        }

        // Update tooltip content
        this.updateTooltipContent();

        // Update button visibility
        this.updateButtonVisibility();

        // Dispatch update event
        this.container.dispatchEvent(new CustomEvent('insight-ui:progress-update', {
            bubbles: true,
            detail: { tagId: this.tagId, value: clampedValue, label: currentLabel }
        }));

        // Handle completion
        if (clampedValue >= this.config.maxValue && !this.hasError) {
            this.onComplete();
        }
    }

    /**
     * Set an error message on the progress bar.
     * @param {string} message - The error message to display
     * @param {boolean} [isFatal=true] - If true, shows error icon and red bar; if false, shows warning icon
     */
    setError(message, isFatal = true) {
        this.hasError = true;
        this.isFatalError = isFatal;

        if (this.errorContainer && this.errorMessage) {
            // Show error container
            ProgressBar.removeClass(this.errorContainer, ProgressBar.classes.hidden);

            // Set message
            this.errorMessage.textContent = message;

            // Update styling based on severity
            if (isFatal) {
                ProgressBar.removeClass(this.errorContainer, ProgressBar.classes.errorWarning);
                ProgressBar.addClass(this.errorContainer, ProgressBar.classes.errorFatal);
                ProgressBar.addClass(this.errorIconWarning, ProgressBar.classes.hidden);
                ProgressBar.removeClass(this.errorIconError, ProgressBar.classes.hidden);

                // Change progress bar to red
                ProgressBar.removeClass(this.fill, ProgressBar.classes.fillNormal);
                ProgressBar.addClass(this.fill, ProgressBar.classes.fillError);
            } else {
                ProgressBar.removeClass(this.errorContainer, ProgressBar.classes.errorFatal);
                ProgressBar.addClass(this.errorContainer, ProgressBar.classes.errorWarning);
                ProgressBar.addClass(this.errorIconError, ProgressBar.classes.hidden);
                ProgressBar.removeClass(this.errorIconWarning, ProgressBar.classes.hidden);
            }
        }

        // Update button visibility
        this.updateButtonVisibility();

        // Dispatch error event
        this.container.dispatchEvent(new CustomEvent('insight-ui:progress-error', {
            bubbles: true,
            detail: { tagId: this.tagId, error: message, isFatal: isFatal }
        }));
    }

    /**
     * Clear the error state.
     */
    clearError() {
        this.hasError = false;
        this.isFatalError = false;

        if (this.errorContainer) {
            // Hide error container
            ProgressBar.addClass(this.errorContainer, ProgressBar.classes.hidden);

            // Reset progress bar color
            ProgressBar.removeClass(this.fill, ProgressBar.classes.fillError);
            ProgressBar.addClass(this.fill, ProgressBar.classes.fillNormal);
        }

        // Update button visibility
        this.updateButtonVisibility();

        // Dispatch clear event
        this.container.dispatchEvent(new CustomEvent('insight-ui:progress-error-clear', {
            bubbles: true,
            detail: { tagId: this.tagId }
        }));
    }

    /**
     * Cancel the progress operation.
     * Stops polling/SSE and optionally calls the cancel URL.
     */
    async cancel() {
        this.isCancelled = true;

        // Stop auto-update
        this.stopPolling();
        this.stopSSE();

        // Call cancel URL if configured
        if (this.config.cancelUrl) {
            try {
                await fetch(this.config.cancelUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });
            } catch (error) {
                console.error('ProgressBar cancel request failed:', error);
            }
        }

        // Show cancelled state
        this.setError('Cancelled', true);

        // Dispatch cancel event
        this.container.dispatchEvent(new CustomEvent('insight-ui:progress-cancel', {
            bubbles: true,
            detail: { tagId: this.tagId, value: this.getValue() }
        }));
    }

    /**
     * Retry the progress operation after an error.
     * Clears the error state and restarts polling/SSE.
     */
    retry() {
        this.isCancelled = false;
        this.clearError();

        // Restart auto-update
        this.startAutoUpdate();

        // Dispatch retry event
        this.container.dispatchEvent(new CustomEvent('insight-ui:progress-retry', {
            bubbles: true,
            detail: { tagId: this.tagId, value: this.getValue() }
        }));
    }

    /**
     * Check if the progress bar has an error.
     * @returns {boolean}
     */
    hasErrorState() {
        return this.hasError;
    }

    /**
     * Check if the progress was cancelled.
     * @returns {boolean}
     */
    wasCancelled() {
        return this.isCancelled;
    }

    /**
     * Reset the progress bar to its initial state.
     */
    reset() {
        // Clear states
        this.isCancelled = false;
        this.clearError();

        // Reset visibility
        this.container.style.display = '';
        this.container.style.opacity = '';
        this.container.style.transition = '';

        // Reset value
        this.update(this.config.minValue);

        // Dispatch reset event
        this.container.dispatchEvent(new CustomEvent('insight-ui:progress-reset', {
            bubbles: true,
            detail: { tagId: this.tagId }
        }));
    }

    /**
     * Manually trigger completion (sets to max value).
     */
    complete() {
        this.clearError();
        this.update(this.config.maxValue);
    }

    /**
     * Get the current progress value.
     * @returns {number}
     */
    getValue() {
        return parseInt(this.fill.dataset.value, 10);
    }

    /**
     * Get the current label.
     * @returns {string}
     */
    getLabel() {
        return this.fill.dataset.label || '';
    }

    onComplete() {
        // Stop auto-update
        this.stopPolling();
        this.stopSSE();

        // Update button visibility
        this.updateButtonVisibility();

        // Dispatch completion event
        this.container.dispatchEvent(new CustomEvent('insight-ui:progress-complete', {
            bubbles: true,
            detail: { tagId: this.tagId, value: this.getValue() }
        }));

        // Hide if configured
        if (this.config.hideOnComplete) {
            setTimeout(() => {
                this.container.style.transition = 'opacity 300ms ease-out';
                this.container.style.opacity = '0';
                setTimeout(() => {
                    this.container.style.display = 'none';
                }, 300);
            }, this.config.completeDelay);
        }
    }

    updateTooltipContent() {
        if (!this.tooltip) return;
        const value = this.fill.dataset.value;
        const label = this.fill.dataset.label;
        const arrow = this.tooltip.querySelector('span');
        this.tooltip.textContent = label ? `${label}: ${value}%` : `${value}%`;
        if (arrow) this.tooltip.appendChild(arrow);
    }

    updateTooltipPosition(event) {
        if (!this.tooltip) return;
        const rect = this.track.getBoundingClientRect();
        const x = Math.max(0, Math.min(event.clientX - rect.left, rect.width));
        this.tooltip.style.left = `${x}px`;
    }

    /**
     * Destroys the progress bar instance and removes all event listeners.
     * Call this before removing the element from DOM.
     */
    destroy() {
        debugLog("Destroy progress bar:", this.tagId);

        // Stop auto-update
        this.stopPolling();
        this.stopSSE();

        // Remove event listeners
        if (this.boundMouseMove) {
            this.track.removeEventListener('mousemove', this.boundMouseMove);
        }
        if (this.boundFocus) {
            this.track.removeEventListener('focus', this.boundFocus);
        }
        if (this.boundCancelClick && this.cancelButton) {
            this.cancelButton.removeEventListener('click', this.boundCancelClick);
        }
        if (this.boundRetryClick && this.retryButton) {
            this.retryButton.removeEventListener('click', this.boundRetryClick);
        }

        // Disconnect observer
        if (this.observer) {
            this.observer.disconnect();
            this.observer = null;
        }

        // Clean up references
        ProgressBar.instances.delete(this.container);
        delete ProgressBar.registry[this.tagId];
        delete this.container.__insightInstance;

        this.container = null;
        this.fill = null;
        this.track = null;
        this.tooltip = null;
        this.errorContainer = null;
        this.errorMessage = null;
        this.cancelButton = null;
        this.retryButton = null;
    }

    /**
     * Get a progress bar instance by its tag ID.
     * @param {string} tagId - The tag ID of the progress bar
     * @returns {ProgressBar|null}
     */
    static get(tagId) {
        return ProgressBar.registry[tagId] || null;
    }

    /**
     * Update a progress bar by its tag ID.
     * @param {string} tagId - The tag ID of the progress bar
     * @param {number} value - The new progress value
     * @param {string} [label] - Optional new label text
     */
    static update(tagId, value, label) {
        const instance = ProgressBar.get(tagId);
        if (instance) {
            instance.update(value, label);
        } else {
            console.warn('ProgressBar: No instance found with id "' + tagId + '"');
        }
    }

    /**
     * Set an error on a progress bar by its tag ID.
     * @param {string} tagId - The tag ID of the progress bar
     * @param {string} message - The error message
     * @param {boolean} [isFatal=true] - If true, shows error styling; if false, shows warning
     */
    static setError(tagId, message, isFatal = true) {
        const instance = ProgressBar.get(tagId);
        if (instance) {
            instance.setError(message, isFatal);
        } else {
            console.warn('ProgressBar: No instance found with id "' + tagId + '"');
        }
    }

    /**
     * Clear the error on a progress bar by its tag ID.
     * @param {string} tagId - The tag ID of the progress bar
     */
    static clearError(tagId) {
        const instance = ProgressBar.get(tagId);
        if (instance) {
            instance.clearError();
        }
    }

    /**
     * Cancel a progress bar by its tag ID.
     * @param {string} tagId - The tag ID of the progress bar
     */
    static cancel(tagId) {
        const instance = ProgressBar.get(tagId);
        if (instance) {
            instance.cancel();
        }
    }

    /**
     * Retry a progress bar by its tag ID.
     * @param {string} tagId - The tag ID of the progress bar
     */
    static retry(tagId) {
        const instance = ProgressBar.get(tagId);
        if (instance) {
            instance.retry();
        }
    }

    /**
     * Reset a progress bar by its tag ID.
     * @param {string} tagId - The tag ID of the progress bar
     */
    static reset(tagId) {
        const instance = ProgressBar.get(tagId);
        if (instance) {
            instance.reset();
        }
    }

    /**
     * Complete a progress bar by its tag ID.
     * @param {string} tagId - The tag ID of the progress bar
     */
    static complete(tagId) {
        const instance = ProgressBar.get(tagId);
        if (instance) {
            instance.complete();
        }
    }

    // Static method for initializing all progress bars
    static initAll() {
        document.querySelectorAll('[data-insight-progress-bar]').forEach(el => new ProgressBar(el));
    }
}
