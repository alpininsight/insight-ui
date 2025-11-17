class Sidebar {
    static instances = new WeakMap();

	constructor(wrapper) {
        if (InsightUI.Sidebar.instances.has(wrapper)) {
            return InsightUI.Sidebar.instances.get(wrapper);
        }

		this.wrapper = wrapper;
		this.sidebar = wrapper.getElementsByTagName("aside")[0];
		this.side = wrapper.getAttribute("data-insight-sidebar");
		this.openBtn = document.querySelector(`.open-btn[data-sidebar-target="${this.side}"]`);
		this.autoClose = this.sidebar.getAttribute("data-auto-close") === "true";

		this.init();

		InsightUI.Sidebar.instances.set(wrapper, this);

        debugLog("New sidebar created: ", this.sidebar, this.side);
	}

	init() {
		if (!this.wrapper) return;

		const isStatic = this.wrapper.getAttribute("data-insight-sidebar-static");
		if (isStatic === "True") return;

		this.wrapper.querySelectorAll('[data-insight-dismiss="sidebar"]').forEach(closeButton => {
			closeButton.addEventListener('click', () => this.closeSidebar());
		});

		// Sidebar initial verstecken
		this.initSidebar();

		if (this.autoClose) {
			this.setupAutoClose();
		}

		if (this.openBtn) {
			this.openBtn.addEventListener('click', () => {
				this.openSidebar();
				this.openBtn.classList.toggle("hidden", true);
			});
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
		document.addEventListener('mousemove', (e) => {
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
		});

		// Schließen, wenn Maus die Sidebar verlässt
		this.sidebar.addEventListener('mouseleave', () => this.closeSidebar());
	}

	// Static method for initializing all sidebar/drawers
	static initAll() {
		const sidebarWrappers = document.querySelectorAll('[data-insight-sidebar]');
		sidebarWrappers.forEach(wrapper => {
			new Sidebar(wrapper);
		});
	}
}

window.InsightUI = window.InsightUI || {};
window.InsightUI.Sidebar = Sidebar;
