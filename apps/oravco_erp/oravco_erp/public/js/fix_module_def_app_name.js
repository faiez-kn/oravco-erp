// Fix Module Def and Module Def List to show "Oravco ERP" instead of "erpnext" and "frappe"
(function() {
	'use strict';
	
	console.log('✓ fix_module_def_app_name.js loaded');
	
	// Map of app names to display names
	const APP_NAME_MAP = {
		'erpnext': 'Oravco ERP',
		'ERPNext': 'Oravco ERP',
		'frappe': 'Oravco ERP',
		'Frappe': 'Oravco ERP'
	};
	
	function getDisplayName(appName) {
		return APP_NAME_MAP[appName] || appName;
	}
	
	function shouldReplace(appName) {
		return APP_NAME_MAP.hasOwnProperty(appName);
	}
	
	
	// Fix Module Def form
	frappe.ui.form.on("Module Def", {
		refresh: function(frm) {
			// Wait for the app_name options to be loaded
			setTimeout(function() {
				if (frm.fields_dict && frm.fields_dict.app_name) {
					const field = frm.fields_dict.app_name;
					
					// Update select dropdown options text (keep values, change display)
					if (field.$input && field.$input.is('select')) {
						field.$input.find('option').each(function() {
							const $opt = $(this);
							const val = $opt.val();
							if (shouldReplace(val)) {
								$opt.text(getDisplayName(val));
							}
						});
					}
					
					// Update the displayed value if current doc has erpnext/frappe
					if (frm.doc.app_name && shouldReplace(frm.doc.app_name)) {
						// Update the input display
						const $wrapper = $(field.wrapper || field.$wrapper);
						if ($wrapper.length) {
							const $display = $wrapper.find('.link-content, .form-control, .awesomplete input');
							if ($display.length) {
								$display.text(getDisplayName(frm.doc.app_name));
							}
						}
					}
				}
			}, 500);
		},
		
		app_name: function(frm) {
			// When app_name changes, update display
			if (frm.doc.app_name && shouldReplace(frm.doc.app_name)) {
				setTimeout(function() {
					const field = frm.fields_dict.app_name;
					if (field && field.$input) {
						if (field.$input.is('select')) {
							field.$input.find('option:selected').text(getDisplayName(frm.doc.app_name));
						}
					}
				}, 100);
			}
		}
	});
	
	// Fix Module Def List view - override the existing onload if it exists
	const originalModuleDefListOnload = frappe.listview_settings["Module Def"]?.onload;
	
	frappe.listview_settings["Module Def"] = {
		onload: function(list_view) {
			// Call original onload if it exists
			if (originalModuleDefListOnload) {
				originalModuleDefListOnload.call(this, list_view);
			}
			
			// Get apps and update filter dropdown options
			frappe.call({
				method: "frappe.core.doctype.module_def.module_def.get_installed_apps",
				callback: function(r) {
					const field = list_view.page.fields_dict.app_name;
					if (!field) return;
					
					try {
						let options = JSON.parse(r.message);
						options.unshift(""); // Add empty option
						
						// Keep original values but update display in dropdown
						field.df.options = options;
						field.set_options();
						
						// Update dropdown option text after it's rendered
						setTimeout(function() {
							if (field.$input && field.$input.is('select')) {
								field.$input.find('option').each(function() {
									const $opt = $(this);
									const val = $opt.val();
									if (shouldReplace(val)) {
										$opt.text(getDisplayName(val));
									}
								});
							}
						}, 200);
					} catch (e) {
						console.warn('Error parsing app names:', e);
					}
				}
			});
		},
		
		formatters: {
			app_name: function(value, row, column, data, default_formatter) {
				// Replace app name display in list cells
				if (shouldReplace(value)) {
					value = getDisplayName(value);
				}
				return default_formatter(value, row, column, data);
			}
		}
	};
	
	// Also fix the app_name field display in list after data loads
	if (typeof frappe !== 'undefined' && frappe.listview) {
		const originalRefresh = frappe.listview.refresh;
		frappe.listview.refresh = function() {
			const result = originalRefresh.apply(this, arguments);
			
			// If this is Module Def list, update app_name displays
			if (this.doctype === 'Module Def') {
				setTimeout(function() {
					// Update all app_name cells in the list
					$('.list-row[data-name]').each(function() {
						const $row = $(this);
						const $appNameCell = $row.find('[data-fieldname="app_name"]');
						if ($appNameCell.length) {
							const currentValue = $appNameCell.text().trim();
							if (shouldReplace(currentValue)) {
								$appNameCell.text(getDisplayName(currentValue));
							}
						}
					});
				}, 500);
			}
			
			return result;
		};
	}
	
	// Monitor for dynamically loaded app_name fields and update them
	if (typeof MutationObserver !== 'undefined') {
		const observer = new MutationObserver(function(mutations) {
			mutations.forEach(function(mutation) {
				mutation.addedNodes.forEach(function(node) {
					if (node.nodeType === 1) { // Element node
						// Check if this is an app_name field
						const $appNameField = $(node).find('[data-fieldname="app_name"]').addBack('[data-fieldname="app_name"]');
						if ($appNameField.length) {
							// Update select options
							$appNameField.find('option').each(function() {
								const $opt = $(this);
								const val = $opt.val();
								if (shouldReplace(val)) {
									$opt.text(getDisplayName(val));
								}
							});
							
							// Update displayed text
							const text = $appNameField.text().trim();
							if (shouldReplace(text)) {
								$appNameField.text(getDisplayName(text));
							}
						}
					}
				});
			});
		});
		
		// Observe the document body for changes
		observer.observe(document.body, {
			childList: true,
			subtree: true
		});
	}
})();

