/**
 * MockupTOC - Interactive mockup Table of Contents for Insight UI.
 *
 * Creates a visual representation of page structure where each mockup region
 * links to and highlights the corresponding section in the content area.
 *
 * Features:
 * - Click on mockup region to scroll to section
 * - Active region highlighting based on scroll position
 * - Keyboard navigation (Tab + Enter)
 * - Accessibility support with ARIA attributes
 *
 * Usage:
 *   <div id="mockup-toc">
 *     <a href="#navbar" data-mockup-region="navbar">Navbar</a>
 *     <a href="#sidebar" data-mockup-region="sidebar">Sidebar</a>
 *   </div>
 *
 *   new MockupTOC({
 *     mockupSelector: '#mockup-toc',
 *     contentSelector: '#content',
 *     offsetTop: 200
 *   });
 */
export class MockupTOC {
	/**
	 * Create a MockupTOC instance.
	 *
	 * @param {Object} options - Configuration options
	 * @param {string} options.mockupSelector - CSS selector for mockup container
	 * @param {string} options.contentSelector - CSS selector for content area
	 * @param {number} [options.offsetTop=200] - Offset from top when calculating active section
	 */
	constructor({ mockupSelector, contentSelector, offsetTop = 200 }) {
		this.mockupContainer = document.querySelector(mockupSelector);
		this.contentContainer = document.querySelector(contentSelector);
		this.offsetTop = offsetTop;

		if (!this.mockupContainer) {
			debugLog("MockupTOC: mockup container not found", mockupSelector);
			return;
		}

		// Get all mockup regions
		this.regions = this.mockupContainer.querySelectorAll('[data-mockup-region]');
		if (this.regions.length === 0) {
			debugLog("MockupTOC: no regions found");
			return;
		}

		// Bound handlers for cleanup
		this.boundScrollHandler = null;
		this.boundClickHandlers = [];
		this.boundKeydownHandlers = [];

		this.init();
		debugLog("MockupTOC initialized", { regions: this.regions.length, offsetTop: this.offsetTop });
	}

	init() {
		this.bindRegions();
		this.setupScrollTracking();
		// Initial highlight
		this.updateActiveRegion();
	}

	/**
	 * Bind click handlers to mockup regions.
	 */
	bindRegions() {
		this.regions.forEach(region => {
			const handler = (e) => {
				e.preventDefault();
				const targetId = region.getAttribute('data-mockup-region');
				this.navigateToSection(targetId);
			};

			region.addEventListener('click', handler);
			this.boundClickHandlers.push({ element: region, handler });

			// Keyboard support
			const keydownHandler = (e) => {
				if (e.key === 'Enter' || e.key === ' ') {
					e.preventDefault();
					const targetId = region.getAttribute('data-mockup-region');
					this.navigateToSection(targetId);
				}
			};
			region.addEventListener('keydown', keydownHandler);
			this.boundKeydownHandlers.push({ element: region, handler: keydownHandler });
		});
	}

	/**
	 * Set up scroll tracking to highlight active region.
	 */
	setupScrollTracking() {
		this.boundScrollHandler = () => this.updateActiveRegion();
		window.addEventListener('scroll', this.boundScrollHandler, { passive: true });
	}

	/**
	 * Update which mockup region is highlighted based on scroll position.
	 */
	updateActiveRegion() {
		const scrollPosition = window.scrollY + this.offsetTop;
		let activeTargetId = null;

		// Build a map of unique section IDs to their positions
		const sectionMap = new Map();
		this.regions.forEach(region => {
			const targetId = region.getAttribute('data-mockup-region');
			if (!sectionMap.has(targetId)) {
				const section = document.getElementById(targetId);
				if (section) {
					const rect = section.getBoundingClientRect();
					sectionMap.set(targetId, {
						top: rect.top + window.scrollY,
						bottom: rect.top + window.scrollY + rect.height
					});
				}
			}
		});

		// Find which section is currently in view
		for (const [targetId, bounds] of sectionMap) {
			if (scrollPosition >= bounds.top && scrollPosition < bounds.bottom) {
				activeTargetId = targetId;
				break;
			}
		}

		// If no section in view, find the closest one above the scroll position
		if (!activeTargetId && sectionMap.size > 0) {
			let closestAbove = null;
			let closestDistance = Infinity;

			for (const [targetId, bounds] of sectionMap) {
				// Only consider sections that are above the current scroll position
				if (bounds.top <= scrollPosition) {
					const distance = scrollPosition - bounds.top;
					if (distance < closestDistance) {
						closestDistance = distance;
						closestAbove = targetId;
					}
				}
			}

			// If we found a section above, use it; otherwise use the first section
			if (closestAbove) {
				activeTargetId = closestAbove;
			} else {
				// We're above all sections, highlight the first one
				activeTargetId = this.regions[0]?.getAttribute('data-mockup-region');
			}
		}

		// Update active state - highlight ALL regions with the same targetId
		this.regions.forEach(region => {
			const regionTargetId = region.getAttribute('data-mockup-region');
			const isActive = regionTargetId === activeTargetId;
			const activeClasses = region.getAttribute('data-active-class')?.split(' ') || [];

			if (isActive) {
				region.setAttribute('aria-current', 'true');
				activeClasses.forEach(cls => cls && region.classList.add(cls));
			} else {
				region.removeAttribute('aria-current');
				activeClasses.forEach(cls => cls && region.classList.remove(cls));
			}
		});
	}

	/**
	 * Navigate to a specific section.
	 *
	 * @param {string} sectionId - ID of the section to scroll to
	 */
	navigateToSection(sectionId) {
		const section = document.getElementById(sectionId);
		if (!section) {
			debugLog("MockupTOC: section not found", sectionId);
			return;
		}

		// Smooth scroll to section
		section.scrollIntoView({ behavior: 'smooth', block: 'start' });

		// Focus the section for accessibility
		if (!section.hasAttribute('tabindex')) {
			section.setAttribute('tabindex', '-1');
		}
		section.focus({ preventScroll: true });

		debugLog("MockupTOC: navigated to", sectionId);
	}

	/**
	 * Destroy the MockupTOC instance and remove all event listeners.
	 */
	destroy() {
		// Remove scroll handler
		if (this.boundScrollHandler) {
			window.removeEventListener('scroll', this.boundScrollHandler);
		}

		// Remove click handlers
		this.boundClickHandlers.forEach(({ element, handler }) => {
			element.removeEventListener('click', handler);
		});
		this.boundClickHandlers = [];

		// Remove keydown handlers
		this.boundKeydownHandlers.forEach(({ element, handler }) => {
			element.removeEventListener('keydown', handler);
		});
		this.boundKeydownHandlers = [];

		debugLog("MockupTOC destroyed");
	}

	/**
	 * Initialize all MockupTOC instances on the page.
	 * Looks for elements with data-insight-mockup-toc attribute.
	 */
	static initAll() {
		document.querySelectorAll('[data-insight-mockup-toc]').forEach(container => {
			const contentSelector = container.getAttribute('data-content-selector') || '#content';
			const offsetTop = parseInt(container.getAttribute('data-offset-top') || '200', 10);

			new MockupTOC({
				mockupSelector: `#${container.id}`,
				contentSelector,
				offsetTop
			});
		});
	}
}
