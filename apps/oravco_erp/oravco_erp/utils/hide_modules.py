import frappe

# Configuration: List of modules to hide by default
# Add or remove module names from this list to hide/show modules
MODULES_TO_HIDE = [
	# "Website",  # Website module is now visible - removed from hidden list
	# Add more modules here as needed, for example:
	# "Blog",
	# "Newsletter",
	# "Help",
]

def hide_modules(module_list=None, unhide=False):
	"""
	Hide or unhide modules from the app interface
	
	Args:
		module_list: List of module names to hide/unhide. If None, uses MODULES_TO_HIDE
		unhide: If True, unhides the modules. If False, hides them.
	
	Example:
		# Hide Website and Blog modules
		hide_modules(["Website", "Blog"])
		
		# Unhide Website module
		hide_modules(["Website"], unhide=True)
		
		# Hide all modules in MODULES_TO_HIDE config
		hide_modules()
	"""
	if module_list is None:
		module_list = MODULES_TO_HIDE
	
	if not module_list:
		print("No modules specified to hide/unhide")
		return
	
	action = "unhide" if unhide else "hide"
	print(f"=" * 60)
	print(f"{action.upper()}ING MODULES: {', '.join(module_list)}")
	print("=" * 60)
	print()
	
	for module_name in module_list:
		try:
			# Step 1: Hide/Unhide Workspace if it exists
			if frappe.db.exists("Workspace", module_name):
				workspace = frappe.get_doc("Workspace", module_name)
				if unhide:
					workspace.is_hidden = 0
					workspace.public = 1
				else:
					workspace.is_hidden = 1
					workspace.public = 0
				workspace.save(ignore_permissions=True)
				print(f"✓ {module_name}: Workspace {'unhidden' if unhide else 'hidden'}")
			
			# Step 2: Update Desktop Icons
			desktop_icons = frappe.get_all("Desktop Icon", filters={"module_name": module_name}, fields=["name"])
			if desktop_icons:
				for icon in desktop_icons:
					icon_doc = frappe.get_doc("Desktop Icon", icon.name)
					if unhide:
						icon_doc.blocked = 0
						icon_doc.hidden = 0
					else:
						icon_doc.blocked = 1
						icon_doc.hidden = 1
					icon_doc.save(ignore_permissions=True)
				print(f"✓ {module_name}: {len(desktop_icons)} Desktop Icon(s) updated")
			
			# Step 3: Block/Unblock for all users
			users = frappe.get_all("User", filters={"enabled": 1}, fields=["name"])
			blocked_count = 0
			unblocked_count = 0
			
			for user in users:
				user_doc = frappe.get_doc("User", user.name)
				blocked_modules = user_doc.get_blocked_modules()
				
				if unhide:
					# Remove from blocked modules
					block_module = frappe.db.exists("Block Module", {
						"parent": user.name,
						"parenttype": "User",
						"parentfield": "block_modules",
						"module": module_name
					})
					if block_module:
						frappe.delete_doc("Block Module", block_module, ignore_permissions=True)
						unblocked_count += 1
				else:
					# Add to blocked modules
					if module_name not in blocked_modules:
						existing = frappe.db.exists("Block Module", {
							"parent": user.name,
							"parenttype": "User",
							"parentfield": "block_modules",
							"module": module_name
						})
						if not existing:
							block_module = frappe.get_doc({
								"doctype": "Block Module",
								"module": module_name,
								"parent": user.name,
								"parenttype": "User",
								"parentfield": "block_modules"
							})
							block_module.insert(ignore_permissions=True)
							blocked_count += 1
			
			if unhide:
				print(f"✓ {module_name}: Unblocked for {unblocked_count} user(s)")
			else:
				print(f"✓ {module_name}: Blocked for {blocked_count} user(s)")
				
		except Exception as e:
			print(f"⚠ {module_name}: Error - {str(e)}")
	
	# Clear all caches
	print("\nClearing caches...")
	frappe.db.commit()
	frappe.clear_cache()
	
	# Clear desktop icons cache
	try:
		from frappe.desk.doctype.desktop_icon.desktop_icon import clear_desktop_icons_cache
		clear_desktop_icons_cache()
	except Exception:
		pass
	
	# Clear workspace cache
	frappe.cache().delete_value("workspace_sidebar_items")
	
	print("✓ All caches cleared")
	print("\n" + "=" * 60)
	print(f"✅ MODULES {action.upper()}D SUCCESSFULLY!")
	print("=" * 60)
	print("\nPlease log out and log back in, then refresh your browser to see changes.")


def hide_website_module():
	"""Hide the Website module (backward compatibility)"""
	hide_modules(["Website"])


def unhide_modules(module_list):
	"""Unhide modules - convenience function"""
	hide_modules(module_list, unhide=True)

