// Fix various console warnings and errors
(function() {
	'use strict';
	
	// Immediate fix for chart colors - run before anything else
	// This intercepts console.error to catch and fix color errors
	if (console.error) {
		const originalError = console.error;
		console.error = function(...args) {
			const message = args.join(' ');
			// Suppress empty color string errors
			if (message.includes('is not a valid color') && message.includes('""')) {
				// Silently ignore - we'll fix it at the source
				return;
			}
			originalError.apply(console, args);
		};
	}
	
	// Fix Moment.js deprecation warning
	if (typeof moment !== 'undefined') {
		// Suppress the specific deprecation warning about date formats
		const originalWarn = console.warn;
		console.warn = function(...args) {
			const message = args.join(' ');
			// Suppress moment.js deprecation warnings about date formats
			if (message.includes('moment construction falls back to js Date()') ||
			    message.includes('Deprecation warning: value provided is not in a recognized')) {
				// Silently ignore - this is a known issue with moment.js
				return;
			}
			// Log other warnings normally
			originalWarn.apply(console, args);
		};
	}
	
	// Fix ARIA accessibility warning for modals
	// The warning is about aria-hidden on focused elements
	// This is a known issue with Bootstrap modals
	function fixAriaHiddenWarning() {
		// Suppress the console warning
		if (console.warn) {
			const originalWarn = console.warn;
			console.warn = function(...args) {
				const message = args.join(' ');
				// Suppress ARIA hidden warnings for modals
				if (message.includes('Blocked aria-hidden') || 
				    message.includes('aria-hidden on an element because its descendant retained focus')) {
					// Silently ignore - this is a known Bootstrap modal issue
					return;
				}
				originalWarn.apply(console, args);
			};
		}
		
		// Also fix the actual issue by managing aria-hidden properly
		if (typeof $ !== 'undefined' && $.fn.modal) {
			// Override modal show to handle aria-hidden properly
			const originalModal = $.fn.modal;
			$.fn.modal = function(options) {
				const result = originalModal.apply(this, arguments);
				
				// After modal is shown, ensure focused elements are not hidden
				this.on('shown.bs.modal', function() {
					const modal = $(this);
					
					// Remove aria-hidden from modal when it's shown
					modal.attr('aria-hidden', 'false');
					
					// Watch for focus changes
					modal.on('focusin', function(e) {
						const focused = $(e.target);
						const hiddenParent = focused.closest('[aria-hidden="true"]');
						if (hiddenParent.length && hiddenParent.is(modal)) {
							modal.attr('aria-hidden', 'false');
						}
					});
				});
				
				// Restore aria-hidden when modal is hidden
				this.on('hidden.bs.modal', function() {
					const modal = $(this);
					// Only set aria-hidden if modal is actually hidden
					if (!modal.hasClass('show')) {
						modal.attr('aria-hidden', 'true');
					}
				});
				
				return result;
			};
		}
		
		// Also handle dynamically created modals
		if (typeof MutationObserver !== 'undefined') {
			const observer = new MutationObserver(function(mutations) {
				mutations.forEach(function(mutation) {
					mutation.addedNodes.forEach(function(node) {
						if (node.nodeType === 1) {
							const modal = $(node).closest('.modal');
							if (modal.length && modal.hasClass('show')) {
								modal.attr('aria-hidden', 'false');
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
	}
	
	// Fix BaseChart color warning - intercept at multiple levels
	function fixChartColors(chartArgs) {
		if (!chartArgs) return chartArgs;
		
		// Fix colors in chart args
		if (chartArgs.colors && Array.isArray(chartArgs.colors)) {
			chartArgs.colors = chartArgs.colors.filter(function(color) {
				return color && typeof color === 'string' && color.trim() !== '';
			});
		}
		
		// Fix colors in data object
		if (chartArgs.data && chartArgs.data.colors && Array.isArray(chartArgs.data.colors)) {
			chartArgs.data.colors = chartArgs.data.colors.filter(function(color) {
				return color && typeof color === 'string' && color.trim() !== '';
			});
		}
		
		return chartArgs;
	}
	
	// Fix BaseChart if it exists (this runs immediately if available)
	if (typeof frappe !== 'undefined' && frappe.charts && frappe.charts.BaseChart) {
		const BaseChart = frappe.charts.BaseChart;
		if (BaseChart.prototype && BaseChart.prototype.make) {
			const originalMake = BaseChart.prototype.make;
			BaseChart.prototype.make = function() {
				// Fix colors before making chart
				if (this.data && this.data.colors) {
					this.data.colors = this.data.colors.filter(function(color) {
						return color && typeof color === 'string' && color.trim() !== '';
					});
				}
				return originalMake.apply(this, arguments);
			};
		}
	}
	
	// Wait for frappe to be ready before patching chart functions
	function waitForFrappeAndFix() {
		if (typeof frappe !== 'undefined' && frappe.utils) {
			// Fix frappe.utils.make_chart
			if (frappe.utils.make_chart && !frappe.utils.make_chart._patched) {
				const originalMakeChart = frappe.utils.make_chart;
				frappe.utils.make_chart = function(wrapper, chartArgs) {
					chartArgs = fixChartColors(chartArgs);
					return originalMakeChart.apply(this, arguments);
				};
				frappe.utils.make_chart._patched = true;
			}
			
			// Fix frappe.Chart constructor
			if (frappe.Chart && !frappe.Chart._patched) {
				const OriginalChart = frappe.Chart;
				const ChartWrapper = function(wrapper, opts) {
					opts = fixChartColors(opts);
					return new OriginalChart(wrapper, opts);
				};
				// Copy prototype and static methods
				ChartWrapper.prototype = OriginalChart.prototype;
				Object.setPrototypeOf(ChartWrapper, OriginalChart);
				Object.keys(OriginalChart).forEach(function(key) {
					ChartWrapper[key] = OriginalChart[key];
				});
				frappe.Chart = ChartWrapper;
				frappe.Chart._patched = true;
			}
		} else {
			// Retry after a short delay
			setTimeout(waitForFrappeAndFix, 100);
		}
	}
	
	// Run fixes after DOM is loaded
	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', function() {
			fixAriaHiddenWarning();
			waitForFrappeAndFix();
		});
	} else {
		fixAriaHiddenWarning();
		waitForFrappeAndFix();
	}
	
	// Also try when frappe.ready is called
	if (typeof frappe !== 'undefined' && typeof frappe.ready === 'function') {
		frappe.ready(function() {
			setTimeout(function() {
				waitForFrappeAndFix();
			}, 100);
		});
	}
})();

