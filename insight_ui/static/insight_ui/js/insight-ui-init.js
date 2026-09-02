/**
 * Insight UI - Component Initializer
 *
 * This module serves as the main entry point for Insight UI JavaScript components.
 * It imports all component classes, exposes them globally via `window.InsightUI`,
 * and initializes all components on DOMContentLoaded and after HTMX content swaps.
 *
 * @module insight-ui-init
 */

import { Accordion } from "./insight-ui-accordion.js";
import { Carousel } from "./insight-ui-carousel.js";
import { Checkbox } from "./insight-ui-checkbox.js";
import { CodeBlock } from "./insight-ui-code-block.js";
import { Collapsible } from "./insight-ui-collapsible.js";
import { DemoIframeController } from "./insight-ui-demo-container.js";
import { Dropdown } from "./insight-ui-dropdown.js";
import { FlipCard } from "./insight-ui-flip-card.js";
import { Floater } from "./insight-ui-floater.js";
import { Modal } from "./insight-ui-modal.js";
import { MockupTOC } from "./insight-ui-mockup-toc.js";
import { Multiselect } from "./insight-ui-multiselect.js";
import { ProgressBar } from "./insight-ui-progress-bar.js";
import { RangeSlider } from "./insight-ui-range-slider.js";
import { Search } from "./insight-ui-search.js";
import { Sidebar } from "./insight-ui-sidebar.js";
import { Tabs } from "./insight-ui-tabs.js";
import { ThemeToggle } from "./insight-ui-theme-toggle.js";
import { ThreeDCarousel } from "./insight-ui-3D-carousel.js";

// Expose component classes for lifecycle cleanup lookups in insight-ui-utils.js
window.InsightUI = window.InsightUI || {};
Object.assign(window.InsightUI, {
	Accordion,
	Carousel,
	Checkbox,
	CodeBlock,
	Collapsible,
	DemoIframeController,
	Dropdown,
	FlipCard,
	Floater,
	Modal,
	MockupTOC,
	Multiselect,
	ProgressBar,
	RangeSlider,
	Search,
	Sidebar,
	Tabs,
	ThemeToggle,
	ThreeDCarousel,
});

/**
 * Initializes all Insight UI component instances.
 * Called on DOMContentLoaded and after HTMX content swaps.
 */
function initAll() {
	Accordion.initAll();
	Carousel.initAll();
	Checkbox.initAll();
	CodeBlock.initAll();
	Collapsible.initAll();
	DemoIframeController.initAll();
	Dropdown.initAll();
	FlipCard.initAll();
	Floater.initAll();
	Modal.initAll();
	MockupTOC.initAll();
	Multiselect.initAll();
	ProgressBar.initAll();
	RangeSlider.initAll();
	Search.initAll();
	Sidebar.initAll();
	Tabs.initAll();
	ThemeToggle.initAll();
	ThreeDCarousel.initAll();
	InsightUI.WebSocket?.init();
}

document.addEventListener('DOMContentLoaded', function () {
	debugLog('InsightUI initializing...');
	debugLog('InsightUI components found:', window.InsightUI);

	// Register HTMX cleanup hooks to prevent memory leaks
	InsightUI.lifecycle.registerHTMXHooks();

	// Initialize delegated event handlers (security hardening)
	InsightUI.handlers.init();

	// Initialize all instances
	initAll();

	// Initialize TOC if present on page load
	const tocEl = document.getElementById("toc");
	if (tocEl) {
		new TableOfContents({
			contentSelector: "main-content",
			tocSelector: "toc",
			offsetTop: 200,
			offsetBottom: 300
		});
	}

	// Initialize all (new) instances after htmx manipulates the DOM
	htmx.on("htmx:afterSwap", function (evt) {
		debugLog("Initialize new instances...")
		initAll();

		// The parameter drill-down section is a narrow, self-contained fragment
		// swap - it never introduces new headings, so skip the (visibly
		// disruptive - the TOC panel blanks out and rebuilds) TOC regeneration
		// below and just move focus into the new content instead.
		// Note: evt.detail.target can be undefined during history navigation (back/forward)
		if (evt.detail.target?.id === "parameter-section") {
			// preventScroll avoids a visible jump: the button that triggered the
			// swap is already in view, so the browser doesn't need to scroll to it.
			document.getElementById("parameter-section-heading")?.focus({ preventScroll: true });
			debugLog("New instances initialized!")
			return;
		}

		// Regenerate TOC after content swap
		const tocEl = document.getElementById("toc");
		if (tocEl) {
			tocEl.innerHTML = "";
			new TableOfContents({
				contentSelector: "main-content",
				tocSelector: "toc",
				offsetTop: 200,
				offsetBottom: 300
			});
		}

		debugLog("New instances initialized!")
	});

	debugLog('Finished with initialization!');

	// Signal that InsightUI is fully initialized
	document.dispatchEvent(new CustomEvent('insightui:ready', { bubbles: true }));
});
