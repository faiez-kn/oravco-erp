// Fix Warehouse Is Group field to be enabled when creating new warehouse
frappe.ui.form.on("Warehouse", {
	refresh: function(frm) {
		// Enable is_group field when creating a new warehouse
		if (frm.is_new()) {
			frm.set_df_property("is_group", "read_only", 0);
			frm.toggle_enable("is_group", true);
		}
	},
	
	setup: function(frm) {
		// Ensure is_group is enabled for new documents
		if (frm.is_new()) {
			frm.set_df_property("is_group", "read_only", 0);
			frm.toggle_enable("is_group", true);
		}
	}
});
