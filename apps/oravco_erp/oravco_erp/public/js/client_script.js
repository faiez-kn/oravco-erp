// Client script to replace any remaining ERPNext references with Oravco ERP
frappe.ui.form.on('System Settings', {
	refresh: function(frm) {
		if (frm.doc.app_name === "ERPNext") {
			frm.set_value('app_name', 'Oravco ERP');
			frm.save();
		}
	}
});

frappe.ui.form.on('Website Settings', {
	refresh: function(frm) {
		if (frm.doc.app_name === "ERPNext") {
			frm.set_value('app_name', 'Oravco ERP');
			frm.save();
		}
	}
});

// Also update on load
frappe.ready(function() {
	// Update System Settings if needed
	frappe.call({
		method: 'frappe.client.get',
		args: {
			doctype: 'System Settings',
			name: 'System Settings'
		},
		callback: function(r) {
			if (r.message && r.message.app_name === "ERPNext") {
				frappe.db.set_value('System Settings', 'System Settings', 'app_name', 'Oravco ERP');
			}
		}
	});
});

