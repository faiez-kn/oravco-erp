// Replace "Powered by ERPNext" or "Built on Frappe" with "Powered by Oravco ERP"
frappe.ready(function() {
	function replaceFooterText() {
		// Replace in all text nodes
		const walker = document.createTreeWalker(
			document.body,
			NodeFilter.SHOW_TEXT,
			null,
			false
		);
		
		let node;
		while (node = walker.nextNode()) {
			if (node.textContent) {
				// Replace "Powered by ERPNext"
				if (node.textContent.includes("Powered by ERPNext")) {
					node.textContent = node.textContent.replace(/Powered by ERPNext/g, "Powered by Oravco ERP");
				}
				// Replace "Built on Frappe" (if you want to change this too)
				if (node.textContent.includes("Built on Frappe")) {
					node.textContent = node.textContent.replace(/Built on Frappe/g, "Powered by Oravco ERP");
				}
			}
		}
		
		// Also replace in links and other elements
		const allElements = document.querySelectorAll('*');
		allElements.forEach(function(el) {
			// Check text content
			if (el.textContent) {
				if (el.textContent.includes("Powered by ERPNext")) {
					el.textContent = el.textContent.replace(/Powered by ERPNext/g, "Powered by Oravco ERP");
				}
				if (el.textContent.includes("Built on Frappe")) {
					el.textContent = el.textContent.replace(/Built on Frappe/g, "Powered by Oravco ERP");
				}
			}
			// Check HTML content (for links)
			if (el.innerHTML) {
				if (el.innerHTML.includes("Powered by ERPNext")) {
					el.innerHTML = el.innerHTML.replace(/Powered by ERPNext/g, "Powered by Oravco ERP");
				}
				if (el.innerHTML.includes("Built on Frappe")) {
					el.innerHTML = el.innerHTML.replace(/Built on Frappe/g, "Powered by Oravco ERP");
				}
			}
		});
	}
	
	// Run immediately
	replaceFooterText();
	
	// Watch for dynamic content changes
	if (typeof MutationObserver !== 'undefined') {
		const observer = new MutationObserver(function(mutations) {
			mutations.forEach(function(mutation) {
				if (mutation.addedNodes.length > 0) {
					replaceFooterText();
				}
			});
		});
		
		observer.observe(document.body, {
			childList: true,
			subtree: true
		});
	}
});

