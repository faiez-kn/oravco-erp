#!/bin/bash
# Copy this file into the container and run it

cd /home/frappe/frappe-bench/sites
python3 << 'PYTHON_EOF'
import sys
sys.path.insert(0, '../apps')
import frappe
frappe.init(site='erporavco.localhost', sites_path='.')
frappe.connect()

print("=" * 60)
print("CLEARING ALL LOGO SETTINGS")
print("=" * 60)

# Clear Navbar Settings
print("\n1. Clearing Navbar Settings logo...")
try:
    navbar = frappe.get_single('Navbar Settings')
    navbar.app_logo = None
    navbar.save(ignore_permissions=True)
    print("   ✓ Cleared")
except Exception as e:
    print(f"   ⚠ Error: {str(e)[:50]}")

# Clear Website Settings
print("\n2. Clearing Website Settings logo...")
try:
    website = frappe.get_single('Website Settings')
    website.app_logo = None
    website.favicon = None
    website.save(ignore_permissions=True)
    print("   ✓ Cleared logo and favicon")
except Exception as e:
    print(f"   ⚠ Error: {str(e)[:50]}")

# Clear caches
print("\n3. Clearing caches...")
frappe.clear_cache()
try:
    frappe.cache().delete_value('app_logo_url')
    for key in frappe.cache().get_keys('bootinfo*'):
        frappe.cache().delete_value(key)
except Exception:
    pass

frappe.db.commit()

print("\n" + "=" * 60)
print("✅ ALL LOGO SETTINGS CLEARED!")
print("=" * 60)
print("\nRestart backend/frontend and refresh browser!")
PYTHON_EOF

