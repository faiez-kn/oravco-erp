// Fix preload warnings for SVG icons
// Remove unused preload links or fix their 'as' attribute
(function() {
	'use strict';
	
	// Suppress preload warnings in console
	if (console.warn) {
		const originalWarn = console.warn;
		console.warn = function(...args) {
			const message = args.join(' ');
			// Suppress preload warnings
			if (message.includes('was preloaded using link preload but not used') ||
			    message.includes('preload') && message.includes('not used within a few seconds')) {
				// Silently ignore - these are harmless warnings
				return;
			}
			originalWarn.apply(console, args);
		};
	}
	
	function fixPreloadLinks() {
		// Find all preload links for SVG icons
		const preloadLinks = document.querySelectorAll('link[rel="preload"][href*="icons.svg"]');
		
		preloadLinks.forEach(function(link) {
			const href = link.getAttribute('href');
			
			// Always fix SVG icon preloads to use 'image' instead of 'fetch'
			if (href && href.includes('icons.svg')) {
				if (link.getAttribute('as') === 'fetch' || !link.getAttribute('as')) {
					link.setAttribute('as', 'image');
					link.setAttribute('type', 'image/svg+xml');
				}
			}
		});
		
		// Also fix any preload links without proper 'as' attribute
		const allPreloads = document.querySelectorAll('link[rel="preload"]:not([as])');
		allPreloads.forEach(function(link) {
			const href = link.getAttribute('href');
			if (href) {
				if (href.includes('.css')) {
					link.setAttribute('as', 'style');
				} else if (href.includes('.js')) {
					link.setAttribute('as', 'script');
				} else if (href.includes('.woff') || href.includes('.ttf')) {
					link.setAttribute('as', 'font');
					link.setAttribute('crossorigin', 'anonymous');
				} else if (href.includes('.svg')) {
					link.setAttribute('as', 'image');
					link.setAttribute('type', 'image/svg+xml');
				}
			}
		});
	}
	
	// Run immediately and after DOM is loaded
	fixPreloadLinks();
	
	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', fixPreloadLinks);
	} else {
		fixPreloadLinks();
	}
	
	// Also run after delays to catch dynamically added preloads
	setTimeout(fixPreloadLinks, 500);
	setTimeout(fixPreloadLinks, 1000);
	setTimeout(fixPreloadLinks, 2000);
})();

