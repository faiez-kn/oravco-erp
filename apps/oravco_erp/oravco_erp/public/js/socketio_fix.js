// Fix WebSocket connection for Docker/production setup
// Override get_host method to use /socket.io path through nginx
(function() {
	'use strict';
	
	// Ensure dev_server is false for Docker/production
	if (typeof window !== 'undefined') {
		// In Docker, we're not in dev mode
		if (window.location.hostname !== 'localhost' || window.location.port !== '8000') {
			window.dev_server = false;
		}
	}
	
	// Wait for frappe.realtime to be available
	function fixSocketIOConnection() {
		if (typeof frappe !== 'undefined' && frappe.realtime && frappe.realtime.get_host) {
			// Override get_host method
			const originalGetHost = frappe.realtime.get_host.bind(frappe.realtime);
			
			frappe.realtime.get_host = function(port = 9000) {
				let host = window.location.origin;
				
				// Force use of nginx proxy path for Docker/production
				// Check if we're in Docker by checking if dev_server is explicitly false
				// or if we're accessing through port 8090 (nginx frontend)
				if (window.dev_server === false || window.location.port === '8090' || 
				    (window.location.hostname !== 'localhost' && window.location.port !== '8000')) {
					// In production/Docker, use /socket.io path through nginx
					return host + `/socket.io/${frappe.boot.sitename}`;
				}
				
				// Use original logic for dev server
				return originalGetHost(port);
			};
			
			// Override init to ensure proper connection
			const originalInit = frappe.realtime.init.bind(frappe.realtime);
			frappe.realtime.init = function(port, lazy_connect) {
				// Ensure dev_server is false
				if (window.location.port === '8090' || window.location.hostname !== 'localhost') {
					window.dev_server = false;
				}
				return originalInit(port, lazy_connect);
			};
			
			// If socket is already initialized, reinitialize it
			if (frappe.realtime.socket) {
				// Disconnect old socket
				if (frappe.realtime.socket.connected) {
					frappe.realtime.socket.disconnect();
				}
				// Clear socket reference
				frappe.realtime.socket = null;
				// Reinitialize with correct path
				setTimeout(function() {
					frappe.realtime.init();
				}, 100);
			}
			
			console.log('✓ WebSocket connection path fixed for Docker/production');
			return true;
		}
		return false;
	}
	
	// Try to fix immediately if frappe is already loaded
	if (fixSocketIOConnection()) {
		return;
	}
	
	// Otherwise wait for frappe to be ready
	if (typeof frappe !== 'undefined' && typeof frappe.ready === 'function') {
		frappe.ready(function() {
			setTimeout(fixSocketIOConnection, 100);
		});
	} else {
		// Fallback: wait for window load
		if (document.readyState === 'loading') {
			document.addEventListener('DOMContentLoaded', function() {
				setTimeout(fixSocketIOConnection, 500);
			});
		} else {
			setTimeout(fixSocketIOConnection, 500);
		}
	}
})();

