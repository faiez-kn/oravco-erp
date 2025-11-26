"""
Update footer powered by text in Website Settings
Run with: bench --site erporavco.localhost execute oravco_erp.utils.update_footer.update_footer
"""
import frappe

def update_footer():
	"""Update footer powered by text to Oravco ERP"""
	try:
		# Set footer_powered in Website Settings
		# Using Jinja2 template format so it gets rendered properly
		footer_text = '{{ _("Powered by {0}").format(\'<a href="#" target="_blank" class="text-muted">Oravco ERP</a>\') }}'
		frappe.db.set_single_value("Website Settings", "footer_powered", footer_text)
		frappe.db.commit()
		frappe.clear_cache()
		print("✅ Footer 'Powered by' text updated to 'Oravco ERP'")
	except Exception as e:
		print(f"❌ Error updating footer: {str(e)}")
		frappe.log_error(f"Error updating footer: {str(e)}")

