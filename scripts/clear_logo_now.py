#!/usr/bin/env python3
import sys
import os

# Set proper paths
os.chdir('/home/frappe/frappe-bench')
sys.path.insert(0, '/home/frappe/frappe-bench/apps')

import frappe

# Initialize with proper sites_path - sites are in /home/frappe/frappe-bench/sites
# But frappe.init expects sites_path to be relative to current directory or absolute
frappe.init(site='erporavco.localhost', sites_path='/home/frappe/frappe-bench/sites')
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
except Exception as e:
    print(f"   ⚠ Cache clear warning: {str(e)[:30]}")

print("   ✓ All caches cleared")

# Commit
frappe.db.commit()

print()
print("=" * 60)
print("✅ ALL LOGO SETTINGS CLEARED!")
print("=" * 60)
print("\nThe navbar will now show a bold black 'O' text instead of an image.")
print("\nNext: Restart backend/frontend and refresh browser!")

