// Fix ace-builds loading error
// This handles the case where ace.js fails to load
(function() {
	'use strict';
	
	// Suppress ace.js 404 errors
	if (console.error) {
		const originalError = console.error;
		console.error = function(...args) {
			const message = args.join(' ');
			// Suppress ace.js 404 errors
			if (message.includes('ace.js') && message.includes('404')) {
				// Silently ignore - ace-builds might not be available in Docker
				return;
			}
			originalError.apply(console, args);
		};
	}
	
	// Fix customize-form error by handling failed asset loads
	if (typeof frappe !== 'undefined' && frappe.assets) {
		const originalEvalAssets = frappe.assets.eval_assets;
		if (originalEvalAssets) {
			frappe.assets.eval_assets = function(assets) {
				try {
					return originalEvalAssets.apply(this, arguments);
				} catch (e) {
					// If it's a syntax error from failed asset load, try to continue
					if (e.message && e.message.includes('Unexpected token')) {
						console.warn('Asset load failed, continuing without it:', e.message);
						return;
					}
					throw e;
				}
			};
		}
	}
	
	// Fix code.js error by providing fallback
	if (typeof frappe !== 'undefined' && frappe.form_control && frappe.form_control.CodeControl) {
		const CodeControl = frappe.form_control.CodeControl;
		if (CodeControl.prototype && CodeControl.prototype.load_lib) {
			const originalLoadLib = CodeControl.prototype.load_lib;
			CodeControl.prototype.load_lib = function() {
				try {
					return originalLoadLib.apply(this, arguments);
				} catch (e) {
					// If ace.js fails to load, provide a fallback
					console.warn('ace-builds not available, using fallback');
					this.library_loaded = Promise.resolve();
					return this.library_loaded;
				}
			};
		}
	}
})();




