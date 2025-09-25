/**
 * Insight UI WebSocket Handler
 */
window.InsightUI = window.InsightUI || {};

InsightUI.WebSocket = {
  init: function() {
    console.log('🔌 InsightUI.WebSocket.init() - Start WebSocket handler initialization');
    console.log('🔍 Current timestamp:', new Date().toISOString());

    // Wait until HTMX is fully loaded
    if (typeof htmx === 'undefined') {
      console.warn('⚠️ HTMX not loaded yet, wait 100ms...');
      setTimeout(() => this.init(), 100);
      return;
    }
    console.log('✅ HTMX found, Version:', htmx.version || 'unknown');
    console.log('🔍 HTMX object:', htmx);
    console.log('🔍 HTMX config:', htmx.config);

    // Detaillierte Extension-Prüfung
    if (!htmx.config.extensions) {
      console.warn('⚠️ HTMX extensions not available, re-initialize in 200ms...');
      setTimeout(() => this.init(), 200);
      return;
    } else {
      console.log('✅ HTMX extensions detected');
      console.log('🔍 HTMX Extensions:', htmx.config.extensions);
    }

    // Check if WebSocket is available in the browser
    if (typeof WebSocket === 'undefined') {
      console.error('❌ WebSocket API not available!');
      return;
    }
    console.log('✅ WebSocket API available!');

    // Check WebSocket components on the site
    const wsComponents = document.querySelectorAll('[hx-ext*="ws"]');
    console.log(`📊 ${wsComponents.length} WebSocket-component(s) found:`);

    wsComponents.forEach((component, index) => {
      const id = component.id || `ws-component-${index}`;
      const wsUrl = component.getAttribute('ws-connect') || 'not set';
      console.log(`  ${index + 1}. ID: ${id}, URL: ${wsUrl}`);
      console.log(`     Element:`, component);
    });

    // Test: Manueller WebSocket-Verbindungstest
    console.log('🧪 Test direct WebSocket connection...');
    try {
      const testWs = new WebSocket('ws://localhost:8765');
      testWs.onopen = () => {
        console.log('✅ Direct WebSocket connection successful:');
        testWs.close();
      };
      testWs.onerror = (e) => {
        console.error('❌ Direct WebSocket connection failed:', e);
      };
      testWs.onclose = (e) => {
        console.log('🔴 Test-WebSocket closed, Code:', e.code, 'Reason:', e.reason);
      };
    } catch (error) {
      console.error('❌ Error creating test WebSocket:', error);
    }

    // WebSocket connection established
    document.body.addEventListener('htmx:wsOpen', function(evt) {
      console.log('🟢 WebSocket connection established:', {
        target: evt.target.id || 'unknown',
        url: evt.detail?.socketWrapper?.socket?.url || 'unknown',
        timestamp: new Date().toISOString()
      });

      const wsElement = evt.target;
      const statusElement = wsElement.querySelector('[id$="-status"]');
      if (statusElement) {
        statusElement.textContent = 'Verbunden';
        statusElement.className = 'insight-websocket__status-text insight-websocket__status-text--connected';
        console.log('✅ Status-Element updated: Verbunden');
      } else {
        console.warn('⚠️ Status element not found for WebSocket:', wsElement.id);
      }
    });

    // WebSocket connection closed
    document.body.addEventListener('htmx:wsClose', function(evt) {
      console.log('🔴 WebSocket connection closed:', {
        target: evt.target.id || 'unknown',
        code: evt.detail?.code || 'unknown',
        reason: evt.detail?.reason || 'unknown',
        wasClean: evt.detail?.wasClean || false,
        timestamp: new Date().toISOString()
      });

      const wsElement = evt.target;
      const statusElement = wsElement.querySelector('[id$="-status"]');
      if (statusElement) {
        statusElement.textContent = 'Disconnected';
        statusElement.className = 'insight-websocket__status-text insight-websocket__status-text--disconnected';
        console.log('✅ Status-Element updated: disconnected');
      }
    });

    // WebSocket Fehler
    document.body.addEventListener('htmx:wsError', function(evt) {
      console.error('❌ WebSocket error:', {
        target: evt.target.id || 'unknown',
        error: evt.detail?.error || 'unknown',
        message: evt.detail?.message || 'unknown',
        timestamp: new Date().toISOString()
      });

      const wsElement = evt.target;
      const statusElement = wsElement.querySelector('[id$="-status"]');
      if (statusElement) {
        statusElement.textContent = 'Connection error';
        statusElement.className = 'insight-websocket__status-text insight-websocket__status-text--error';
        console.log('✅ Status-Element updated: Connection error');
      }
    });

    // WebSocket received message - HTMX v2 WebSocket Extension
    document.body.addEventListener('htmx:wsAfterMessage', function(evt) {
      console.log('📨 WebSocket received message:', {
        target: evt.target.id || 'unknown',
        messageLength: evt.detail?.message?.length || 0,
        message: evt.detail?.message || 'no message',
        timestamp: new Date().toISOString()
      });

      // Check if the message contains HTML (for HTMX OOB swaps)
      if (evt.detail?.message && evt.detail.message.trim().startsWith('<')) {
        console.log('📄 HTML message detected, HTMX processed automatically');
        return; // HTMX automatically processes HTML
      }

      // Process JSON messages manually
      try {
        const wsElement = evt.target;
        const outputElement = wsElement.querySelector('[id$="-output"]');
        if (outputElement && evt.detail?.message) {
          const data = JSON.parse(evt.detail.message);
          const formattedData = `
            <div class="mb-2 p-2 border-l-4 border-blue-500 bg-white dark:bg-gray-600 rounded">
              <div class="text-xs text-secondary">${new Date().toLocaleTimeString()}</div>
              <div class="font-semibold text-blue-600 dark:text-blue-400">Connection: ${data.connection_id?.substring(0, 8) || 'unknown'}</div>
              <div class="text-sm space-y-1">
                <div>💾 Disk: ${data.content?.disk?.used_gb || 0}GB / ${data.content?.disk?.total_gb || 0}GB</div>
                <div>🧠 Memory: ${data.content?.memory?.percent_used || 0}% used</div>
                <div>🌐 Client: ${data.client_info?.ip || 'unknown'}</div>
              </div>
            </div>
          `;

          // Add new message at the beginning
          const tempDiv = document.createElement('div');
          tempDiv.innerHTML = formattedData;
          outputElement.insertBefore(tempDiv.firstElementChild, outputElement.firstElementChild);

          // Limit the number of messages displayed
          const messages = outputElement.querySelectorAll('div.mb-2');
          if (messages.length > 10) {
            messages[messages.length - 1].remove();
          }
        }
      } catch (error) {
        console.error('❌ Error processing WebSocket message:', error);
        console.log('📝 Raw message:', evt.detail?.message);
      }
    });

    // WebSocket send message
    document.body.addEventListener('htmx:wsBeforeSend', function(evt) {
      console.log('📤 WebSocket send message:', {
        target: evt.target.id || 'unknown',
        messageLength: evt.detail?.message?.length || 0,
        timestamp: new Date().toISOString()
      });
    });

    // WebSocket try to reconnect
    document.body.addEventListener('htmx:wsConnecting', function(evt) {
      console.log('🔄 WebSocket Reconnect-Versuch:', {
        target: evt.target.id || 'unknown',
        attempt: evt.detail?.attempt || 'unknown',
        timestamp: new Date().toISOString()
      });

      const wsElement = evt.target;
      const statusElement = wsElement.querySelector('[id$="-status"]');
      if (statusElement) {
        statusElement.textContent = 'Establish connection...';
        statusElement.className = 'insight-websocket__status-text insight-websocket__status-text--connecting';
      }
    });

    console.log('✅ InsightUI WebSocket Handler initialized successfully');
  }
};
