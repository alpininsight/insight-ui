export class Sidebar {
	// Weak references used to prevent multiple initialization of the same instance
    static instances = new WeakMap();

	constructor(wrapper) {
		// If an instance for this element already exists, return it
        if (Sidebar.instances.has(wrapper)) {
            return Sidebar.instances.get(wrapper);
        }

		this.wrapper = wrapper;
		this.sidebar = wrapper.getElementsByTagName("aside")[0];
		this.side = wrapper.getAttribute("data-insight-sidebar");
		this.openBtn = document.querySelector(`.open-btn[data-sidebar-target="${this.side}"]`);
		this.autoClose = this.sidebar.getAttribute("data-auto-close") === "true";

		// Store bound handlers for cleanup
		this.boundCloseButtons = [];
		this.boundOpenBtnClick = null;
		this.boundMouseMove = null;
		this.boundMouseLeave = null;

		this.init();

		this.wrapper.__insightInstance = this;
		Sidebar.instances.set(wrapper, this);

        debugLog("New sidebar created: ", this.sidebar, this.side);
	}

	init() {
		if (!this.wrapper) return;

		const isStatic = this.wrapper.getAttribute("data-insight-sidebar-static");
		if (isStatic === "True") return;

		this.wrapper.querySelectorAll('[data-insight-dismiss="sidebar"]').forEach(closeButton => {
			const handler = () => this.closeSidebar();
			this.boundCloseButtons.push({ element: closeButton, handler });
			closeButton.addEventListener('click', handler);
		});

		// Sidebar initial verstecken
		this.initSidebar();

		if (this.autoClose) {
			this.setupAutoClose();
		}

		if (this.openBtn) {
			this.boundOpenBtnClick = () => {
				this.openSidebar();
				this.openBtn.classList.toggle("hidden", true);
			};
			this.openBtn.addEventListener('click', this.boundOpenBtnClick);
		}
	}

	initSidebar() {
		if (document.documentElement.dir === "rtl") {
			if (this.side === "right") this.sidebar.style.transform = 'translateX(-100%)';
			else if (this.side === "left") this.sidebar.style.transform = 'translateX(100%)';
		} else {
			if (this.side === "right") this.sidebar.style.transform = 'translateX(100%)';
			else if (this.side === "left") this.sidebar.style.transform = 'translateX(-100%)';
		}
	}

	openSidebar() {
		this.wrapper.classList.remove("hidden");
		InsightUI.utils.trapFocus(this.wrapper);
		this.sidebar.style.transform = 'translateX(0)';
	}

	closeSidebar() {
		if (document.documentElement.dir === "rtl") {
			if (this.side === "right") this.sidebar.style.transform = 'translateX(-100%)';
			else if (this.side === "left") this.sidebar.style.transform = 'translateX(100%)';
		} else {
			if (this.side === "right") this.sidebar.style.transform = 'translateX(100%)';
			else if (this.side === "left") this.sidebar.style.transform = 'translateX(-100%)';
		}

		this.sidebar.addEventListener('transitionend', (event) => {
			// Todo: sometimes the transformation gets skipped, find fix
			this.wrapper.classList.add("hidden");
			if (this.openBtn) this.openBtn.classList.toggle("hidden", false);
		}, { once: true });
	}

	setupAutoClose() {
		// Öffnen, wenn Maus nahe an der Fenster Seite ist
		this.boundMouseMove = (e) => {
			const xThreshold = 50; // Pixel Abstand vom Rand
			const yThreshold = 0;  // 64 Pixel Abstand vom oberen Rand (wird durch Navbar bestimmt)

			if (e.clientY > yThreshold) {
				if (document.documentElement.dir === "rtl") {
					if (this.side === "right" && e.clientX < xThreshold) {
						this.openSidebar();
					} else if (this.side === "left" && window.innerWidth - e.clientX < xThreshold) {
						this.openSidebar();
					}
				} else {
					if (this.side === "right" && window.innerWidth - e.clientX < xThreshold) {
						this.openSidebar();
					} else if (this.side === "left" && e.clientX < xThreshold) {
						this.openSidebar();
					}
				}
			}
		};
		document.addEventListener('mousemove', this.boundMouseMove);

		// Schließen, wenn Maus die Sidebar verlässt
		this.boundMouseLeave = () => this.closeSidebar();
		this.sidebar.addEventListener('mouseleave', this.boundMouseLeave);
	}

	/**
	 * Destroys the sidebar instance and removes all event listeners.
	 * Call this before removing the element from DOM.
	 */
	destroy() {
		debugLog("Destroy sidebar: ", this.sidebar, this.side);

		// Remove close button handlers
		this.boundCloseButtons.forEach(({ element, handler }) => {
			element.removeEventListener('click', handler);
		});
		this.boundCloseButtons = [];

		// Remove open button handler
		if (this.openBtn && this.boundOpenBtnClick) {
			this.openBtn.removeEventListener('click', this.boundOpenBtnClick);
		}

		// Remove auto-close handlers
		if (this.boundMouseMove) {
			document.removeEventListener('mousemove', this.boundMouseMove);
		}
		if (this.boundMouseLeave) {
			this.sidebar.removeEventListener('mouseleave', this.boundMouseLeave);
		}

		Sidebar.instances.delete(this.wrapper);
		delete this.wrapper.__insightInstance;

		this.wrapper = null;
		this.sidebar = null;
	}

	// Static method for initializing all sidebar/drawers
	static initAll() {
		document.querySelectorAll('[data-insight-sidebar]').forEach(wrapper => new Sidebar(wrapper));
	}
}
