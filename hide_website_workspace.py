#!/usr/bin/env python3
import sys
import os

os.chdir('/home/frappe/frappe-bench/sites')
sys.path.insert(0, '/home/frappe/frappe-bench/apps')

import frappe
frappe.init(site='erporavco.localhost', sites_path='.')
frappe.connect()

print("=" * 60)
print("HIDING WEBSITE WORKSPACE")
print("=" * 60)
print()

try:
    # Get the Website Workspace
    website_workspace = frappe.get_doc("Workspace", "Website")
    
    # Hide it by setting is_hidden = 1
    website_workspace.is_hidden = 1
    
    # Also make it non-public
    website_workspace.public = 0
    
    website_workspace.save(ignore_permissions=True)
    
    print("✅ Website Workspace hidden successfully!")
    print(f"   - is_hidden: {website_workspace.is_hidden}")
    print(f"   - public: {website_workspace.public}")
    
except frappe.DoesNotExistError:
    print("⚠ Website Workspace not found")
except Exception as e:
    print(f"⚠ Error: {str(e)}")
    import traceback
    traceback.print_exc()

# Also ensure Website is blocked for all users (redundant but safe)
print("\n2. Ensuring Website is blocked for all users...")
try:
    users = frappe.get_all("User", filters={"enabled": 1}, fields=["name"])
    for user in users:
        user_doc = frappe.get_doc("User", user.name)
        blocked_modules = user_doc.get_blocked_modules()
        if "Website" not in blocked_modules:
            existing = frappe.db.exists("Block Module", {
                "parent": user.name,
                "parenttype": "User",
                "parentfield": "block_modules",
                "module": "Website"
            })
            if not existing:
                block_module = frappe.get_doc({
                    "doctype": "Block Module",
                    "module": "Website",
                    "parent": user.name,
                    "parenttype": "User",
                    "parentfield": "block_modules"
                })
                block_module.insert(ignore_permissions=True)
    print(f"   ✓ Blocked for all {len(users)} users")
except Exception as e:
    print(f"   ⚠ Error: {str(e)}")

# Clear all caches
print("\n3. Clearing all caches...")
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

print("   ✓ All caches cleared")

print("\n" + "=" * 60)
print("✅ WEBSITE MODULE COMPLETELY HIDDEN!")
print("=" * 60)
print("\nPlease:")
print("1. Log out and log back in")
print("2. Hard refresh: Ctrl+Shift+R")
print("3. The Website module should now be gone!")

