// Replace any remaining ERPNext references with Oravco ERP in the UI
frappe.ready(function() {
	// Function to replace text in DOM
	function replaceText(node) {
		if (node.nodeType === 3) { // Text node
			node.textContent = node.textContent.replace(/ERPNext/gi, 'Oravco ERP');
		} else {
			node.childNodes.forEach(replaceText);
		}
	}

	// Replace on page load
	replaceText(document.body);

	// Watch for dynamic content changes
	const observer = new MutationObserver(function(mutations) {
		mutations.forEach(function(mutation) {
			mutation.addedNodes.forEach(function(node) {
				if (node.nodeType === 1) { // Element node
					replaceText(node);
				}
			});
		});
	});

	observer.observe(document.body, {
		childList: true,
		subtree: true
	});

	// Override app title in boot info
	if (frappe.boot && frappe.boot.apps_info) {
		Object.keys(frappe.boot.apps_info).forEach(function(app) {
			if (frappe.boot.apps_info[app]) {
				if (frappe.boot.apps_info[app].app_title === "ERPNext") {
					frappe.boot.apps_info[app].app_title = "Oravco ERP";
				}
			}
		});
	}

	// Update page title
	if (document.title) {
		document.title = document.title.replace(/ERPNext/gi, 'Oravco ERP');
	}
});

