import frappe

frappe.init('erporavco.localhost')
frappe.connect()

# Set footer_powered in Website Settings
footer_text = '{{ _("Powered by {0}").format(\'<a href="#" target="_blank" class="text-muted">Oravco ERP</a>\') }}'
frappe.db.set_single_value("Website Settings", "footer_powered", footer_text)
frappe.db.commit()
frappe.clear_cache()

print("✅ Footer 'Powered by' text updated to 'Oravco ERP'")

