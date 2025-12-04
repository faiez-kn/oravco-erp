"""
Enable editing access for Installed Applications settings
"""
import frappe


def enable_app_settings_edit():
	"""
	Enable System Manager users to edit Installed Applications settings
	"""
	print("=" * 60)
	print("ENABLING INSTALLED APPLICATIONS EDIT ACCESS")
	print("=" * 60)
	
	# Check current user
	user = frappe.session.user
	print(f"Current User: {user}")
	roles = frappe.get_roles(user)
	print(f"User Roles: {', '.join(roles)}")
	
	if user != "Administrator" and "System Manager" not in roles:
		print("\n⚠ WARNING: Your user doesn't have System Manager role!")
		print("   You need System Manager role to edit Installed Applications.")
		print("   To fix: Go to User > [Your User] > Roles and add 'System Manager'")
		return False
	
	# Get Installed Applications doctype
	print("\n" + "=" * 60)
	print("UPDATING INSTALLED APPLICATIONS DOCTYPE")
	print("=" * 60)
	
	try:
		installed_apps_doc = frappe.get_doc("DocType", "Installed Applications")
		
		# Ensure System Manager has full permissions
		system_manager_perm = None
		for perm in installed_apps_doc.permissions:
			if perm.role == "System Manager":
				system_manager_perm = perm
				break
		
		if system_manager_perm:
			if not system_manager_perm.write:
				print("Fixing System Manager write permission...")
				system_manager_perm.write = 1
				system_manager_perm.create = 1
				system_manager_perm.delete = 1
				installed_apps_doc.save(ignore_permissions=True)
				print("✓ Updated System Manager permissions")
			else:
				print("✓ System Manager already has write permission")
		else:
			print("Adding System Manager permission...")
			installed_apps_doc.append("permissions", {
				"role": "System Manager",
				"create": 1,
				"read": 1,
				"write": 1,
				"delete": 1,
				"export": 1,
				"print": 1,
				"email": 1,
				"report": 1,
				"share": 1
			})
			installed_apps_doc.save(ignore_permissions=True)
			print("✓ Added System Manager permissions")
		
		# Make the field editable (remove read_only restriction)
		print("\n" + "=" * 60)
		print("MAKING FIELDS EDITABLE")
		print("=" * 60)
		
		for field in installed_apps_doc.fields:
			if field.fieldname == "installed_applications":
				if field.read_only:
					print("Removing read_only restriction from installed_applications field...")
					field.read_only = 0
					installed_apps_doc.save(ignore_permissions=True)
					print("✓ Field is now editable")
				else:
					print("✓ Field is already editable")
				break
		
		# Also check child table fields
		installed_app_child = frappe.get_doc("DocType", "Installed Application")
		fields_made_editable = []
		for field in installed_app_child.fields:
			if field.read_only and field.fieldname in ["app_name", "app_version", "git_branch", "has_setup_wizard", "is_setup_complete"]:
				print(f"Making {field.fieldname} editable...")
				field.read_only = 0
				fields_made_editable.append(field.fieldname)
		
		if fields_made_editable:
			installed_app_child.save(ignore_permissions=True)
			print(f"✓ Made {len(fields_made_editable)} child table fields editable: {', '.join(fields_made_editable)}")
		else:
			print("✓ Child table fields are already editable")
		
		# Clear caches
		print("\n" + "=" * 60)
		print("CLEARING CACHES")
		print("=" * 60)
		frappe.clear_cache()
		frappe.reload_doc("core", "doctype", "installed_applications")
		frappe.reload_doc("core", "doctype", "installed_application")
		print("✓ Cleared cache and reloaded doctypes")
		
		print("\n" + "=" * 60)
		print("✅ SUCCESS: Installed Applications is now editable!")
		print("=" * 60)
		print("\nYou can now:")
		print("  1. Go to Setup > Installed Applications")
		print("  2. Edit application settings")
		print("  3. Update setup completion status")
		print("  4. Modify application versions")
		
		return True
		
	except Exception as e:
		print(f"\n❌ ERROR: {str(e)}")
		frappe.log_error(f"Error enabling app settings edit: {str(e)}")
		return False


if __name__ == "__main__":
	frappe.init(site="erporavco.localhost")
	frappe.connect()
	enable_app_settings_edit()
	frappe.db.commit()

