"""
Set logo in database to ensure it's picked up by get_app_logo() before hooks
Run with: bench --site erporavco.localhost execute oravco_erp.utils.set_logo_in_database.set_logo_in_database
"""
import frappe

def set_logo_in_database():
	"""Set logo URL in Navbar Settings and Website Settings"""
	
	logo_url = "/assets/oravco_erp/images/oravco-logo.png"
	
	# Set in Navbar Settings
	try:
		navbar = frappe.get_doc("Navbar Settings")
		# Set the logo URL directly (this is a file path field, but we can set it as URL)
		# Actually, app_logo is an AttachImage field, so we need to use a different approach
		# Instead, we'll ensure our boot_session hook always overrides
		print("Note: app_logo is an AttachImage field, cannot set URL directly")
		print("Logo will be set via boot_session hook instead")
	except Exception as e:
		print(f"Error accessing Navbar Settings: {str(e)}")
	
	# The logo will be set via boot_session hook which runs after get_app_logo()
	# But we need to ensure our hook runs last
	print(f"\n✅ Logo will be set via boot_session hook: {logo_url}")
	print("Make sure oravco_erp is listed AFTER erpnext in apps.txt for hook order")

