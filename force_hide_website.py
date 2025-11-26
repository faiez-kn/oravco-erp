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
print("FORCE HIDING WEBSITE MODULE")
print("=" * 60)
print()

# Method 1: Update all Website desktop icons (standard and user copies)
print("1. Updating Desktop Icon records...")
try:
    # Update standard icon
    frappe.db.sql("""
        UPDATE `tabDesktop Icon` 
        SET blocked=1, hidden=1 
        WHERE module_name='Website' AND standard=1
    """)
    
    # Also update any user copies
    frappe.db.sql("""
        UPDATE `tabDesktop Icon` 
        SET hidden=1 
        WHERE module_name='Website' AND standard=0
    """)
    
    print("   ✓ Desktop Icon records updated")
except Exception as e:
    print(f"   ⚠ Error: {str(e)}")

# Method 2: Use Desktop Icon API
print("\n2. Using Desktop Icon API...")
try:
    from frappe.desk.doctype.desktop_icon.desktop_icon import set_hidden, clear_desktop_icons_cache
    
    # Hide for all users (global)
    set_hidden("Website", user=None, hidden=1)
    
    # Also hide for Administrator specifically
    set_hidden("Website", user="Administrator", hidden=1)
    
    # Clear cache
    clear_desktop_icons_cache()
    
    print("   ✓ Desktop Icon API called")
except Exception as e:
    print(f"   ⚠ Error: {str(e)}")

# Method 3: Block via User's blocked_modules
print("\n3. Blocking in User settings...")
try:
    # Get Administrator user
    admin = frappe.get_doc("User", "Administrator")
    
    # Add Website to blocked modules if not already there
    blocked_modules = admin.get_blocked_modules()
    if "Website" not in blocked_modules:
        # Create Block Module entry
        block_module = frappe.get_doc({
            "doctype": "Block Module",
            "module": "Website",
            "parent": "Administrator",
            "parenttype": "User",
            "parentfield": "block_modules"
        })
        block_module.insert(ignore_permissions=True)
        print("   ✓ Added to Administrator's blocked modules")
    else:
        print("   ✓ Already in blocked modules")
except Exception as e:
    print(f"   ⚠ Error: {str(e)}")

# Commit and clear all caches
print("\n4. Clearing all caches...")
frappe.db.commit()
frappe.clear_cache()

# Clear desktop icons cache for all users
try:
    from frappe.desk.doctype.desktop_icon.desktop_icon import clear_desktop_icons_cache
    clear_desktop_icons_cache()
except Exception:
    pass

# Clear user-specific caches
frappe.cache().delete_value("desktop_icons")
frappe.cache().delete_value("desktop_icons:Administrator")

print("   ✓ All caches cleared")

print("\n" + "=" * 60)
print("✅ WEBSITE MODULE HIDDEN!")
print("=" * 60)
print("\nPlease:")
print("1. Hard refresh your browser: Ctrl+Shift+R (or Cmd+Shift+R on Mac)")
print("2. Clear browser cache if needed")
print("3. Log out and log back in if it still appears")

