#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '/home/frappe/frappe-bench')

import frappe
frappe.init(site='erporavco.localhost')
frappe.connect()

# Clear Navbar Settings
try:
    navbar_settings = frappe.get_single("Navbar Settings")
    navbar_settings.app_logo = None
    navbar_settings.save(ignore_permissions=True)
    print("✓ Navbar logo cleared")
except Exception as e:
    print(f"⚠ Error clearing Navbar: {e}")

# Clear Website Settings
try:
    website_settings = frappe.get_single("Website Settings")
    website_settings.app_logo = None
    website_settings.favicon = None
    website_settings.save(ignore_permissions=True)
    print("✓ Website logo cleared")
    print("✓ Favicon cleared")
except Exception as e:
    print(f"⚠ Error clearing Website: {e}")

# Clear caches
frappe.clear_cache()
frappe.cache().delete_value("app_logo_url")
frappe.cache().delete_value("website_settings")
frappe.cache().delete_value("navbar_settings")

for key in frappe.cache().get_keys("bootinfo*"):
    frappe.cache().delete_value(key)

frappe.db.commit()
print("✅ All logo settings cleared! Restart backend/frontend and refresh browser.")

