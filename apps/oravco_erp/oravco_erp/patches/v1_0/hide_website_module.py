import frappe

def execute():
	"""Hide configured modules from desktop icons and workspaces"""
	try:
		from oravco_erp.utils.hide_modules import hide_modules
		# This will use MODULES_TO_HIDE from hide_modules.py
		hide_modules()
	except Exception as e:
		frappe.log_error(f"Error hiding modules: {str(e)}")

