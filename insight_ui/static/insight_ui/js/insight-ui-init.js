/**
 * Insight UI - Component Initializer
 */

import { Accordion } from "./insight-ui-accordion.js";
import { Carousel } from "./insight-ui-carousel.js";
import { Checkbox } from "./insight-ui-checkbox.js";
import { CodeBlock } from "./insight-ui-code-block.js";
import { Collapsible } from "./insight-ui-collapsible.js";
import { DemoIframeController } from "./insight-ui-demo-container.js";
import { Dropdown } from "./insight-ui-dropdown.js";
import { Floater } from "./insight-ui-floater.js";
import { Modal } from "./insight-ui-modal.js";
import { Multiselect } from "./insight-ui-multiselect.js";
import { Sidebar } from "./insight-ui-sidebar.js";
import { Tabs } from "./insight-ui-tabs.js";
import { ThemeToggle } from "./insight-ui-theme-toggle.js";
import { ThreeDCarousel } from "./insight-ui-3D-carousel.js";

function initAll() {
	Accordion.initAll();
	Carousel.initAll();
	Checkbox.initAll();
	CodeBlock.initAll();
	Collapsible.initAll();
	DemoIframeController.initAll();
	Dropdown.initAll();
	Floater.initAll();
	Modal.initAll();
	Multiselect.initAll();
	Sidebar.initAll();
	Tabs.initAll();
	ThemeToggle.initAll();
	ThreeDCarousel.initAll();
	// InsightUI.WebSocket.init();
}

document.addEventListener('DOMContentLoaded', function () {
	debugLog('InsightUI initializing...');
	debugLog('InsightUI components found:', window.InsightUI);

	// Initialize all instances
	initAll();

	// Initialize all (new) instances after htmx manipulates the DOM
	htmx.on("htmx:afterSwap", function (evt) {
		debugLog("Initialize new instances...")
		initAll();
		debugLog("New instances initialized!")
	});

	debugLog('Finished with initialization!');
});
