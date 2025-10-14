/**
 * Insight UI - Component Initializer
 */

document.addEventListener('DOMContentLoaded', function () {
  console.log('🚀 InsightUI Initialisierung gestartet');
  console.log('🔍 InsightUI Objekt:', window.InsightUI);
  console.log('🔍 HTMX verfügbar:', typeof htmx !== 'undefined');
  console.log('🔍 WebSocket API verfügbar:', typeof WebSocket !== 'undefined');

  // Check if all modules available
  console.log('🔍 Available modules:');
  console.log('  - Code Block:', typeof InsightUI.CodeBlock);
  console.log('  - Collapsible:', typeof InsightUI.Collapsible);
  console.log('  - Dropdown:', typeof InsightUI.Dropdown);
  console.log('  - Modal:', typeof InsightUI.Modal);
  console.log('  - Popover:', typeof InsightUI.Popover);
  console.log('  - Language Select:', typeof InsightUI.SelectLanguage);
  console.log('  - Sidebar:', typeof InsightUI.Sidebar);
  console.log('  - Theme Toggle:', typeof InsightUI.ThemeToggle);
  console.log('  - Tooltip:', typeof InsightUI.Tooltip);
  console.log('  - Accordion:', typeof InsightUI.Accordion);
  console.log('  - Tabs:', typeof InsightUI.Tabs);
  console.log('  - 3D Carousel:', typeof InsightUI.ThreeDCarousel);
  console.log('  - WebSocket:', typeof InsightUI.WebSocket);

  // Initialize all modules
  window.initCarousels();
  InsightUI.CodeBlock.init();
  InsightUI.Collapsible.init();
  InsightUI.Dropdown.init();
  InsightUI.Modal.init();
  InsightUI.Popover.init();
  InsightUI.SelectLanguage.init();
  InsightUI.Sidebar.init();
  InsightUI.ThemeToggle.init();
  InsightUI.Tooltip.init();
  InsightUI.Accordion.init();
  InsightUI.Tabs.init();
  InsightUI.ThreeDCarousel.init();
  // InsightUI.WebSocket.init();
  // console.log('🔌 WebSocket initialisiert');

  // Re-Init off all (new) objects
  htmx.on("htmx:load", function(evt) {
    window.initCarousels();
    InsightUI.CodeBlock.init();
    InsightUI.Collapsible.init();
    InsightUI.Dropdown.init();
    InsightUI.Modal.init();
    InsightUI.Popover.init();
    InsightUI.SelectLanguage.init();
    InsightUI.Sidebar.init();
    // InsightUI.ThemeToggle.init();
    InsightUI.Tooltip.init();
    InsightUI.Accordion.init();
    InsightUI.Tabs.init();
    InsightUI.ThreeDCarousel.init();
  });

  console.log('✅ Alle InsightUI Komponenten erfolgreich initialisiert');
});
