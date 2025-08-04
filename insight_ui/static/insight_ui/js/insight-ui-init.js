/**
 * Insight UI - Component Initializer
 */
console.log('📄 insight-ui-init.js wird geladen...');

document.addEventListener('DOMContentLoaded', function () {
  console.log('🚀 InsightUI Initialisierung gestartet');
  console.log('🔍 InsightUI Objekt:', window.InsightUI);
  console.log('🔍 HTMX verfügbar:', typeof htmx !== 'undefined');
  console.log('🔍 WebSocket API verfügbar:', typeof WebSocket !== 'undefined');

  // Prüfe ob alle Module verfügbar sind
  console.log('🔍 Verfügbare Module:');
  console.log('  - Navbar:', typeof InsightUI.Navbar);
  console.log('  - Alert:', typeof InsightUI.Alert);
  console.log('  - ThemeToggle:', typeof InsightUI.ThemeToggle);
  console.log('  - Modal:', typeof InsightUI.Modal);
  console.log('  - Sidebar:', typeof InsightUI.Sidebar);
  console.log('  - Form:', typeof InsightUI.Form);
  console.log('  - WebSocket:', typeof InsightUI.WebSocket);

  InsightUI.Navbar?.init?.();
  console.log('📊 Navbar initialisiert');

  InsightUI.Alert?.init?.();
  console.log('🚨 Alert initialisiert');

  InsightUI.ThemeToggle?.init?.();
  console.log('🌓 ThemeToggle initialisiert');

  InsightUI.Modal?.init?.();
  console.log('📋 Modal initialisiert');

  InsightUI.Sidebar?.init?.();
  console.log('📂 Sidebar initialisiert');

  InsightUI.Form?.init?.();
  console.log('📝 Form initialisiert');

  // InsightUI.WebSocket?.init?.();
  // console.log('🔌 WebSocket initialisiert');

  console.log('✅ Alle InsightUI Komponenten erfolgreich initialisiert');
});

console.log('📄 insight-ui-init.js vollständig geladen');
