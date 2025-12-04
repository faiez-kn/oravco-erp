// Force update logo everywhere on client side
// This ensures the logo is refreshed even if cached
(function() {
	'use strict';
	
	const LOGO_PATH = '/files/oravco-logo.png';
	const LOGO_PATH_ASSETS = '/assets/oravco_erp/images/oravco-logo.png';
	const TIMESTAMP = '?v=' + Date.now();
	
	function updateLogo(img, path) {
		if (!img) return;
		
		// Force reload by adding timestamp
		const currentSrc = img.src || img.getAttribute('src');
		if (currentSrc && (currentSrc.includes('oravco-logo') || currentSrc.includes('erpnext') || currentSrc.includes('frappe'))) {
			// Update to new logo with timestamp to bypass cache
			const newSrc = path + TIMESTAMP;
			img.src = newSrc;
			img.setAttribute('src', newSrc);
			
			// Handle load error - try alternative path
			img.onerror = function() {
				if (path === LOGO_PATH) {
					img.src = LOGO_PATH_ASSETS + TIMESTAMP;
				} else {
					img.src = LOGO_PATH + TIMESTAMP;
				}
			};
		}
	}
	
	function updateAllLogos() {
		// Update navbar logo
		const navbarLogos = document.querySelectorAll('.app-logo, .navbar-brand img, [class*="app-logo"]');
		navbarLogos.forEach(function(img) {
			updateLogo(img, LOGO_PATH);
		});
		
		// Update login page logo
		const loginLogos = document.querySelectorAll('.page-card-head img, .login-logo img, .app-logo');
		loginLogos.forEach(function(img) {
			updateLogo(img, LOGO_PATH);
		});
		
		// Update splash screen logo
		const splashLogos = document.querySelectorAll('.splash img, [class*="splash"] img');
		splashLogos.forEach(function(img) {
			updateLogo(img, LOGO_PATH);
		});
		
		// Update apps page logos
		const appCards = document.querySelectorAll('.app-card img, [data-app-name="oravco_erp"] img');
		appCards.forEach(function(img) {
			updateLogo(img, LOGO_PATH_ASSETS);
		});
		
		// Update favicon
		let favicon = document.querySelector('link[rel="icon"], link[rel="shortcut icon"]');
		if (favicon) {
			favicon.href = LOGO_PATH + TIMESTAMP;
		} else {
			favicon = document.createElement('link');
			favicon.rel = 'icon';
			favicon.href = LOGO_PATH + TIMESTAMP;
			document.head.appendChild(favicon);
		}
		
		// Update boot logo URL if available
		if (typeof frappe !== 'undefined' && frappe.boot) {
			frappe.boot.app_logo_url = LOGO_PATH + TIMESTAMP;
		}
	}
	
	// Run immediately
	updateAllLogos();
	
	// Run after DOM is loaded
	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', updateAllLogos);
	} else {
		updateAllLogos();
	}
	
	// Run after frappe is ready
	if (typeof frappe !== 'undefined' && typeof frappe.ready === 'function') {
		frappe.ready(function() {
			setTimeout(updateAllLogos, 100);
		});
	}
	
	// Watch for dynamically added logos
	if (typeof MutationObserver !== 'undefined') {
		const observer = new MutationObserver(function(mutations) {
			mutations.forEach(function(mutation) {
				mutation.addedNodes.forEach(function(node) {
					if (node.nodeType === 1) {
						// Check if it's an img or contains imgs
						if (node.tagName === 'IMG') {
							updateLogo(node, LOGO_PATH);
						} else {
							const imgs = node.querySelectorAll && node.querySelectorAll('img');
							if (imgs) {
								imgs.forEach(function(img) {
									updateLogo(img, LOGO_PATH);
								});
							}
						}
					}
				});
			});
		});
		
		observer.observe(document.body, {
			childList: true,
			subtree: true
		});
	}
	
	// Also update on route change (for SPA navigation)
	if (typeof frappe !== 'undefined' && frappe.router) {
		const originalRoute = frappe.router.route;
		frappe.router.route = function() {
			const result = originalRoute.apply(this, arguments);
			setTimeout(updateAllLogos, 200);
			return result;
		};
	}
})();




