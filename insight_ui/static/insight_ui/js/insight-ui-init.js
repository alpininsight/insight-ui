/**
 * Insight UI - Component Initializer
 */

function initAll() {
	window.initCarousels();
	InsightUI.Accordion.initAll();
	InsightUI.Checkbox.initAll();
	InsightUI.CodeBlock.initAll();
	InsightUI.Collapsible.initAll();
	InsightUI.Dropdown.initAll();
	InsightUI.Floater.initAll();
	InsightUI.Modal.initAll();
	InsightUI.Multiselect.initAll();
	InsightUI.SelectLanguage.init();
	InsightUI.Sidebar.initAll();
	InsightUI.Tabs.initAll();
	InsightUI.ThemeToggle.initAll();
	InsightUI.ThreeDCarousel.init();
	// InsightUI.WebSocket.init();
}

document.addEventListener('DOMContentLoaded', function () {
	debugLog('InsightUI initializing...');
	debugLog('InsightUI components found:', window.InsightUI);
	// debugLog('HTMX available:', typeof htmx !== 'undefined');
	// debugLog('WebSocket API available:', typeof WebSocket !== 'undefined');

	// htmx.logger = function(elt, event, data) {
    //     if(console) {
    //         debugLog("INFO:", event, elt, data);
    //     }
    // }

	// Initialize all instances
	initAll();

	// Initialize all (new) instances after htmx manipulates the DOM
	htmx.on("htmx:afterRequest", function (evt) {
		debugLog("Initialize new instances...")
		initAll();
		debugLog("New instances initialized!")
	});

	debugLog('Finished with initialization!');
});
