// Oravco ERP Branding Script
// This replaces any remaining instances of "ERPNext" with "Oravco ERP" in the UI

(function() {
	'use strict';

	// Function to replace text in DOM nodes
	function replaceTextInNode(node) {
		if (node.nodeType === Node.TEXT_NODE) {
			// Replace any remaining ERPNext references with Oravco ERP
			if (node.textContent) {
				node.textContent = node.textContent.replace(/ERPNext/g, 'Oravco ERP');
			}
		} else if (node.nodeType === Node.ELEMENT_NODE) {
			// Skip script and style tags
			if (node.tagName !== 'SCRIPT' && node.tagName !== 'STYLE') {
				// Replace in attributes
				if (node.title) {
					node.title = node.title.replace(/ERPNext/g, 'Oravco ERP');
				}
				if (node.alt) {
					node.alt = node.alt.replace(/ERPNext/g, 'Oravco ERP');
				}
				if (node.placeholder) {
					node.placeholder = node.placeholder.replace(/ERPNext/g, 'Oravco ERP');
				}
				
				// Recursively process child nodes
				for (let i = 0; i < node.childNodes.length; i++) {
					replaceTextInNode(node.childNodes[i]);
				}
			}
		}
	}

	// Replace on page load
	document.addEventListener('DOMContentLoaded', function() {
		replaceTextInNode(document.body);
	});

	// Watch for dynamic content changes
	if (typeof MutationObserver !== 'undefined') {
		const observer = new MutationObserver(function(mutations) {
			mutations.forEach(function(mutation) {
				mutation.addedNodes.forEach(function(node) {
					if (node.nodeType === Node.ELEMENT_NODE || node.nodeType === Node.TEXT_NODE) {
						replaceTextInNode(node);
					}
				});
			});
		});

		observer.observe(document.body, {
			childList: true,
			subtree: true
		});
	}

	// Override boot info if available
	if (typeof frappe !== 'undefined' && frappe.boot) {
		// Update boot info
		if (frappe.boot.apps_info) {
			Object.keys(frappe.boot.apps_info).forEach(function(app) {
				const appInfo = frappe.boot.apps_info[app];
				if (appInfo && appInfo.app_title === "ERPNext") {
					appInfo.app_title = "Oravco ERP";
				}
			});
		}

		// Update system settings in boot
		if (frappe.boot.sysdefaults && frappe.boot.sysdefaults.app_name === "ERPNext") {
			frappe.boot.sysdefaults.app_name = "Oravco ERP";
		}
	}

	// Update page title
	function updatePageTitle() {
		if (document.title) {
			document.title = document.title.replace(/ERPNext/g, 'Oravco ERP');
		}
	}

	updatePageTitle();
	setInterval(updatePageTitle, 1000); // Update every second for dynamic title changes

	// Override frappe.get_route_str if needed
	if (typeof frappe !== 'undefined' && frappe.get_route_str) {
		const originalGetRouteStr = frappe.get_route_str;
		frappe.get_route_str = function() {
			const route = originalGetRouteStr.apply(this, arguments);
			return route.replace(/ERPNext/g, 'Oravco ERP');
		};
	}
})();

