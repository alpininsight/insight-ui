/**
 * Unified Tabs component supporting both HTMX and static content modes.
 *
 * Modes are auto-detected:
 * - **HTMX mode**: Tabs have `hx-get` attributes, content loaded via HTMX
 * - **Static mode**: Tabs have `data-tab-panel` attributes, panels shown/hidden
 *
 * Expected structure:
 * ```html
 * <div data-insight-tabs>
 *   <div role="tablist">
 *     <button role="tab" data-tab-panel="panel1" aria-selected="true">Tab 1</button>
 *     <button role="tab" data-tab-panel="panel2">Tab 2</button>
 *   </div>
 *   <div data-tab-panels>
 *     <div id="panel1">Content 1</div>
 *     <div id="panel2" class="hidden">Content 2</div>
 *   </div>
 * </div>
 * ```
 */
export class Tabs {
	static instances = new WeakMap();

	constructor(element) {
		if (Tabs.instances.has(element)) {
			return Tabs.instances.get(element);
		}

		this.element = element;
		this.tablist = element.querySelector('[role="tablist"]');
		this.tabs = Array.from(this.tablist.querySelectorAll('[role="tab"]'));
		this.panelContainer = element.querySelector('[data-tab-panels]') || element.children[1];

		// Auto-detect mode: static tabs have data-tab-panel attributes
		this.isStatic = this.tabs.some(tab => tab.hasAttribute('data-tab-panel'));

		// Store bound handlers for cleanup
		this.boundTabHandlers = [];
		this.boundHTMXAfterSwap = null;

		this.bindEvents();

		this.element.__insightInstance = this;
		Tabs.instances.set(element, this);

		debugLog("New tabs created (static=" + this.isStatic + "): ", this.element);
	}

	bindEvents() {
		this.tabs.forEach((tab, index) => {
			const keydownHandler = (e) => this.handleKeyDown(e, index);
			const clickHandler = () => this.activateTab(tab);
			tab.addEventListener('keydown', keydownHandler);
			tab.addEventListener('click', clickHandler);
			this.boundTabHandlers.push({ element: tab, keydownHandler, clickHandler });
		});

		// HTMX focus handler (only for HTMX mode)
		if (!this.isStatic) {
			const tabContentId = this.panelContainer?.id;
			if (tabContentId) {
				this.boundHTMXAfterSwap = (event) => {
					if (event.detail.target.id === tabContentId) {
						this.panelContainer.focus();
					}
				};
				document.body.addEventListener('htmx:afterSwap', this.boundHTMXAfterSwap);
			}
		}
	}

	handleKeyDown(e, index) {
		let newIndex = null;
		const length = this.tabs.length;

		switch (e.key) {
			case 'ArrowRight':
				newIndex = (index + 1) % length;
				break;
			case 'ArrowLeft':
				newIndex = (index - 1 + length) % length;
				break;
			case 'Home':
				newIndex = 0;
				break;
			case 'End':
				newIndex = length - 1;
				break;
		}

		if (newIndex !== null) {
			e.preventDefault();
			this.tabs[newIndex].focus();
			// In static mode, also activate the tab on keyboard navigation
			if (this.isStatic) {
				this.activateTab(this.tabs[newIndex]);
			}
		}
	}

	activateTab(selectedTab) {
		this.tabs.forEach(tab => {
			const isSelected = tab === selectedTab;

			// Update ARIA state
			tab.setAttribute('aria-selected', isSelected ? 'true' : 'false');
			tab.setAttribute('tabindex', isSelected ? '0' : '-1');

			// Update styling
			if (isSelected) {
				tab.classList.remove('border-transparent', 'text-secondary');
				tab.classList.add('border-insight-primary', 'text-insight-primary');
			} else {
				tab.classList.remove('border-insight-primary', 'text-insight-primary');
				tab.classList.add('border-transparent', 'text-secondary');
			}

			// Static mode: show/hide panels
			if (this.isStatic) {
				const panelId = tab.getAttribute('data-tab-panel');
				const panel = panelId ? document.getElementById(panelId) : null;
				if (panel) {
					panel.classList.toggle('hidden', !isSelected);
					panel.setAttribute('aria-hidden', !isSelected);
				}
			}
		});

		// HTMX mode: update panel aria-label
		if (!this.isStatic && this.panelContainer) {
			this.panelContainer.setAttribute('aria-label', selectedTab.id);
		}
	}

	destroy() {
		debugLog("Destroy tabs: ", this.element);

		this.boundTabHandlers.forEach(({ element, keydownHandler, clickHandler }) => {
			element.removeEventListener('keydown', keydownHandler);
			element.removeEventListener('click', clickHandler);
		});
		this.boundTabHandlers = [];

		if (this.boundHTMXAfterSwap) {
			document.body.removeEventListener('htmx:afterSwap', this.boundHTMXAfterSwap);
		}

		Tabs.instances.delete(this.element);
		delete this.element.__insightInstance;

		this.element = null;
		this.tabs = null;
		this.panelContainer = null;
	}

	static initAll() {
		document.querySelectorAll("[data-insight-tabs]").forEach(el => new Tabs(el));
	}
}
