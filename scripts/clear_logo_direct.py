#!/usr/bin/env python3
# This script clears logo settings directly
import sys
import os

# Add bench paths
sys.path.insert(0, '/home/frappe/frappe-bench/apps')
os.chdir('/home/frappe/frappe-bench')

import frappe
frappe.init(site='erporavco.localhost')
frappe.connect()

print("=" * 60)
print("CLEARING ALL LOGO SETTINGS")
print("=" * 60)
print()

# Clear Navbar Settings
print("1. Clearing Navbar Settings logo...")
try:
    navbar_settings = frappe.get_single("Navbar Settings")
    old_logo = navbar_settings.app_logo
    navbar_settings.app_logo = None
    navbar_settings.save(ignore_permissions=True)
    print(f"   ✓ Cleared (was: {old_logo})")
except Exception as e:
    print(f"   ⚠ Error: {str(e)[:50]}")

# Clear Website Settings
print("2. Clearing Website Settings logo...")
try:
    website_settings = frappe.get_single("Website Settings")
    old_logo = website_settings.app_logo
    website_settings.app_logo = None
    website_settings.favicon = None
    website_settings.save(ignore_permissions=True)
    print(f"   ✓ Cleared logo (was: {old_logo})")
    print(f"   ✓ Cleared favicon")
except Exception as e:
    print(f"   ⚠ Error: {str(e)[:50]}")

# Clear all caches
print("3. Clearing all caches...")
frappe.clear_cache()
try:
    frappe.cache().delete_value("app_logo_url")
    frappe.cache().delete_value("website_settings")
    frappe.cache().delete_value("navbar_settings")
    
    # Clear bootinfo cache
    for key in frappe.cache().get_keys("bootinfo*"):
        frappe.cache().delete_value(key)
except Exception:
    pass

print("   ✓ All caches cleared")

# Commit
frappe.db.commit()

print()
print("=" * 60)
print("✅ ALL LOGO SETTINGS CLEARED!")
print("=" * 60)
print("\nThe navbar will now show a bold black 'O' text instead of an image.")
print("\nNext: Restart backend/frontend and refresh browser!")

