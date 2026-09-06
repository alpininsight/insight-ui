// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * FlipCard component for Insight UI.
 *
 * Creates a card that flips 180° when clicking a trigger button.
 * Manages aria-hidden state for screen reader accessibility.
 *
 * @example
 * // HTML structure
 * <div data-insight-flip-card>
 *   <div data-flip-inner>
 *     <div data-flip-front>Front content</div>
 *     <div data-flip-back aria-hidden="true">Back content</div>
 *   </div>
 *   <button data-flip-trigger>Flip</button>
 * </div>
 */
export class FlipCard {
    /** @type {WeakMap<HTMLElement, FlipCard>} Weak references to prevent multiple initialization */
    static instances = new WeakMap();

    /**
     * Creates a new FlipCard instance.
     *
     * @param {HTMLElement} container - The container element with data-insight-flip-card attribute
     */
    constructor(container) {
        if (FlipCard.instances.has(container)) {
            return FlipCard.instances.get(container);
        }

        this.container = container;
        this.inner = container.querySelector('[data-flip-inner]');
        this.front = container.querySelector('[data-flip-front]');
        this.back = container.querySelector('[data-flip-back]');
        this.triggers = container.querySelectorAll('[data-flip-trigger]');

        this.isFlipped = false;
        this.clickHandler = (e) => this.toggle(e);
        this.keyHandler = (e) => this.handleKeydown(e);

        this.init();

        this.container.__insightInstance = this;
        FlipCard.instances.set(container, this);

        debugLog("New flip card created: ", this.container);
    }

    /**
     * Initializes the flip card by binding event handlers.
     */
    init() {
        this.front.inert = false;
        this.back.inert = true;

        this.triggers.forEach(trigger => {
            trigger.addEventListener('click', this.clickHandler);
            trigger.addEventListener('keydown', this.keyHandler);
        });
    }

    /**
     * Handles keydown events for accessibility.
     *
     * @param {KeyboardEvent} e - The keyboard event
     */
    handleKeydown(e) {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            this.toggle(e);
        }
    }

    /**
     * Toggles the flip state of the card.
     *
     * @param {Event} e - The triggering event
     */
    toggle(e) {
        e.stopPropagation();
        this.isFlipped = !this.isFlipped;

        if (this.isFlipped) {
            this.inner.classList.add('rotate-y-180');
            this.front.setAttribute('aria-hidden', 'true');
            this.back.setAttribute('aria-hidden', 'false');
            this.front.inert = true;
            this.back.inert = false;
        } else {
            this.inner.classList.remove('rotate-y-180');
            this.front.setAttribute('aria-hidden', 'false');
            this.back.setAttribute('aria-hidden', 'true');
            this.front.inert = false;
            this.back.inert = true;
        }

        // Focus the trigger on the now-visible side after animation
        setTimeout(() => {
            const visibleTriggers = Array.from(this.triggers).filter(t => {
                const side = t.closest('[data-flip-front], [data-flip-back]');
                if (!side) return false;
                return side.getAttribute('aria-hidden') !== 'true';
            });
            if (visibleTriggers.length > 0) {
                visibleTriggers[0].focus();
            }
        }, 500);
    }

    /**
     * Destroys the flip card instance and removes all event listeners.
     */
    destroy() {
        debugLog("Destroy flip card: ", this.container);

        this.triggers.forEach(trigger => {
            trigger.removeEventListener('click', this.clickHandler);
            trigger.removeEventListener('keydown', this.keyHandler);
        });

        FlipCard.instances.delete(this.container);
        delete this.container.__insightInstance;

        this.container = null;
        this.inner = null;
        this.front = null;
        this.back = null;
        this.triggers = null;
    }

    /**
     * Initializes all flip card instances on the page.
     *
     * @static
     */
    static initAll() {
        document.querySelectorAll('[data-insight-flip-card]').forEach(el => new FlipCard(el));
    }
}
