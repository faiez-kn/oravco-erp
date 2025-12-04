// Client script to replace any remaining ERPNext references with Oravco ERP
// Using try-catch to prevent any errors from breaking the form
frappe.ui.form.on('System Settings', {
	refresh: function(frm) {
		try {
			// Only update if the value is actually "ERPNext" and form is loaded
			if (frm.doc && frm.doc.app_name === "ERPNext" && !frm.is_new()) {
				// Silently update the field value without triggering events
				frm.set_value('app_name', 'Oravco ERP', null, true);
			}
		} catch (e) {
			// Silently fail - don't break the form
			console.warn('Error updating System Settings app_name:', e);
		}
	}
});

frappe.ui.form.on('Website Settings', {
	refresh: function(frm) {
		try {
			// Only update if the value is actually "ERPNext" and form is loaded
			if (frm.doc && frm.doc.app_name === "ERPNext" && !frm.is_new()) {
				// Silently update the field value without triggering events
				frm.set_value('app_name', 'Oravco ERP', null, true);
			}
		} catch (e) {
			// Silently fail - don't break the form
			console.warn('Error updating Website Settings app_name:', e);
		}
	}
});

