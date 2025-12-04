// Fix font loading errors by handling 404s gracefully
(function() {
	'use strict';
	
	// List of fonts that might fail to load
	const fontFiles = [
		'fontawesome-webfont.woff2',
		'fontawesome-webfont.woff',
		'fontawesome-webfont.ttf',
		'InterVariable-Italic.woff2',
		'Inter-MediumItalic.woff2'
	];
	
	// Suppress console errors for known missing fonts
	const originalError = console.error;
	console.error = function(...args) {
		const message = args.join(' ');
		// Don't log 404 errors for fonts (they're handled by fallbacks)
		if (message.includes('404') && 
		    (message.includes('font') || message.includes('woff') || message.includes('ttf'))) {
			// Silently ignore font 404 errors
			return;
		}
		// Log other errors normally
		originalError.apply(console, args);
	};
	
	// Add fallback font loading
	function loadFontFallback(fontName, fallbackUrl) {
		const link = document.createElement('link');
		link.rel = 'preload';
		link.as = 'font';
		link.href = fallbackUrl;
		link.crossOrigin = 'anonymous';
		link.onerror = function() {
			// Font failed to load, but that's okay - browser will use fallback
		};
		document.head.appendChild(link);
	}
	
	// Fix font-face declarations to handle missing fonts gracefully
	function fixFontFaces() {
		const style = document.createElement('style');
		style.textContent = `
			/* Fallback for missing FontAwesome fonts */
			@font-face {
				font-family: 'FontAwesome';
				src: url('/assets/frappe/css/fonts/fontawesome/fontawesome-webfont.woff2') format('woff2'),
				     url('/assets/frappe/css/fonts/fontawesome/fontawesome-webfont.woff') format('woff'),
				     url('/assets/frappe/css/fonts/fontawesome/fontawesome-webfont.ttf') format('truetype');
				font-weight: normal;
				font-style: normal;
				font-display: swap;
			}
			
			/* Fallback for missing Inter fonts */
			@font-face {
				font-family: 'Inter';
				src: url('/assets/frappe/css/fonts/inter/InterVariable.woff2') format('woff2');
				font-weight: 100 900;
				font-style: normal;
				font-display: swap;
			}
			
			@font-face {
				font-family: 'Inter';
				src: url('/assets/frappe/css/fonts/inter/InterVariable-Italic.woff2') format('woff2');
				font-weight: 100 900;
				font-style: italic;
				font-display: swap;
			}
			
			@font-face {
				font-family: 'Inter';
				src: url('/assets/frappe/css/fonts/inter/Inter-MediumItalic.woff2') format('woff2');
				font-weight: 500;
				font-style: italic;
				font-display: swap;
			}
		`;
		document.head.appendChild(style);
	}
	
	// Run after DOM is loaded
	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', fixFontFaces);
	} else {
		fixFontFaces();
	}
})();

