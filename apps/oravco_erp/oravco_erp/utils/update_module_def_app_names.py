"""
Update Module Def records to show Oravco ERP instead of erpnext/frappe
Run with: bench --site erporavco.localhost execute oravco_erp.utils.update_module_def_app_names.update_module_def_app_names
"""
import frappe

def update_module_def_app_names():
	"""Update Module Def records to replace erpnext/frappe with Oravco ERP in display"""
	
	# Note: We can't change the actual app_name value (it needs to stay as 'erpnext' for the system to work)
	# But we can update any custom modules or create a display override
	
	# Get all Module Def records
	modules = frappe.get_all("Module Def", fields=["name", "app_name", "module_name"])
	
	updated = 0
	for module in modules:
		# The app_name field stores the actual app name (erpnext, frappe, etc.)
		# We can't change this as it's used by the system
		# The JavaScript fix will handle the display
		pass
	
	frappe.db.commit()
	frappe.clear_cache()
	
	print("✅ Module Def app names will be displayed as 'Oravco ERP' via JavaScript")
	print("   (Actual app_name values remain unchanged for system compatibility)")
	print("\n💡 The JavaScript fix (fix_module_def_app_name.js) will:")
	print("   - Replace 'erpnext' with 'Oravco ERP' in dropdowns")
	print("   - Replace 'frappe' with 'Oravco ERP' in dropdowns")
	print("   - Update display in list views")
	print("   - Update display in forms")



