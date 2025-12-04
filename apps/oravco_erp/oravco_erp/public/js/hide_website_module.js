// Hide Website module from sidebar and desktop
(function() {
	'use strict';
	
	console.log('✓ hide_website_module.js loaded');
	
	const MODULES_TO_HIDE = ['Website']; // Add more modules here if needed
	
	function hideModuleFromUI(moduleName) {
		// Hide from sidebar (workspace)
		const sidebarSelector = `.sidebar-item[data-name="${moduleName}"], .workspace-link[data-name="${moduleName}"]`;
		$(sidebarSelector).hide();
		
		// Hide from desktop icons
		const desktopIconSelector = `.desktop-icon[data-module-name="${moduleName}"]`;
		$(desktopIconSelector).hide();
		
		// Hide from module selector
		const moduleSelector = `.module-link[data-module="${moduleName}"], .module-item[data-module="${moduleName}"]`;
		$(moduleSelector).hide();
		
		// Hide from workspace sidebar items
		$(`.workspace-sidebar-item[data-name="${moduleName}"]`).hide();
		$(`.workspace-item[data-name="${moduleName}"]`).hide();
	}
	
	function hideAllConfiguredModules() {
		MODULES_TO_HIDE.forEach(moduleName => {
			hideModuleFromUI(moduleName);
		});
	}
	
	// Hide modules when DOM is ready
	$(document).ready(function() {
		hideAllConfiguredModules();
	});
	
	// Hide modules when sidebar is loaded/refreshed
	if (typeof frappe !== 'undefined') {
		// Hook into workspace sidebar refresh
		const originalGetWorkspaceSidebarItems = frappe.desk?.get_workspace_sidebar_items;
		if (originalGetWorkspaceSidebarItems) {
			frappe.desk.get_workspace_sidebar_items = function() {
				const result = originalGetWorkspaceSidebarItems.apply(this, arguments);
				setTimeout(hideAllConfiguredModules, 100);
				return result;
			};
		}
		
		// Hide when workspace is loaded
		frappe.router.on('change', function() {
			setTimeout(hideAllConfiguredModules, 200);
		});
		
		// Hide when desktop icons are loaded
		if (frappe.desk?.desktop) {
			const originalGetDesktopIcons = frappe.desk.desktop.get_desktop_icons;
			if (originalGetDesktopIcons) {
				frappe.desk.desktop.get_desktop_icons = function() {
					const result = originalGetDesktopIcons.apply(this, arguments);
					setTimeout(hideAllConfiguredModules, 100);
					return result;
				};
			}
		}
	}
	
	// Use MutationObserver to hide modules that appear dynamically
	if (typeof MutationObserver !== 'undefined') {
		const observer = new MutationObserver(function(mutations) {
			let shouldHide = false;
			mutations.forEach(function(mutation) {
				mutation.addedNodes.forEach(function(node) {
					if (node.nodeType === 1) { // Element node
						const $node = $(node);
						// Check if any hidden module appears
						MODULES_TO_HIDE.forEach(moduleName => {
							if ($node.is(`[data-name="${moduleName}"], [data-module-name="${moduleName}"], [data-module="${moduleName}"]`) ||
								$node.find(`[data-name="${moduleName}"], [data-module-name="${moduleName}"], [data-module="${moduleName}"]`).length > 0) {
								shouldHide = true;
							}
						});
					}
				});
			});
			
			if (shouldHide) {
				hideAllConfiguredModules();
			}
		});
		
		// Observe sidebar and desktop areas
		$(document).ready(function() {
			const sidebar = document.querySelector('.sidebar, .workspace-sidebar, .desk-sidebar');
			const desktop = document.querySelector('.desktop, .desktop-icons');
			
			if (sidebar) {
				observer.observe(sidebar, {
					childList: true,
					subtree: true
				});
			}
			
			if (desktop) {
				observer.observe(desktop, {
					childList: true,
					subtree: true
				});
			}
			
			// Also observe body for dynamically added elements
			observer.observe(document.body, {
				childList: true,
				subtree: true
			});
		});
	}
	
	// Additional CSS to ensure hidden modules stay hidden
	const style = document.createElement('style');
	style.textContent = `
		/* Hide Website module from sidebar */
		.sidebar-item[data-name="Website"],
		.workspace-link[data-name="Website"],
		.workspace-sidebar-item[data-name="Website"],
		.workspace-item[data-name="Website"],
		.module-link[data-module="Website"],
		.module-item[data-module="Website"] {
			display: none !important;
		}
		
		/* Hide Website desktop icon */
		.desktop-icon[data-module-name="Website"] {
			display: none !important;
		}
		
		/* Hide Website from module selector */
		.module-selector [data-module="Website"],
		.module-list [data-module="Website"] {
			display: none !important;
		}
	`;
	document.head.appendChild(style);
	
	console.log('✓ Website module hidden from UI');
})();

