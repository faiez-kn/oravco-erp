// Fix WebSocket connection for Docker/production setup
// Override get_host method to use /socket.io path through nginx
(function() {
	'use strict';
	
	// Wait for frappe.realtime to be available
	function fixSocketIOConnection() {
		if (typeof frappe !== 'undefined' && frappe.realtime && frappe.realtime.get_host) {
			// Override get_host method
			const originalGetHost = frappe.realtime.get_host.bind(frappe.realtime);
			
			frappe.realtime.get_host = function(port = 9000) {
				let host = window.location.origin;
				if (window.dev_server) {
					// Use original logic for dev server
					return originalGetHost(port);
				}
				// In production/Docker, use /socket.io path through nginx
				return host + `/socket.io/${frappe.boot.sitename}`;
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
				frappe.realtime.init();
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

