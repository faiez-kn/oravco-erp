"""
Script to set logo in Navbar/Website Settings and update footer text
Run with: bench --site erporavco.localhost execute oravco_erp.utils.set_logo_and_footer.set_logo_and_footer
"""
import frappe

def set_logo_and_footer():
	"""Set logo URL and footer text in database"""
	
	# Set logo in Navbar Settings (if not already set)
	try:
		navbar_settings = frappe.get_doc("Navbar Settings")
		if not navbar_settings.app_logo:
			# Set the logo URL - this should be accessible via /assets/
			navbar_settings.app_logo = "/assets/oravco_erp/images/oravco-logo.png"
			navbar_settings.save(ignore_permissions=True)
			print("✓ Logo set in Navbar Settings")
	except Exception as e:
		print(f"⚠ Error setting logo in Navbar Settings: {str(e)}")
	
	# Set logo in Website Settings (if not already set)
	try:
		website_settings = frappe.get_doc("Website Settings")
		if not website_settings.app_logo:
			website_settings.app_logo = "/assets/oravco_erp/images/oravco-logo.png"
			website_settings.save(ignore_permissions=True)
			print("✓ Logo set in Website Settings")
	except Exception as e:
		print(f"⚠ Error setting logo in Website Settings: {str(e)}")
	
	# Update footer "Powered by" text (plain HTML)
	try:
		frappe.db.set_single_value("Website Settings", "footer_powered", 
			'Powered by <a href="#" target="_blank" class="text-muted">Oravco ERP</a>')
		print("✓ Footer 'Powered by' text updated")
	except Exception as e:
		print(f"⚠ Error updating footer text: {str(e)}")
	
	frappe.db.commit()
	frappe.clear_cache()
	print("\n✅ Logo and footer updated successfully!")

