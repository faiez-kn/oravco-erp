// Oravco ERP Branding Script
// This replaces all instances of "ERPNext" with "Oravco ERP" in the UI

(function() {
	'use strict';

	// Function to replace text in DOM nodes
	function replaceTextInNode(node) {
		if (node.nodeType === Node.TEXT_NODE) {
			if (node.textContent) {
				node.textContent = node.textContent.replace(/ERPNext/g, 'Oravco ERP');
			}
		} else if (node.nodeType === Node.ELEMENT_NODE) {
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
	function applyBranding() {
		replaceTextInNode(document.body);
		
		// Update page title
		if (document.title) {
			document.title = document.title.replace(/ERPNext/g, 'Oravco ERP');
		}
	}

	// Apply immediately
	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', applyBranding);
	} else {
		applyBranding();
	}

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
	if (typeof frappe !== 'undefined') {
		frappe.ready(function() {
			// Update boot info
			if (frappe.boot && frappe.boot.apps_info) {
				Object.keys(frappe.boot.apps_info).forEach(function(app) {
					const appInfo = frappe.boot.apps_info[app];
					if (appInfo && appInfo.app_title === "ERPNext") {
						appInfo.app_title = "Oravco ERP";
					}
				});
			}

			// Update system settings in boot
			if (frappe.boot && frappe.boot.sysdefaults && frappe.boot.sysdefaults.app_name === "ERPNext") {
				frappe.boot.sysdefaults.app_name = "Oravco ERP";
			}
		});
	}

	// Update page title periodically
	setInterval(function() {
		if (document.title) {
			document.title = document.title.replace(/ERPNext/g, 'Oravco ERP');
		}
	}, 1000);
})();

