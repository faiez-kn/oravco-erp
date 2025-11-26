import frappe

APP_LOGO_PATH = "/files/oravco-logo.png"

def boot_session(bootinfo):
	"""Override app name in boot session"""
	# Replace any remaining ERPNext references with Oravco ERP in bootinfo
	if "apps_info" in bootinfo:
		for app_name, app_info in bootinfo["apps_info"].items():
			if app_info:
				if app_info.get("app_title") == "ERPNext":
					app_info["app_title"] = "Oravco ERP"
				if app_info.get("app_name") == "erpnext":
					app_info["app_name"] = "oravco_erp"
	
	# Update system settings app_name in bootinfo
	if "sysdefaults" in bootinfo:
		if bootinfo["sysdefaults"].get("app_name") == "ERPNext":
			bootinfo["sysdefaults"]["app_name"] = "Oravco ERP"
		# Always set to Oravco ERP
		bootinfo["sysdefaults"]["app_name"] = "Oravco ERP"
	
	# Override app logo URL with custom logo served from /files/
	bootinfo["app_logo_url"] = APP_LOGO_PATH
	
	# Update system settings in database
	try:
		current_app_name = frappe.db.get_single_value("System Settings", "app_name")
		if current_app_name == "ERPNext":
			frappe.db.set_single_value("System Settings", "app_name", "Oravco ERP")
			frappe.db.commit()
	except Exception:
		pass

def extend_bootinfo(bootinfo=None):
	"""
	Extend bootinfo hook - runs AFTER get_app_logo() is called
	This ensures we override ERPNext's logo even if get_app_logo() picked it up
	"""
	if bootinfo is None:
		return
	
	# ALWAYS override with our custom logo
	bootinfo["app_logo_url"] = APP_LOGO_PATH

def after_install():
	"""Update branding after app installation"""
	ensure_branding()
	
	# Hide configured modules (runs only on install/migrate)
	try:
		from oravco_erp.utils.hide_modules import hide_modules
		hide_modules()
	except Exception:
		pass
	
	frappe.db.commit()
	frappe.clear_cache()
	
def ensure_branding():
	"""Ensure all branding values (logos, splash, footer text) are set"""
	# Update System Settings
	frappe.db.set_single_value("System Settings", "app_name", "Oravco ERP")
	
	# Update Website Settings
	try:
		frappe.db.set_single_value("Website Settings", "app_name", "Oravco ERP")
		frappe.db.set_single_value("Website Settings", "app_logo", APP_LOGO_PATH)
		frappe.db.set_single_value("Website Settings", "splash_image", APP_LOGO_PATH)
		# Update footer "Powered by" text (HTML with translation support)
		# Using the same format as ERPNext but with Oravco ERP
		footer_text = '{{ _("Powered by {0}").format(\'<a href="#" target="_blank" class="text-muted">Oravco ERP</a>\') }}'
		frappe.db.set_single_value("Website Settings", "footer_powered", footer_text)
	except Exception as e:
		frappe.log_error(f"Error updating Website Settings: {str(e)}")
	
	# Update Navbar Settings logo
	try:
		frappe.db.set_single_value("Navbar Settings", "app_logo", APP_LOGO_PATH)
	except Exception:
		pass
	
	frappe.db.commit()
	frappe.clear_cache()

