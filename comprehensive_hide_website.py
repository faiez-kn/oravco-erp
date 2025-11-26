#!/usr/bin/env python3
import sys
import os

# Set proper paths
os.chdir('/home/frappe/frappe-bench/sites')
sys.path.insert(0, '/home/frappe/frappe-bench/apps')

import frappe
frappe.init(site='erporavco.localhost', sites_path='.')
frappe.connect()

print("=" * 60)
print("COMPREHENSIVE WEBSITE MODULE HIDING")
print("=" * 60)
print()

# Method 1: Block in User's blocked_modules for all users
print("1. Blocking Website module for all users...")
try:
    users = frappe.get_all("User", filters={"enabled": 1}, fields=["name"])
    for user in users:
        user_doc = frappe.get_doc("User", user.name)
        blocked_modules = user_doc.get_blocked_modules()
        if "Website" not in blocked_modules:
            # Check if Block Module already exists
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
    print(f"   ✓ Blocked for {len(users)} users")
except Exception as e:
    print(f"   ⚠ Error: {str(e)}")

# Method 2: Update all Desktop Icons
print("\n2. Updating all Desktop Icon records...")
try:
    # Update standard icons
    frappe.db.sql("""
        UPDATE `tabDesktop Icon` 
        SET blocked=1, hidden=1 
        WHERE module_name='Website'
    """)
    
    # Also ensure all user copies are hidden
    frappe.db.sql("""
        UPDATE `tabDesktop Icon` 
        SET hidden=1 
        WHERE module_name='Website'
    """)
    
    count = frappe.db.sql("SELECT COUNT(*) FROM `tabDesktop Icon` WHERE module_name='Website'")[0][0]
    print(f"   ✓ Updated {count} Desktop Icon records")
except Exception as e:
    print(f"   ⚠ Error: {str(e)}")

# Method 3: Hide in Module Def if it exists
print("\n3. Checking Module Def...")
try:
    if frappe.db.exists("Module Def", "Website"):
        module_def = frappe.get_doc("Module Def", "Website")
        # Note: Module Def doesn't have a hide field, but we can check it
        print(f"   ✓ Module Def exists (app: {module_def.app_name})")
except Exception as e:
    print(f"   ⚠ Error: {str(e)}")

# Method 4: Clear ALL caches aggressively
print("\n4. Clearing all caches...")
try:
    # Clear desktop icons cache
    from frappe.desk.doctype.desktop_icon.desktop_icon import clear_desktop_icons_cache
    clear_desktop_icons_cache()
    
    # Clear general cache
    frappe.clear_cache()
    
    # Clear user-specific desktop icons cache
    users = frappe.get_all("User", filters={"enabled": 1}, fields=["name"])
    for user in users:
        frappe.cache().delete_value(f"desktop_icons:{user.name}")
    
    # Clear bootinfo cache
    for key in frappe.cache().get_keys("bootinfo*"):
        frappe.cache().delete_value(key)
    
    print("   ✓ All caches cleared")
except Exception as e:
    print(f"   ⚠ Error: {str(e)}")

# Commit
frappe.db.commit()

print("\n" + "=" * 60)
print("✅ COMPREHENSIVE HIDING COMPLETE!")
print("=" * 60)
print("\nIMPORTANT NEXT STEPS:")
print("1. Log out completely from the app")
print("2. Clear browser cache: Ctrl+Shift+Delete")
print("3. Log back in")
print("4. Hard refresh: Ctrl+Shift+R")
print("\nIf Website module still appears, it might be in a custom Workspace.")
print("Check Workspace doctype and remove Website module from there.")

